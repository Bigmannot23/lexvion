from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import sys

if len(sys.argv) != 3:
    print("Usage: python verify_file.py <file_to_verify> <signature_file>")
    sys.exit(1)

file_to_verify = sys.argv[1]
signature_file = sys.argv[2]

# Load public key
with open("output_watermarking/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Read file content
with open(file_to_verify, "rb") as f:
    content = f.read()

# Read signature
with open(signature_file, "rb") as f:
    signature = f.read()

# Verify
try:
    public_key.verify(
        signature,
        content,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    print("Signature is VALID.")
except Exception:
    print("Signature is INVALID or file has been tampered with.")
