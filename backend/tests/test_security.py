def test_tc_sec_01_sql_injection_literal_returns_401(client, seeded_data):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "' OR '1'='1", "password": "anything"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


def test_tc_sec_02_route_guard_without_jwt_returns_403(client):
    response = client.get("/api/v1/admin/dashboard")
    assert response.status_code == 403
