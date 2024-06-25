import stripe
from stripe import SignatureVerificationError
from fastapi import HTTPException, status
from pydantic import BaseModel
from app.settings import get_settings
from app.logs import get_logger

logger = get_logger(__name__)
settings = get_settings()
stripe.api_key = settings.stripe_api_key


class StripePayment(BaseModel):
    user_id: str
    user_email: str
    entity_id: str
    price_id: str
    quantity: int = 1
    mode: str = 'subscription'
    auto_tax: bool = True

    def create_checkout_session(self):
        """Create a new checkout session with Stripe."""
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': self.price_id,
                        'quantity': self.quantity,
                    },
                ],
                mode=self.mode,
                success_url=f"{settings.frontend_origin}/become-a-seller/payment-successful",
                cancel_url=f"{settings.frontend_origin}/become-a-seller/payment-failed",
                automatic_tax={'enabled': self.auto_tax},
                metadata={
                    'customer_user_id': self.user_id,
                    'customer_email': self.user_email,
                    'entity_id': self.entity_id,
                    'price_id': self.price_id,
                }
            )
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating checkout session: {e}")

        return checkout_session


async def stripe_fullfillment(request: dict, signature: str = None):
    """Handle the fullfillment of a Stripe webhook."""
    if signature is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stripe signature header missing.")

    body = await request.body()
    body = body.decode('utf-8')

    try:
        event = stripe.Webhook.construct_event(
            body, signature, settings.stripe_endpoint_secret
        )
    except ValueError as e:
        logger.error(f"Error decoding event: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error decoding event: {e}")
    except SignatureVerificationError as e:
        logger.error(f"Signature verification error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Signature verification error: {e}")

    if event.type == 'checkout.session.completed':
        return stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )
    else:
        logger.warning(f"Stripe: Unhandled event type: {event.type}")


async def subscription_cancel(subscription_id: str) -> None:
    """Cancel a subscription with Stripe."""
    if not subscription_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subscription ID is not present.")
    try:
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True,
        )
    except Exception as e:
        logger.critical(f"Error cancelling subscription: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error cancelling subscription: {e}")
    return subscription.cancel_at
