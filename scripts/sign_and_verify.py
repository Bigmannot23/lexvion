from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Load keys
with open("output_watermarking/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("output_watermarking/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

def sign_output(content_bytes):
    return private_key.sign(
        content_bytes,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )

def verify_output(content_bytes, signature):
    try:
        public_key.verify(
            signature,
            content_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False

if __name__ == "__main__":
    # Example: sign some text and immediately verify it
    content = b"Sample output for Lexvion compliance"
    sig = sign_output(content)
    print("Signature (hex):", sig.hex())

    # Save signature
    with open("output_watermarking/sample.sig", "wb") as f:
        f.write(sig)

    # Save content as well
    with open("output_watermarking/sample.txt", "wb") as f:
        f.write(content)

    # Try verifying
    is_valid = verify_output(content, sig)
    print("Signature valid?", is_valid)
