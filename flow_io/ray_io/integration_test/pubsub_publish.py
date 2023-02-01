import json

from google.cloud import pubsub_v1

topic = 'projects/pubsub-test-project/topics/incoming_topic'
client = pubsub_v1.PublisherClient()
print('Publishing to: ', topic)
future = client.publish(topic, json.dumps({'field': 1}).encode('UTF-8'))
future.result()
