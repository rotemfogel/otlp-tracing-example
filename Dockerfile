FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-emit-project -o requirements.txt \
 && uv pip install --system --target /deps -r requirements.txt

FROM gcr.io/distroless/python3-debian13
COPY --from=build /deps /deps
COPY src/otlp_tracing_example /app
WORKDIR /app
ENV PYTHONPATH=/deps
ENTRYPOINT ["/usr/bin/python3"]
