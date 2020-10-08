import datetime


class Comment:
    def __init__(self, text, university):
        self.text = text.strip()
        self.university = university

    university = ""
    text = ""
    date = datetime.MINYEAR
    mark = 0
    like = 0
    id = 0
    trust = 0.0
