import click
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.auth.models import User

def register_cli(app):
    @app.cli.command("create-admin")
    @click.option("--email", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(email, password):
        email = email.strip().lower()
        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if user:
            user.role = "admin"
            user.password_hash = generate_password_hash(password)
        else:
            user = User(
                email=email,
                password_hash=generate_password_hash(password),
                first_name="Admin",
                last_name="Digimarket",
                role="admin",
            )
            db.session.add(user)

        db.session.commit()
        click.echo("Admin créé / mis à jour.")
