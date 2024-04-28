from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def generate_symmetric_key():
    return Fernet.generate_key().hex()


@app.get("/symmetric/key")
def get_symmetric_key():
    global symmetric_key
    symmetric_key = generate_symmetric_key()
    return {"key": symmetric_key}


@app.post("/symmetric/key")
def set_symmetric_key(key: str):
    global symmetric_key
    symmetric_key = key


@app.post("/symmetric/encode")
def symmetric_encode(message: str):
    symmetric_key = generate_symmetric_key
    if not symmetric_key:
        raise HTTPException(status_code=400, detail="Symmetric key not set")
    cipher = Fernet(Fernet.generate_key())
    encrypted_message = cipher.encrypt(message.encode())
    return {"encrypted_message": encrypted_message.decode()}


@app.post("/symmetric/decode")
def symmetric_decode(encrypted_message: str):
    global symmetric_key
    if not symmetric_key:
        raise HTTPException(status_code=400, detail="Symmetric key not set")
    cipher = Fernet(symmetric_key)
    decrypted_message = cipher.decrypt(encrypted_message.encode())
    return {"decrypted_message": decrypted_message.decode()}


def generate_asymmetric_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


asymmetric_private_key, asymmetric_public_key = generate_asymmetric_key()


@app.get("/asymmetric/key")
def get_asymmetric_key():
    global asymmetric_private_key, asymmetric_public_key
    asymmetric_private_key, asymmetric_public_key = generate_asymmetric_key()
    return {
        "private_key": asymmetric_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode(),
        "public_key": asymmetric_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
    }


@app.get("/asymmetric/key/ssh")
def get_asymmetric_key_ssh():
    global asymmetric_private_key, asymmetric_public_key
    if not asymmetric_private_key or not asymmetric_public_key:
        raise HTTPException(status_code=400, detail="Asymmetric key pair not generated")
    private_ssh = asymmetric_private_key.private_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    public_ssh = asymmetric_public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    ).decode()
    return {"private_key": private_ssh, "public_key": public_ssh}


@app.post("/asymmetric/key")
def set_asymmetric_key(keys: dict):
    global asymmetric_private_key, asymmetric_public_key
    try:
        private_key = serialization.load_pem_private_key(
            keys["private_key"].encode(),
            password=None,
            backend=default_backend()
        )
        public_key = serialization.load_pem_public_key(
            keys["public_key"].encode(),
            backend=default_backend()
        )
        asymmetric_private_key = private_key
        asymmetric_public_key = public_key
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid keys: {e}")


@app.post("/asymmetric/verify")
def asymmetric_verify(message: str):
    global asymmetric_private_key
    if not asymmetric_private_key:
        raise HTTPException(status_code=400, detail="Asymmetric key not set")
    signature = asymmetric_private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return {"signature": signature.hex()}


@app.post("/asymmetric/sign")
def asymmetric_sign(message: str, signature: str):
    global asymmetric_public_key
    if not asymmetric_public_key:
        raise HTTPException(status_code=400, detail="Asymmetric key not set")
    try:
        asymmetric_public_key.verify(
            bytes.fromhex(signature),
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return {"verified": True}
    except Exception as e:
        return {"verified": False, "error": str(e)}


@app.post("/asymmetric/encode")
def asymmetric_encode(message: str):
    global asymmetric_public_key
    if not asymmetric_public_key:
        raise HTTPException(status_code=400, detail="Asymmetric key not set")
    encrypted_message = asymmetric_public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return {"encrypted_message": encrypted_message.hex()}


@app.post("/asymmetric/decode")
def asymmetric_decode(encrypted_message: str):
    global asymmetric_private_key
    if not asymmetric_private_key:
        raise HTTPException(status_code=400, detail="Asymmetric key not set")
    decrypted_message = asymmetric_private_key.decrypt(
        bytes.fromhex(encrypted_message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return {"decrypted_message": decrypted_message.decode()}
