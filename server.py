import base64
import os
import gzip
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from flask import Flask, request, jsonify

### Environment variables
load_dotenv()

PORT = int( os.getenv("PORT") )
FORMAT = os.getenv("FORMAT")

### Encryption data
key = Fernet.generate_key()
cipherSuite = Fernet(key)

### Server
app = Flask(__name__)

@app.route("/", methods=["GET"])
def serveKey():
    return jsonify(
        {"key": key.decode(FORMAT) }
    )

@app.route("/", methods=["POST"])
def takeFile():
    req = request.get_json()

    name = req.get("name", "DEFAULT")
    files = req.get("files", {})

    for fileName, fileData in files.items():
        fileContent = base64.b64decode(fileData.encode(FORMAT))
        fileContent = gzip.decompress(fileContent)
        fileContent = cipherSuite.decrypt(fileContent)

        # Open file to write to
        os.makedirs(name, exist_ok=True)
        with open(os.path.join(name, fileName), "wb") as file:
            file.write(fileContent)
            print("Created " + fileName)

    return jsonify(message="success")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)