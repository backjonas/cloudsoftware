import os
from google.cloud import storage
import functions_framework

@functions_framework.http
def create_text_file_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        Return the fileName in the body of the response.
        Return a HTTP status code of 200.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    request_data = request.get_json()
    file_name = request_data.get('fileName')
    file_content = request_data.get('fileContent')
    storage_client = storage.Client()
    bucket_name = os.environ.get('BUCKET_ENV_VAR')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    with blob.open('w') as file:
        file.write(file_content)

    return { "fileName": file_name }