FROM python:alpine
WORKDIR /order-service
COPY . /order-service
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "run.py" ]