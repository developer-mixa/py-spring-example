FROM python:3.10.13

WORKDIR /

COPY . .

# COPY app.py .
# COPY requirements.txt .

RUN pip install -r requirements.txt

#CMD ["python3", "-m", "gunicorn", "--bind", "0.0.0.0:8080", "--workers=4", "app:run"]
CMD ["python3", "-m" ,"main"]
#CMD ["waitress-serve", "--listen=*:8080", "app:run"]