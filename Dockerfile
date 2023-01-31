FROM python:3.9

RUN mkdir /usr/app
WORKDIR /usr/app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
EXPOSE 5000
CMD ["python3", "main.py"]
