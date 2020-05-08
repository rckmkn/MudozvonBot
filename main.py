# coding: utf8

'''
ОПИСАНИЕ 

MudozvonBot -- это бот, который проверят каждое сообщение от
Артема Каца (vk.com/id143868161) и в случае наличия там упоминаний
отправляет сообщение <<БЛЯДЬ ДА ТЫ ЗАЕБАЛ МУДОЗВОН>> 

ID Артема -- 143868161
'''

# Встроенные модули
from json import load # Для загрузки json-а со всеми данными
from re import search # Для поиска id в сообщений

# Внешние модули
from sanic import Sanic, response # Для сервера
from sanic.response import json # Для ответа от сервера в форме json-а
from vk_api import VkApi # Для работы с VK-api

# Получение json со всеми данными (Токеном, ID группы, названием и тп.)       
with open("DataExample.json", "r", encoding="utf-8") as file:
    # В дата хранятся поля:
    # Name -- название бота
    # Token -- токен группы
    # SecretCode -- секретный код для проверки сообщений
    # ArtemID -- ID Артема
    # ConfirmationCode -- код для подтверждения
    # GroupId -- ID группы
    data = load(file) 
    
BotApi = VkApi(token = data["Token"])
Bot = BotApi.get_api() 

# Создание сервера
application = Sanic(__name__)
@application.route('/', methods=["POST"])
def main(request):
    # Получение данных из запроса в dict
    request = request.json
    
    # Проверка секретного ключа
    if   (request["secret"] == data["SecretCode"]):
        # Если тип запроса -- подтверждение
        if   (request["type"] == "confirmation"):
            return response.text(data["ConfirmationCode"])
        
        # Если тип запроса -- сообщение
        elif (request["type"] == "message_new"):
            # Получаем из запроса именно данные о сообщений
            message = request["object"]["message"]
            
            # Если сообщение от Артема Каца и там есть ссылка
            if (message["from_id"] == data["ArtemID"]) and (search(r'id\d+', message["text"])):
                report = "БЛЯДЬ ДА ТЫ ЗАЕБАЛ МУДОЗВОН"
                Bot.messages.send(peer_id = message["peer_id"],
                                  message = report,
                                  random_id = 0)                        
        
        return response.text("ok")

# Запуск сервера
if   (__name__ == "__main__"):
    application.run(host="")
    #127.0.0.1   