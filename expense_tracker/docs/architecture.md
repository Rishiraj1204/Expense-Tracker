# Architecture

The application follows a Flask MVC-style structure:

- `routes/` handles HTTP requests
- `services/` prepares dashboard and analytics data
- `models/` contains ORM entities
- `dsa/` contains custom data structures and algorithms
- `analytics/` contains time-series and trend analysis helpers
- `templates/` defines Jinja2 views
- `static/` stores CSS and JavaScript assets
