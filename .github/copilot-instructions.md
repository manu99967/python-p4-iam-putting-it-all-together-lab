# Copilot Instructions for AI Agents

## Project Overview
This project is a full-stack web application for managing users and recipes, focusing on authentication and authorization. It consists of a Flask backend (`server/`) and a React frontend (`client/`). The backend uses SQLAlchemy ORM, Flask-RESTful, and session-based authentication. The frontend is a standard Create React App setup.

## Architecture & Data Flow
- **Backend (`server/`)**: Exposes RESTful endpoints for user signup, login, session check, logout, and recipe CRUD. Models are in `models.py`. API resources are in `app.py`.
- **Frontend (`client/`)**: React app communicates with the backend via fetch/AJAX. Auth state is managed via session cookies.
- **Database**: Managed with SQLAlchemy and Alembic migrations. Models: `User` (with secure password hashing) and `Recipe` (belongs to User).

## Key Workflows
- **Setup**:
  - Backend: `pipenv install && pipenv shell`, then `cd server`
  - Frontend: `npm install --prefix client`
- **Run**:
  - Backend: `python app.py` (from `server/`)
  - Frontend: `npm start --prefix client`
- **Migrations**:
  - `flask db init` (once), `flask db revision --autogenerate`, `flask db upgrade`
- **Seeding**: `python seed.py` (from `server/`)
- **Testing**:
  - All: `pytest`
  - Models: `pytest testing/models_testing/`
  - App endpoints: `pytest testing/app_testing/app_test.py`

## Project-Specific Patterns
- **User Auth**: Session-based, not JWT. User ID is stored in Flask session.
- **Password Hashing**: Use bcrypt, never expose or return password hashes.
- **Error Handling**: API errors are returned as JSON with `errors` or `error` keys, and appropriate HTTP status codes (401, 422, etc).
- **Model Validations**: Enforced both at the DB and in model logic (e.g., username uniqueness, recipe instructions length).
- **Frontend Auth**: React checks `/check_session` on load to auto-login users.

## Integration Points
- **API Endpoints**: Defined in `server/app.py` using Flask-RESTful resources.
- **Models**: Defined in `server/models.py`. Relationships: User has many Recipes; Recipe belongs to User.
- **Testing**: Custom tests in `testing/` directory. Use pytest, not unittest.

## Conventions
- **Error messages**: Always return as JSON arrays for validation errors (e.g., `{ "errors": ["message"] }`).
- **Session**: Use Flask's `session` object for login state.
- **Frontend**: Use fetch/AJAX for all API calls. Do not use GraphQL or websockets.

## Examples
- To add a new protected resource, require `user_id` in session and return 401 if missing.
- To add a new model, update `models.py`, create a migration, and update seed/test files.

---
For more details, see `README.md` (root and client/) and `server/app.py` for API structure.
