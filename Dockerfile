FROM python:3.12-slim

WORKDIR /todoApp

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r /todoApp/requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT [ "bash", "-c", "bash /todoApp/entrypoint.sh" ]


# run the docker file 
#docker build -t todoapp .
#docker run -p 8000:8000 todoapp

