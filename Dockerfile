FROM python:3.9

RUN mkdir /usr/app
WORKDIR /usr/app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
EXPOSE 8000
CMD ["python3", "-m", "gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "main:app", "--timeout", "120"]
