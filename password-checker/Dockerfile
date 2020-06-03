FROM ubuntu:latest
LABEL maintainer="Gian Marco Mennecozzi"

ENV USER user
ENV PASS haaukins

RUN apt-get update && \
    apt-get install -y vsftpd supervisor gcc && \
    mkdir -p /var/run/vsftpd/empty

RUN mkdir -p /var/log/supervisor

COPY src/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD src/start.sh /usr/local/bin/start.sh
ADD src/vsftpd.conf /etc/vsftpd.conf

RUN chmod +x /usr/local/bin/start.sh
RUN mkdir /ftp
COPY /src/password_check /

VOLUME ["/ftp"]

EXPOSE 20 21
EXPOSE 12020-12025

ENTRYPOINT ["/usr/local/bin/start.sh"]

CMD ["/usr/bin/supervisord"]
