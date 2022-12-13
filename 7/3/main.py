import os
import json
import base64
from concurrent import futures
from google.cloud import pubsub_v1
import functions_framework


@functions_framework.cloud_event
def restaurant_orders_pubsub(cloud_event):
    message_data = cloud_event.data['message']['data']
    decoded_message = base64.b64decode(message_data)
    attrs = json.loads(decoded_message)

    type = attrs.get('type', None) 
    if type == 'takeout':
        topic_id = 'restaurant_takeout_orders'
    elif type == 'eat-in':
        topic_id = 'restaurant_eat-in_orders'
    else:
        return

    publisher = pubsub_v1.PublisherClient()
    project_id = 'sunlit-mantra-363108'
    topic_path = publisher.topic_path(project_id, topic_id)
    publisher.publish(topic_path, json.dumps(attrs).encode('utf-8'))
    return
