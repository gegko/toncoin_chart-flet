import requests
import flet as ft
import pandas as pd
from datetime import datetime, timedelta


from_str = (datetime.today() - timedelta(days=335)) \
    .timestamp().__int__().__str__()
to_str = datetime.today() \
    .timestamp().__int__().__str__()

base_url = 'https://api.coingecko.com/api/v3/'
prices_url = 'coins/the-open-network/market_chart/range/'
headers = {'accept': 'application/json'}
params = {
    "id": "the-open-network",
    "vs_currency": "usd",
    "from": from_str,
    "to": to_str,
}

r = requests.get(
    base_url + prices_url,
    params=params,
    headers=headers
)
yearly_data = r.json()
dt = [
    datetime.fromtimestamp(dt / 1000).date().strftime('%b')
    for dt, _ in yearly_data['prices']
]
data_frame = pd.DataFrame(dt, columns=['month']) \
    .drop_duplicates(keep='first')
date_data = zip(
    [round(i, -1) for i in data_frame.index.to_list()],
    data_frame.month.to_list()
)

labels = [
    ft.ChartAxisLabel(
                    value=value,
                    label=ft.Container(
                        ft.Text(
                            text,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(
                                0.5, ft.colors.ON_SURFACE
                            ),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                )
    for value, text in date_data
]

price_data = [round(price, 5) for _, price in yearly_data['prices']]

def chart():
    return ft.LineChart(
        tooltip_bgcolor=ft.colors.WHITE,
        min_y=int(min(price_data)),
        max_y=int(max(price_data)),
        min_x=0,
        max_x=len(price_data) - 1,
        expand=True,
        bottom_axis=ft.ChartAxis(
            labels=labels,
            labels_size=32,
        ),
        height=130,
        width=1200,
        data_series=[
            ft.LineChartData(
                data_points=None,
                color=ft.colors.BLUE_700,
                curved=True,
                below_line_gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[
                        ft.colors.with_opacity(0.55, ft.colors.BLUE_700),
                        "#f6f9fe"
                    ]
                )
            ),
        ],
    )
