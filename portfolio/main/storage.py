import os
import requests

from django.core.files.storage import Storage
from vercel.oidc import get_vercel_oidc_token


class VercelBlobStorage(Storage):

    def _get_auth(self):
        token = get_vercel_oidc_token()
        store_id = os.environ["BLOB_STORE_ID"]

        if not token:
            raise RuntimeError("Vercel OIDC token was not found.")

        return token, store_id

    def _save(self, name, content):
        token, store_id = self._get_auth()

        file_data = content.read()

        url = "https://vercel.com/api/blob"

        response = requests.put(
            url,
            params={"pathname": name},
            headers={
                "Authorization": f"Bearer {token}",
                "x-vercel-blob-store-id": store_id.replace("store_", ""),
                "x-api-version": "12",
            },
            data=file_data,
            timeout=30,
        )

        response.raise_for_status()

        blob = response.json()

        return blob["pathname"]

    def exists(self, name):
        return False

    def url(self, name):
        store_id = os.environ["BLOB_STORE_ID"].replace("store_", "")
        return f"https://{store_id}.public.blob.vercel-storage.com/{name}"

    def delete(self, name):
        try:
            token, store_id = self._get_auth()

            url = "https://vercel.com/api/blob/delete"

            requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "x-vercel-blob-store-id": store_id.replace("store_", ""),
                    "x-api-version": "12",
                    "Content-Type": "application/json",
                },
                json={"urls": [name]},
                timeout=30,
            ).raise_for_status()

        except Exception:
            pass
