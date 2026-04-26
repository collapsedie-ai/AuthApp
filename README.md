Cобственная система аутентификации и авторизации.
Все ключевые элементы- токены, middleware, роли и разрешения реализованы без использования готовых инструментов Djnango.

Система включает:

1) Кастомную токен‑аутентификацию
2) Middleware, подставляющий request.user
3) Полностью функциональные FBV‑эндпоинты
4) Систему ролей и разрешений (RBAC)
5) API для управления ролями (только для администраторов)
6) Пример защищённого ресурса
7) Тестовые данные для демонстрации работы

config/        настройки Django
accounts/      аутентификация, токены, профиль
access/        роли, разрешения, RBAC


### 1. Взаимодействие с пользователем (Auth / Accounts API)
Система реализует полный набор функций для работы с пользователем без использования встроенной Django/DRF аутентификации.
Вся логика кастомная.

-Регистрация
Пользователь отправляет:["first_name", "last_name", "middle_name", "email", "password", "password2"]
Система: Cоздаёт пользователя, хэширует пароль, сохраняет в БД, возвращает успешный ответ
<font size="3">POST /api/accounts/register/</font>

-Login
Пользователь отправляет email + пароль.
Система:проверяет пароль, создаёт токен (AuthToken), возвращает токен клиенту
Каждый запрос содержит заголовок: Authorization: Token <token>
<font size="3">POST /api/accounts/login/</font>


-Профиль текущего пользователя
Выводит информацию об авторизованном пользователе.
<font size="3">GET /api/accounts/me/</font>

-Обновление профиля
Пользователь может изменить:имя,фамилию и отчество,но требуется токен.
<font size="3">POST /api/accounts/update/</font>

-Удаление пользователя (мягкое) 
Польностью деактивирует всего пользователя, все токены деактивируются, пользователь разлогинивается, войти снова невозможно.
<font size="3">DELETE /api/accounts/update/</font>

-Logout(Выход)
Деактивирует только текущий токен.
<font size="3">POST /api/accounts/logout/</font>

-Logout all(Выход со всех устройств)
Деактивирует все токены пользователя.
<font size="3">POST /api/accounts/logout_all/</font>

### 2. <font size="4">Система разграничения прав доступа(RBAC Admin API (управление ролями и правами))</font>


<font size="3">GET /api/access/roles/</font>    Список ролей
Admin: ✔ имеет доступ
User: ✖ запрещено (403)

<font size="3">GET /api/access/permissions/</font>  Список всех permissions
Admin: ✔ имеет доступ
User: ✖ запрещено (403)

<font size="3">GET /api/access/roles/<role_id>/permissions/</font>  Список permissions конкретной роли
Admin: ✔ имеет доступ
User: ✖ запрещено (403)

<font size="3">POST /api/access/roles/<role_id>/permissions/add/</font>     Добавить permission роли
Admin: ✔ может добавлять permissions ролям
User: ✖ запрещено (403)

<font size="3">POST /api/access/roles/<role_id>/permissions/remove/</font>  Удалить permission у роли
Admin: ✔ может удалять permissions у ролей
User: ✖ запрещено (403)


<font size="4">Tasks Mock API (проверка RBAC на бизнес‑логике)</font>

<font size="3">GET /api/access/tasks/</font>    Получить список задач (tasks:read)

<font size="3">POST /api/access/tasks/create/</font> Создать задачу (tasks:write)

<font size="3">DELETE /api/access/tasks/delete/</font> Удалить задачу (tasks:delete)

<font size="4">User Management API (только admin)</font>

<font size="3">POST /api/access/users/<user_id>/set_role/</font> Назначить роль пользователю
Admin: ✔ имеет доступ
User: ✖ запрещено (403)

<font size="3">POST /api/access/users/<user_id>/set_staff/</font> Изменить is_staff
Admin: ✔ имеет доступ
User: ✖ запрещено (403)

<font size="3">POST /api/access/users/<user_id>/set_superuser/</font> Изменить is_superuser
Admin: ✔ имеет доступ
User: ✖ запрещено (403)


<font size="4">Итого по правам доступа</font>
*User может:
-accounts:read
-accounts:logout
-tasks:read

*Admin может:
-accounts:read
-accounts:write
-accounts:delete
-accounts:logout
-tasks:read
-tasks:write
-tasks:delete
-управлять ролями пользователей (set_role)
-менять is_staff
-менять is_superuser
-просматривать список ролей
-просматривать список permissions
-просматривать permissions роли
-добавлять permissions роли
-удалять permissions у роли

В проекте используется ролевая модель RBAC.
Доступ определяется не самим пользователем, а его ролью.
Каждая роль содержит набор разрешений (permission), которые описывают действия (action) над ресурсами (resource).

При каждом запросе система определяет, к какому ресурсу относится операция и какое действие выполняется, после чего проверяет, есть ли у роли пользователя соответствующее разрешение.
Неаутентифицированный пользователь получает 401 Unauthorized, аутентифицированный без нужного разрешения — 403 Forbidden.
Если разрешение есть — запрос выполняется.

Дополнительно используется таблица RolePermission, которая связывает роли с разрешениями.
Именно она определяет, какие права фактически принадлежат каждой роли, поскольку сами роли не содержат прав напрямую — все разрешения назначаются через RolePermission.

Для регистрации json:
{
  "first_name": "Иван",
  "last_name": "Иванов",
  "middle_name": "Иванович",
  "email": "mail@example.com",
  "password": "12345",
  "password2": "12345"
}


НЕавторизованный пользователь (без токена)					
GET /api/access/roles/ 			401

GET /api/access/permissions/		401

GET /api/access/roles/1/permissions/	401

POST /api/access/roles/1/permissions/add/	401

POST /api/access/roles/1/permissions/remove/	401

GET /api/access/tasks/	401

POST /api/access/tasks/create/ 401

POST /api/access/tasks/delete/ 401 

POST /api/access/users/1/set_role/ 401 

POST /api/access/users/1/set_staff/ 401 

POST /api/access/users/1/set_superuser/ 401

Admin 

GET /api/access/roles/ список ролей			200

GET /api/access/permissions/	список permissions		200

GET /api/access/roles/1/permissions/ permissions роли			200

POST /api/access/roles/1/permissions/add/	Добавить permission роли	200

POST /api/access/roles/1/permissions/remove/	Удалить permission роли		200

GET /api/access/tasks/ Список задач						200

POST /api/access/tasks/create/ Создать задачу					200

POST /api/access/tasks/delete/	Удалить задачу					200
	
POST /api/access/users/3/set_role/	Назначить роль пользователю		200

POST /api/access/users/3/set_staff/ Изменить is_staff				200

POST /api/access/users/3/set_superuser/	Изменить is_superuser			200

User

GET /api/access/tasks/ список задач 200

POST /api/access/tasks/create/ Создать задачу 403

DELETE /api/access/tasks/delete/ удалить задачу 403
	
GET /api/access/roles/ список ролей 403

GET /api/access/permissions/ список permission 403

GET /api/access/roles/1/permissions/ Получить permissions роли 403

POST /api/access/roles/1/permissions/add/ Добавить permission роли 403

POST /api/access/roles/1/permissions/remove/ Удалить permission роли 403

POST /api/access/users/3/set_role/ Изменить роль пользователя 403

POST /api/access/users/3/set_staff/ Изменить is_staff 403

POST /api/access/users/3/set_superuser/	Изменить is_superuser 403











