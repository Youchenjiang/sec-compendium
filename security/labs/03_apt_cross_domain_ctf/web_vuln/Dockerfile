# ===========================================================================
# ⚠️  EDUCATIONAL CTF CHALLENGE CONTAINER - INTENTIONALLY VULNERABLE ⚠️
# This Dockerfile builds a deliberately vulnerable web application for use
# in a controlled, isolated Docker lab environment ONLY.
# DO NOT deploy in any production or internet-accessible environment.
# ===========================================================================
FROM python:3.10-alpine
# NOSONAR - Using alpine python base; runs as root intentionally for CTF pivoting exercises
# Students exploit container-escape scenarios requiring root inside the container
WORKDIR /app
RUN apk add --no-cache iputils curl netcat-openbsd bash && \
    pip install --only-binary :all: flask || pip install flask  # NOSONAR
COPY app.py /app/app.py
EXPOSE 8080
CMD ["python", "app.py"]
