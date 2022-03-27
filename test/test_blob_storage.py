from multiprocessing.sharedctypes import Value
import unittest
from dotenv import load_dotenv
import uuid
import os


from src.utils.azure.blob_storage import BlobStorage, BlobStorageUpload

class TestBlobStorage(unittest.TestCase):
    load_dotenv(".env")
    def setUp(self):
        self.storage_url = os.environ.get("BLOB_STORAGE_URL")
        self.storage_key = os.environ.get("BLOB_STORAGE_KEY")
        self.account_name = os.environ.get("BLOB_STORAGE_ACCOUNT_NAME")
        self.storage_container_name = "profile-pictures"
        self.upload_data = open("test/test_files/test_file.txt", "rb")
        random_string = str(uuid.uuid4())[:4]
        self.file_name = f"test_text_file_{random_string}.txt"
        self.blob_file_link = f"{self.storage_url}/{self.storage_container_name}/{self.file_name}"
        
    def test_object_exists(self):
        class_object = BlobStorage 
        self.assertTrue(class_object)
        self.upload_data.close()
        
    def test_get_environment(self):
        class_object = BlobStorage(storage_container_name=self.storage_container_name) 
        class_object.get_environment()
        self.assertEqual(class_object.storage_url, self.storage_url)
        self.assertEqual(class_object.storage_key, self.storage_key)
        self.upload_data.close()
        
    def test_get_blob_client(self):
        class_object = BlobStorage(storage_container_name=self.storage_container_name, file_name=self.file_name) 
        class_object.get_environment()
        class_object.get_blob_client()
        self.assertEqual(class_object.blob_client.account_name, self.account_name)
        class_object.blob_client.close()
        self.upload_data.close()
    
    def test_get_blob_service_client(self):
        class_object = BlobStorage(storage_container_name=self.storage_container_name) 
        class_object.get_environment()
        class_object.get_blob_service_client()
        self.assertEqual(class_object.blob_service_client.account_name, self.account_name)
        self.assertEqual(class_object.storage_container_name, self.storage_container_name)
        class_object.blob_service_client.close()
        self.upload_data.close()
        
    def test_get_storage_container_client(self):
        class_object = BlobStorage(storage_container_name=self.storage_container_name) 
        class_object.get_environment()
        class_object.get_blob_service_client()
        class_object.get_storage_container_client()
        self.assertEqual(class_object.storage_container.container_name, self.storage_container_name)
        class_object.storage_container.close()
        self.upload_data.close()
           
    def test_upload_file_to_container(self):
        class_object = BlobStorageUpload(storage_container_name=self.storage_container_name, upload_data=self.upload_data, file_name=self.file_name) 
        class_object.get_environment()
        class_object.get_blob_service_client()
        class_object.get_storage_container_client()
        class_object.upload_data_to_container()
        class_object.get_blob_client() # to use the exists() method in next line for test 
        self.assertTrue(class_object.blob_client.exists()) # tests a file exists on blob
        class_object.storage_container.close()
        class_object.blob_service_client.close()
        class_object.blob_client.close()
        self.upload_data.close()
        
    def test_upload_file_to_container_file_link(self):
        class_object = BlobStorageUpload(storage_container_name=self.storage_container_name, upload_data=self.upload_data, file_name=self.file_name) 
        class_object.get_environment()
        class_object.get_blob_service_client()
        class_object.get_storage_container_client()
        class_object.upload_data_to_container()
        class_object.get_blob_file_link()
        class_object.get_blob_client() # to use the exists() method in next line for test 
        self.assertTrue(class_object.blob_client.exists()) # tests a file exists on blob
        self.assertEqual(class_object.blob_file_link, self.blob_file_link)
        class_object.storage_container.close()
        class_object.blob_service_client.close()
        class_object.blob_client.close()
        self.upload_data.close()