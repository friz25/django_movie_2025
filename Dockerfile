FROM python
#COPY requirements.txt .
#COPY tests/test_api.py .
COPY . /app/
#COPY pages .
#COPY tests .
#RUN mkdir allure-results
RUN cd app && pip install -r requirements.txt

# установка Chrome (нужен для Selenium тестов)
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN apt-get update && apt-get install -y google-chrome-stable
#CMD ["pytest", "tests/test_api.py", "--alluredir=allure-results"]

# если без DockerCompose:
#EXPOSE 8000
#ENTRYPOINT ["python", "manage.py"]
#CMD ["runserver", "0.0.0.0:8000"]

# чтоб Создать Образ / В терминале venv :
#docker build -t dj_docker .

# Запуск :
#docker run --rm -it -p 8000:8000 dj_docker
#Проверьте http://localhost:8000/