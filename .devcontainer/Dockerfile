FROM python:3.11-slim

RUN apt-get update && apt-get install -y git

WORKDIR /apps

COPY ../requirements.txt ./
RUN pip install -r requirements.txt

COPY ../ ./

CMD ["uvicorn", "apps.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
