# -*- coding: utf-8 -*-

import os
import boto3
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")

# Cliente S3 (Cloudflare R2 é compatível com S3)
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name="auto"
)

print("\n🌐 Conexão com Cloudflare R2")
print("════════════════════════════")
print(f"🔗 Endpoint : {R2_ENDPOINT}")
print(f"🪣 Bucket   : {R2_BUCKET}")
print("════════════════════════════")

try:
    response = s3.list_objects_v2(Bucket=R2_BUCKET)

    status = response["ResponseMetadata"]["HTTPStatusCode"]

    if status == 200:
        print("✅ Conexão realizada com sucesso!")
        print(f"📂 Objetos no bucket: {response.get('KeyCount', 0)}")
    else:
        print(f"❌ Erro na conexão (status {status})")

    print("\n📄 Detalhes técnicos")
    print("────────────────────")
    print("HTTP Status:", status)
    print(
        "Request ID :",
        response["ResponseMetadata"]["HTTPHeaders"].get("cf-ray")
    )

except Exception as e:
    print("❌ Falha ao conectar no Cloudflare R2")
    print("Erro:", e)
