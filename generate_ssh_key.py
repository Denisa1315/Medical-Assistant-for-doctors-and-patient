from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import os

home = os.path.expanduser('~')
ssh_dir = os.path.join(home, '.ssh')
if not os.path.exists(ssh_dir):
    os.makedirs(ssh_dir, exist_ok=True)

private_path = os.path.join(ssh_dir, 'medical_assistant_id_ed25519')
public_path = private_path + '.pub'

# Do not overwrite existing keys
if os.path.exists(private_path) or os.path.exists(public_path):
    print(f"Key files already exist. Private: {os.path.exists(private_path)}, Public: {os.path.exists(public_path)}")
    print("If you want to overwrite, delete existing files and run again.")
    raise SystemExit(1)

# Generate key
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Serialize private key in OpenSSH format (no encryption)
try:
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    )
except Exception:
    # Fallback to PKCS8 PEM if OpenSSH private format not supported
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

# Serialize public key in OpenSSH format
pub_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)

# Write files with correct permissions where possible
with open(private_path, 'wb') as f:
    f.write(priv_bytes)

try:
    # Set private key file permission to 600 on POSIX-like systems
    os.chmod(private_path, 0o600)
except Exception:
    pass

with open(public_path, 'wb') as f:
    f.write(pub_bytes + b"\n")

print(f"Generated SSH keypair:\nPrivate: {private_path}\nPublic: {public_path}")
print("Public key (copy the whole line below):\n")
print(pub_bytes.decode())
