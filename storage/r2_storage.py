# -*- coding: utf-8 -*-

import os
import uuid
import boto3
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL") 


# Cliente S3 (Cloudflare R2)
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name="auto",
)


def upload_image(
    file_bytes: bytes,
    original_filename: str,
    folder: str = "skins",
) -> str:
    """
    Faz upload de uma imagem para o Cloudflare R2.
    Retorna a key do objeto (caminho dentro do bucket).
    """

    extension = os.path.splitext(original_filename)[1].lower()
    unique_name = f"{uuid.uuid4()}{extension}"
    object_key = f"{folder}/{unique_name}"

    print("\n📤 Upload para Cloudflare R2")
    print("──────────────────────────")
    print(f"📦 Bucket : {R2_BUCKET}")
    print(f"🗂️ Key    : {object_key}")

    s3.put_object(
        Bucket=R2_BUCKET,
        Key=object_key,
        Body=file_bytes,
        ContentType=_guess_content_type(extension),
        ACL="public-read",
    )

    print("✅ Upload concluído com sucesso")

    return object_key


def get_public_url(object_key: str) -> str:
    """
    Retorna a URL pública do arquivo no R2.
    """

    if not R2_PUBLIC_URL:
        raise RuntimeError(
            "R2_PUBLIC_URL não configurada no arquivo .env"
        )

    return f"{R2_PUBLIC_URL}/{object_key}"


def _guess_content_type(extension: str) -> str:
    """
    Define Content-Type básico baseado na extensão.
    """
    if extension == ".png":
        return "image/png"
    if extension in [".jpg", ".jpeg"]:
        return "image/jpeg"
    if extension == ".webp":
        return "image/webp"
    return "application/octet-stream"
