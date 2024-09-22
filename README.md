# Django Todo Website

A simple Django-based web application for managing and tracking tasks.

## Features

- User authentication (register, login, logout)
- Create, read, update, and delete (CRUD) tasks

## Prerequisites

- Python 3.7+
- PostgreSQL (or any other supported database)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/trolchiha/DjangoTodoWebsite.git
    cd DjangoTodoWebsite
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser (admin account):

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Configuration

Update the environment variables in the `.env` file as needed, especially for database settings.

## Usage

- Access the application at `http://localhost:8000`
- Admin interface is available at `http://localhost:8000/admin` (use the superuser credentials created during setup)

## API Endpoints

- **GET /tasks/**: List all tasks
- **POST /tasks/**: Create a new task
- **GET /tasks/{task_id}/**: Retrieve a task by ID
- **PUT /tasks/{task_id}/**: Update a task by ID
- **DELETE /tasks/{task_id}/**: Delete a task by ID

## Testing

Run the tests using:

```bash
pytest
