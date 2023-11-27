## Цель работы:
Настроить репозиторий так, чтобы после пуша в него автоматически собирался докер образ и результат его сборки сохранялся на dockerhub

## Задачи:
* Настроить работу CI/CD в текущем репозитории путем добавления в репозиторий файл .github/workflows/docker-build.yaml, который будет собирать новый образ и заливать на dockerhub;
* Добавить секреты в настройках репозитория;
* Проверить 2 лбраза с разными сборками: показать что во 2 случае собрался обновленный проект (после пуша).

## Ход работы

 Создание репозитория с проектом

 В качестве рабочего проекта был загружен дефолтный проект Web-API на ASP.net Core, в котором реализован контроллер WeatherForecast, в котором реализован метод Get() (get-запрос к серверу). Сейчас он возвращает массив ранломных прогнозов (от 1 до 5):
 ```
   [ApiController]
   [Route("[controller]")]
   public class WeatherForecastController : ControllerBase
   {
       private static readonly string[] Summaries = new[]
       {
       "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
       };
  
       private readonly ILogger<WeatherForecastController> _logger;
  
       public WeatherForecastController(ILogger<WeatherForecastController> logger)
       {
           _logger = logger;
       }
  
       [HttpGet(Name = "GetWeatherForecast")]
       public IEnumerable<WeatherForecast> Get()
       {
           return Enumerable.Range(1, 5).Select(index => new WeatherForecast
           {
               Date = DateTime.Now.AddDays(index),
               TemperatureC = Random.Shared.Next(-20, 55),
               Summary = Summaries[Random.Shared.Next(Summaries.Length)]
           })
           .ToArray();
       }
   }
  ```


 Настроить работу CI/CD в текущем репозитории

 Для настройки используется GitHub Actions. Был реалихован файл файл .github/workflows/docker-build.yaml (в комментариях файла есть пояснения):
  ```
 name: Docker Build

 on:
   push:
     branches:
       - master ## ветка(и), для которой ниже создается job при push'e
 
 
 jobs:
   build:
     runs-on: ubuntu-latest ## используется ubuntu, так как там предустановлен docker
 
     steps:
       - name: Checkout Repository ## доступ к репозиторию
         uses: actions/checkout@v2
 
       - name: Docker loggin in ##вход в учетную запись dockerhub, куда будет зугружен собранный образ
         uses: docker/login-action@v3
         with:
           username: ${{ secrets.DOCKER_USERNAME }} ##логин от аккаунта 
           password: ${{ secrets.DOCKER_PASSWORD }} ##пароль от аккаунта
     
       - name: Docker loggin in ##вход в учетную запись dockerhub, куда будет зугружен собранный образ на dockerhub
         uses: docker/build-push-action@v5
         with:
           context: "./" ##Путь к папке с проектом для сборки
           push: true
           tags: philippkorkunov/test:latest

  ```

 Настроить секреты

 В этих строчках мы ссылаемся на секреты DOCKER_USERNAME и DOCKER_PASSWORD, которые мы создали в настроках репозитория

 ```
  username: ${{ secrets.DOCKER_USERNAME }} ##логин от аккаунта 
  password: ${{ secrets.DOCKER_PASSWORD }} ##пароль от аккаунта
  ```

![png1](./images/1.png)
Теперь запустим заново workflow. Получаем

![png2](./images/2.png)

Тест сборки


Получаем собранный образ
  ```
 docker pull philippkorkunov/test
  ```
Запускаем его на 8080 порту командой, который слушает 80 порт запущенного в докере API
 ```
 docker run -p 8080:80 philippkorkunov/test
 ```
Делаем запрос. http://localhost:8080/WeatherForecast. Как видно, нам пришел ответ (в виде json) с массивом прогнозов погоды, то есть проект собрался и развернулся в докере.
![png3](./images/3.png)

Теперь введем следующую команду

  ```
minikube service example-app-service
  ```
Она покажет нам внешний IP по которому доступен наш сервис

![png4](./images/4.png)

А также мгновенно откроет браузер с нашим сервисом

![png5](./images/5.png)

## Вывод
В данной лабораторной работе нами были созданы 2 YAML файла для создания локального kubernetes кластера, а также развернут сервис одной командой запуска. Во время выполнения лабораторной работы проблем не возникло.

## Выполнили
Студенты группы К34211: Наумов М., Захаров Е. и Коркунов. Ф
