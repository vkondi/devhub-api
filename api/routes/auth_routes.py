from flask import Blueprint, jsonify, request
from services.rsa_encryption_service import RSAEncryption
from cryptography.hazmat.primitives import serialization

# Initialize RSA Encryption Manager
rsa_manager = RSAEncryption()

# Create a blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/public_key', methods=['GET'])
def get_public_key():
    """
    Enfdpoint to retrieve the RSA public key.
    """
    if rsa_manager.public_key:
        try:
            public_key_pem = rsa_manager.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            return jsonify({
                "publicKey": public_key_pem.decode('utf-8')
            }), 200
        except Exception as e:
            print(f"[auth_bp][get_public_key] >> Error retrieving public key: {e}")
            return jsonify({"error": "Failed to retrieve public key"}), 500
    else:
        return jsonify({"error": "Public key not available"}), 500
    

@auth_bp.route('/encrypt_test/<string:plaintext>', methods=['GET'])
def encrypt_test(plaintext):
    """
    Endpoint to test RSA encryption of a given plaintext string.
    """
    try:
        ciphertext = rsa_manager.encrypt(plaintext)
        if ciphertext:
            return jsonify({
                "plaintext": plaintext,
                "ciphertext": ciphertext
            }), 200
        else:
            return jsonify({"error": "Encryption failed"}), 500
    except Exception as e:
        print(f"[auth_bp][encrypt_test] >> Error during encryption: {e}")
        return jsonify({"error": "Encryption error"}), 500
    
@auth_bp.route('/decrypt_test', methods=['POST'])
def decrypt_test():
    """
    Endpoint to test RSA decryption of a given Base64-encoded ciphertext string.
    Expects JSON body with 'ciphertext' field.
    """
    data = request.get_json()
    if not data or 'ciphertext' not in data:
        return jsonify({"error": "Missing 'ciphertext' in request body"}), 400
    
    ciphertext_b64 = data['ciphertext']
    try:
        plaintext = rsa_manager.decrypt(ciphertext_b64)
        if plaintext:
            return jsonify({
                "ciphertext": ciphertext_b64,
                "plaintext": plaintext
            }), 200
        else:
            return jsonify({"error": "Decryption failed"}), 500
    except Exception as e:
        print(f"[auth_bp][decrypt_test] >> Error during decryption: {e}")
        return jsonify({"error": "Decryption error"}), 500