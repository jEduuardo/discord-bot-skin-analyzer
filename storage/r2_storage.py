# -*- coding: utf-8 -*-

import os
import uuid
import boto3
from dotenv import load_dotenv

<<<<<<< HEAD
# Carrega variáveis de ambiente
=======
# Carrega vari�veis de ambiente
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68
load_dotenv()

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")
<<<<<<< HEAD
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL") 

=======
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")  # opcional, mas recomendado
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68

# Cliente S3 (Cloudflare R2)
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
<<<<<<< HEAD
    region_name="auto",
=======
    region_name="auto"
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68
)


def upload_image(
    file_bytes: bytes,
    original_filename: str,
<<<<<<< HEAD
    folder: str = "skins",
) -> str:
    """
    Faz upload de uma imagem para o Cloudflare R2.
    Retorna a key do objeto (caminho dentro do bucket).
=======
    folder: str = "skins"
) -> str:
    """
    Faz upload de uma imagem para o Cloudflare R2
    Retorna a key do objeto (caminho dentro do bucket)
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68
    """

    extension = os.path.splitext(original_filename)[1].lower()
    unique_name = f"{uuid.uuid4()}{extension}"
    object_key = f"{folder}/{unique_name}"

<<<<<<< HEAD
    print("\n📤 Upload para Cloudflare R2")
    print("──────────────────────────")
    print(f"📦 Bucket : {R2_BUCKET}")
    print(f"🗂️ Key    : {object_key}")
=======
    print("\n?? Upload para Cloudflare R2")
    print("??????????????????????????")
    print(f"?? Bucket : {R2_BUCKET}")
    print(f"?? Key    : {object_key}")
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68

    s3.put_object(
        Bucket=R2_BUCKET,
        Key=object_key,
        Body=file_bytes,
        ContentType=_guess_content_type(extension),
<<<<<<< HEAD
        ACL="public-read",
    )

    print("✅ Upload concluído com sucesso")
=======
        ACL="public-read"
    )

    print("? Upload conclu�do com sucesso")
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68

    return object_key


def get_public_url(object_key: str) -> str:
    """
<<<<<<< HEAD
    Retorna a URL pública do arquivo no R2.
=======
    Retorna a URL p�blica do arquivo no R2
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68
    """

    if not R2_PUBLIC_URL:
        raise RuntimeError(
<<<<<<< HEAD
            "R2_PUBLIC_URL não configurada no arquivo .env"
=======
            "R2_PUBLIC_URL n�o configurada no .env"
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68
        )

    return f"{R2_PUBLIC_URL}/{object_key}"


def _guess_content_type(extension: str) -> str:
    """
<<<<<<< HEAD
    Define Content-Type básico baseado na extensão.
    """
    if extension == ".png":
        return "image/png"
    if extension in [".jpg", ".jpeg"]:
        return "image/jpeg"
    if extension == ".webp":
=======
    Define Content-Type b�sico baseado na extens�o
    """
    if extension in [".png"]:
        return "image/png"
    if extension in [".jpg", ".jpeg"]:
        return "image/jpeg"
    if extension in [".webp"]:
>>>>>>> fba511dfb6b5229b5842777eae7386494812dd68
        return "image/webp"
    return "application/octet-stream"
