FROM tiangolo/uwsgi-nginx-flask:python3.6 
RUN rm -R /app
COPY . /app
RUN pip install -r /app/requirements.txt
