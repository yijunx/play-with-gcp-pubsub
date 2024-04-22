# this is the place where the the tasks are done..
import json
from google.auth import jwt
from google.cloud import pubsub_v1
from app.utils.config import get_config, Settings
import json
from app.handlers.base_handler import SlowHandler


def get_subsriber(config: Settings):
    service_account_info = json.load(open(config.SUBSCRIBER_CRED_LOCATION))
    audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

    credentials = jwt.Credentials.from_service_account_info(
        service_account_info, audience=audience
    )
    return pubsub_v1.SubscriberClient(credentials=credentials)


def do_tasks(subclient: pubsub_v1.SubscriberClient, config: Settings):
    # topic_name = f"projects/{config.GCP_PROJECT}/topics/{config.GCP_TOPIC}"

    subscription_name = f"projects/{config.GCP_PROJECT}/subscriptions/{config.GCP_SUB}"

    def callback(message):
        # print(message.data)

        t = json.loads(message.data)
        # print(message.attributes)  # -> {'spam': 'eggs'}
        SlowHandler().handle(task=t)
        # print(type(message))
        message.ack()

    with subclient as subscriber:
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
    subclient = get_subsriber(config=config)
    do_tasks(subclient=subclient, config=config)