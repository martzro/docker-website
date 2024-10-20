FROM python:3.11.4-alpine

WORKDIR usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "modify-poopsheet:app", "--port","8000"]