FROM python:3.10.7
WORKDIR /djangoProject/
COPY requirements.txt /djangoProject/
RUN pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.8.0-py3-none-any.whl
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver"]