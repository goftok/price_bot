# Price Bot

This is a simple bot that can be used to track ads on Marktplaats.nl and 2dehands.be. Bot will send you a message on Telegram when a new ad is posted that matches your search criteria.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.8 or higher
- Installed Poetry (version >= 1.8.2)

## Installation

1. Clone the repository
2. Install dependencies using Poetry:

```shell
poetry install
```

3. Activate the virtual environment:

```shell
poetry shell
```

4. Create a `.env` file in the root of the project and add the following variables:

```shell
BOT_TOKEN=your_telegram_bot_token
CHAT_ID1=your_telegram_chat_id
CHAT_ID2=your_telegram_chat_id
CHAT_ID3=your_telegram_chat_id
CHAT_ID4=your_telegram_chat_id
```

## Usage

1. Run the bot:

```shell
python main.py
```

## Adding new search criteria

To add new search criteria upu need to modify the config.py file. If you want to add new chat_id, you need to add it to the .env file and add it to \_secrets.py file.

## Config

This configuration file defines the parameters for scraping car data. Each section in the configuration represents a different data source or scraping rule set.

Template for configuration sections:

```python
template_config = {
    "source": str,                              # Identifier for the data source (custom name).
    "min_price": (type(None), int),             # Minimum price for filtering, can be None.
    "max_price": (type(None), int),             # Maximum price for filtering, can be None.
    "min_year": (type(None), int),              # Minimum year for filtering, can be None.
    "max_year": (type(None), int),              # Maximum year for filtering, can be None.
    "min_mileage": (type(None), int),           # Minimum mileage for filtering, can be None.
    "max_mileage": (type(None), int),           # Maximum mileage for filtering, can be None.
    "chat_id": str,                             # Chat ID for sending messages or alerts.
    "not_allowed_models": (type(None), list),   # List of not allowed car models, can be None for no restriction.
    "allowed_models": (type(None), list),       # List of allowed car models, can be None for no restriction.
    "is_automatic": (type(None), bool),         # Filter for automatic transmission, can be None.
    "url_numbers": int,                         # Number of URLs to process.
    "function_for_message": callable,           # Function to create messages for bot.
    "api_link": str,                            # Link to the API for data scraping.
    "max_distance_nijmegen": (type(None), int), # Max distance from Nijmegen for filtering, can be None.
    "max_distance_leuven": (type(None), int),   # Max distance from Leuven for filtering, can be None.
    "query_params": dict,                       # Dictionary of query parameters for API requests.
}
```
