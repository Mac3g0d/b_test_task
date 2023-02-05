import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_customers(client: TestClient, customer):
    response = client.get('/api/v1/customers/').json()
    fetched_customer = response['results'][0]
    assert len(response['results']) == 1
    assert fetched_customer['id'] == str(customer.id)
    assert fetched_customer['name'] == customer.name
