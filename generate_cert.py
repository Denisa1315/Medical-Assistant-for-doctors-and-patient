"""
Generate self-signed SSL certificate using Python
No external tools needed!
"""

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime
import os

# Certificate details
hostname = "10.152.119.140"
key_file = f"{hostname}-key.pem"
cert_file = f"{hostname}.pem"

print("🔐 Generating self-signed SSL certificate...")
print(f"   Hostname: {hostname}")
print(f"   Key file: {key_file}")
print(f"   Cert file: {cert_file}")

# Check if already exist
if os.path.exists(key_file) and os.path.exists(cert_file):
    print("✅ Certificate already exists!")
    exit(0)

# Generate private key
print("\n1️⃣ Generating private key...")
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate certificate
print("2️⃣ Generating certificate...")
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"India"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Chennai"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Medical Assistant"),
    x509.NameAttribute(NameOID.COMMON_NAME, hostname),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName(hostname),
        x509.DNSName(f"*.{hostname}"),
    ]),
    critical=False,
).sign(private_key, hashes.SHA256(), default_backend())

# Save private key
print("3️⃣ Saving private key...")
with open(key_file, "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Save certificate
print("4️⃣ Saving certificate...")
with open(cert_file, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("\n" + "="*60)
print("✅ SSL CERTIFICATE GENERATED SUCCESSFULLY!")
print("="*60)
print(f"✅ Private key: {key_file}")
print(f"✅ Certificate: {cert_file}")
print(f"✅ Valid for: 365 days")
print(f"✅ Hostname: {hostname}")
print("\nYou can now use these files with serve_https.py")
print("="*60)
