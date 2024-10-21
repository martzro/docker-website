FROM python:3.11.4-alpine

# Install PostgreSQL client and development packages
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "modify-poopsheet:app", "--host", "0.0.0.0", "--port", "8000"]
