from database.database_constants import seconds_to_hours
import polyline
import folium

def format_time_as_hours(total_seconds):
    total_hours = total_seconds * seconds_to_hours
    formatted_time = f"{int(total_hours)}:{round(60 * (total_hours - int(total_hours))):02d}"
    return formatted_time

def map_html(plot):
    coords = polyline.decode(plot)
    map = folium.Map(location=coords[0], zoom_start=15)
    folium.PolyLine(coords, weight=5).add_to(map)
    map.fit_bounds([min(coords, key=lambda x: x[0]),
              max(coords, key=lambda x: x[0])])
    map_html = map._repr_html_()
    return map_html