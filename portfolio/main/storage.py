from django.core.files.storage import Storage
from vercel.blob import BlobClient


class VercelBlobStorage(Storage):
    def _save(self, name, content):
        client = BlobClient()

        file_data = content.read()

        blob = client.put(
            name,
            file_data,
            access="public",
            add_random_suffix=True,
        )

        return blob.pathname

    def exists(self, name):
        return False

    def url(self, name):
        client = BlobClient()
        return client.url(name)

    def delete(self, name):
        client = BlobClient()
        try:
            client.delete([self.url(name)])
        except Exception:
            pass
