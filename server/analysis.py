from database import DB
class Analyser:
    def __init__(self, username, db):
        self.runs = db.get_runs_by_username(username)

    