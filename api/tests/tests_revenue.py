def test_revenue_endpoint(client):
    response = client.get("/orders/revenue")
    assert response.status_code == 200
    data = response.json()
    assert "total_orders" in data
    assert "total_revenue" in data