FROM python:3

RUN mkdir /backend/
WORKDIR /backend/
COPY . /backend/

EXPOSE 80

RUN apt-get update && apt-get install
RUN pip install -qr requirements.txt

CMD ["python", "backend.py"]
