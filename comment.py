import datetime


class Comment:
    def __init__(self, text, university):
        self.text = text.strip()
        self.university = university

    university = -1
    text = ""
    date = datetime.MINYEAR
    mark = 0
    like = 0
    id = -1
    trust = 0.0
    orig_id = -1
    source = -1