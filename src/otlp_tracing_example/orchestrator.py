import os
import requests
from flask import Flask, jsonify
from tracing import setup_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# 1. Initialize Tracing for the Orchestrator
setup_tracing("orchestrator-service")

app = Flask(__name__)

# 2. Instrument Flask (extracts trace context from incoming requests)
FlaskInstrumentor().instrument_app(app)

# 3. Instrument Requests (injects trace context into outgoing HTTP calls)
RequestsInstrumentor().instrument()

@app.route('/orchestrate', methods=['GET'])
def orchestrate():
    results = {}
    urls = os.environ.get("ADAPTER_URLS", "http://localhost:5001,http://localhost:5002,http://localhost:5003").split(",")
    
    # The 'requests' library automatically injects the 'traceparent' header here
    try:
        for i, url in enumerate(urls, 1):
            results[f'adapter_{i}'] = requests.get(f"{url}/process").json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "data": results})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
