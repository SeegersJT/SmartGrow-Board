import firebase_admin
from firebase_admin import credentials, storage
import os
import sys

# optional: Import UUID4 to create access token
from uuid import uuid4

# base64 decoded key file will be stored in temporary directory on runner machine
# https://github.com/marketplace/actions/base64-to-file
githubTempPath = '/Users/runner/work/_temp'

# google cloud's service account key file absolute path on github's machine directory
# note that the file name must be matched with the file name created from timheuer/base64-to-file@v1 action on the workflow
keyFilePath = githubTempPath + '/smart-grow-41b4b-c5425ce2afb8.json'

# apply the bucket domain to the credentials
cred = credentials.Certificate(keyFilePath)
firebase_admin.initialize_app(cred, {
    'storageBucket' : 'smart-grow-41b4b.appspot.com'
})

# refer to the storage bucket
bucket = storage.bucket()

# get the upload file's path in repository's directory
# the file to upload in this scenario (a zip file) is in the same directory with the script
# fileName = 'firmware.bin'
# dirname = os.path.dirname(os.path.realpath(__file__))
# fileFullPath = dirname + '/' + fileName
dirname = os.path.dirname(os.path.realpath(__file__))
fileFullPath = '..//.pio//build//esp32doit-devkit-v1//firmware.bin'

print("fileFullPath")
print(fileFullPath)

print("dirname")
print(dirname)

# if the file name contains file path, the bucket will create folders corresponding to the path.
blob = bucket.blob(fileFullPath)

# optional: Create new token, this one only used for downloading directly from firebase console page
accessToken = uuid4()

# optional: Create new dictionary with the metadata
metadata = { "firebaseStorageDownloadTokens": accessToken }

# optional: Set meta data for the blob wich contains the access token
blob.metadata = metadata

#upload to firebase storage
blob.upload_from_filename(fileFullPath)

# optional: make the file public
blob.make_public()

print("your file url ", blob.public_url)

#==================================================================
# Open the binary file for reading

file = open(fileFullPath, "rb")

# Read the first five numbers into a list

number = list(file.read(5))

# Print the list

print(number)

# Close the file

file.close()