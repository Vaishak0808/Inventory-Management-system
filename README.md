# Inventory-Management-system
Inventory management system
This repository contains an Inventory Management System built using Django, Django REST Framework, and Redis for caching. It provides user authentication and item management functionalities.
# Inventory Management System

This repository is an Inventory Management System built using Django and Django REST Framework. The project includes JWT-based authentication, Redis caching for frequently accessed data, and various API endpoints for managing inventory items.

## Features

- *JWT Authentication:* Secured APIs using JWT tokens.
- *User Authentication:* Users can login via API.
- *CRUD Operations:* Allows Create, Read, Update, and Delete operations on items.
- *Redis Caching:* Implements caching for fetching item lists to improve performance.
- *Error Logging:* Logs all exceptions with detailed user information for easier debugging.

## Endpoints

### POST /inventory/items/
Create a new item.

#### Request Body:
```json
{
  "vchr_name": "Item Name",
  "txt_description": "Item description"
}

