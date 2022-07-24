### Общие сведения
Авторизация пользователей реализована с python-jose.  
Типизация данных запросов/ответов сервера.

Обновлённая коллекция [Postman](https://www.getpostman.com/collections/914bdb90302845426060)

Во время работы сервиса возникает единовременный не критический SAWarning из-за  
использования execute метода sqlmodel.

### Запуск:  
Зависимости:
- Docker
- Docker-compose

Для использования сервиса необходимо обозначить каталог монтирования  
базы данных Postgres:
```bash
  ylab_postgres_db:
    container_name: ylab_postgres_db
    image: postgres:latest
    volumes:
      - /mnt/small/share/cont/:/var/lib/postgresql/data/
```
1. Клонировать репозиторий и перейти в корневой каталог задания
```bash
git clone https://github.com/Wayfarer545/Y_LAB/ && cd Y_LAB/week_4
```
2. Инициализировать сборку приложения и запуск зависимостей
```bash
docker-compose up
```

В случае использования скрипта вне контейнера Docker на базе ОС Windows, необходимо  
внести изменения в файл alembic.ini секции script_location = src/migrations, 
заменив на src\migrations.
---


Основные изменения:
- добавлен роутер, касающийся авторизованных действий
- добавлены схемы типизации Request/Response 
- добавлен класс, отвечающий за логику эндпоинтов авторизованных действий
- обновлён класс RedisCache
- добавлены два соединения Redis (правильнее было бы через пул заводить)
- добавлена миграция Account, отвечающая за таблицу с данными пользователей
- Кэш в Redis содержит black list и перечень всех refresh tokens с доступом по uuid
- обновлён файл requirements.txt

Изменения в коллекции Postman:
- добавлен скрипт присвоения нового access token при  
обновлении информации о себе;
- запросы типа login передают только username и password  
- запросы типа logout передаются с access token

