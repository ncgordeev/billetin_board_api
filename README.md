<h3 align="center">API доски объявлений</h3>

### О проекте:

Проект представляет собой backend-часть сайта объявлений, реализованного в виде API. Целью проекта
является предоставление функционала для создания, управления и взаимодействия с объявлениями через программный
интерфейс. Backend-часть обеспечивает основные возможности и безопасность взаимодействия пользователей с платформой.

#### Основные функции и возможности:

1. Авторизация и аутентификация пользователей:
    - Регистрация новых пользователей.
    - Вход в систему с использованием JWT (JSON Web Token) для обеспечения безопасной аутентификации.
    - Поддержка сессий и управление токенами для защиты данных пользователей.


2. Распределение ролей между пользователями:
    - Поддержка ролей "Пользователь" и "Админ".
    - Администраторы обладают расширенными правами, включая управление всеми объявлениями и пользователями.


3. Восстановление пароля:
    - Функционал для восстановления пароля через электронную почту.
    - Безопасный процесс смены пароля с подтверждением личности пользователя.


4. CRUD для объявлений:
    - Создание, чтение, обновление и удаление объявлений через API.
    - Пользователи могут управлять только своими объявлениями.
    - Администраторы могут редактировать или удалять любые объявления на платформе.


5. Отзывы под объявлениями:
    - Возможность оставлять отзывы под объявлениями.
    - API для управления комментариями, включая создание, редактирование и удаление отзывов.


6. Поиск объявлений:
    - Поиск объявлений по названию с использованием фильтров и сортировки.
    - API для быстрого и точного поиска объявлений.

### Технологии:

- [![Python](https://img.shields.io/badge/Python-092E20?style=flat&logo=Python)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=Django)](https://www.djangoproject.com/)
- [![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=flat)](https://www.django-rest-framework.org/)
- [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-092E20?style=flat&logo=PostgreSQL)](https://www.postgresql.org/)
- [![JWT](https://img.shields.io/badge/JWT-092E20?style=flat)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [![CORS](https://img.shields.io/badge/CORS-092E20?style=flat)](https://pypi.org/project/django-cors-headers/)
- [![Swagger](https://img.shields.io/badge/Swagger-092E20?style=flat)](https://swagger.io/)

### Настройка проекта:

Для работы с проектом произведите базовые настройки.

#### 1. Клонирование проекта

Клонируйте репозиторий используя следующую команду.

  ```sh
  git clone https://github.com/ncgordeev/billetin_board_api.git
  ```

#### 2. Редактирование .env.sample:

- В корне проекта должно быть 2 файла .env.local и .env.docker создайте их по шаблону .env.sample и отредактируйте
  параметры:
    ```text
    # Postgresql
    DB_NAME="db_name" - название вашей БД
    DB_USER="postgres" - имя пользователя БД
    DB_PASSWORD="secret" - пароль пользователя БД
    DB_HOST="host" - для .env.local 127.0.0.1 для .env.docker db
    DB_PORT=5432 - port
    
    # Django
    SECRET_KEY=secret_key - секретный ключ django проекта
    HOST=127.0.0.1:8000 - заменяем хост API
    
    # Mailing  
    EMAIL_HOST_USER='your_email@yandex.ru' - ваш email yandex
    EMAIL_HOST_PASSWORD='your_yandex_smtp_password' - ваш пароль smtp (подробнее о настройке ниже)
    
    # Superuser
    ADMIN_EMAIL='admin@test.com' - email регистрации администратора сайта
    ADMIN_PASSWORD='secret' - пароль регистрации администратора сайта
    ```
    - О настройке почты smtp:
      [Настройка почтового сервиса SMTP ](https://proghunter.ru/articles/setting-up-the-smtp-mail-service-for-yandex-in-django)

#### 3.1 Запуск проекта через Docker:

- установите Docker себе в систему, перейдя по [ссылке](https://docs.docker.com/engine/install/)
- для сборки проекта и запуска введите команду:

   ```text
   docker-compose up -d --build
   ```

#### 3.2 Запуск проекта локально:

- Примените миграции:
   ```text
   python manage.py migrate
   ```

- Для создания суперюзера используйте команду:
   ```text
   python manage.py csu
   ```

- Запустите проект:
   ```text
   python manage.py runserver
   ```

#### 4. Использование:

- перейдите по адресу: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

### Использование API:

- Авторизация и аутентификация
    - Регистрация:
      ```text
       POST /api/users/register/
       {
         "first_name": "User",
         "last_name": "Test",
         "phone": "1234567890",
         "email": "testuser@example.com",
         "password": "your_password"
       }
       ```
    - Вход:
       ```text
       POST /api/token/
       {
         "email": "testuser@example.com",
         "password": "your_password"
       }
       ```
    - Сброс пароля:
       ```text
       POST /api/users/reset_password/
       {
         "email": "testuser@example.com"
       }
       
       POST /api/users/reset_password_confirm/{uid}/{token}/
       {  
         "new_password": "P4$$W0RD"
       }
       ```

### Документация API:

- Документация доступна по адресу /swagger/ после запуска сервера.
