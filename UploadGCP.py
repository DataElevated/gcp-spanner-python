from google.oauth2 import service_account
from google.cloud import storage

def ListAllBuckets():
    """Lists all buckets."""

    credentials = service_account.Credentials.from_service_account_file(
    './digitalcore-poc-67645bca1a2a.json')
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)
        blobs = storage_client.list_blobs(bucket)
        for blob in blobs:
            print(blob.name)

def ListBlob(bucket, blob):
    """Lists all buckets."""

    credentials = service_account.Credentials.from_service_account_file(
    './digitalcore-poc-67645bca1a2a.json')
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)
        blobs = storage_client.list_blobs(bucket)
        for blob in blobs:
            print(blob.name)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    blob

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


if __name__ == '__main__':
    import glob,sys,os
    # This is my path
    path="E:/Project/Spanner/Phase1/Data/1-staged/Production/Transactions"
    for CurrentFile in glob.glob(path + '/*.csv'):
        print(CurrentFile)
        fileName_absolute = os.path.basename(CurrentFile)                
        print("Only file name: ", fileName_absolute)
        upload_blob("ddoctest", CurrentFile, "data/1-staged/Production/Transactions/{}".format(fileName_absolute))