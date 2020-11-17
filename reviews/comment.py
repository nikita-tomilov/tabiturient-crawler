import datetime


class Comment:
    def __init__(self, text, uni_idx):
        self.text = text.strip()
        self.university = uni_idx

    university = -1
    text = ""
    date = datetime.MINYEAR
    mark = 0
    like = 0
    orig_id = -1
    trust = 0.0
    source = -1
