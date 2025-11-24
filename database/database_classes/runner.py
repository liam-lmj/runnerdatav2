import sqlite3

class Runner:
    def __init__(self, runner_id):
        self.runner_id = runner_id
        self.prefered_unit = "Miles"
        self.prefered_tracking = "Heartrate"
        self.lt1 = 160
        self.lt2 = 167
        self.hard = 173