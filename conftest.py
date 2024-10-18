import pytest
from endpoints.create_meme import CreateMeme
from endpoints.update_meme import UpdateMeme
from endpoints.get_memes import GetMemes
from endpoints.get_meme_by_id import GetMemeById
from endpoints.delete_meme import DeleteMeme
from endpoints.authorize import GetUserToken
from endpoints.token_live import TokenLive


@pytest.fixture()
def create_meme_endpoint(session_token):
    return CreateMeme(session_token)


@pytest.fixture()
def update_meme_endpoint(session_token):
    return UpdateMeme(session_token)


@pytest.fixture()
def get_memes_endpoint(session_token):
    return GetMemes(session_token)


@pytest.fixture()
def get_meme_by_id_endpoint(session_token):
    return GetMemeById(session_token)


@pytest.fixture()
def delete_meme_endpoint(session_token):
    return DeleteMeme(session_token)


@pytest.fixture()
def authorize_user_endpoint():
    return GetUserToken()


@pytest.fixture()
def check_live_token_endpoint():
    return TokenLive()


@pytest.fixture()
def meme_id(create_meme_endpoint, delete_meme_endpoint, request):
    body = {
        "text": "пример текста для фикстуры",
        "url": "https://example.com",
        "tags": ["пример", "данные"],
        "info": {
            "author": "Иван Иваныч",
            "date": "2024-10-01"
        }
    }
    response = create_meme_endpoint.create(body)
    create_meme_endpoint.check_status_200()
    response_data = response.json()
    meme_id = response_data.get("id")
    yield meme_id
    if "no_auto_delete" not in request.node.keywords:
        delete_meme_endpoint.delete(meme_id)


@pytest.fixture(scope="session")
def session_token():
    user_token = GetUserToken()
    response = user_token.authorize_endpoint("user_1")
    user_token.check_status_200()
    token_data = response.json()
    token = token_data.get("token")
    return token


@pytest.fixture(scope="session")
def second_user_token():
    user_token = GetUserToken()
    response = user_token.authorize_endpoint("user_2")
    user_token.check_status_200()
    token_data = response.json()
    token = token_data.get("token")
    return token


@pytest.fixture()
def del_meme(request):
    yield
    meme_id = getattr(request.node, 'meme_id', None)
    if meme_id:
        deleter = DeleteMeme(request.node.token)
        deleter.delete(meme_id)
        deleter.check_status_200()
        print(f"Deleted meme with ID: {meme_id}")
