FROM python:2.7
ADD . /code
ENV PYTHONPATH $PYTHONPATH:./
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "magic/api/app.py"]