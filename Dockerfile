FROM python:3.10-slim

WORKDIR /app

ADD requirements.txt .

# RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ADD update-github-release-version.py .

ENTRYPOINT [ "python", "/app/update-github-release-version.py" ]
