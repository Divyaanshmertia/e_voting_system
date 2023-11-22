from flask import current_app
from google.cloud import storage

class GCSUtil:
    @staticmethod
    def upload_file_to_gcs(file_stream, filename):
        """
        Uploads a file to Google Cloud Storage.

        Args:
            file_stream: The file stream to upload.
            filename: The name of the file in the storage bucket.

        Returns:
            The public URL of the uploaded file.
        """
        client = storage.Client()
        bucket = client.bucket(current_app.config['GCS_BUCKET'])
        blob = bucket.blob(filename)
        blob.upload_from_string(
            file_stream.read(),
            content_type=file_stream.content_type
        )
        return blob.public_url
