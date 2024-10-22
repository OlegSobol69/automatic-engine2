import allure
import pytest

TEST_DATA = [
    {"text": "Это пример текста 1", "url": "https://example.com/1", "tags": ["пример1", "json1", "данные1"],
     "info": {"author": "Иван Иванов1", "date": "2024-10-01", "views": 100}},
    {"text": "Это  пример текста2", "url": "https://example.com/2", "tags": ["пример2", "обновление2"],
     "info": {"author": "Пётр Петров2", "views": 200}}
]

NEGATIVE_DATA = [
    ({"text": 12345, "url": "https://example.com", "tags": ["пример", "json"], "info": {"author": "Иван"}}, "text"),
    ({"text": "test", "url": 67890, "tags": ["пример", "test"], "info": {"author": "Иван"}}, "url"),
    ({"text": "test", "url": "https://example.com", "tags": "invalid_tags", "info": {"author": "Иван"}}, "tags"),
    ({"text": "test", "url": "https://example.com", "tags": ["пример"], "info": "invalid_info"}, "info")
]

INVALID_UPDATE_BODIES = [
    ({}, 'empty request body'),
    ({"tags": ["исправлено"], "info": {"author": "Иван Иванов", "date": "2024-10-01"}}, 'missing required fields'),
    ({"id": 123, "text": 123, "url": True, "tags": "json", "info": "invalid_info"}, 'invalid data types'),
    ({"id": 123, "text": "A" * 10001, "url": "https://example.com", "tags": ["long_text"],
      "info": {"author": "Иван Иванов", "date": "2024-10-01"}}, 'text length limit')
]


VALID_UPDATE_BODIES = [
    {"id": None, "text": "Обновленный текст мемa.", "url": "https://updated-example.com",
     "tags": ["тест", "апдейт"], "info": {"director": "Иван Иванов", "message": "allowed"}},
    {"id": None, "text": "Другой обновленный текст.", "url": "https://another-example.com",
     "tags": ["пример", "json"], "info": {"author": "Мария Смирнова", "views": 150}}
]


@pytest.mark.parametrize('body', TEST_DATA)
@allure.feature('Create Meme')
def test_create_meme_check_valid_data(create_meme_endpoint, body, del_meme, request):
    create_meme_endpoint.create(body, request=request)
    create_meme_endpoint.check_response_time()
    create_meme_endpoint.check_response_is_not_empty()
    create_meme_endpoint.check_status_200()
    create_meme_endpoint.check_response_has_id()
    create_meme_endpoint.check_content_type()
    create_meme_endpoint.check_field_types()
    create_meme_endpoint.check_url_format()
    create_meme_endpoint.check_response_has_mandatory_fields()

    create_meme_endpoint.check_valid_fields(
        expected_text=body["text"],
        expected_url=body["url"],
        expected_tags=body["tags"],
        expected_info=body["info"],
        expected_user="user_1"
    )


@pytest.mark.parametrize('body', TEST_DATA)
@allure.feature('Create Meme without token (expecting 401)')
def test_create_meme_without_token(create_meme_endpoint, body):
    headers_without_token = {key: value for key, value in create_meme_endpoint.headers.items() if
                             key != 'Authorization'}
    create_meme_endpoint.create(body, custom_headers=headers_without_token)
    create_meme_endpoint.check_status_401_without_token()


@pytest.mark.parametrize("invalid_body, field_name", NEGATIVE_DATA)
@allure.feature('Create Meme with invalid data')
def test_create_meme_with_invalid_data(create_meme_endpoint, invalid_body, field_name):
    create_meme_endpoint.create(invalid_body)
    create_meme_endpoint.check_status_400_bad_request()
    print(f"Checked invalid field: {field_name}")


@pytest.mark.no_auto_delete
@allure.feature('Delete Meme')
def test_delete_meme(meme_id, delete_meme_endpoint):
    delete_meme_endpoint.delete(meme_id)
    delete_meme_endpoint.check_response_time()
    delete_meme_endpoint.check_status_200()

    delete_meme_endpoint.check_successful_deletion_message(meme_id)
    delete_meme_endpoint.delete(meme_id)
    delete_meme_endpoint.check_status_404_for_confirm_deleted_meme()


@allure.feature('Delete Meme check status code 405 Method Not Allowed')
def test_delete_invalid_method(delete_meme_endpoint, meme_id):
    response = delete_meme_endpoint.send_post_method_request_in_delete(meme_id)
    delete_meme_endpoint.check_status_405(response)


@allure.feature('Delete Meme check status code 404 and 400')
def test_delete_nonexistent_and_invalid_id_responses(delete_meme_endpoint):
    delete_meme_endpoint.delete(meme_id=0)
    delete_meme_endpoint.check_status_404()
    delete_meme_endpoint.delete(meme_id="invalid")
    delete_meme_endpoint.check_status_400_bad_request()


@allure.feature('Delete Meme without token')
def test_delete_meme_without_token(meme_id, delete_meme_endpoint):
    headers_without_token = {key: value for key, value in delete_meme_endpoint.headers.items() if
                             key != 'Authorization'}
    delete_meme_endpoint.delete(meme_id, custom_headers=headers_without_token)
    delete_meme_endpoint.check_status_401_without_token()


@allure.feature('Delete Meme with another user token')
def test_delete_meme_with_another_user_token(meme_id, delete_meme_endpoint, second_user_token):
    delete_meme_endpoint.delete(meme_id, custom_headers={'Authorization': second_user_token})
    delete_meme_endpoint.check_status_403_with_another_user_token()


