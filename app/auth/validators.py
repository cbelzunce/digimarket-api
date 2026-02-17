import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ'-]{2,50}$")

CARACTERES_SPECIAUX = set("!@#$%^&*()-_=+[]{};:,.?/")

def validate_password(password: str) -> str | None:
    if len(password) < 10:
        return "Le mot de passe doit contenir au moins 10 caractères."
    if not any(c.islower() for c in password):
        return "Le mot de passe doit contenir au moins une lettre minuscule."
    if not any(c.isupper() for c in password):
        return "Le mot de passe doit contenir au moins une lettre majuscule."
    if not any(c.isdigit() for c in password):
        return "Le mot de passe doit contenir au moins un chiffre."
    if not any(c in CARACTERES_SPECIAUX for c in password):
        return "Le mot de passe doit contenir au moins un caractère spécial."
    return None


def validate_register(data: dict) -> dict:
    errors = {}

    # Email
    email = (data.get("email") or "").strip().lower()
    if not email:
        errors["email"] = "L'adresse email est obligatoire."
    elif not EMAIL_RE.match(email):
        errors["email"] = "Le format de l'adresse email est invalide."

    # Prénom
    first_name = (data.get("first_name") or "").strip()
    if not first_name:
        errors["first_name"] = "Le prénom est obligatoire."
    elif not NAME_RE.match(first_name):
        errors["first_name"] = "Le prénom contient des caractères invalides."

    # Nom
    last_name = (data.get("last_name") or "").strip()
    if not last_name:
        errors["last_name"] = "Le nom est obligatoire."
    elif not NAME_RE.match(last_name):
        errors["last_name"] = "Le nom contient des caractères invalides."

    # Mot de passe
    password = data.get("password") or ""
    if not password:
        errors["password"] = "Le mot de passe est obligatoire."
    else:
        error_pwd = validate_password(password)
        if error_pwd:
            errors["password"] = error_pwd

    return errors


def validate_connexion(data: dict) -> dict:
    errors = {}

    email = (data.get("email") or "").strip().lower()

    mot_de_passe = data.get("password") or ""

    if not email:
        errors["email"] = "L'adresse email est obligatoire."
    elif not EMAIL_RE.match(email):
        errors["email"] = "Le format de l'adresse email est invalide."

    if not mot_de_passe:
        errors["password"] = "Le mot de passe est obligatoire."

    return errors
