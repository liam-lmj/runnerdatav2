from datetime import datetime
from ..database_constants import day_map, valid_activity_types
import sqlite3
import os

class Activity:
    def __init__(self, activity, attributes):
        self.activity_id = activity
        self.exists = self.activity_exitst()
        self.valid = self.valid_activity(attributes)

    def activity_exitst(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"SELECT * FROM ACTIVITY WHERE activity_id = ?", (self.activity_id,))
        exists = c.fetchone()
        conn.close()
        if exists:
            return True
        else:
            return False

    def valid_activity(self, attributes):
        activity_type = attributes["type"]
        return activity_type in valid_activity_types

    def set_activity_attributes(self, attributes):
        self.activity_date = attributes["start_date"]
        self.activity_meters = attributes["distance"]
        self.activity_seconds = attributes["moving_time"]
        self.map_plot = attributes["map"]["summary_polyline"]
        self.heartrate_average = attributes["average_heartrate"]
        self.heartrate_max = attributes["max_heartrate"]
        self.runner_id = attributes["athlete"]["id"]

        self.set_activity_week()

    def set_activity_week(self):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        date = datetime.strptime(self.activity_date, date_format)
        self.week = date.strftime("%W-%Y")
        day_number = date.strftime("%w")
        self.day = day_map[day_number]

    def add_to_database(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"""INSERT INTO ACTIVITY 
                  VALUES (?,?,?,?,?,?,?,?,?,?)""",
                  (self.activity_id,
                   self.activity_date,
                   self.week,
                   self.day,
                   self.runner_id,
                   self.activity_meters,
                   self.activity_seconds,
                   self.map_plot,
                   self.heartrate_average,
                   self.heartrate_max))
        conn.commit()
        conn.close()

    def database_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'runner_data.db')
        return db_path