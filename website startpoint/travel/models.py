class Destination: 
    def __init__(self, name, description, image_url, currency, comments):
        self.name = name
        self.description = description
        self.image_url = image_url
        self.currency = currency
        self.comments = comments

class Comment:
    def __init__(self, user, text, created_at):
        self.user = user
        self.text = text
        self.created_at = created_at

