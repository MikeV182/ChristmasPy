try:
    from telethon import TelegramClient
    from threading import Thread
    from parser import Parser
    import traceback, sys, requests, os
    from lxml import html


    parser = Parser('config.json')
    greetings_dict = {}
    greetings_chats = []
    api_id, api_hash, greetings_chats = parser.parse_config()
    client = TelegramClient('client', api_id, api_hash)


    def scrap_web_page(page_id, greetings_dict):
        url = 'https://pozdravok.com/pozdravleniya/prazdniki/noviy-god/korotkie/' \
            + str(page_id) + '.htm'
        print(f'started scrapping page {page_id}:\n\t', url)
        responce = requests.get(url)
        if responce.status_code == 200:
            element_tree = html.fromstring(responce.content)
        else:
            print('a problem occured when sending request to a web page:\n\t', 
                  url, 
                  f'\n\t status code: {responce.status_code}')
            os._exit(1)
        id = 1
        while True:
            selected_greeting = element_tree.xpath(
                f'//div[@class="content"]/p[{id}]/text()')
            selected_greeting_id = element_tree.xpath(
                f'//div[@class="content"]/p[{id}]/@id')
            if len(selected_greeting) == 0:
                break
            else:
                greetings_dict[selected_greeting_id[0]] = selected_greeting
                id += 1
        print(f'page {page_id} status: \033[32m[DONE]\033[0m')


    async def main():
        me = await client.get_me()
        print('\n==== LOGGED IN AS ====')
        print('Username:', me.username, '\nPhone:', me.phone)

        print('\n==== STARTED SCRAPPING THE GREETINGS PAGE ====')
        # starting from second page because first page has unique url '/', 
        # but others will have formats like this '/i.htm'
        i = 2 
        active_threads = []
        while i <= 6:
            thread = Thread(target=scrap_web_page, args=(i, greetings_dict))
            i += 1
            active_threads.append(thread)
            thread.start()

        for thread in active_threads: # waiting for all threads to terminate
            thread.join()
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
