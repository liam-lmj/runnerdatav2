import sqlite3
import os
from database.database_constants import deafult_run_type, meters_to_kilometers, meters_to_miles
from database.database_helper_functions import try_decimal

class Gear:
    def __init__(self, id, active, default_type, shoe, total_distance, unit, runner):
        self.gear_id = id
        self.gear_name = shoe
        self.runner_id = runner

        if unit == "Miles":
            conversion = 1 / meters_to_miles
        elif unit == "Kilometers":
            conversion = 1 / meters_to_kilometers

        self.total_distance = str(try_decimal(total_distance) * try_decimal(conversion))
        self.default_type = default_type
        self.active = active

        if self.gear_exists():
            self.update_existing_gear()
        else:
            self.insert_new_gear()
        
        self.clear_defaults()

    def clear_defaults(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("UPDATE GEAR SET default_type = ? WHERE default_type = ? AND runner_id = ? AND gear_id != ?", 
                    (
                        deafult_run_type,
                        self.default_type,
                        self.runner_id,
                        self.gear_id
                    ))
        conn.commit()
        conn.close()

    def gear_exists(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM GEAR WHERE gear_id = ?", (self.gear_id,))
        gear = c.fetchone()
        conn.close()

        return gear is not None
    
    def insert_new_gear(self):
        db_path = self.database_path()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO gear (runner_id, gear_name, total_distance, active, default_type)
            VALUES (?, ?, ?, ?, ?)
        """, (self.runner_id, self.gear_name, self.total_distance, self.active, self.default_type))
        conn.commit()
        conn.close()
    
    def update_existing_gear(self):
        db_path = self.database_path()

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""UPDATE GEAR SET gear_name = ?, 
                                        total_distance = ?, 
                                        default_type = ?,
                                        active = ?
                    WHERE gear_id = ?""", 
                    (
                        self.gear_name,
                        self.total_distance,
                        self.default_type,
                        self.active,
                        self.gear_id
                    ))
        conn.commit()
        conn.close()

    def database_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'runner_data.db')
        return db_path