FROM python:3.6-alpine3.8

COPY alppb-runner.py alppb-runner.py
COPY requirements.txt requirements.txt
COPY alppb/* alppb/

RUN pip install -r requirements.txt

ENTRYPOINT [ "./alppb-runner.py" ]
