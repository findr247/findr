from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client
from django.conf import settings
import os


class SupabaseStorage(Storage):
    def __init__(self):
        # Initialize Supabase client using credentials from settings
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.bucket_name = settings.SUPABASE_BUCKET_NAME  # Bucket name from settings

    def _open(self, name, mode='rb'):
        # Fetch the file from Supabase
        response = self.supabase.storage.from_(self.bucket_name).download(name)
        if response.error:
            raise FileNotFoundError(f"The file {name} could not be opened.")
        return ContentFile(response.content)

    def _save(self, name, content):
        name = name.replace('\\', '/')
        # Save the file to Supabase
        content.open()  # Ensure the content file is open
        response = self.supabase.storage.from_(self.bucket_name).upload(name, content.read())
        content.close()
        if not response:
            raise Exception(f"Error uploading file: {response.error.message}")
        return name

    def delete(self, name):
        # Delete the file from Supabase
        response = self.supabase.storage.from_(self.bucket_name).remove([name])
        if not response:
            raise Exception(f"Error deleting file: {response.error.message}")

    def exists(self, name):
        response = self.supabase.storage.from_(self.bucket_name).list(path=os.path.dirname(name))
        return any(file['name'] == os.path.basename(name) for file in response)

    def url(self, name):
        # Return the public URL for the file
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{name}"

    def size(self, name):
        response = self.supabase.storage.from_(self.bucket_name).list(path=os.path.dirname(name))
        file_metadata = next((file for file in response if file['name'] == os.path.basename(name)), None)
        if file_metadata:
            return file_metadata['metadata']['size']  # File size in bytes
        raise FileNotFoundError(f"The file {name} does not exist.")
