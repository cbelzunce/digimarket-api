def test_register_then_login_ok(client):
    r = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "MotDePasseTest456!",
        "first_name": "Chris",
        "last_name": "Test",
    })
    assert r.status_code == 201

    r = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "MotDePasseTest456!",
    })
    assert r.status_code == 200
    data = r.get_json()
    assert "access_token" in data


def test_register_twice_same_email(client):
    r = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "MotDePasseTest456!",
        "first_name": "Chris",
        "last_name": "Test",
    })
    assert r.status_code == 201

    r2 = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "MotDePasseTest456!",
        "first_name": "Chris",
        "last_name": "Test",
    })
    assert r2.status_code == 409
    data = r2.get_json()
    assert "L'email existe" in data["message"]


def test_register_then_login_wrong_password(client):
    r = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "MotDePasseTest456!",
        "first_name": "Chris",
        "last_name": "Test",
    })
    assert r.status_code == 201

    r = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "MauvaisMotDePasseTest456!",
    })
    assert r.status_code == 401
    data = r.get_json()
    assert "message" in data
    assert "Identifiants invalides" in data["message"]

