import json
from google.auth import jwt
from google.cloud import pubsub_v1
from app.utils.config import get_config, Settings

def get_publisher(config: Settings):
    service_account_info = json.load(open(config.PUBLISHER_CRED_LOCATION))

    audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
    credentials = jwt.Credentials.from_service_account_info(
        service_account_info, audience=audience
    )
    credentials_pub = credentials.with_claims(audience=audience)
    return pubsub_v1.PublisherClient(credentials=credentials_pub)


def publish(publisher: pubsub_v1.PublisherClient, config: Settings):
    topic_name = f"projects/{config.GCP_PROJECT}/topics/{config.GCP_TOPIC}"

    # subscription_name = f"projects/{config.GCP_PROJECT}/subscriptions/{config.GCP_SUB}"
    # publisher.create_topic(name=topic_name)

    # here we put up json data
    tasks = {
        "task_id": "1123",
        "foo": "bar",
        "x": 1.33,
        "y": True,
        "z": None
    }
    future = publisher.publish(topic_name, json.dumps(tasks).encode(), spam='eggs')
    future.result()


if __name__ == "__main__":
    config = get_config()
    p = get_publisher(config=config)
    publish(publisher=p, config=config)