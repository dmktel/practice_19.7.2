from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password, not_valid_auth_key
import os

pf = PetFriends()

# Positive tests
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Tux', animal_type='penguin',
                                     age='4', pet_photo='images/pinguino.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Tux", "pinguin", "3", "images/pinguino.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_create_pet_simple_with_valid_data(name='Tux', animal_type='penguin',
                                     age='4'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_set_photo_with_valid_data(pet_photo='images/pinguino.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] != ''
    else:
        raise Exception("There is no my pets")

# Negative tests
# Not valid email test
def test_get_api_key_for_not_valid_user(email=not_valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# Not valid password test
def test_get_api_key_for_not_valid_user(email=valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# Not valid auth key test
def test_get_all_pets_with_not_valid_auth_key(filter=''):

    status, result = pf.get_list_of_pets(not_valid_auth_key, filter)
    assert status == 403

# Not valid pet_id test
def test_set_photo_with_incorrect_pet_id(pet_photo='images/dog.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Make incorrect pet_id value
    pet_id = 'asdfjg'

    status, result = pf.set_photo(auth_key, pet_id, pet_photo)
    assert status != 200

# Not valid image format test
def test_set_photo_with_wrong_format(pet_photo='images/pdf.pdf'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.set_photo(auth_key, pet_id, pet_photo)
    assert status != 200

# Failed tests
# Missing one argument in add_new_pet request
def test_failed_add_new_pet_without_one_argument(name='Tux', animal_type='penguin', pet_photo='images/pinguino.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, pet_photo)

    assert status == 200
    assert result['name'] == name

# Trying to set string instead file in set photo request
def test_failed_set_photo_with_valid_data(pet_photo=''):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] != ''
    else:
        raise Exception("There is no my pets")

# Missing one argument in update_pet_info request
def test_failed_update_self_pet_info(name='Мурзик', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# Passed tests but with ERRORS!!!
# Passed test with error int/string type
def test_passed_with_error_update_self_pet_info(name='Doggy', animal_type='dog', age='abc'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# Passed test with not allowed image NEF format in set photo request
def test_passed_with_error_nef_set_photo_with_valid_data(pet_photo='images/nef.NEF'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] != ''
    else:
        raise Exception("There is no my pets")

# Passed test with not allowed image TIFF format in set photo request
def test_set_passed_with_error_tiff_photo_with_valid_data(pet_photo='images/tiff.tiff'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] != ''
    else:
        raise Exception("There is no my pets")