import configuration
import requests
import data

# Создание нового пользователя
#       Параметры: user_body - тело запроса
def post_new_user(user_body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # подставляем полный url
                         json = user_body,
                         headers = data.user_headers)   # заголовки из файла data.py - не изменяются

# Создание набора пользователя
#     Параметры: kit_headers - заголовки запроса, kit_body - тело запроса
def post_new_user_kit(kit_headers, kit_body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_KIT_PATH,  # подставляем полный url
                         json = kit_body,
                         headers = kit_headers)
