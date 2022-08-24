FROM python:3-slim

WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .

RUN python3 app.py

ENV HF_DATASETS_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1
COPY static .
EXPOSE 9000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9000", "--no-debugger", "--no-reload"]
