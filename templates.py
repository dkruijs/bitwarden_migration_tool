class Item():
    def __init__(self, 
                 organization_id, collection_ids, folder_id, 
                 type, name, notes, 
                 favorite, fields, login, 
                 secure_note, card, identity, reprompt):
        self.organization_id = None,
        self.collection_ids = None,
        self.folder_id = None,
        self.type = 1,
        self.name = "Item name",
        self.notes = "Some notes about this item.",
        self.favorite = False,
        self.fields = [],
        self.login = None,
        self.secure_note = None,
        self.card = None,
        self.identity = None,
        self.reprompt = 0