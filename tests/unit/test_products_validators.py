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
    errors = validate_product_creation(data)
    assert "ean" in errors

def test_product_validator_ean_not_13():
    data = {
        "ean": "376012345678937601234567893760123456789",
        "brand": "Logitech",
        "name": "Clavier",
        "description": "AZERTY",
        "category": "accessoires",
        "price": 35.0,
        "stock": 14,
    }
    errors = validate_product_creation(data)
    assert "ean" in errors
    assert "Le code EAN doit contenir exactement 13 chiffres." in errors["ean"]

def test_product_validator_name_missing():
    data = {
        "ean": "3760123456789",
        "brand": "Logitech",
        "name": "",
        "description": "AZERTY",
        "category": "accessoires",
        "price": 35.0,
        "stock": 14,
    }
    errors = validate_product_creation(data)
    assert "name" in errors

def test_product_validator_brand_missing():
    data = {
        "ean": "3760123456789",
        "brand": "",
        "name": "Clavier",
        "description": "AZERTY",
        "category": "accessoires",
        "price": 35.0,
        "stock": 14,
    }
    errors = validate_product_creation(data)
    assert "brand" in errors

def test_product_validator_description_missing():
    data = {
        "ean": "3760123456789",
        "brand": "Logitech",
        "name": "Clavier",
        "description": "",
        "category": "accessoires",
        "price": 35.0,
        "stock": 14,
    }
    errors = validate_product_creation(data)
    assert "description" in errors

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
    errors = validate_product_creation(data)
    assert "stock" in errors
    assert "Le stock doit être un entier positif." in errors["stock"]

def test_product_validator_price_negative():
    data = {
        "ean": "3760123456789",
        "brand": "Logitech",
        "name": "Clavier",
        "description": "AZERTY",
        "category": "accessoires",
        "price": -35,
        "stock": 1,
    }
    errors = validate_product_creation(data)
    assert "price" in errors
    assert "Le prix doit être positif." in errors["price"]

def test_product_validator_price_NaN():
    data = {
        "ean": "3760123456789",
        "brand": "Logitech",
        "name": "Clavier",
        "description": "AZERTY",
        "category": "accessoires",
        "price": "toto",
        "stock": 1,
    }
    errors = validate_product_creation(data)
    assert "price" in errors
    assert "Le prix doit être un nombre." in errors["price"]