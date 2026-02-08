# -*- coding: utf-8 -*-

from storage.r2_storage import upload_image, get_public_url

with open("skinteste.png", "rb") as f:
    data = f.read()

key = upload_image(data, "skinteste.png")
url = get_public_url(key)

print("✅ Upload concluído com sucesso")
print(url)


# R2_PUBLIC_URL=https://SEU_BUCKET.SEU_SUBDOMINIO.r2.dev

# https://skin-bot-images.xxx.r2.dev
