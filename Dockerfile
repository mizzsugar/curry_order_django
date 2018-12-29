FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir workspace
WORKDIR /workspace
ADD . /workspace/
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["python3", "curry_order/manage.py", "runserver", "0.0.0.0:8001"]