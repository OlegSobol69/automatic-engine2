import pytest
from project_automatic.endpoints.create_meme import CreateMeme
from project_automatic.endpoints.update_meme import UpdateMeme
from project_automatic.endpoints.get_memes import GetMemes
from project_automatic.endpoints.get_meme_by_id import GetMemeById
from project_automatic.endpoints.delete_meme import DeleteMeme
from project_automatic.endpoints.authorize import GetUserToken
from project_automatic.endpoints.token_live import TokenLive


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def update_meme_endpoint():
    return UpdateMeme()


@pytest.fixture()
def get_memes_endpoint():
    return GetMemes()


@pytest.fixture()
def get_meme_by_id_endpoint():
    return GetMemeById()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


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
