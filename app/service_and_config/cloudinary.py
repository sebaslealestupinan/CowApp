import cloudinary
from  cloudinary.uploader import upload
import cloudinary.api
import os
from dotenv import load_dotenv
from fastapi import UploadFile
import uuid
load_dotenv()

CLOUDINARY_CLOUD = os.getenv("CLOUDINARY_CLOUD")
CLOUDINARY_KEY = os.getenv("CLOUDINARY_KEY")
CLOUDINARY_SECRET = os.getenv("CLOUDINARY_SECRET")

_configured = False

def init_cloudinary():
    global _configured
    if not _configured:
        if not CLOUDINARY_CLOUD or not CLOUDINARY_KEY or not CLOUDINARY_SECRET:
            raise ValueError("Faltan credenciales de Cloudinary")

        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD,
            api_key=CLOUDINARY_KEY,
            api_secret=CLOUDINARY_SECRET,
            secure=True
        )
        _configured = True

async def upload_to_cloudinary(file: UploadFile):
    init_cloudinary()

    file_content = await file.read()
    filename = f"{uuid.uuid4()}_{file.filename}"

    result = upload(
        file_content,
        public_id=filename,
        folder="fastapi_uploads",
        resource_type="auto"
    )

    return {
        "url": result.get("secure_url"),
        "public_id": result.get("public_id"),
        "size": result.get("bytes"),
        "format": result.get("format")
    }