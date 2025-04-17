Plant Management API - Documentation
Description
This application is a REST API built with FastAPI and SQLAlchemy, designed to manage a local SQLite database for the `Plant` entity (production plants). It provides full CRUD operations, automated testing, and a data visualization script.
Technologies Used
- FastAPI – modern web framework for building APIs
- SQLite – lightweight local database
- SQLAlchemy – ORM for relational database interaction
- Pydantic – data validation and serialization
- Pytest – automated testing
- GitHub Actions – continuous integration for testing on every push or pull request
- Pandas, Matplotlib, Seaborn – for data visualization
Project Structure
P-G Project/
 API.py                  # FastAPI app with CRUD endpoints
clase.py                # SQLAlchemy models + database connection
schemas.py              # Pydantic models for input/output validation
test_api.py             # Automated tests for the API
 plot_plants.py          # Script for generating capacity chart
project.db              # SQLite database
.github/workflows/
 tests.yml           # GitHub Actions workflow for automated testing
How to Run the Application
1. Install dependencies:
pip install fastapi sqlalchemy uvicorn pydantic pytest httpx pandas matplotlib seaborn

2. Start the FastAPI server:
uvicorn API:app --reload

3. Access the app in browser:
- API Root: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
API Endpoints – Plant
POST    /plants/         Create a new plant
GET     /plants/         Retrieve all plants
GET     /plants/{id}     Retrieve a plant by ID
PUT     /plants/{id}     Update an existing plant
DELETE  /plants/{id}     Delete an existing plant
Automated Testing
Tests are written in `test_api.py` using `pytest` and `fastapi.testclient`. They cover all CRUD operations for the `Plant` entity.

Run tests locally:
pytest test_api.py -v

Tests are also configured to run automatically via GitHub Actions on each push or pull request to the `main` branch.
GitHub Actions Workflow
The `.github/workflows/tests.yml` file defines the CI steps:

- Runs tests on each push and pull request
- Installs dependencies
- Executes `pytest`

You can include the test status badge in `README.md`:
![Test Status](https://github.com/USERNAME/REPO/actions/workflows/tests.yml/badge.svg)
Data Visualization
The `plot_plants.py` script queries the `plants` table and generates a bar chart showing the total capacity for each plant, using Pandas and Seaborn.

Run the script:
python plot_plants.py

The chart opens in a pop-up window and includes:
- Plant names on the X-axis
- Total capacity on the Y-axis
Future Improvements
- Add JWT authentication
- Implement CRUD for `Product`, `Material`, etc.
- Integrate a frontend (Streamlit or React)
- Add isolated testing using in-memory SQLite
