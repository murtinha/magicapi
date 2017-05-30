FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENV PYTHONPATH $PYTHONPATH:./magic/api/app
CMD ["python", "magic/api/app.py"]