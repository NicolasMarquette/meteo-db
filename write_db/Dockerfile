FROM python:3.9
ADD requirements.txt /app/requirements.txt
WORKDIR /app/
RUN apt-get update && pip install -r requirements.txt
ADD write_db.py /app/write_db.py
CMD python -u write_db.py