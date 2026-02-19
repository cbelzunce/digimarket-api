STATUS = {"en_attente", "validee", "expediee", "annulee"}

def validate_order_creation(data: dict)-> dict:
    errors = {}

    shipping_address = (data.get("shipping_address") or "").strip()
    items = data.get("items")

    if not shipping_address:
        errors["shipping_address"] = "L'adresse de livraison est obligatoire."
    elif len(shipping_address) > 255:
        errors["shipping_address"] = "L'adresse de livraison ne doit pas dépasser 255 caractères."

    if not isinstance(items, list) or len(items) == 0:
        errors["items"] = "La commande doit contenir au moins un produit."
        return errors

     # items = [{ "product_id": 1, "quantity": 2 }, ...]
    items_errors = []
    for i, it in enumerate(items):
        e = {}
        pid = it.get("product_id")
        qty = it.get("quantity")

        # Check product_id
        if pid is None:
            e["product_id"] = "product_id est obligatoire."
        else:
            try:
                int(pid)
            except (TypeError, ValueError):
                e["product_id"] = "product_id doit être un entier."

        # Check quantité
        if qty is None:
            e["quantity"] = "quantity est obligatoire."
        else:
            try:
                q = int(qty)
                if q <= 0:
                    e["quantity"] = "quantity doit être > 0."
            except (TypeError, ValueError):
                e["quantity"] = "quantity doit être un entier."

        items_errors.append(e)

    if any(items_errors):
        errors["items_details"] = items_errors

    return errors

def validate_status_patch(data: dict) -> dict:

    erreurs = {}
    status = (data.get("status") or "").strip()

    if not status:
        erreurs["status"] = "Le statut est obligatoire."
    elif status not in STATUS:
        erreurs["status"] = "Statut invalide. Valeurs: en_attente, validee, expediee, annulee."

    return erreurs
