# Logging module
import asyncio
import logging
import sys

# Aiogram imports
from aiogram import Bot, Dispatcher, types  # type: ignore
from aiogram.dispatcher.filters import Text  # type: ignore
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup  # type: ignore
from aiogram.types import InlineKeyboardButton  # type: ignore
from aiogram.utils import executor  # type: ignore
from pytonconnect import TonConnect

# Local modules to work with Database and Ton network
import config
import ton
import db
from connector import get_connector

logger = logging.getLogger(__file__)

# Initialize the bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def welcome_handler(message: types.Message):
    # Function that sends the welcome message with main keyboard to user

    uid = message.from_user.id  # Not neccessary, just to make code shorter

    # If user doesn't exist in database, insert it
    if not db.check_user(uid):
        db.add_user(uid)

    # Keyboard with two main buttons: Deposit and Balance
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Deposit'))
    keyboard.row(KeyboardButton('Balance'))

    # Send welcome text and include the keyboard
    await message.answer('Hi!\nI am example bot '
                         'made for [this article](https://'
                         'docs.ton.org/develop/dapps/tutorials'
                         '/accept-payments-in-a-telegram-bot-2).\n'
                         'My goal is to show how simple it is to receive '
                         'payments in TonCoin with Python.\n\n'
                         'Use keyboard to test my functionality.',
                         reply_markup=keyboard,
                         protect_content=False,
                         parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['share', 'help'])
async def share_handler(message: types.Message):
    # Function that sends the welcome message with main keyboard to user

    uid = message.from_user.id  # Not neccessary, just to make code shorter

    # If user doesn't exist in database, insert it
    if not db.check_user(uid):
        db.add_user(uid)

    # Keyboard with two main buttons: Deposit and Balance
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton('Select a group',
                                  url=f'https://t.me/{config.BOT_NAME}?startgroup=frommenu')
    keyboard.add(button)
    await message.answer('Hi!\nI am example bot '
                         'You can share me in other groups!\n',
                         reply_markup=keyboard,
                         protect_content=False,
                         parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['wallet'])
async def wallet_handler(message: types.Message):
    chat_id = message.chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    if connected:
        button1 = InlineKeyboardButton('Send Transaction', callback_data='send_tr')
        button2 = InlineKeyboardButton('Disconnect', callback_data='disconnect')
        keyboard.add(button1)
        keyboard.add(button2)
        await message.answer(text='You are already connected!', reply_markup=keyboard)

    else:
        wallets_list = TonConnect.get_wallets()
        for wallet in wallets_list:
            button1 = InlineKeyboardButton(text=wallet['name'], callback_data=f'connect:{wallet["name"]}')
            keyboard.add(button1)
        await message.answer(text='Choose wallet to connect', reply_markup=keyboard)


@dp.message_handler(commands='balance')
@dp.message_handler(Text(equals='balance', ignore_case=True))
async def balance_handler(message: types.Message):
    # Function that shows user his current balance

    uid = message.from_user.id

    # Get user balance from database
    # Also don't forget that 1 TON = 1e9 (billion) NanoTON
    user_balance = db.get_balance(uid) / 1e9

    # Format balance and send to user
    await message.answer(f'Your balance: *{user_balance:.2f} TON*',
                         parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands='deposit')
@dp.message_handler(Text(equals='deposit', ignore_case=True))
async def deposit_handler(message: types.Message):
    # Function that gives user the address to deposit

    uid = message.from_user.id

    # Keyboard with deposit URL
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Deposit',
                                  url=f'ton://transfer/{config.DEPOSIT_ADDRESS}&text={uid}')
    keyboard.add(button)

    # Send text that explains how to make a deposit into bot to user
    await message.answer('It is very easy to top up your balance here.\n'
                         'Simply send any amount of TON to this address:\n\n'
                         f'`{config.DEPOSIT_ADDRESS}`\n\n'
                         f'And include the following comment: `{uid}`\n\n'
                         'You can also deposit by clicking the button below.',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Create Aiogram executor for our bot
    ex = executor.Executor(dp)

    # Launch the deposit waiter with our executor
    ex.loop.create_task(ton.start())

    # Launch the bot
    ex.start_polling()
