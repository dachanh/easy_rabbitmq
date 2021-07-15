FROM python:3.8-slim
WORKDIR /var/www
COPY consumer_div/task_queue.py .
COPY consumer_div/tasks.py .
COPY consumer_div/requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "tasks.py"]