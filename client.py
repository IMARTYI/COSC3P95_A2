import random
import base64
import gzip
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import requests

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource

#### Set up Jaeger exporter and tracing
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

tracer_provider = TracerProvider(resource=Resource.create({"service.name": "client"}))
trace.set_tracer_provider(tracer_provider)
tracer_provider.add_span_processor(SimpleSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer(__name__)

### Environment variables
load_dotenv()

PORT = int( os.getenv("PORT") )
FORMAT = os.getenv("FORMAT")
FOLDER_NAME = "localFolder"

url = f"http://127.0.0.1:{PORT}/"

names = ["David", "Marty", "Person", "Someone", "Rex", "John Doe"]

def main():
    with tracer.start_as_current_span("Get Key") as span:
        ## Get the key
        response = requests.get(url)
        key = response.json()["key"]
        cipherSuite = Fernet( key.encode(FORMAT) )

    with tracer.start_as_current_span("Construct JSON") as span:
        # Get list of file names in folder
        files = os.listdir(FOLDER_NAME) # Grab the contents of the file to send
        filesJSON = {}

        numOfFiles = len(files)#random.randint(1, len(files))

        span.set_attribute("File count", numOfFiles)

        ## Construct the files json
        for i in range(numOfFiles):
            with tracer.start_as_current_span("Read file") as child:
                fileName = random.choice( files )
                files.remove(fileName)

                child.set_attribute("File", fileName)



                with open(os.path.join(FOLDER_NAME, fileName), "r") as file:
                    fileContent = file.read().encode(FORMAT)
                    encryptedContent = cipherSuite.encrypt(fileContent)
                    encryptedContent = gzip.compress(encryptedContent)
                    filesJSON[fileName] = base64.b64encode(encryptedContent).decode(FORMAT)
                    child.add_event(f"Added file {fileName} to JSON")
    
    ## Send a post request for server to transfer files
    requests.post(url, json={
        "name": random.choice(names),
        "files": filesJSON
    })

if __name__ == "__main__":
    with tracer.start_as_current_span("Main") as span:
        main()