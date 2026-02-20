# 🛒 Digimarket API

Backend e-commerce développé en **Flask** avec authentification **JWT**,
gestion des rôles (RBAC) et traitement transactionnel des commandes.

Projet déployé en prod : https://cbelzunce.pythonanywhere.com/

------------------------------------------------------------------------

## 🧱 Stack technique

-   **Python 3.10+**
-   **Flask**
-   **Flask-SQLAlchemy (ORM)**
-   **SQLite**
-   **PyJWT**
-   **Pytest (tests unitaires & fonctionnels)**

------------------------------------------------------------------------

## 🚀 Installation & lancement

``` bash
git clone https://github.com/cbelzunce/digimarket-api.git
cd digimarket-api

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python run.py
```

API disponible sur :

http://localhost:5000


## 🔑 Création d’un utilisateur administrateur

Après installation des dépendances :

```bash
source .venv/bin/activate
export FLASK_APP=run.py
flask create-admin
```

------------------------------------------------------------------------

## 📦 Fonctionnalités

### 👤 Authentification

-   Inscription utilisateur
-   Connexion avec génération de token JWT
-   Gestion des rôles : `client` / `admin`

------------------------------------------------------------------------

### 📦 Catalogue Produits

-   Listing avec filtres (`q`, `category`)
-   CRUD complet (admin uniquement)
-   Contrainte d'unicité EAN
-   Validation métier (stock ≥ 0, prix ≥ 0)

------------------------------------------------------------------------

### 🧾 Commandes

-   Création avec vérification du stock
-   Calcul automatique du total
-   Gestion des statuts :
    -   `en_attente`
    -   `validee`
    -   `expediee`
    -   `annulee`
-   RBAC :
    -   Client → voit ses commandes
    -   Admin → voit toutes les commandes

------------------------------------------------------------------------

## 📚 Endpoints API

### 🔐 Authentification

- **POST** `/api/auth/register`
- **POST** `/api/auth/login`

### 📦 Produits

- **GET** `/api/produits`
- **GET** `/api/produits/{id}`
- **POST** `/api/produits` (Admin)
- **PUT** `/api/produits/{id}` (Admin)
- **DELETE** `/api/produits/{id}` (Admin)

### 🧾 Commandes

- **GET** `/api/commandes`
- **GET** `/api/commandes/{id}`
- **GET** `/api/commandes/{id}/lignes`
- **POST** `/api/commandes`
- **PATCH** `/api/commandes/{id}` (Admin)

------------------------------------------------------------------------

## 🧪 Tests

Tests unitaires et fonctionnels via Pytest.

``` bash
python -m pytest -vv --cov=app --cov-report=term-missing
```
