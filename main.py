from telethon import TelegramClient

from parser import Parser

if __name__ == '__main__':
    parser = Parser("config.json")
    api_id, api_hash = parser.parse_config()

    with TelegramClient('client', api_id, api_hash) as client:
        client.loop.run_until_complete(
            client.send_message('me', 'Hello, myself!'))
