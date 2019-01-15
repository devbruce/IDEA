FROM devbruce/idea:nginx-uwsgi-mecabko

# Set Env
ENV DJANGO_SETTINGS_MODULE config.settings.deploy

# Copy IDEA files to container
COPY . /srv/IDEA

# Make staticfiles
WORKDIR /srv/IDEA/app
RUN python3 manage.py collectstatic --noinput

# Nginx
RUN rm -rf /etc/nginx/sites-available/* /etc/nginx/sites-enabled/* && \
    cp -f /srv/IDEA/.config/IDEA.nginx /etc/nginx/sites-available && \
    ln -sf /etc/nginx/sites-available/IDEA.nginx /etc/nginx/sites-enabled/IDEA.nginx

# Supervisor
RUN cp /srv/IDEA/.config/supervisord.conf /etc/supervisor/conf.d

EXPOSE 80
CMD supervisord -n
