FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get install -y sudo && \
    apt-get install -y vim

RUN mkdir /var/run/sshd
RUN echo 'root:V58qFUIR0X7etOST' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN userdel -r nobody
RUN useradd -m user && echo 'user:haaukins' | chpasswd

RUN usermod -s /bin/bash user

RUN mkdir -p /home/user/Documents/
RUN mkdir -p /home/user/Desktop/
RUN mkdir -p /home/user/Downloads/
RUN mkdir -p /home/user/Pictures/

COPY src/script /home/user/Desktop/script
RUN chown root:root /home/user/Desktop/script
RUN chmod 500 /home/user/Desktop/script

RUN echo "user ALL=(ALL) NOPASSWD:/usr/bin/vi" >> /etc/sudoers

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
