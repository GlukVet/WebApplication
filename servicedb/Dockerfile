FROM python:3

RUN ["mkdir", "/servicedb/"]
WORKDIR /servicedb/

COPY . /servicedb/

RUN apt-get update && apt-get install

RUN apt-get install -y \ 
libpq-dev \
python3-dev \
gcc \
&& apt-get clean

RUN pip install  -qr requirements.txt

CMD ["python", "servicedb.py"]
