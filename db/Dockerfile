FROM library/postgres

COPY init.sql /docker-entrypoint-initdb.d/

RUN chmod 777 /docker-entrypoint-initdb.d/init.sql
