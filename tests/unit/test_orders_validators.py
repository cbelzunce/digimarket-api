from app.orders.validators import validate_order_creation

def test_order_validator_ok():
    data = {
        "shipping_address": "12 rue de la République, 75000 Paris",
        "items": [
            { "product_id": 1, "quantity": 1 },
            { "product_id": 2, "quantity": 3 }
        ]
    }
    assert validate_order_creation(data) == {}

def test_order_validator_shipping_address_missing():
    data = {
        "shipping_address": "",
        "items": [
            { "product_id": 1, "quantity": 1 },
            { "product_id": 2, "quantity": 3 }
        ]
    }

    errors = validate_order_creation(data)
    assert "shipping_address" in errors

def test_order_validator_shipping_address_too_long():
    data = {
        "shipping_address":
        """
        shipping_address": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Pellentesque enim metus, ultrices at risus vel, mollis gravida mi. Quisque ut ex convallis,
        tempor arcu varius, imperdiet urna. Morbi hendrerit rutrum diam.
        Pellentesque varius id lectus nec tempus.
        Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;
        Suspendisse luctus mattis orci.
        """,
        "items": [
            { "product_id": 1, "quantity": 1 },
            { "product_id": 2, "quantity": 3 }
        ]
    }

    errors = validate_order_creation(data)
    assert "shipping_address" in errors
    assert "L'adresse de livraison ne doit pas dépasser 255 caractères." in errors["shipping_address"]

def test_order_validator_product_id_missing():
    data = {
        "shipping_address": "12 rue de la République, 75000 Paris",
        "items": [
            { "product_id": None, "quantity": 1 },
            { "product_id": 2, "quantity": 3 }
        ]
    }

    errors = validate_order_creation(data)
    assert "product_id" in errors["items_details"][0]
    assert "product_id est obligatoire." in errors["items_details"][0]["product_id"]