import sqlite3
import os

class Lap:
    def __init__(self, lap_id, lap_dictionary, runner_id, prefered_tracking, lt1, lt2, hard):
        self.lap_id = lap_id
        self.runner_id = runner_id
        self.lap_split = lap_dictionary["split"]
        self.activity_id = lap_dictionary["activity"]["id"]
        self.lap_meters = lap_dictionary["distance"]
        self.lap_seconds = lap_dictionary["moving_time"]        
        self.lap_heartrate_average = lap_dictionary["average_heartrate"]
        self.lap_heartrate_max = lap_dictionary["max_heartrate"]
        self.lap_cadence = lap_dictionary["average_cadence"]

        self.set_lap_type(prefered_tracking, lt1, lt2, hard)

    def set_lap_type(self, prefered_tracking, lt1, lt2, hard):
        if prefered_tracking == "Heartrate":
            value = self.lap_heartrate_average
        elif prefered_tracking == "Pace":
            value = - (self.lap_meters / self.lap_seconds)
            lt1, lt2, hard = -lt1, -lt2, -hard
        else:
            raise ValueError("Invalid value for prefered_tracking")
        
        if value > hard:
            self.lap_type = "Hard"
        elif value > lt2:
            self.lap_type = "LT2"
        elif value > lt1:
            self.lap_type = "LT1"
        else:
            self.lap_type = "Easy"

    def add_to_database(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"""INSERT INTO LAP 
                  VALUES (?,?,?,?,?,?,?,?,?,?)""",
                  (self.lap_id,
                   self.lap_split,
                   self.lap_type,
                   self.activity_id,
                   self.runner_id,
                   self.lap_meters,
                   self.lap_seconds,
                   self.lap_heartrate_average,
                   self.lap_heartrate_max,
                   self.lap_cadence))
        conn.commit()
        conn.close()

    def database_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'runner_data.db')
        return db_path