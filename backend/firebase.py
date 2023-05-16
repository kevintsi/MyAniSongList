import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('anisonglist-firebase-admin.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'anisonglist.appspot.com'
})

bucket = storage.bucket()

# 'bucket' is an object defined in the google-cloud-storage Python library.
# See https://googlecloudplatform.github.io/google-cloud-python/latest/storage/buckets.html
# for more details.
