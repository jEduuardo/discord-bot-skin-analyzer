from PIL import Image
import imagehash
import io

HASH_BITS = 64

def generate_hash(image_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return str(imagehash.phash(img))


def calculate_similarity(hash1: str, hash2: str) -> float:
    h1 = imagehash.hex_to_hash(hash1)
    h2 = imagehash.hex_to_hash(hash2)
    distance = h1 - h2
    return 100 - (distance * 100 / HASH_BITS)
