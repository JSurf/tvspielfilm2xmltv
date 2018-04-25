FROM python:2
WORKDIR /usr/src/app
COPY . .
RUN make install

#CMD [ "python", "./your-daemon-or-script.py" ]