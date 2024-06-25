# from fastapi import APIRouter, status, Depends, Request, Header, HTTPException
# from fastapi.responses import JSONResponse
# from app.settings import get_settings
# from app.logs import get_logger
# from app.integrations.stripe_service import StripePayment
# from app.models.StripeFulfillment import StripeFulfillment
# from app.models.Dealer import Dealer
# from app.services.auth import FirebaseUser
# from app.services.auth import get_current_user
# from app.models.StripeFulfillment import subscription_options

# logger = get_logger(__name__)
# settings = get_settings()

# router = APIRouter(
#     prefix='/checkout',
#     tags=['Payments'],
# )


# @router.post('/upgrade-to-dealer')
# async def upgrade_to_dealer(body: dict, current_user: FirebaseUser = Depends(get_current_user)):
#     subscription_option = subscription_options.get(body.get('sub_type'))
#     if not subscription_option:
#         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid subscription type")

#     stripe_payment = StripePayment(
#         **subscription_option,
#         user_id=current_user.uid,
#         user_email=current_user.email
#     )
#     checkout_session = stripe_payment.create_checkout_session()
#     return JSONResponse(status_code=status.HTTP_200_OK, content={"url": checkout_session.url})


# @router.post('/fullfillment', status_code=status.HTTP_200_OK)
# async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
#     logger.debug("Stripe webhook received. stripe_signature: %s", stripe_signature)
#     fulfillment = await StripeFulfillment().fulfill(request=request, signature=stripe_signature)

#     # If the fulfillment is for a dealer subscription, upgrade the user to a dealer here
#     if fulfillment.user_pdf_id == subscription_options['dealer_yearly']['user_pdf_id'] or fulfillment.user_pdf_id == subscription_options['dealer_monthly']['user_pdf_id']:
#         dealer = await Dealer.find_one(Dealer.user_id == fulfillment.user_id)
#         if not dealer:
#             dealer = Dealer(user_id=fulfillment.user_id, user_email=fulfillment.user_email)
#         dealer.subscription_id = fulfillment.subscription_id
#         dealer.subscription_active = True
#         await dealer.save()
