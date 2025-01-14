# ChristmasPy (script for sending Xmas greetings to all your telegram buddies)

The idea of making such script was inspired by famous and honorable blogger Igor Link and his video about automatic compliments sender in telegram, here's the repository of the project: https://github.com/link1107/AutomaticCompliments

## Guides

0. On repository page press 'Code' -> 'Download ZIP' -> unzip it wherever you like 

1. Install Python if it's not on your PC (Script was developed using Python 3.12.8)

2. After installing Python you will need to install Telethon - library to work with Telegram API (TDLib)
> pip3 install telethon

3. Enter the following link, paste your phone number and wait for confirmation code in your telegram app 
> https://my.telegram.org/

4. Choose 'API development tools' -> 'Creating an application'. Fill in 'App title' and 'Short name', press 'Create application'. You will need two variables called: 'api_id' && 'api_hash'

5. Open 'config.json' file in unzipped project folder. Paste 'api_id' && 'api_hash' values from previous step in relevant fields

6. Fill in the 'chats' field with usernames or phone numbers separating them with a comma - this will be the users you will send a greetings to. In the default version of 'config.json' there is only ["me", "me"] - so that script will send two random greetings in your 'Saved Messages' chat so you can test the program locally before actually sending greetings to others.

7. If you're ready, just launch the script from your terminal
> python3 main.py

Script will ask you to login to your telegram account on a first launch, then it will create a 'client.session' file so that on futher launches you won't need to complete the authorization.

## Links

- Telethon repository: https://github.com/LonamiWebs/Telethon/tree/v1
- Greetings website: https://pozdravok.com/pozdravleniya/prazdniki/noviy-god/korotkie/
- Good article on xpath requests: https://habr.com/ru/articles/753332/ 