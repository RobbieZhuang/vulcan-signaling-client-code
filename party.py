class Party:
    def __init__(self, party_id, host_id):
        self.party_id = party_id
        self.host_id = host_id
        self.client_ids = []

    def get_client_ids(self):
        return self.client_ids
    
    def get_party_id(self):
        return self.party_id
    
    def get_host_id(self):
        return self.host_id

    def add_client(self, client_id):
        self.client_ids.append(client_id)