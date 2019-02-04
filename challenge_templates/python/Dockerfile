FROM python:3

RUN apt-get update --fix-missing && apt-get install -y xinetd
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /usr/src/app
COPY ./src .
RUN pip install --no-cache-dir -r requirements.txt

# Configuration files/scripts
ADD config/ctf.xinetd /etc/xinetd.d/ctf
ADD config/run_xinetd.sh /etc/run_xinetd.sh
ADD config/run_challenge.sh /run_challenge.sh


RUN chmod +x /run_challenge.sh
RUN chmod +x /etc/run_xinetd.sh

RUN service xinetd restart

