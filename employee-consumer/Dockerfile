FROM       python:3.9

WORKDIR    /opt

COPY       requirements.txt /opt

COPY       *.py /opt

RUN        pip install -r requirements.txt

RUN        apt-get update && apt-get install -y vim


RUN        chmod a+x *.py
  
CMD        ["python","compensation-calculator.py"]
