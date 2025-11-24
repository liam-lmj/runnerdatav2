import json
import plotly
import plotly.express as px
import pandas as pd
from database.database_constants import lap_types

def weekly_mileage_type_pie(data):
    pie_df = pd.DataFrame({
        'Types': ['Easy', 'LT1', 'LT2', 'Hard'],
        'Distance': [sum(activity.get(lap_type, 0) for activity in data) for lap_type in lap_types]
    })
    fig_pie = px.pie(pie_df, names="Types", values="Distance")
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    pie_chart = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    return pie_chart   