FROM python:3.9.10-alpine3.14
WORKDIR /srv
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . /srv
ENV FLASK_APP=app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
