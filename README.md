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
    


