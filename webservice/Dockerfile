FROM       python:3.9

WORKDIR    /app

COPY       requirements.txt /app/

RUN        pip install -r requirements.txt

RUN        apt-get update && apt-get install -y vim

COPY       *.py /app/

COPY       entrypoint.sh /app/

RUN        chmod a+x *.py
RUN        chmod a+x *.sh 
  

CMD ["./entrypoint.sh"]