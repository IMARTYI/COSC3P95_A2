import base64
import gzip
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import requests

### Environment variables
load_dotenv()

PORT = int( os.getenv("PORT") )
FORMAT = os.getenv("FORMAT")
FOLDER_NAME = "localFolder"

url = f"http://127.0.0.1:{PORT}/"
def main():
    ## Get the key
    response = requests.get(url)
    key = response.json()["key"]
    cipherSuite = Fernet( key.encode(FORMAT) )

    # Get list of file names in folder
    files = os.listdir(FOLDER_NAME) # Grab the contents of the file to send
    filesJSON = {}

    ## Construct the files json
    for fileName in files:
        # Open each file in byte read mode
        with open(os.path.join(FOLDER_NAME, fileName), "r") as file:
            fileContent = file.read().encode(FORMAT)
            encryptedContent = cipherSuite.encrypt(fileContent)
            encryptedContent = gzip.compress(encryptedContent)
            filesJSON[fileName] = base64.b64encode(encryptedContent).decode(FORMAT)
    
    requests.post(url, json={
        "name": "NAME",
        "files": filesJSON
    })

if __name__ == "__main__":
    main()