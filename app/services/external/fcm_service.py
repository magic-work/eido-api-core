from firebase_admin import firestore, messaging
from firebase_admin.firestore import firestore as fsq
from app.models.Notification import Notification
from app.logs import get_logger

logger = get_logger(__name__)


class PushNotificationService:

    def __init__(self):
        self.firestore_db = firestore.client()

    def add_user_to_topic(self, user_id, topic):
        """Subscribe a user to a topic"""
        fs_user = self.firestore_db.collection('users').document(user_id)
        fcm_tokens = self.get_fcm_tokens(fs_user)
        logger.info("Adding user '%s' to topic '%s'", user_id, topic)
        if not fcm_tokens:
            logger.warning("No FCM tokens found for user %s", user_id)
            return
        response = messaging.subscribe_to_topic(fcm_tokens, topic)
        if response.errors:
            logger.error("Errors were encountered during fcm subscribe: %s", response.errors[0].__dict__)

    def remove_user_from_topic(self, user_id: str, topic: str) -> None:
        """Unsubscribe a user from a topic"""
        fs_user = self.firestore_db.collection('users').document(user_id)
        fcm_tokens = self.get_fcm_tokens(fs_user)
        logger.info("Removing user '%s' from topic '%s'", user_id, topic)
        if not fcm_tokens:
            logger.warning("No FCM tokens found for user %s", user_id)
            return
        response = messaging.unsubscribe_from_topic(fcm_tokens, topic)
        if response.errors:
            logger.error("Errors were encountered during fcm unsubscribe: %s", response.errors[0].__dict__)

    def get_fcm_tokens(self, fs_user) -> list[str]:
        fcm_tokens = fs_user.collection('fcm_tokens').order_by('created_at', direction=fsq.Query.DESCENDING).get()
        return [fcm_token.to_dict().get('fcm_token') for fcm_token in fcm_tokens]

    def delete_fcm_tokens(self):
        fcm_tokens = self.user.collection('fcm_tokens').get()
        logger.info("Deleting all FCM tokens for user %s", self.firebase_uid)
        return [fcm_token.reference.delete() for fcm_token in fcm_tokens]

    def send_notification_to_user(self, user_id: str, notification: Notification, routing_data, badge: int = 0) -> None:
        """Create a notification message and send to multiple devices by passing a list of registration tokens"""
        logger.info("Preparing to send notification to user: %s", user_id)

        fs_user = self.firestore_db.collection('users').document(user_id)
        user_tokens = self.get_fcm_tokens(fs_user)

        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound='default',
                    badge=badge
                )
            )
        )
        pending_notification=messaging.Notification(title=notification.title, body=notification.body, image=notification.image_url)
        multicast_message = messaging.MulticastMessage(
            notification=pending_notification,
            tokens=user_tokens,
            apns=apns,
            data=routing_data
        )

        try:
            logger.info("Sending notification with title '%s' to users: '%s'", notification.title, user_id)
            messaging.send_multicast(multicast_message)
        except Exception as exp:
            logger.error("Error while sending notification to devices: %s", exp)

    def send_push_notification_to_topic(self, topic, notification, routing_data) -> None:
        """Create a notification message and send to a topic."""
        logger.info("Sending notification with title '%s' to topic '%s'", notification.title, topic)
        notification=messaging.Notification(title=notification.title, body=notification.body, image=notification.image_url)

        # iOS-specific payload
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound='default',
                )
            )
        )

        message = messaging.Message(
            notification=notification,
            topic=topic,
            apns=apns,
            data=routing_data
        )

        try:
            messaging.send(message)
            logger.info("The notification was sent to topic %s", topic)
        except Exception as exp:
            logger.error("Error while sending notification to topic %s: %s", topic, exp)
