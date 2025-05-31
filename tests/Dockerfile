FROM python:3.10.17

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip --root-user-action ignore && \
    pip install --no-cache-dir -r /tmp/requirements.txt --root-user-action ignore

ADD ./app /app
WORKDIR /app
