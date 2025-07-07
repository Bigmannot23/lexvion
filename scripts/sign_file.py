from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import sys

if len(sys.argv) != 2:
    print("Usage: python sign_file.py <file_to_sign>")
    sys.exit(1)

file_to_sign = sys.argv[1]

# Load private key
with open("output_watermarking/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Read file content
with open(file_to_sign, "rb") as f:
    content = f.read()

# Sign the file
signature = private_key.sign(
    content,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256(),
)

# Save the signature
sig_filename = file_to_sign + ".sig"
with open(sig_filename, "wb") as f:
    f.write(signature)

print(f"Signed: {file_to_sign}")
print(f"Signature saved as: {sig_filename}")
