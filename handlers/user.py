import uuid
import random
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart

from keyboards import keyboards
from config_data.config import Config, load_config
from database import database

from GigaQueryEngine import create_random_text, prompts_text

from aiogram.fsm.state import StatesGroup, State


