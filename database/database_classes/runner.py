import sqlite3
from ..database_constants import deafult_lt2, deafult_hard, deafult_lt1, default_preferred_tracking, default_preferred_unit
import os

class Runner:
    def __init__(self, runner_id):
        self.runner_id = runner_id
        self.get_or_set_attributes()

    def get_or_set_attributes(self):
        existing_attributes = self.get_runner(self.runner_id)
        if existing_attributes:
            self.preferred_unit = existing_attributes["preferred_unit"]
            self.prefered_tracking = existing_attributes["preferred_tracking"]
            self.lt1 = existing_attributes["lt1"]
            self.lt2 = existing_attributes["lt2"]
            self.hard = existing_attributes["hard"]
        else:
            self.preferred_unit = default_preferred_unit
            self.preferred_tracking = default_preferred_tracking
            self.lt1 = deafult_lt1
            self.lt2 = deafult_lt2
            self.hard = deafult_hard
            self.add_to_database()
    
    def dict_factory(self, cursor, row): 
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def database_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))  
        parent_dir = os.path.dirname(current_dir)                  
        db_path = os.path.join(parent_dir, 'runner_data.db')
        return db_path
    
    def get_runner(self, runner):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        conn.row_factory = self.dict_factory

        c = conn.cursor()
        c.execute("SELECT * FROM RUNNER WHERE runner_id = ?", (runner,))
        runner = c.fetchone()
        conn.close

        return runner
    
    def add_to_database(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"""INSERT INTO RUNNER 
                  VALUES (?,?,?,?,?,?)""",
                  (self.runner_id,
                   self.prefered_unit,
                   self.prefered_tracking,
                   self.lt1,
                   self.lt2,
                   self.hard))
        conn.commit()
        conn.close()