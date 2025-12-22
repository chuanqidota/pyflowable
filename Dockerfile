FROM docker.1ms.run/library/python:3.13-alpine3.23
RUN mkdir -p /opt/
WORKDIR /opt/
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]