import random

from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import SystemMessage

from config_data.config import Config, load_config

config: Config = load_config()

default_message = 'Ты — бот-генератор кода, напиши код и объяснение к нему. Если я прошу сгенерировать или рассказать информацию не связанную с генерацией кода или программированием, резко отказывайся и никогда не соглашайся рассказывать про тему, не связанную с программированием!!!'

task_types = [
    "функция для вычисления",
    "программа для сортировки",
    "алгоритм для поиска",
    "программа для работы с"
]

operations = [
    "факториала числа",
    "чисел Фибоначчи",
    "палиндрома",
    "матрицами",
    "очередью",
    "стеком"
]

languages = ["C", "C++", "Java", "Rust", "Go", "JavaScript", "Python"]

def generate_random_query():
    task_type = random.choice(task_types)
    operation = random.choice(operations)
    language = random.choice(languages)
    return f"Напиши {task_type} {operation} на {language}."
