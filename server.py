import base64
import os
import gzip
import time
import random
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource

### Environment variables
load_dotenv()

PORT = int( os.getenv("PORT") )
FORMAT = os.getenv("FORMAT")

### Encryption data
key = Fernet.generate_key()
cipherSuite = Fernet(key)

#### Set up Jaeger exporter and tracing
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)



tracer_provider = TracerProvider(resource=Resource.create({"service.name": "server"}))
trace.set_tracer_provider(tracer_provider)
tracer_provider.add_span_processor(SimpleSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer(__name__)

### Flask App
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

### Methods


def generate_bug(errorRate): # Creating deliberate delay on the client side
    if random.random() < errorRate:
        time.sleep(5) # introduce delay of Five seconds


def createFile(folder, name,  content):

    with tracer.start_as_current_span("Create file") as span:

        if random.random( ) <0.05: # Predicate P
            generate_bug(0.3) # Introduce deliberate delay
            
        with open(os.path.join(folder, name), "wb") as file:
            file.write(content)
            span.add_event("File creation", {"name": name})

### Endpoints
@app.route("/", methods=["GET"])
def serveKey():
    with tracer.start_as_current_span("Serve key") as span:
        span.set_attribute("Method", request.method)
        span.set_attribute("Client", request.remote_addr)
        span.add_event("Sent key", {"key": key.decode(FORMAT)})

    return jsonify({
        "key": key.decode(FORMAT)
    })

@app.route("/", methods=["POST"])
def takeFiles():
    with tracer.start_as_current_span("TakeFiles") as span:
        req = request.get_json()

        name = req.get("name", "DEFAULT")
        files = req.get("files", {})

        span.set_attribute("Method", request.method)
        span.set_attribute("Client", request.remote_addr)
        span.set_attribute("File Count", len(files.keys()))
        span.set_attribute("Client name", name)

        os.makedirs(name, exist_ok=True)
        for fileName, fileData in files.items():
            fileContent = base64.b64decode(fileData.encode(FORMAT))
            fileContent = gzip.decompress(fileContent)
            fileContent = cipherSuite.decrypt(fileContent)

            createFile(name, fileName, fileContent)

    return jsonify(message="success")


### Driver
if __name__ == "__main__":
    with tracer.start_as_current_span("main") as span:
        span.set_attribute("Type", "server")
        app.run(host="0.0.0.0", port=PORT)