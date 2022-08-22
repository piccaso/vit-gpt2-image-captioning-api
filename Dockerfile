FROM python:3.9-slim-bullseye

WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py .

RUN python3 app.py

ENV HF_DATASETS_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1

EXPOSE 9000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9000", "--no-debugger", "--no-reload"]