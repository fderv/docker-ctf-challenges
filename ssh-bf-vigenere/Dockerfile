FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y openssh-server

RUN mkdir /var/run/sshd
RUN echo 'root:rootpass' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN mkdir -p /home/user/Documents/
RUN mkdir -p /home/user/Desktop/
RUN mkdir -p /home/user/Downloads/
RUN mkdir -p /home/user/Pictures/

COPY src/MIWPZPWFDUERTSHHRKR /home/user/Documents/MIWPZPWFDUERTSHHRKR
COPY src/NYQKHPX /home/user/Documents/NYQKHPX

RUN chmod 755 /home/user/Documents/NYQKHPX
RUN chmod 755 /home/user/Documents/MIWPZPWFDUERTSHHRKR

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
