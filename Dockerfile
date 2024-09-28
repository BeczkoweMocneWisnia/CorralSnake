FROM python:3.10

WORKDIR /DigitalLurker
COPY . .

RUN apt-get update
RUN #apt-get -y upgrade
RUN apt-get -y install python3 python3-pip python3-gdal gdal-bin gettext
RUN pip install -r requirements.txt
RUN python3 /CorralSnake/manage.py migrate
RUN python3 /CorralSnake/manage.py compilemessages

EXPOSE 8000

RUN chmod +x /CorralSnake/entrypoint.sh
ENTRYPOINT ["/DigitalLurker/entrypoint.sh"]