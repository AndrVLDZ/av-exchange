from datetime import datetime
from xml.etree import ElementTree as ET

import requests

CBR_MAIN_URL = "https://www.cbr.ru/scripts/XML_daily.asp"
CBR_BACKUP_URL = "https://www.cbr-xml-daily.ru/latest.js"
NBK_URL = url = "https://nationalbank.kz/rss/rates_all.xml"


def get_rate_cbr() -> tuple[str, float]:
    try:
        return get_rate_cbr_main()
    except Exception:
        return get_rate_cbr_backup()


def get_rate_cbr_main() -> tuple[str, float]:
    try:
        response = requests.get(CBR_MAIN_URL)
        response.raise_for_status()

        xml_content = response.content
        root = ET.fromstring(xml_content)
        date = root.attrib["Date"]
        rate = None

        for curr in root.findall("Valute"):
            char_code = curr.find("CharCode").text
            if char_code == "KZT":
                value = float(curr.find("Value").text.replace(",", "."))
                rate = 1 / value
                break

        if rate is None:
            raise ValueError("Не удалось найти курс KZT в данных ЦБ РФ")

        return date, rate

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


def get_currency_rates_nbrk() -> tuple[str, float]:
    response = requests.get(NBK_URL)
    xml_content = response.content
    root = ET.fromstring(xml_content)

    for item in root.findall('.//item'):
        title = item.find('title').text
        if title == 'RUB':
            rate = float(item.find('description').text)
            date = item.find('pubDate').text
            break

    return date, rate


def calculate_average_rate() -> dict:
    cbr_date, cbr_rate = get_rate_cbr()
    nbrk_date, nbrk_rate = get_currency_rates_nbrk()

    average_rate = (cbr_rate + nbrk_rate) / 2
    date, time = datetime.now().strftime("%d.%m.%Y %H:%M").split()


    return {
        "cbr_date": cbr_date,
        "cbr_rate": str(cbr_rate).replace(".", ","),
        "nbrk_date": nbrk_date,
        "nbrk_rate": str(nbrk_rate).replace(".", ","),
        "average_rate": str(average_rate).replace(".", ","),
        "calculation_date": date,
        "calculation_time": time,
    }
