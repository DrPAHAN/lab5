# 📘 Лабораторная работа №5: Сетевое взаимодействие между Docker-контейнерами

---

## 🎯 Цель работы
Развернуть два независимых Docker-контейнера (приложение и СУБД) вручную, настроить пользовательскую сеть, обеспечить их взаимодействие через встроенный Docker DNS, вывести приложение на порт, отличный от `80`.

---

## 🛠 Стек технологий
| Компонент       | Версия/Образ          |
|-----------------|-----------------------|
| Приложение      | Python 3.11 + Flask   |
| База данных     | PostgreSQL 15-alpine  |
| Сеть            | Docker `bridge`       |
| Управление      | Docker CLI (без Compose) |

---

## Предварительные требования
- Установленный и запущенный `docker`
- Доступ к терминалу с правами пользователя в группе `docker`
- Базовые навыки работы с CLI

---

## Ход выполнения

### 1. Создание пользовательской сети
Пользовательская сеть обеспечивает встроенное DNS-разрешение имён контейнеров.
```
docker network create --driver bridge app-lab5-net
```

### 2. Запуск контейнера с базой данных
```
docker run -d \
  --name lab5-db \
  --network app-lab5-net \
  -e POSTGRES_USER=labuser \
  -e POSTGRES_PASSWORD=labpass123 \
  -e POSTGRES_DB=labdb \
  -v lab5-db-data:/var/lib/postgresql/data \
  postgres:15-alpine
```

### 3. Сборка и запуск приложения
```
# Сборка образа
docker build -t lab5-app:latest .

# Запуск контейнера
docker run -d \
  --name lab5-app \
  --network app-lab5-net \
  -p 5000:5000 \
  -e DB_NAME=labdb \
  -e DB_USER=labuser \
  -e DB_PASS=labpass123 \
  lab5-app:latest
```

### Проверка работоспособности

| Команда         | Ожидаемый результат   |
|-----------------|-----------------------|
| ```docker ps --filter "name=lab5" ```    | Оба контейнера в статусе Up   |
| ``` docker exec lab5-app python -c "import socket; print(socket.gethostbyname('lab5-db'))" ```| Внутренний IP БД (например, 172.18.0.2)  |
| ``` curl http://localhost:5000 ```   | {"status":"ok","db_version":"PostgreSQL 15.x..."}       |
| ``` docker logs lab5-app ```    | Логи Flask: ``` Running on http://0.0.0.0:5000 ``` |
| ``` docker network inspect app-lab5-net ``` | Оба контейнера в секции Containers |
