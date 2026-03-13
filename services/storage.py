import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
BUCKET = os.getenv("SUPABASE_BUCKET")

def upload_avatar(file_bytes, filename, content_type):

    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{filename}"

    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": content_type
    }

    response = requests.post(
        url,
        headers=headers,
        data=file_bytes
    )

    if response.status_code not in [200, 201]:
        raise Exception(response.text)

    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{filename}"