@allure.feature('Get meme by id')
def test_get_meme_by_id(meme_id, get_meme_by_id_endpoint):
    get_meme_by_id_endpoint.get_meme_by_id(meme_id)
    get_meme_by_id_endpoint.check_response_time()
    get_meme_by_id_endpoint.check_status_200()
    get_meme_by_id_endpoint.check_response_is_not_empty()
    get_meme_by_id_endpoint.check_field_types()
    get_meme_by_id_endpoint.check_response_has_mandatory_fields()
    get_meme_by_id_endpoint.check_meme_id_matches(meme_id)


@allure.feature('Get Meme by ID - Not Found Response')
def test_get_meme_by_id_not_found(get_meme_by_id_endpoint):
    get_meme_by_id_endpoint.get_meme_by_id(meme_id=0)
    get_meme_by_id_endpoint.check_status_404()


@allure.feature('Get Meme by ID check status code 405 Method Not Allowed')
def test_get_meme_by_id_invalid_method(get_meme_by_id_endpoint, meme_id):
    response = get_meme_by_id_endpoint.send_patch_method_request_in_get_meme_by_id(meme_id)
    get_meme_by_id_endpoint.check_status_405(response)


@allure.feature('Get meme by id without token')
def test_get_meme_by_id_without_token(meme_id, get_meme_by_id_endpoint):
    headers_without_token = {key: value for key, value in get_meme_by_id_endpoint.headers.items() if
                             key != 'Authorization'}
    get_meme_by_id_endpoint.get_meme_by_id(meme_id, custom_headers=headers_without_token)
    get_meme_by_id_endpoint.check_status_401_without_token()


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


@allure.feature('Get all memes without token')
def test_get_memes_without_token(get_memes_endpoint):
    headers_without_token = {key: value for key, value in get_memes_endpoint.headers.items() if
                             key != 'Authorization'}
    get_memes_endpoint.get_all_memes(custom_headers=headers_without_token)
    get_memes_endpoint.check_status_401_without_token()


@allure.feature('Get all memes check status code 405 Method Not Allowed')
def test_get_memes_invalid_method(get_memes_endpoint):
    response = get_memes_endpoint.send_put_method_request_in_get_memes()
    get_memes_endpoint.check_status_405(response)


@pytest.mark.parametrize('body', VALID_UPDATE_BODIES)
@allure.feature('Update Meme')
def test_update_meme_check_valid_data(update_meme_endpoint, meme_id, body):
    update_meme_endpoint.update(meme_id, body)
    update_meme_endpoint.check_response_time()
    update_meme_endpoint.check_response_is_not_empty()
    update_meme_endpoint.check_status_200()
    update_meme_endpoint.check_field_types()

    update_meme_endpoint.check_valid_fields(
        expected_text=body["text"],
        expected_url=body["url"],
        expected_tags=body["tags"],
        expected_info=body["info"],
        expected_user="user_1"
    )


@allure.feature('Update Meme check status code 405 Method Not Allowed')
def test_update_meme_invalid_method(update_meme_endpoint, meme_id):
    response = update_meme_endpoint.send_post_method_request_in_update(meme_id)
    update_meme_endpoint.check_status_405(response)


@pytest.mark.parametrize("body", [
    {"id": 0, "text": "обновление 1", "url": "https://example.com", "tags": [], "info": {}},
    {"id": 999999, "text": "обновления 2", "url": "https://example.com", "tags": [], "info": {}}
])
@allure.feature('Update non-existent meme')
def test_update_non_existent_meme_status_404(update_meme_endpoint, body):
    non_existent_meme_id = body["id"]
    update_meme_endpoint.update(non_existent_meme_id, body)
    update_meme_endpoint.check_status_404()
    print(f"Checked update of non-existent meme with id: {non_existent_meme_id} and body: {body}")


@pytest.mark.parametrize("invalid_body, error_message", INVALID_UPDATE_BODIES)
@allure.feature('Update Meme with invalid data')
def test_update_meme_with_invalid_data(update_meme_endpoint, meme_id, invalid_body, error_message):
    update_meme_endpoint.update(meme_id, invalid_body)
    update_meme_endpoint.check_status_400_bad_request()
    print(f"Checked invalid case: {error_message}")


@pytest.mark.parametrize('body', VALID_UPDATE_BODIES)
@allure.feature('Update Meme without token')
def test_update_meme_without_token(update_meme_endpoint, meme_id, body):
    headers_without_token = {key: value for key, value in update_meme_endpoint.headers.items() if
                             key != 'Authorization'}
    update_meme_endpoint.update(meme_id, body, custom_headers=headers_without_token)
    update_meme_endpoint.check_status_401_without_token()


@pytest.mark.parametrize('body', VALID_UPDATE_BODIES)
@allure.feature('Update Meme with another user token')
def test_update_meme_with_another_token(update_meme_endpoint, meme_id, second_user_token, body):
    update_meme_endpoint.update(meme_id, body, custom_headers={'Authorization': second_user_token})
    update_meme_endpoint.check_status_403_with_another_user_token()


@allure.feature('Authorize and get token')
def test_get_token_user(authorize_user_endpoint):
    authorize_user_endpoint.authorize_endpoint("user_1")
    authorize_user_endpoint.check_response_time()
    authorize_user_endpoint.check_status_200()

    authorize_user_endpoint.check_token_in_response()
    authorize_user_endpoint.check_user_in_response("user_1")


@allure.feature('Token live right now')
def test_token_live(check_live_token_endpoint):
    check_live_token_endpoint.token_live_endpoint()
    check_live_token_endpoint.check_response_time()
    check_live_token_endpoint.check_status_200()


@allure.feature('Check invalid token status 404')
def test_token_live_with_invalid_token(check_live_token_endpoint):
    invalid_token = "invalid_token"
    check_live_token_endpoint.token_live_endpoint(custom_token=invalid_token)
    check_live_token_endpoint.check_status_404_for_invalid_token()
