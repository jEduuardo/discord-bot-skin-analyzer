from PIL import Image
import imagehash

def generate_phash(image_path: str) -> str:
    """
    Gera hash perceptual (pHash) da imagem
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        return str(imagehash.phash(img))


def similarity_percent(hash_a: str, hash_b: str) -> float:
    """
    Retorna similaridade percentual entre dois hashes
    """
    h1 = imagehash.hex_to_hash(hash_a)
    h2 = imagehash.hex_to_hash(hash_b)

    distance = h1 - h2
    max_bits = h1.hash.size

    return round((1 - distance / max_bits) * 100, 2)
