import allure
import pytest


@allure.feature('Create Meme')
def test_create_meme(create_meme_endpoint):
    create_meme_endpoint.create()
    create_meme_endpoint.check_status_200()


@pytest.mark.no_auto_delete
@allure.feature('Delete Meme')
def test_delete_meme(meme_id, delete_meme_endpoint):
    delete_meme_endpoint.delete(meme_id)
    delete_meme_endpoint.check_status_200()


@allure.feature('Get meme by id')
def test_get_meme_by_id(meme_id, get_meme_by_id_endpoint):
    get_meme_by_id_endpoint.get_meme_by_id(meme_id)
    get_meme_by_id_endpoint.check_status_200()


@allure.feature('Get all memes')
def test_get_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()
    get_memes_endpoint.check_status_200()


@allure.feature('Update Meme')
def test_update_meme(update_meme_endpoint, meme_id):
    update_meme_endpoint.update(meme_id)
    update_meme_endpoint.check_status_200()


@allure.feature('Authorize and get token')
def test_get_token_user(authorize_user_endpoint):
    authorize_user_endpoint.authorize_endpoint()
    authorize_user_endpoint.check_status_200()


@allure.feature('Token live right now')
def test_token_live(check_live_token_endpoint):
    check_live_token_endpoint.token_live_endpoint()
    check_live_token_endpoint.check_status_200()
