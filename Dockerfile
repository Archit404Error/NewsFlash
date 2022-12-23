FROM python:3.9

RUN mkdir /usr/app
WORKDIR /usr/app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python3", "main.py"]
