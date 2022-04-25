FROM python:3.7
ADD . /server
ADD sources.list /etc/apt/ 
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /server/requirements.txt
EXPOSE 7777
CMD ["sh","/server/start.sh" ]
