FROM python:3.10-alpine
WORKDIR /app
RUN apk add --no-cache iputils curl netcat-openbsd bash
RUN pip install flask
COPY app.py /app/app.py
EXPOSE 8080
CMD ["python", "app.py"]
