from datetime import datetime
from xml.etree import ElementTree as ET

import requests

MAIN_CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"
CBR_BACKUP_URL = "https://www.cbr-xml-daily.ru/latest.js"


def get_rate_cbr() -> tuple[str, float]:
    try:
        return get_rate_cbr_main()
    except Exception:
        return get_rate_cbr_backup()


def get_rate_cbr_main() -> tuple[str, float]:
    try:
        response = requests.get(MAIN_CBR_URL)
        response.raise_for_status()

        xml_content = response.content
        root = ET.fromstring(xml_content)
        date = root.attrib["Date"]
        rub_rate = None

        for curr in root.findall("Valute"):
            char_code = curr.find("CharCode").text
            if char_code == "KZT":
                value = float(curr.find("Value").text.replace(",", "."))
                rub_rate = 1 / value
                break

        if rub_rate is None:
            raise ValueError("Не удалось найти курс KZT в данных ЦБ РФ")

        return date, rub_rate

    except Exception as e:
        raise Exception(f"Основная функция не сработала: {e}")


def get_rate_cbr_backup() -> tuple[str, float]:
    try:
        response = requests.get(CBR_BACKUP_URL)
        response.raise_for_status()

        data = response.json()
        date = str(data["date"]).split("-")
        date.reverse()
        date = ".".join(date)
        rate = data["rates"]["KZT"]

        return date, rate

    except Exception as e:
        raise Exception(f"Резервная функция не сработала: {e}")


def get_currency_rates_nbrk():
    url = "https://nationalbank.kz/rss/rates_all.xml"
    response = requests.get(url)
    xml_content = response.content
    root = ET.fromstring(xml_content)

    for item in root.findall('.//item'):
        title = item.find('title').text
        if title == 'RUB':
            rub_rate = float(item.find('description').text)
            date = item.find('pubDate').text
            break

    return date, rub_rate


def calculate_average_rate() -> dict:
    data_cbr = get_rate_cbr()
    data_nbrk = get_currency_rates_nbrk()

    average_rate = (data_cbr[1] + data_nbrk['rate']) / 2

    return {
        "cbr_date": data_cbr[0],
        "cbr_rate": data_cbr[1],
        "nbrk_date": data_nbrk["date"],
        "nbrk_rate": data_nbrk["rate"],
        "average_rate": average_rate,
        "calculation_time": datetime.now().strftime("%d.%m.%Y %H:%M")
    }


get_currency_rates_nbrk()
get_rate_cbr()