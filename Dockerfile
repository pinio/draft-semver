FROM python:3.8-alpine

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD update-github-release-version.py .

ENTRYPOINT [ "python", "update-github-release-version.py" ]
