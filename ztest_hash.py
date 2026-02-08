from services.hash_utils import generate_phash, similarity_percent

IMG1 = r"C:\Users\Usuario\Downloads\skins1.png"
IMG2 = r"C:\Users\Usuario\Downloads\skins2.png"

h1 = generate_phash(IMG1)
h2 = generate_phash(IMG2)

similarity = similarity_percent(h1, h2)

print("Hash 1:", h1)
print("Hash 2:", h2)
print(f"Similaridade: {similarity:.2f}%")

if similarity >= 85:
    print("? Skin bloqueada (muito parecida)")
else:
    print("? Skin aceita (suficientemente diferente)")
