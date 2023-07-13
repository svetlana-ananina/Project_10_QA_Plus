# Набор тестов для проверки параметра 'name' при создании набора пользователя
# в Яндекс.Прилавок с помощью API Яндекс.Приловок
import data
import sender_stand_request

#================================================================
# Вспомогательные функции
# Получение заголовков для создания набора пользователя
#       Параметры: authToken - авторизационный токен пользователя
def get_kit_headers(authToken):
    current_headers = data.kit_headers.copy()
    current_headers["Authorization"] = "Bearer " + authToken
    return current_headers

# Получение тела запроса для создания набора пользователя
#       Параметры: kit_name - название набора
def get_kit_body(kit_name):
    current_kit_body = data.kit_body.copy()
    current_kit_body["name"] = kit_name
    return current_kit_body

# Cоздание набора пользователя
#     Параметры: authToken - токен пользователя, kit_body - тело запроса набора для создания набора
def create_new_user_kit(authToken, kit_body):
    kit_headers = get_kit_headers(authToken)
    return sender_stand_request.post_new_user_kit(kit_headers, kit_body)    # Запрос к API

# Создание нового пользователя
# Функция возвращает authToken пользователя
def create_new_user():
    user_body = data.user_body.copy()
    response = sender_stand_request.post_new_user(user_body)    # Запрос к API
    assert response.status_code == 201
    assert response.json()["authToken"] != ""
    return response.json()["authToken"]

#================================================================
# Позитивные проверки
# Создание набора пользователя
#       Параметры: kit_name - название нового набора
#       ОР: Ожидаемый код ответа - 201
#           В ответе поле 'name' совпадает с полем 'name' в запросе (kit_name)
def positive_assert(kit_name):
    authToken = create_new_user()
    kit_body = get_kit_body(kit_name)
    response = create_new_user_kit(authToken, kit_body)         # Запрос к API
    assert response.status_code == 201
    assert response.json()["name"] == kit_name

# Негативные проверки
# Создание набора пользователя
#       Параметры: kit_body - тело запроса на создание набора
#       ОР: Ожидаемый код ответа - 400
#           В ответе поле 'code' равно 400
def negative_assert_kit_body(kit_body):
    authToken = create_new_user()
    response = create_new_user_kit(authToken, kit_body)         # Запрос к API
    assert response.status_code == 400
    assert response.json()["code"] == 400

# Создание набора пользователя
#       Параметры: kit_name - название нового набора
#       Функция формирует тело запроса и передает в основную функцию 'negative_assert_kit_body(kit_body)'
def negative_assert(kit_name):
    kit_body = get_kit_body(kit_name)
    negative_assert_kit_body(kit_body)

#================================================================
# Тесты
# Тест 1 Успешное создание набора
# Название набора содержит допустимое количество символов: 1
def test_1_create_kit_1_letter_in_name_get_success_response():
    positive_assert("a")

# Тест 2 Успешное создание набора
# Название набора содержит допустимое количество символов: 511
def test_2_create_kit_511_letter_in_name_get_success_response():
    positive_assert(data.kit_name_of_511_letters)

# Тест 3 Ошибка создания набора
# Название набора содержит количество символов меньше допустимого: 0
def test_3_create_kit_empty_name_get_error_response():
    negative_assert("")

# Тест 4 Ошибка создания набора
# Название набора содержит количество символов больше допустимого: 512
def test_4_create_kit_512_letter_in_name_get_error_response():
    negative_assert(data.kit_name_of_512_letters)

# Тест 5 Успешное создание набора
# В названии набора разрешены английские буквы
def test_5_create_kit_english_letter_in_name_get_success_response():
    positive_assert("QWErty")

# Тест 6 Успешное создание набора
# В названии набора разрешены русские буквы
def test_6_create_kit_russian_letter_in_name_get_success_response():
    positive_assert("Мария")

# Тест 7 Успешное создание набора
# В названии набора разрешены спецсимволы
def test_7_create_kit_has_special_symbol_in_name_get_success_response():
    positive_assert("\"№%@\",")

# Тест 8 Успешное создание набора
# В названии набора разрешены пробелы
def test_8_create_kit_has_space_in_name_get_success_response():
    positive_assert(" Человек и КО ")

# Тест 9 Успешное создание набора
# В названии набора разрешены цифры
def test_9_create_kit_has_number_in_name_get_success_response():
    positive_assert("123")

# Тест 10 Ошибка создания набора
# Параметр не передан в запросе
def test_10_create_kit_no_name_get_error_response():
    negative_assert_kit_body(data.kit_body_empty)

# Тест 11 Ошибка создания набора
# Передан другой тип параметра: число
def test_11_create_kit_number_type_name_get_error_response():
    negative_assert_kit_body(data.kit_body_number)
