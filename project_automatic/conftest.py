import pytest
from project_automatic.endpoints.create_meme import CreateMeme
from project_automatic.endpoints.update_meme import UpdateMeme
from project_automatic.endpoints.get_memes import GetMemes
from project_automatic.endpoints.get_meme_by_id import GetMemeById
from project_automatic.endpoints.delete_meme import DeleteMeme
from project_automatic.endpoints.authorize import GetUserToken
from project_automatic.endpoints.token_live import TokenLive


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
    response = create_meme_endpoint.create()
    create_meme_endpoint.check_status_200()
    response_data = response.json()
    meme_id = response_data.get("id")
    yield meme_id
    if "no_auto_delete" not in request.node.keywords:
        delete_meme_endpoint.delete(meme_id)


@pytest.fixture(scope="session")
def session_token():
    user_token = GetUserToken()
    response = user_token.authorize_endpoint()
    user_token.check_status_200()
    token_data = response.json()
    token = token_data.get("token")
    return token
