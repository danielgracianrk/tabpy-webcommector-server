from python:slim-buster

#BEGIN: Tabpy server
RUN python -m pip install --upgrade pip
RUN pip install tabpy
#END: Tabpy server

#BEGIN: node server
RUN apt-get upgrade
RUN apt-get update
RUN apt-get -y install npm
RUN npm install node

EXPOSE 3000

ENV USER=nodejs
ENV HOME=/home/$USER
ENV PATHTOAPP=/Users/n645776/curro/webdataconnector/

ADD $PATHTOAPP $HOME/app
#END: node server



ENTRYPOINT tabpy