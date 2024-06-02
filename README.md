# Faciliter Blog APIs Assessment

A basic FastAPI backend for a blogging platform that manages posts and authors. It supports basic CRUD (Create, Read, Update, Delete) operations for both entities.

## Features

- Endpoints for managing authors and posts
- SQLAlchemy for ORM (Object Relational Mapping)
- Pydantic models for request validation and serialization
- Basic error handling
- Automatic interactive API documentation (Swagger UI)
- PostgreSQL database integration

## Project Structure

faciliter_blog/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── crud/
│ │ ├── init.py
│ │ ├── author.py
│ │ └── post.py
│ ├── models/
│ │ ├── init.py
│ │ ├── author.py
│ │ └── post.py
│ ├── schemas/
│ │ ├── init.py
│ │ ├── author.py
│ │ └── post.py
│ ├── db/
│ │ ├── init.py
│ │ └── database.py
│ └── api/
│ ├── init.py
│ ├── author.py
│ └── post.py
└── README.md
└── run_tests.sh
└── requirements.txt


## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/fastapi_blog.git
   cd fastapi_blog


2.  **Create Virtual Environment and Install Requirements**
    ```bash
        python3 -m venv env
        source env/bin/activate  # On Windows use `env\Scripts\activate`
        pip install -r requirements.txt
    ```

3. **Create New Postgres Database Table and Update your .env file**
    ```sql
        CREATE DATABASE dbname;
    ```

    ```env
        DATABASE_URL=postgresql://user:password@localhost/dbname
    ```

4. **Run Migrations**
    ```bash
        python3 -m app.db.database
    ```

5. **Start Server**

    ```bash
        uvicorn app.main:app --reload
    ```

6. **Access Documentation**

    ```
        http://127.0.0.1:8000/docs
    ```

7. **Run and Excute Tests Script**

    ```
        chmod +x run_tests.sh
        ./run_tests.sh
    ```


## Access the API documentation:

Open your browser and navigate to http://127.0.0.1:8000/docs to access the Swagger UI interactive API documentation.

## Internal API Endpoints Documentation

    ```
        ./api_doc.txt file
    ```