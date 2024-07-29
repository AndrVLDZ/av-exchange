from dataclasses import dataclass
import flet as ft
from currency_rates import calculate_average_rate


@dataclass
class Data:
    cbr_date: str
    cbr_rate: str
    nbrk_date: str
    nbrk_rat: str
    calculation_date: str
    calculation_time: str
    average_rate: str


def get_rates() -> None:
    rates = calculate_average_rate()
    Data.cbr_date = rates["cbr_date"]
    Data.cbr_rate = rates["cbr_rate"]
    Data.nbrk_date = rates["nbrk_date"]
    Data.nbrk_rate = rates["nbrk_rate"]
    Data.calculation_date = rates["calculation_date"]
    Data.calculation_time = rates["calculation_time"]
    Data.average_rate = rates["average_rate"]


def main(page: ft.Page):
    page.title = "Курсы валют"
    page.scroll = "adaptive"


    def update_rates(e):
        get_rates()
        cbr_date_text.value = f"Курс ЦБ РФ на {Data.cbr_date}:"
        cbr_rate_text.value = f"{Data.cbr_rate}"
        nbrk_date_text.value = f"Курс НБРК на {Data.nbrk_date}:"
        nbrk_rate_text.value = f"{Data.nbrk_rate}"
        avg_date_text.value = f"Средний курс на {Data.calculation_date} ({Data.calculation_time}):"
        avg_rate_text.value = f"{Data.average_rate}"
        page.update()


    def copy_to_clipboard(e, text):
        page.set_clipboard(text)


    get_rates()
    cbr_date_text = ft.Text(f"Курс ЦБ РФ на {Data.cbr_date}:")
    cbr_rate_text = ft.Text(f"{Data.cbr_rate}")
    nbrk_date_text = ft.Text(f"Курс НБРК на {Data.nbrk_date}:")
    nbrk_rate_text = ft.Text(f"{Data.nbrk_rate}")
    avg_date_text = ft.Text(f"Средний курс на {Data.calculation_date} ({Data.calculation_time}):")
    avg_rate_text = ft.Text(f"{Data.average_rate}")

    cbr_copy_button = ft.ElevatedButton("Копировать", on_click=lambda e: copy_to_clipboard(e, cbr_rate_text.value))
    nbrk_copy_button = ft.ElevatedButton("Копировать", on_click=lambda e: copy_to_clipboard(e, nbrk_rate_text.value))
    avg_copy_button = ft.ElevatedButton("Копировать", on_click=lambda e: copy_to_clipboard(e, avg_rate_text.value))
    update_button = ft.ElevatedButton("Обновить", on_click=update_rates)

    page.add(
        ft.Row([cbr_date_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([cbr_rate_text, cbr_copy_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([nbrk_date_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([nbrk_rate_text, nbrk_copy_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([avg_date_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([avg_rate_text, avg_copy_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([update_button], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
