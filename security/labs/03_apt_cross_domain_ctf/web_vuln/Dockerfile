# ===========================================================================
# ⚠️  EDUCATIONAL CTF CHALLENGE CONTAINER - INTENTIONALLY VULNERABLE ⚠️
# This Dockerfile builds a deliberately vulnerable web application for use
# in a controlled, isolated Docker lab environment ONLY.
# DO NOT deploy in any production or internet-accessible environment.
# ===========================================================================
FROM python:3.10-alpine
WORKDIR /app
RUN apk add --no-cache bash curl iputils netcat-openbsd && \
    pip install --no-cache-dir --only-binary :all: flask==3.0.3 || pip install --no-cache-dir flask==3.0.3
COPY app.py /app/app.py
EXPOSE 8080
CMD ["python", "app.py"]
