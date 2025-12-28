# Auth System

Собственная система аутентификации и авторизации на Django REST Framework .

### Реализовано
- Регистрация / Логин / Логаут / Обновление профиля / Мягкое удаление
- JWT-токены + bcrypt для паролей
- Ролевая модель + правила доступа 
- Middleware для request.user
- Mock-ресурсы для демонстрации прав

### Технологии
Django · DRF · PostgreSQL · bcrypt · PyJWT

### Основные эндпоинты
- POST /register/
- POST /login/
- POST /logout/
- PUT /profile/update/
- DELETE /profile/delete/
- /admin/rules/ 
- /products/ 

