
# Inventory Management System

This repository is an Inventory Management System built using Django and Django REST Framework. The project includes JWT-based authentication, Redis caching for frequently accessed data, and various API endpoints for managing inventory items.

## Features

- *JWT Authentication:* Secured APIs using JWT tokens.
- *User Authentication:* Users can login via API.
- *CRUD Operations:* Allows Create, Read, Update, and Delete operations on items.
- *Redis Caching:* Implements caching for fetching item lists to improve performance.
- *Error Logging:* Logs all exceptions with detailed user information for easier debugging.
## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Vaishak0808/Inventory-Management-system.git
   cd inventory_management_system
   ```
   
3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   
4. Configure your database settings and Redis settings in settings.py.

   The application connects to Redis using the host and port specified in the Django settings.py file:
   ```
   CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Default Redis port and DB number
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
   }

   ```
   
5. Setup database
   
   First, create the PostgreSQL database manually using the command line.

   Open your terminal and access the PostgreSQL prompt
   ```
   sudo -u postgres psql
   
   In the PostgreSQL prompt, create the database:
   
   CREATE DATABASE inventory_management_system;
   
   Create a user and grant them access to the database:

   CREATE USER your_user_name WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE inventory_management_system TO your_user_name;

   ```
      
7. Run the migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
8. Create a superuser to access the Django admin:
   ```
   python manage.py createsuperuser
   ```
   
9. Start the development server:
   ```
   python manage.py runserver
   ```
   
10. Start Redis
   ```
    redis-server
   ```


## Endpoints

### POST /inventory/items/
Create a new item.

#### Request Body:
```json
{
  "vchr_name": "Item Name",
  "txt_description": "Item description"
}
```
Logging
The project uses a custom logger for error tracking. All errors are logged with user details and the specific line number where the error occurred.

Caching
Redis caching is implemented for item listing to reduce database load. Cached data expires every 5 minutes, and the cache is invalidated when an item is created, updated, or deleted.

