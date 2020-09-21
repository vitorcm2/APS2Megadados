from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

# TESTES ERROS 404


def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_delete_unexistent_task():
    # gera uuid aleatório
    uuid_ = uuid.uuid4()

    response = client.delete(f"/task/{uuid_}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}


def test_get_unexistent_task():
    # gera uuid aleatório
    uuid_ = uuid.uuid4()

    response = client.get(f"/task/{uuid_}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}


def test_patch_unexistent_task():
    # gera uuid aleatório
    uuid_ = uuid.uuid4()

    # json necessário para passar as infos
    response = client.patch(
        f"/task/{uuid_}", json={"description": "testing error", "completed": "False"})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}


# ERROS 422


def test_patch_invalid_task():
    # uuid errado (string)
    uuid_ = "string qualquer"

    # json necessário para passar as infos
    response = client.patch(
        f"/task/{uuid_}", json={"description": "testing error", "completed": "False"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}


def test_put_invalid_task():
    # uuid errado (string)
    uuid_ = "string qualquer"

    # json necessário para passar as infos
    response = client.put(
        f"/task/{uuid_}", json={"description": "testing error", "completed": "False"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}

# TESTES ACERTOS 200


def test_get_list_existent_task():
    response = client.get('/task')
    assert response.status_code == 200
    # json da lista sempre vazia no começo
    assert response.json() == {}


def test_get_completed_task_list():
    response_true = client.post(
        "/task", json={"description": "testing error", "completed": "True"})
    response_false = client.post(
        "/task", json={"description": "testing error", "completed": "False"})
    response = client.get('/task?completed=true')
    assert response.status_code == 200
    # json da lista sempre vazia no começo
    assert response.json() == {response_true.json(): {
        "description": "testing error", "completed": True}}
    responsedelete1 = client.delete(f"/task/{response_true.json()}")
    responsedelete1 = client.delete(f"/task/{response_false.json()}")


def test_get_incompleted_task_list():
    response_true = client.post(
        "/task", json={"description": "testing error", "completed": "True"})
    response_false = client.post(
        "/task", json={"description": "testing error", "completed": "False"})
    response = client.get('/task?completed=false')
    assert response.status_code == 200
    # json da lista sempre vazia no começo
    assert response.json() == {response_false.json(): {
        "description": "testing error", "completed": False}}
    responsedelete1 = client.delete(f"/task/{response_true.json()}")
    responsedelete1 = client.delete(f"/task/{response_false.json()}")


def test_create_a_new_task():
    response = client.post(
        "/task", json={"description": "testing error", "completed": "False"})
    assert response.status_code == 200
    response1 = client.delete(f"/task/{response.json()}")


def test_get_existent_task():
    response = client.post(
        "/task", json={"description": "testing error", "completed": "False"})
    #assert response.status_code == 200

    response1 = client.get(f"/task/{response.json()}")
    assert response1.status_code == 200
    response1 = client.delete(f"/task/{response.json()}")


def test_put_task():
    response = client.post(
        "/task", json={"description": "testing error", "completed": "False"})
    #assert response.status_code == 200

    response1 = client.put(
        f"/task/{response.json()}", json={"description": "testing error", "completed": "False"})
    assert response1.status_code == 200
    response1 = client.delete(f"/task/{response.json()}")


def test_delete_existent_task():
    response = client.post(
        "/task", json={"description": "testing error", "completed": "False"})
    #assert response.status_code == 200

    response1 = client.delete(f"/task/{response.json()}")
    assert response1.status_code == 200


def test_patch_existent_task():
    response = client.post(
        "/task", json={"description": "testing error", "completed": "False"})
    #assert response.status_code == 200

    response1 = client.patch(
        f"/task/{response.json()}", json={"description": "testing error", "completed": "False"})
    assert response1.status_code == 200
    response1 = client.delete(f"/task/{response.json()}")
