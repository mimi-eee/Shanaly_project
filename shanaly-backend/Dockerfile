FROM python:3.11.7-alpine3.19

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./main.py .
COPY ./database.py .
COPY ./models.py .
COPY ./domain/ ./domain/
COPY ./core/ ./core/
COPY ./templates/ ./templates/
COPY ./frontend/ ./frontend/
COPY ./init_data/ ./init_data/

EXPOSE 8000

CMD sh -c 'python main.py'