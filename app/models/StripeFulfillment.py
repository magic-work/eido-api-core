# from app.models.MongoModel import MongoModel
# from app.integrations.stripe_service import stripe_fullfillment
# from app.settings import get_settings

# settings = get_settings()


# class StripeFulfillment(MongoModel):
#     fullfillment_id: str | None = None
#     stripe_customer_id: str | None = None
#     payment_intent: str | None = None
#     payment_status: str | None = None
#     amount_total: int | None = None
#     currency: str | None = None
#     mode: str | None = None
#     subscription_id: str | None = None
#     user_id: str | None = None
#     user_email: str | None = None
#     entity_id: str | None = None
#     price_id: str | None = None

#     async def fulfill(self, **kwargs):
#         fullfillment = await stripe_fullfillment(**kwargs)
#         if fullfillment:
#             self.fullfillment_id = fullfillment.id
#             self.stripe_customer_id = fullfillment.customer
#             self.payment_intent = fullfillment.payment_intent
#             self.payment_status = fullfillment.payment_status
#             self.amount_total = fullfillment.amount_total # in cents, not dollars
#             self.currency = fullfillment.currency
#             self.mode = fullfillment.mode
#             self.subscription_id = fullfillment.subscription
#             self.user_id = fullfillment.metadata.customer_user_id
#             self.user_email = fullfillment.metadata.customer_email
#             self.entity_id = fullfillment.metadata.entity_id
#             self.price_id = fullfillment.metadata.price_id
#             await self.save()
#         return self


# subscription_options = {
#     'dealer_yearly': {
#         'price_id': settings.yearly_dealer_subscription_price_id,
#         'entity_id': settings.yearly_dealer_subscription_entity_id,
#         'mode': settings.subscription_mode,
#     },
#     'dealer_monthly': {
#         'price_id': settings.monthly_dealer_subscription_price_id,
#         'entity_id': settings.monthly_dealer_subscription_entity_id,
#         'mode': settings.subscription_mode,
#     }
# }
