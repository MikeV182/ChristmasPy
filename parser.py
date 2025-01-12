import json

class Parser:
    def __init__(self, config_file):
        self.config_file = config_file
        
    def parse_config(self):
        with open(self.config_file) as config:
            data = json.load(config)
            api_id = int(data['api_id'])
            api_hash = data['api_hash']
            chats = data['chats']         
        return api_id, api_hash, chats
