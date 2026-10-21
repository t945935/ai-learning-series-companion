FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml requirements.txt ./
COPY app ./app
COPY fixtures ./fixtures

ENV PYTHONPATH=/app
ENV HOST=0.0.0.0
ENV PORT=8000
ENV FIXTURE_DIR=/app/fixtures/documents
ENV DATA_PATH=/data/store.json

RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)"
CMD ["python", "-m", "app.main"]
