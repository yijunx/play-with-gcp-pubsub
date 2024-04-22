# this is some backend listen to google pubsub, and it has a user
# it only gets the message of a user!

# this is the place where the the tasks are done..
import json
from google.auth import jwt
from google.cloud import pubsub_v1
from app.utils.config import get_config, Settings
import json
from app.handlers.base_handler import SlowHandler


class PubSubReceiver:
    def __init__(self, config: Settings) -> None:

        service_account_info = json.load(open(config.SUBSCRIBER_CRED_LOCATION))
        audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

        credentials = jwt.Credentials.from_service_account_info(
            service_account_info, audience=audience
        )
        self.client = pubsub_v1.SubscriberClient(credentials=credentials)


    def start(self, callback):
        subscription_name = f"projects/{config.GCP_PROJECT}/subscriptions/{config.GCP_SUB}"

        with self.client as subscriber:
            # need to create subscription?
            # subscriber.create_subscription(
            #     name=subscription_name, topic=topic_name)
            future = subscriber.subscribe(subscription_name, callback)
            try:
                future.result()
            except KeyboardInterrupt:
                future.cancel()


if __name__ == "__main__":
    config = get_config()
    from typing import Callable
    def create_callback(user_id) -> Callable:

        def callback(message):
            # this message is not string, but google object
            # print(message.attributes) is a dict
            if message.attributes.get("user_id") == user_id:
                # message.data is in bytes
                t = json.loads(message.data)
                print(t)
                # ws.send(str(t)) or json.dumps(t)
                message.ack()
        return callback

    r = PubSubReceiver(config=config)
    r.start(callback=create_callback(user_id="fakeuserid1"))