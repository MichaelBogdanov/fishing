import sys
import requests
from getpass4 import getpass


# Конфигурация сервера
SERVER_URL = "https://itcube-vn.ru/fishing_api"


def auth_menu(choice=None, username=None, password=None):
    """Меню авторизации в консоли"""
    while True:
        print("\n=== Рыбалка ===")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Выйти")
        
        if not choice:
            choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            return login(username, password)
        elif choice == "2":
            return register(username, password)
        elif choice == "3":
            sys.exit()
        else:
            print("Неверный выбор!")

def login(username=None, password=None):
    """Функция входа"""
    if not username:
        username = input("Логин: ").strip()
    if not password:
        password = getpass("Введите пароль: ").strip()
    
    try:
        response = requests.post(f"{SERVER_URL}/login/", json={
            'username': username,
            'password': password
        }, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успешный вход! Текущий счет: {data['user']['score']}")
            return data['user']
        else:
            print(f"Ошибка: {response.json().get('error', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException:
        print("Ошибка подключения к серверу!")
        return None

def register(username=None, password=None):
    """Функция регистрации"""
    if not username:
        username = input("Придумайте логин: ").strip()
    if not password:
        password = getpass("Введите пароль: ").strip()
    
    # Отладочная информация
    url = f"{SERVER_URL}/register/"
    print(f"Отправка POST запроса на: {url}")
    print(f"Данные: username={username}, password=****")
    
    try:
        response = requests.post(
            url, 
            json={
                'username': username,
                'password': password
            },
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Статус код: {response.status_code}")
        print(f"Полный ответ: {response.text}")
        
        if response.status_code == 201:
            print("Регистрация успешна! Теперь войдите в аккаунт.")
            return login()
        else:
            try:
                error_data = response.json()
                print(f"Ошибка сервера: {error_data}")
            except:
                print(f"Не удалось разобрать ответ: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения к серверу: {e}")
        return None

def update_server_score(username, score):
    """Обновление счета на сервере"""
    try:
        requests.post(f"{SERVER_URL}/update-score/", json={
            'username': username,
            'score': score
        })
    except requests.exceptions.RequestException:
        print("Не удалось обновить счет на сервере")

def get_fish_rarities_from_server():
    """Получение редкостей рыб с сервера"""
    try:
        response = requests.get(f"{SERVER_URL}/fish-rarities/")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        print("Не удалось загрузить редкости рыб с сервера")
    return None
