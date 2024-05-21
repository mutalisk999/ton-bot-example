# TON payments Telegram Bot Example

Example of Telegram bot that can receive payments in TON.

All sources

`bot.py` is a program to run Telegram bot

`config.py` is a config file

`db.py` is a module to interact with sqlite3 database

`ton.py` is a module to handle payments in TON

# Setup
You need to complete 4 simple steps to set up and run the bot
### 1. Clone repository:
    git clone https://github.com/mutalisk999/ton-bot-example.git
    cd ton-bot-example
### 2. Install PyPi packages
    pip install -r requirements.txt
    # or
    poetry install
    # or
    pipenv lock
    pipenv install
### 3. Configure the bot
Open file `.env` and enter your Bot token, Deposit address and Toncenter API key.

You can also switch between Mainnet and Testnet there by changing `RUN_IN_MAINNET` to `True` or `False`
### 4. Run the bot
    python bot.py
    # or
    poetry run python3 bot.py
    # or
    pipenv run python bot.py
