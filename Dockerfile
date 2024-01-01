FROM python:3
# INSTALL PIP STUFF FROM REQUIREMENTS.TXT
COPY ./requirements.txt /app/requirements.txt
RUN mkdir /output
WORKDIR /app
RUN pip install -r requirements.txt
COPY ./src /app
ENTRYPOINT ["python", "scrape.py"]
