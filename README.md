# av-exchange

## About

Flet desktop application for calculating the average exchange rate of tenge to ruble based on the rates from the Central Bank of the Russian Federation and the National Bank of the Republic of Kazakhstan.

The project uses a third-party [API](https://www.cbr-xml-daily.ru/) to get CBR rates as a backup if the official CBR API is unavailable.

## Dependencies

- python 3.14.4
- flet 0.23.2

All dependencies and project configuration can be found in `pyproject.toml` or installed via poetry:

```shell
poetry install
poetry shell
```
