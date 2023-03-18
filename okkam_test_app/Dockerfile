FROM python:latest
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD ./*.py ./
EXPOSE 8080
ENTRYPOINT ["python", "main.py"]
