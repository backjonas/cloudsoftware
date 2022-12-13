import os
import io 
from google.cloud import storage, vision
import functions_framework


@functions_framework.cloud_event
def image_to_text_storage(cloud_event):
    data = cloud_event.data

    bucket_name = data['bucket']
    file_name = data['name']

    if file_name.endswith('txt'):
        return



    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(f'/tmp/{file_name}')
    with io.open(f'/tmp/{file_name}', 'rb') as file:
        content = file.read()
    
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    text_annotations = client.text_detection(image=image).text_annotations
    response_text = ''.join([i.description for i in text_annotations])

    file_name = os.path.splitext(file_name)[0]
    blob = bucket.blob(f'{file_name}.txt')
    with blob.open('w') as file:
        file.write(response_text)
