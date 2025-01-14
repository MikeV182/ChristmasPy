import json, os, traceback, sys

try:
    class Parser:
        def __init__(self, config_file):
            self.config_file = config_file
        
        def parse_config(self):
            try:
                with open(self.config_file) as config:
                    data = json.load(config)
                    api_id = int(data['api_id'])
                    api_hash = data['api_hash']
                    chats = data['chats']         
                return api_id, api_hash, chats
            except KeyError as e:
                print(f'KeyError occured - no such field in \'config.json\': {str(e)} \033[31m[ERROR]\033[0m')
                os._exit(1)
            except FileNotFoundError as e:
                print(f'FileNotFoundError occured: {str(e)} \033[31m[ERROR]\033[0m')
                os._exit(1)
except KeyboardInterrupt:
    print('Keyboard interrupt from a user: \033[32m[OK]\033[0m')
except:
    print('An unexpected error occured: \033[31m[ERROR]\033[0m')
    print('\n==== ERROR INFORMATION ====')
    traceback.print_exc(limit=2, file=sys.stdout)
    print('==== END ====')