FROM python:3.10.2

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

ADD ./app /app
WORKDIR /app
