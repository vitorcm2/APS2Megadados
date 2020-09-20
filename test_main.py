from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

# ERROS 404


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


def test_patch_unvalid_task():
    # uuid errado (string)
    uuid_ = "string qualquer"

    # json necessário para passar as infos
    response = client.patch(
        f"/task/{uuid_}", json={"description": "testing error", "completed": "False"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}


def test_put_unvalid_task():
    # uuid errado (string)
    uuid_ = "string qualquer"

    # json necessário para passar as infos
    response = client.put(
        f"/task/{uuid_}", json={"description": "testing error", "completed": "False"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}

# ACERTOS 200


def test_get_list_existent_task():
    response = client.get('/task')
    assert response.status_code == 200
    # json da lista sempre vazia no começo
    assert response.json() == {}


def test_get_existent_task():
    # json para existir uma task
    response = client.post(
        "/task", json={"description": "testing error", "completed": "False"})
    assert response.status_code == 200
