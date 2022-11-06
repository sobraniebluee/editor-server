FROM python
FROM mysql

WORKDIR /app

COPY . .

#RUN pip3 install pipenv
#RUN pipenv install

CMD [ "python", "main.py"]