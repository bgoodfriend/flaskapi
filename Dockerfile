FROM ubuntu:latest
MAINTAINER Bob Goodfriend bob.goodfriend@gmail.com
RUN apt-get update -y \
	&& apt-get install -y python3.7 python3-dev \
	&& ln -s /usr/bin/python3.7 /usr/bin/python

# python3-pip will only install to 3.6, so so the following is necessary
RUN apt-get install -y wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# Install python app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install app
COPY app.py .
COPY rates.py .
RUN mkdir static/
COPY static/swagger.json static/


EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
