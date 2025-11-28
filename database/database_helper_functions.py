from database.database_constants import seconds_to_hours, seconds_to_minutes, units_dict, pace_conversion_dict
import polyline
import folium

def lap_data_summary_fields(data):
    total_time = sum(lap.get("lap_seconds", 0) for lap in data)
    formated_total_time = format_time_as_hours(total_time)

    total_distance = sum(lap.get("lap_meters", 0) for lap in data)

    if total_time > 0:
        average_heartrate = round(sum((lap.get("lap_seconds") * lap.get("lap_heartrate_average")) for lap in data) / total_time, 2)
        cadence = round(sum((lap.get("lap_seconds") * lap.get("lap_cadence")) for lap in data) / total_time, 2)
    else:
        average_heartrate = 0
        cadence = 0
    return total_distance, formated_total_time, average_heartrate, cadence
    


def get_lap_types(data):
    return {lap.get("lap_type") for lap in data}

def filter_lap_data(data, lap_type):
    filtered_data = []
    for lap in data:
        if lap.get("lap_type") == lap_type:
            filtered_data.append(lap)
    return filtered_data


def format_time_as_hours(total_seconds):
    total_hours = total_seconds * seconds_to_hours
    formatted_time = f"{int(total_hours)}h {round(60 * (total_hours - int(total_hours))):02d}m"
    return formatted_time

def format_time_as_minutes(total_seconds):
    total_hours = total_seconds * seconds_to_minutes
    formatted_time = f"{int(total_hours)}m {round(60 * (total_hours - int(total_hours))):02d}s"
    return formatted_time

def map_html(plot):
    coords = polyline.decode(plot)
    map = folium.Map(location=coords[0], zoom_start=15)
    folium.PolyLine(coords, weight=5).add_to(map)
    map.fit_bounds([min(coords, key=lambda x: x[0]),
              max(coords, key=lambda x: x[0])])
    map_html = map._repr_html_()
    return map_html

def format_unit(unit):
    return  units_dict.get(unit)

def format_pace(unit, lap_pace):
    conversion = pace_conversion_dict.get(unit, 1)
    converted_lap_pace = conversion / lap_pace
    formatted_lap_pace = f"{int(converted_lap_pace)}:{round(60 * (converted_lap_pace - int(converted_lap_pace))):02d} /{format_unit(unit)}"
    return formatted_lap_pace
