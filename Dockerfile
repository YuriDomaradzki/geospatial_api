FROM python:3.10
EXPOSE 5000

ADD . /app
WORKDIR /app

RUN	pip install --upgrade pip && \
	pip install --upgrade setuptools

RUN pip install -e .[all]

CMD ["flask", "run", "--host", "0.0.0.0"]