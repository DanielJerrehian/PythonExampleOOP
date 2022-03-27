from azure.storage.blob import BlobServiceClient, BlobClient
import os


class BlobStorage:
    def __init__(self, storage_container_name=None, file_name=None):
        self.storage_container_name = storage_container_name
        self.file_name = file_name
        self.blob_service_client = None
        self.blob_client = None
        self.storage_url = None
        self.storage_key = None
        self.connection_string = None
        self.storage_container = None
            
    def get_environment(self):
        self.storage_url = os.environ.get("BLOB_STORAGE_URL")
        self.storage_key = os.environ.get("BLOB_STORAGE_KEY")
        self.connection_string = os.environ.get("BLOB_CONNECTION_STRING")
            
    def get_blob_client(self):
        self.blob_client = BlobClient.from_connection_string(conn_str=self.connection_string, container_name=self.storage_container_name, blob_name=self.file_name)        
            
    def get_blob_service_client(self):
        self.blob_service_client = BlobServiceClient(account_url=self.storage_url, credential=self.storage_key)
                
    def get_storage_container_client(self):
        self.storage_container = self.blob_service_client.get_container_client(self.storage_container_name)
        

class BlobStorageUpload(BlobStorage):
    def __init__(self, storage_container_name=None, upload_data=None, file_name=None):
        super().__init__(storage_container_name=storage_container_name, file_name=file_name)
        self.upload_data = upload_data
        self.file_name = file_name
        self.blob_file_link = None
            
    def upload_data_to_container(self):
        self.storage_container.upload_blob(name=self.file_name, data=self.upload_data)
        
    def get_blob_file_link(self):
        self.blob_file_link = f"{self.blob_service_client.url}{self.storage_container_name}/{self.file_name}"

    