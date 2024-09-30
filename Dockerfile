FROM python
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./app ./app
COPY ./tests ./tests
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
