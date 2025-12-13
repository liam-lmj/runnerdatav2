import sqlite3
import os

class Plan:
    def __init__(self, week, runner, am_values, pm_values, sessions):
        self.week = week
        self.runner_id = runner
        self.am_values = am_values
        self.pm_values = pm_values
        self.sessions = sessions

        if self.plan_exists():
            self.update_plan()
        else:
            self.add_to_database()
    
    def add_to_database(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"""INSERT INTO PLAN 
                  VALUES (?,?,?,?,?)""",
                  (self.week,
                   self.runner_id,
                   self.am_values,
                   self.pm_values,
                   self.sessions))
        conn.commit()
        conn.close()
    
    def update_plan(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            UPDATE PLAN
            SET week = ?,
                runner_id = ?,
                am_values = ?,
                pm_values = ?,
                sessions = ?
            WHERE week = ? AND runner_id = ?
        """,
        (
            self.week,
            self.runner_id,
            self.am_values,
            self.pm_values,
            self.sessions,
            self.week,        
            self.runner_id
        ))
        conn.commit()
        conn.close()

    def plan_exists(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM PLAN WHERE runner_id = ? AND week = ?", (self.runner_id, self.week))
        plan = c.fetchone()
        conn.close()

        return plan is not None

    def database_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'runner_data.db')
        return db_path