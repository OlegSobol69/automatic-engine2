import allure
import pytest


@allure.feature('Create Meme')
def test_create_meme(create_meme_endpoint):
    create_meme_endpoint.create()

    create_meme_endpoint.check_status_200()
    create_meme_endpoint.check_response_has_id()
    create_meme_endpoint.check_content_type()
    create_meme_endpoint.check_field_types()
    create_meme_endpoint.check_url_format()

    create_meme_endpoint.delete_meme()

    create_meme_endpoint.create_without_token()
    create_meme_endpoint.check_status_401()


@pytest.mark.parametrize("invalid_body, field_name", [
    ({"text": 12345, "url": "https://example.com", "tags": ["пример", "json"], "info": {"author": "Иван"}}, "text"),
    ({"text": "test", "url": 67890, "tags": ["пример", "test"], "info": {"author": "Иван"}}, "url"),
    ({"text": "test", "url": "https://example.com", "tags": "invalid_tags", "info": {"author": "Иван"}}, "tags"),
    ({"text": "test", "url": "https://example.com", "tags": ["пример"], "info": "invalid_info"}, "info")
])
@allure.feature('Create Meme with invalid data')
def test_create_meme_with_invalid_data(create_meme_endpoint, invalid_body, field_name):
    create_meme_endpoint.create_with_custom_body(invalid_body)
    create_meme_endpoint.check_status_400()
    print(f"Checked invalid field: {field_name}")


@pytest.mark.no_auto_delete
@allure.feature('Delete Meme')
def test_delete_meme(meme_id, delete_meme_endpoint):
    delete_meme_endpoint.delete(meme_id)
    delete_meme_endpoint.check_status_200()
    delete_meme_endpoint.check_successful_deletion_message(meme_id)
    delete_meme_endpoint.check_status_404(meme_id)
    delete_meme_endpoint.check_status_401_without_token(meme_id)
    delete_meme_endpoint.check_status_400_invalid_id("invalid")


# @pytest.mark.no_auto_delete
@allure.feature('Delete Meme with another user token')
def test_delete_meme_with_another_user_token(meme_id, delete_meme_endpoint, second_user_token):
    delete_meme_endpoint.check_status_403_with_another_user_token(meme_id, second_user_token)


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
    authorize_user_endpoint.authorize_endpoint("user_1")
    authorize_user_endpoint.check_status_200()


@allure.feature('Token live right now')
def test_token_live(check_live_token_endpoint):
    check_live_token_endpoint.token_live_endpoint()
    check_live_token_endpoint.check_status_200()
