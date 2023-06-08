FROM python:3.8.6-64bit
WORKDIR /djangoProject/
COPY requirements.txt /djangoProject/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver"]
