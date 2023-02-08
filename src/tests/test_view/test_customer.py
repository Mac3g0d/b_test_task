import pytest
from fastapi.testclient import TestClient


def test_get_customers(client: TestClient, many_customers):
    response = client.get('/api/v1/customers/')
    assert response.status_code == 200
    assert len(response.json()['results']) == len(many_customers)


def test_get_customer_detail(client: TestClient, customer):
    fetched_customer = client.get(f'/api/v1/customers/{customer.id}').json()
    assert fetched_customer
    assert fetched_customer['id'] == str(customer.id)
    assert fetched_customer['name'] == customer.name


def test_create_customer(client: TestClient, customer_data):
    fetched_customer = client.post('/api/v1/customers/', data=customer_data.json(exclude={'id'})).json()
    assert fetched_customer
    assert fetched_customer['name'] == customer_data.name


def test_update_customer(client: TestClient, customer):
    fetched_customer = client.patch(f'/api/v1/customers/{customer.id}', json=dict(name=customer.name * 2)).json()
    assert fetched_customer
    assert fetched_customer['id'] == str(customer.id)
    assert fetched_customer['name'] == customer.name * 2


def test_delete_customer(client: TestClient, customer):
    fetched_customer = client.delete(f'/api/v1/customers/{customer.id}')
    assert fetched_customer.status_code == 204

