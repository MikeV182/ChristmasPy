try:
    from telethon import TelegramClient
    import asyncio
    from parser import Parser
    import traceback, sys, re, requests
    from lxml import html


    parser = Parser('config.json')
    greetings_dict = {}
    greetings_chats = []
    api_id, api_hash, greetings_chats = parser.parse_config()
    client = TelegramClient('client', api_id, api_hash)


    def scrap_web_page(greetings_dict):
        url = 'https://pozdravok.com/pozdravleniya/prazdniki/noviy-god/korotkie/'
        responce = requests.get(url)
        if responce.status_code == 200:
            element_tree = html.fromstring(responce.content)
        else:
            print('a problem occured when sending request to a web page:\n\t', 
                  url, 
                  f'\n\tstatus code: {responce.status_code}')
        firts_greeting = element_tree.xpath('//div[@class="content"]/p[1]/text()')
        print(firts_greeting)


    async def main():
        me = await client.get_me()
        print('\n==== LOGGED IN AS ====')
        print('Username:', me.username, '\nPhone:', me.phone)

        print('\n==== STARTED SCRAPPING THE GREETINGS PAGE ====')
        scrap_web_page(greetings_dict)
        print('==== GREETINGS COLLECTED ====')

        print('\n==== SENDING GREETIGNS TO ALL MENTIONED USERS ====')


    with client:
        client.loop.run_until_complete(main())

except KeyboardInterrupt:
    print('Keyboard interrupt from a user: \033[32m[OK]\033[0m')
except:
    print('An unexpected error occured: \033[31m[ERROR]\033[0m')
    print('\n==== ERROR INFORMATION ====')
    traceback.print_exc(limit=2, file=sys.stdout)
    print('==== END ====')
