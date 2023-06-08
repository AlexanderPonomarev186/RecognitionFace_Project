FROM python:3.10.7
WORKDIR /djangoProject/
COPY requirements.txt /djangoProject/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .