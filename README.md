# Optimetrik

Full-stack приложение для управления поверкой средств измерений.

## Запуск

```bash
docker-compose up -d  
```

## Сервисы:  
- Фронтенд: http://localhost  
- Бэкенд API: http://localhost:8000  
- Swagger: http://localhost:8000/docs  

## Технологии
Backend: FastAPI, PostgreSQL, SQLAlchemy  
Frontend: VueJS, Vite  
CI/CD: GitHub Actions  

## Миграции
```bash
docker exec backend_container alembic upgrade head
```