FROM python:3.8-alpine

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD update-github-release-version.py .

ENTRYPOINT [ "python", "/app/update-github-release-version.py" ]
