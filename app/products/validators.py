def validate_product_creation(data: dict) -> dict:
    errors = {}

    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip()
    category = (data.get("category") or "").strip()
    price = data.get("price", None)
    stock = data.get("stock", None)

    if not name:
        errors["name"] = "Le nom est obligatoire."
    elif len(name) > 120:
        errors["name"] = "Le nom ne doit pas dépasser 120 caractères."

    if not description:
        errors["description"] = "La description est obligatoire."

    if not category:
        errors["category"] = "La catégorie est obligatoire."
    elif len(category) > 80:
        errors["category"] = "La catégorie ne doit pas dépasser 80 caractères."

    if price is None:
        errors["price"] = "Le prix est obligatoire."
    else:
        try:
            p = float(price)
            if p < 0:
                errors["price"] = "Le prix doit être positif."
        except (TypeError, ValueError):
            errors["price"] = "Le prix doit être un nombre."

    if stock is None:
        errors["stock"] = "Le stock est obligatoire."
    else:
        try:
            s = int(stock)
            if s < 0:
                errors["stock"] = "Le stock doit être un entier positif."
        except (TypeError, ValueError):
            errors["stock"] = "Le stock doit être un entier."

    return errors


def validate_product_update(data: dict) -> dict:
    return validate_product_creation(data)
