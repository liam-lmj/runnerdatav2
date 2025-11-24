from database.database_constants import seconds_to_hours

def format_time_as_hours(total_seconds):
    total_hours = total_seconds * seconds_to_hours
    formatted_time = f"{int(total_hours)}:{round(60 * (total_hours - int(total_hours))):02d}"
    return formatted_time