FROM python:3.9-slim
WORKDIR /usr/src
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN pip install -r requirements.txt --src /usr/src
EXPOSE 8000
ENTRYPOINT ["python", "-m", "app.main"]