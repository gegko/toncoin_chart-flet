import time
import flet as ft
from chart import chart, price_data


def chart_container():
    return ft.Container(
        alignment=ft.alignment.bottom_center,
        bgcolor="#f6f9fe",
        shadow=ft.BoxShadow(
            spread_radius=.5,
            blur_radius=.5,
            blur_style=ft.ShadowBlurStyle.OUTER,
            color=ft.colors.BLACK26,
        ),
        width=1000,
        height=275,
        margin=ft.margin.symmetric(horizontal=125),
        border_radius=10,
        content=chart(),
    )


PRICE_TEXT = 'Toncoin price'
PRICE_VALUE = f"${price_data[-1]:.5f}"


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Stack(
            [
                chart_container(),
                ft.Column(
                    left=150,
                    top=20,
                    spacing=5,
                    controls=[
                        ft.Text(PRICE_TEXT, color=ft.colors.GREY_600),
                        ft.Text(
                            PRICE_VALUE,
                            size=20,
                            color=ft.colors.BLACK,
                            weight=ft.FontWeight.BOLD
                        ),
                    ],
                ),
            ],
        )
    )
    line_chart = page.controls[0].controls[0].content
    data_points = line_chart.data_series[0].data_points

    for x, y in enumerate(price_data):
        data_points.append(ft.LineChartDataPoint(x, y))
        if x % 3 == 0:
            line_chart.update()
            time.sleep(0.01)

    page.update()

ft.app(main)
