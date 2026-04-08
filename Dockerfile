FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pyyaml pydantic openai

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "baseline/baseline.py"] 
