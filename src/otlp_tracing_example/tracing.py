from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

def setup_tracing(service_name):
    # Set the service name for the traces
    resource = Resource(attributes={"service.name": service_name})
    provider = TracerProvider(resource=resource)
    
    # Configure the OTLP Exporter (Defaults to http://localhost:4318/v1/traces)
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    
    # Set the global trace provider
    trace.set_tracer_provider(provider)
