from python:slim-buster

#BEGIN: Tabpy server
RUN python -m pip install --upgrade pip
RUN pip install tabpy

COPY tabpy_server /usr/local/lib/python3.8/site-packages/tabpy/tabpy_server

EXPOSE 9004
#END: Tabpy server


ENTRYPOINT tabpy