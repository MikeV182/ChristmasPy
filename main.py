try:
    from telethon import TelegramClient
    from threading import Thread
    from parser import Parser
    import traceback, sys, requests, os, random
    from lxml import html


    parser = Parser('config.json')
    greetings_dict = {}
    api_id, api_hash, greetings_chats = parser.parse_config()
    client = TelegramClient('client', api_id, api_hash)


    def scrap_web_page(page_id, greetings_dict):
        url = 'https://pozdravok.com/pozdravleniya/prazdniki/noviy-god/korotkie/' \
            + str(page_id) + '.htm'
        print(f'Started scrapping page {page_id}:\n\t', url)
        responce = requests.get(url)
        if responce.status_code == 200:
            element_tree = html.fromstring(responce.content)
        else:
            print('A problem occured when sending request to a web page:\n\t', 
                  url, 
                  f'\n\t Status code: {responce.status_code}')
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
        print(f'Page {page_id} status: \033[32m[DONE]\033[0m')

    async def send_random_greeting(chat, greetings_dict):
        try:
            print(f'Sending greeting to: \033[33m{chat}\033[0m')
            random_greeting_lines = random.choice(list(greetings_dict.values()))
            final_greeting = ''
            for line in random_greeting_lines:
                final_greeting += line + '\n'
            final_greeting = final_greeting.strip('\n')
            await client.send_message(chat, final_greeting)
            print(f'User \033[33m{chat}\033[0m greeting status: \033[32m[SENT]\033[0m')
        except ValueError:
            print(f'No user has such username(or phone): {chat} \033[31m[ERROR]\033[0m')

    async def main():
        me = await client.get_me()
        print('\n==== LOGGED IN AS ====')
        print('Username:', me.username, '\nPhone:', me.phone)

        print('\n==== STARTED SCRAPPING GREETINGS PAGES ====')
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
        for chat in greetings_chats:
            await send_random_greeting(chat, greetings_dict)
        print('==== ALL GREETINGS ARE SENT ====')

    with client:
        client.loop.run_until_complete(main())

except KeyboardInterrupt:
    print('Keyboard interrupt from a user: \033[32m[OK]\033[0m')
except:
    print('An unexpected error occured: \033[31m[ERROR]\033[0m')
    print('\n==== ERROR INFORMATION ====')
    traceback.print_exc(limit=2, file=sys.stdout)
    print('==== END ====')
