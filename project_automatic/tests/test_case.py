import allure
import pytest
# import pytest_check as check


@allure.feature('Create Meme')
def test_create_meme(create_meme_endpoint):
    create_meme_endpoint.create()
    create_meme_endpoint.check_response_time()
    create_meme_endpoint.check_response_is_not_empty()
    create_meme_endpoint.check_status_200()

    create_meme_endpoint.check_response_has_id()
    create_meme_endpoint.check_content_type()
    create_meme_endpoint.check_field_types()
    create_meme_endpoint.check_url_format()
    create_meme_endpoint.check_response_has_mandatory_fields()

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
    delete_meme_endpoint.check_response_time()

    delete_meme_endpoint.check_status_200()
    delete_meme_endpoint.check_successful_deletion_message(meme_id)
    delete_meme_endpoint.check_status_405_invalid_method(meme_id)
    delete_meme_endpoint.check_status_404(meme_id)
    delete_meme_endpoint.check_status_401_without_token(meme_id)
    # delete_meme_endpoint.check_status_400_invalid_id("invalid")


# @pytest.mark.no_auto_delete
@allure.feature('Delete Meme with auto delete')
def test_delete_meme_with_another_user_token(meme_id, delete_meme_endpoint, second_user_token):
    delete_meme_endpoint.check_status_403_with_another_user_token(meme_id, second_user_token)


@allure.feature('Get meme by id')
def test_get_meme_by_id(meme_id, get_meme_by_id_endpoint):
    get_meme_by_id_endpoint.get_meme_by_id(meme_id)
    get_meme_by_id_endpoint.check_response_time()
    get_meme_by_id_endpoint.check_status_200()
    get_meme_by_id_endpoint.check_response_is_not_empty()

    get_meme_by_id_endpoint.check_field_types()
    get_meme_by_id_endpoint.check_response_has_mandatory_fields()
    get_meme_by_id_endpoint.check_meme_id_matches(meme_id)
    get_meme_by_id_endpoint.check_status_404("0")
    get_meme_by_id_endpoint.check_status_405(meme_id)
    get_meme_by_id_endpoint.get_meme_by_id_without_token_status_401(meme_id)


@allure.feature('Get all memes')
def test_get_memes(get_memes_endpoint):
    get_memes_endpoint.get_all_memes()
    get_memes_endpoint.check_response_time()
    get_memes_endpoint.check_response_is_not_empty()
    get_memes_endpoint.check_status_200()

    get_memes_endpoint.check_response_structure()
    get_memes_endpoint.check_each_meme_fields()
    get_memes_endpoint.check_field_types_for_each_meme()
    get_memes_endpoint.check_for_duplicate_memes()
    get_memes_endpoint.check_memes_sorted_by_id()
    get_memes_endpoint.get_memes_without_token_status_401()
    get_memes_endpoint.get_memes_with_invalid_method_status_405()


@allure.feature('Update Meme')
def test_update_meme(update_meme_endpoint, meme_id):
    update_meme_endpoint.update(meme_id)
    update_meme_endpoint.check_response_time()

    update_meme_endpoint.check_status_200()


@allure.feature('Authorize and get token')
def test_get_token_user(authorize_user_endpoint):
    authorize_user_endpoint.authorize_endpoint("user_1")
    authorize_user_endpoint.check_response_time()

    authorize_user_endpoint.check_status_200()


@allure.feature('Token live right now')
def test_token_live(check_live_token_endpoint):
    check_live_token_endpoint.token_live_endpoint()
    check_live_token_endpoint.check_response_time()

    check_live_token_endpoint.check_status_200()
