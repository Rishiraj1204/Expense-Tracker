# Expense Tracker with Analytics

A Python-focused Flask expense tracker built with SQLite, SQLAlchemy, Jinja2 templates, Chart.js, and pytest.

## Features
- User registration, login, logout, and profile management
- Expense and income CRUD
- Category and budget management
- Dashboard cards and charts
- Notifications, reports, and CSV export
- DSA utilities: hash map, max heap, min heap, top-k, merge sort, searching, queue
- Analytics: time series, trends, moving average, anomaly detection, recurring expense detection
- Seed data generator for quick testing

## Project Structure
- `expense_tracker/` — Flask application package
- `run.py` — application entry point
- `seed.py` — sample data generator
- `tests/` — pytest suite
- `docs/` — SRS, architecture, database, and algorithms documentation

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python run.py
   ```
4. Generate sample data:
   ```bash
   python seed.py
   ```

## Testing
Run the test suite from the project root:

```bash
pytest -q
```

## Notes
The app uses SQLite stored in the `instance/` folder and keeps authentication sessions in Flask.
