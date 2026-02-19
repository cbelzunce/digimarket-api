from app.products.validators import validate_product_creation

def test_product_validator_ok():
    data = {
        "ean": "3760123456789",
        "brand": "Logitech",
        "name": "Clavier",
        "description": "AZERTY",
        "category": "accessoires",
        "price": 35.0,
        "stock": 14,
    }
    assert validate_product_creation(data) == {}

def test_product_validator_ean_missing():
    data = {
        "brand": "Logitech",
        "name": "Clavier",
        "description": "AZERTY",
        "category": "accessoires",
        "price": 35.0,
        "stock": 14,
    }
    erreurs = validate_product_creation(data)
    assert "ean" in erreurs

def test_product_validator_stock_negative():
    data = {
        "ean": "3760123456789",
        "brand": "Logitech",
        "name": "Clavier",
        "description": "AZERTY",
        "category": "accessoires",
        "price": 35.0,
        "stock": -1,
    }
    erreurs = validate_product_creation(data)
    assert "stock" in erreurs