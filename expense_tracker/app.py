from flask import Flask, redirect, render_template, session, url_for

from expense_tracker.config import Config
from expense_tracker.models import db


def register_blueprints(app: Flask) -> None:
    from expense_tracker.routes.auth import auth_bp
    from expense_tracker.routes.dashboard import dashboard_bp
    from expense_tracker.routes.expenses import expenses_bp
    from expense_tracker.routes.income import income_bp
    from expense_tracker.routes.categories import categories_bp
    from expense_tracker.routes.budgets import budgets_bp
    from expense_tracker.routes.analytics import analytics_bp
    from expense_tracker.routes.notifications import notifications_bp
    from expense_tracker.routes.reports import reports_bp
    from expense_tracker.routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(budgets_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(profile_bp)


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_blueprints(app)

    @app.route("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("dashboard.dashboard"))
        return render_template("index.html")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
