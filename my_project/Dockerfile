FROM python:3.8-slim
WORKDIR /var/www
COPY my_project/server.py .
COPY my_project/requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]