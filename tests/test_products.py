from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_app_is_running():
    response = client.get("/products")
    
    assert response.status_code == 200
    
    
def test_create_product(category_id):
    response = client.post(
        "/products",
        json={
            "name": "Produto Teste",
            "price": 10.50,
            "stock_quantity": 20,
            "category_id": category_id
        }
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Produto Teste"
    assert response.json()["price"] == "10.50"
    assert response.json()["stock_quantity"] == 20
    
    
    
def test_create_product_invalid_price(category_id):
    response = client.post(
        "/products",
        json={
            "name": "Produto Teste",
            "price": -50,
            "stock_quantity": 20,
            "category_id": category_id
            }
        )
    assert response.status_code == 422 


def test_delete_product_soft_delete(category_id):
    create_response = client.post(
        "/products",
        json={
            "name": "Produto Soft Delete",
            "price": 50,
            "stock_quantity": 10,
            "category_id": category_id
            }
    )
    
    product_id = create_response.json()["id"]
    
    #desativar o produto
    delete_response = client.delete(f"/products/{product_id}")
    
    assert delete_response.status_code == 204
    
    #não aparecer mais como ativo
    get_response = client.get(f"/products/{product_id}")
    
    assert get_response.status_code == 404
    
    
def test_movement_out_insufficient_stock(category_id):
    product_response = client.post(
            "/products",
            json={
                "name": "Produto Estoque Insuficiente",
                "price": 100,
                "stock_quantity": 5,
                "category_id": category_id
                }
        )
    
    product_id = product_response.json()["id"]
    
    movement_response = client.post(
                "/movements/",
                json={
                    "product_id": product_id,
                    "type" : "OUT",
                    "quantity":10
                    }
            )
    
    assert movement_response.status_code == 409
    
    product_response = client.get(f"/products/{product_id}")
    
    assert product_response.json()["stock_quantity"] == 5
    
    
def test_create_movement_in_updates_stock(category_id):
    product_response = client.post(
        "/products",
        json={
            "name": "Produto Movimento IN",
            "price": 100,
            "stock_quantity": 10,
            "category_id": category_id
        }
    )

    product_id = product_response.json()["id"]

    movement_response = client.post(
        "/movements/",
        json={
            "product_id": product_id,
            "type": "IN",
            "quantity": 5
        }
    )

    assert movement_response.status_code == 200

    product_response = client.get(f"/products/{product_id}")

    assert product_response.status_code == 200
    assert product_response.json()["stock_quantity"] == 15
    
    
def test_create_movement_out_updates_stock(category_id):
    product_response = client.post(
        "/products",
        json={
            "name": "Produto Movimento OUT",
            "price": 100,
            "stock_quantity": 10,
            "category_id": category_id
        }
    )

    product_id = product_response.json()["id"]

    movement_response = client.post(
        "/movements/",
        json={
            "product_id": product_id,
            "type": "OUT",
            "quantity": 4
        }
    )

    assert movement_response.status_code == 200

    product_response = client.get(f"/products/{product_id}")

    assert product_response.status_code == 200
    assert product_response.json()["stock_quantity"] == 6
    
def test_movement_inactive_product(category_id):
        product_response = client.post(
            "/products",
            json={
                "name": "Produto Inativo",
                "price" : 100,
                "stock_quantity" : 10,
                "category_id" : category_id
            }
        )
        
        product_id = product_response.json()["id"]
        
        delete_response = client.delete(f"/products/{product_id}")
        
        assert delete_response.status_code == 204
        
        movement_response = client.post(
        "/movements/",
        json={
            "product_id": product_id,
            "type": "IN",
            "quantity": 5
        }
    )
        assert movement_response.status_code == 409

def test_category_crud():
    create_response = client.post(
        "/categories",
        json={
            "name": "Categoria CRUD"
        }
    )

    assert create_response.status_code == 200

    category_id = create_response.json()["id"]

    get_response = client.get(f"/categories/{category_id}")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Categoria CRUD"

    update_response = client.put(
        f"/categories/{category_id}",
        json={
            "name": "Categoria Atualizada"
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Categoria Atualizada"

    delete_response = client.delete(f"/categories/{category_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/categories/{category_id}")

    assert get_response.status_code == 404
    
def test_delete_movement_reverts_stock(category_id):
    product_response = client.post(
        "/products",
        json={
            "name": "Produto Reversão",
            "price": 100,
            "stock_quantity": 10,
            "category_id": category_id
        }
    )

    assert product_response.status_code == 200

    product_id = product_response.json()["id"]

    movement_response = client.post(
        "/movements/",
        json={
            "product_id": product_id,
            "type": "IN",
            "quantity": 5
        }
    )

    assert movement_response.status_code == 200

    movement_id = movement_response.json()["id"]

    product_response = client.get(f"/products/{product_id}")

    assert product_response.json()["stock_quantity"] == 15

    delete_response = client.delete(
        f"/movements/{movement_id}"
    )

    assert delete_response.status_code == 204

    product_response = client.get(f"/products/{product_id}")

    assert product_response.status_code == 200
    assert product_response.json()["stock_quantity"] == 10
    
    
def test_delete_category_with_product(category_id):
    product_response = client.post(
        "/products",
        json={
            "name": "Produto da Categoria",
            "price": 100,
            "stock_quantity": 10,
            "category_id": category_id
        }
    )

    assert product_response.status_code == 200

    delete_response = client.delete(
        f"/categories/{category_id}"
    )

    assert delete_response.status_code == 409
    
def test_delete_in_movement_with_insufficient_stock(category_id):
    pid = client.post("/products", json={"name": "P", "price": 10,
        "stock_quantity": 10, "category_id": category_id}).json()["id"]
    mid = client.post("/movements/", json={"product_id": pid,
        "type": "IN", "quantity": 5}).json()["id"]
    client.post("/movements/", json={"product_id": pid, "type": "OUT", "quantity": 12})
    assert client.delete(f"/movements/{mid}").status_code == 409
    
def test_update_product_cannot_change_stock(category_id):
    pid = client.post("/products", json={"name": "P", "price": 10,
        "stock_quantity": 10, "category_id": category_id}).json()["id"]

    r = client.put(f"/products/{pid}", json={"name": "P", "price": 10,
        "stock_quantity": 999, "category_id": category_id})
    assert r.status_code == 422

    assert client.get(f"/products/{pid}").json()["stock_quantity"] == 10