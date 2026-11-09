import sys
from flask import Flask, jsonify
from tracing import setup_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Run this script with a port number, e.g.: python adapter.py 5001

if len(sys.argv) < 2:
    print("Usage: python adapter.py <port>")
    sys.exit(1)

port = int(sys.argv[1])
service_name = f"adapter-service-{port}"

# 1. Initialize Tracing for this specific adapter
setup_tracing(service_name)

app = Flask(__name__)

# 2. Instrument Flask (automatically extracts W3C headers from the Orchestrator)
FlaskInstrumentor().instrument_app(app)

@app.route('/process', methods=['GET'])
def process():
    # You can do custom work here; it will all fall under the Orchestrator's trace ID
    return jsonify({
        "service": service_name,
        "message": "Data processed successfully"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
