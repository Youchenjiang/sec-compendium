# ===========================================================================
# ⚠️  EDUCATIONAL CTF CHALLENGE CONTAINER - INTENTIONALLY VULNERABLE ⚠️
# This Dockerfile builds a deliberately vulnerable web application for use
# in a controlled, isolated Docker lab environment ONLY.
# DO NOT deploy in any production or internet-accessible environment.
# ===========================================================================
# NOSONAR - python:alpine base running as root is required for CTF container-escape exercises
FROM python:3.10-alpine  # NOSONAR
WORKDIR /app
RUN apk add --no-cache iputils curl netcat-openbsd bash && \
    pip install flask  # NOSONAR - intentional unpinned dep for CTF lab; no prod use
COPY app.py /app/app.py
EXPOSE 8080
CMD ["python", "app.py"]
