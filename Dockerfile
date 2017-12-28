FROM tiangolo/uwsgi-nginx-flask:python3.6 
RUN rm -R /app
COPY . /app
COPY entrypoint.sh /
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN pip install -r /app/requirements.txt
ENV FLASK_APP /app/main.py
ENV FLASK_DEBUG 1
COPY proxy_params /etc/nginx/
