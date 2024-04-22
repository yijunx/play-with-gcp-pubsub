# play-with-gcp-pubsub

here are the documentation
https://cloud.google.com/python/docs/reference/pubsub/latest

### steps

* go the gcp pubsub, create a topic, under the topic, create sub
* copy the dev.env.template, use your topic, and sub
* create 2 service acct on gcloud. 
    * pub/sub publisher
    * pub/sub subscriber
* download the json credential and save in credentials
    * go into the service accounts
    * click on keys, then add a json key, then it will be downloaded. save them as `publisher.json` and `subscriber.json` in the place specified by your dev.env
* now you are good to go, time to use
    * app/tasks.py to listen
    * app/create_task.py to put tasks for tasks.py to listen and process
    
### experiments

* on each worker, the tasks are done asynchronizely. this can be demonstrated by the `SlowHandler`. 

    ```
    class SlowHandler(BaseHandler):
        def handle(self, task):
            time.sleep(5)
            print(f"slowly handled at {datetime.now()}")
    ```


    if there are multiple tasks running with this slowhandler (io bound), a task will not wait for 5 seconds to start next.

* multiple workers:

    this can be demonstrated by open 3 terminals in the devcontainer. one terminal keeps running `python app/create_task.py`. and the other 2 runs `python app/tasks.py` to execute the tasks. we can see that the tasks are distributed among the 2 worker! (but not sure how, but they dont do duplicate work! thats the best!)

* anything like the routing key:

    yes there is. this can be done by attributes. say in when create task:

    ```
    tasks = {
        "task_id": "1123",
        "foo": "bar",
        "x": 1.33,
        "y": True,
        "z": None
    }
    future = publisher.publish(
        topic_name,
        json.dumps(tasks).encode(),
        user_id='fakeuserid1'
    )
    future.result()
    ```

    here i added `user_id=xxxxx` when publish. then at the receiving end: here we can let user only get (and ack) his message, based on attributes!!

    ```
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
    ```

* how to package this together with celery + redis|rmq for task queue
    * actually just the main.py (or its equivalent needs to change), and maybe check things like retry..
    * the rest should be very easy to migrate because they are just handlers
