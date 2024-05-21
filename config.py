import os

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = os.getenv("BOT_NAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEPOSIT_ADDRESS = os.getenv("DEPOSIT_ADDRESS")

RUN_IN_MAINNET = False  # Switch True/False to change mainnet to testnet

if RUN_IN_MAINNET:
    API_KEY = os.getenv("MAINNET_API_KEY")
    API_BASE_URL = 'https://toncenter.com'
else:
    API_KEY = os.getenv("TESTNET_API_KEY")
    API_BASE_URL = 'https://testnet.toncenter.com'
