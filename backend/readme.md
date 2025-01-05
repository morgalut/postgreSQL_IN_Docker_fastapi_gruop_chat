
# Chat Application Backend

This project is a FastAPI-based backend with PostgreSQL as the database. Follow the steps below to set up, run, and interact with the application.

---
uvicorn main:app --host 0.0.0.0 --port 8000

## Setup and Running the Project

### 1. Build and Start Docker Containers
To build and start the containers, run:
```bash
docker-compose up -d
```

---

## Setting Up the Database

### 2. Access PostgreSQL
Connect to the PostgreSQL database:
```bash
docker-compose exec postgres1 psql -U postgres
```

### 3. Create a New Database
Inside the `psql` prompt, create the database:
```sql
CREATE DATABASE my_database;
```

### 4. Run Database Initialization Script
Run the provided SQL script to create necessary tables:
```bash
docker-compose exec postgres1 psql -U postgres -d my_database -f /docker-entrypoint-initdb.d/message_user.sql
```

---

## Testing the Backend API

### 5. Register a New User
Use `curl` to register a new user:
```bash
curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d "{\"username\":\"new_user\", \"email\":\"new_user@example.com\"}"
```

### 6. Retrieve All Users
Retrieve the list of registered users:
```bash
curl -X GET http://localhost:8000/users/
```

### 7. Send a Message
Send a message from a user:
```bash
curl -X POST http://localhost:8000/messages/ -H "Content-Type: application/json" -d "{\"user_id\":1, \"content\":\"Hello, World!\"}"
```

### 8. Retrieve All Messages
Retrieve all messages:
```bash
curl -X GET http://localhost:8000/messages/
```

---

## Notes

- Ensure that all necessary containers (`backend`, `postgres1`, and `react-app`) are running before interacting with the API.
- For more advanced configurations, refer to the `docker-compose.yml` file and adjust ports or other settings as needed.

---

Happy Coding! 🚀
