FROM python:3.6

WORKDIR /app

COPY requirements.txt ./
COPY bower.json ./
COPY .bowerrc ./

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y build-essential
RUN npm install -g bower
RUN bower install --allow-root
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod 700 run.sh

EXPOSE 8001

CMD [ "./run.sh"]