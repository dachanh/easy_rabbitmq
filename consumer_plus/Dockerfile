FROM python:3.8-slim
WORKDIR /var/www
COPY consumer_plus/task_queue.py .
COPY consumer_plus/tasks.py .
COPY consumer_plus/requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "tasks.py"]
