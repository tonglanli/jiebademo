class Text:
    def __init__(self, id, name, author, period, path, uploader, uploadDate):
        self.id = id
        self.name = name
        self.author = author
        self.period = period
        self.path = path
        self.uploader = uploader
        self.uploadDate = uploadDate

class KeyCount:
    def __init__(self, key, count):
        self.key = key
        self.count = count

class YKeyCount:
    def __init__(self, key, count):
        self.key = key
        self.count = count