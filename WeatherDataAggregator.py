# WeatherDataAggregator.py

from datetime import datetime, timedelta

import time

import requests
import pandas as pd
from tqdm import tqdm


class WeatherDataAggregator:
    """
    Klasė, skirta meteorologinių duomenų surinkimui ir apdorojimui.
    """

    def __init__(self, station_code: str, api_url: str):
        """
        Inicijuoja duomenų rinkimo klasę.

        :param station_code: Meteorologinės stoties kodas, duomenims gauti.
        :param api_url: API prieigos adresas.
        """

        self.station_code = station_code
        self.base_url = api_url
        self.df_data = pd.DataFrame()
        self.df_forecast = pd.DataFrame()
        self.stations = {}
        self.places = {}

    def _fetch_metadata(self) -> None:
        """
        Užkrauna stočių ir vietovių metaduomenis iš API.

        :return: None
        """

        url_stations = "https://api.meteo.lt/v1/stations"
        url_places = "https://api.meteo.lt/v1/places"

        try:
            r = requests.get(url_stations)
        except requests.RequestException as e:
            raise HTTPException(status_code=502,
                                detail=f"Nepavyko gauti stočių duomenų: {e}"
                                )

        self.stations = r.json()
        self.stations = {item['code']: item for item in self.stations}

        try:
            r = requests.get(url_places)
        except requests.RequestException as e:
            raise HTTPException(status_code=502,
                                detail=f"Nepavyko gauti vietovių duomenų: {e}"
                                )

        self.places = r.json()
        self.places = {item['code']: item for item in self.places}

    def fetch_last_days(self, num_days: int = 7) -> pd.DataFrame:
        """
        Užkrauna istorinius orų prognozės paskutinių N dienų duomenis.
        Mėgina įkelti duomenis iš lokalaus .parquet failo, jei randa.
        Priešingu atveju siunčia duomenis iš API ir išsaugo juos.

        :param num_days: Kiek dienų N atgal grąžinami duomenis. (numatyta: 7).
        :return: Istorinių orų stebėjimų duomenys.
        """

        if self._station_valid(self.station_code):

            today = datetime.utcnow().date()
            dates = [today - timedelta(days=i) for i in range(num_days)]
            min_date = min(dates).strftime("%Y%m%d")
            max_date = max(dates).strftime("%Y%m%d")
            filename = f"{self.station_code}_{min_date}_{max_date}_data.parquet"

            all_records = []

            try:
                self.df_data = pd.read_parquet(filename)
                print(f"Duomenys įkelti iš failo: {filename}")

            except FileNotFoundError:
                print("Duomenys siunčiami iš api.meteo.lt")

                for date in tqdm(dates, "Parsiųstos dienos"):
                    url = f"{self.base_url}/v1/stations/{self.station_code}/observations/{date}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        data = response.json()
                        records = [
                            {
                                'time': obs.get('observationTimeUtc'),
                                'temperature': obs.get('airTemperature'),
                                'precipitation': obs.get('precipitation'),
                                'relativeHumidity': obs.get('relativeHumidity')
                            }
                            for obs in data.get('observations', [])
                            if 'observationTimeUtc' in obs
                        ]
                        all_records.extend(records)
                    else:
                        print(f"Nepavyko gauti duomenų {date}. Statusas: {response.status_code}")

                    time.sleep(1)

                self.df_data = pd.DataFrame(all_records)

                self.df_data['time'] = pd.to_datetime(self.df_data['time'], utc=True)
                self.df_data.set_index('time', inplace=True)
                self.df_data.to_parquet(filename)

            return self.df_data
        else:
            raise ValueError(f"Stotis {self.station_code=} neegzistuoja.")

    def fetch_forecast(self, code: str) -> pd.DataFrame:
        """
        Užkrauna ilgalaikę orų prognozę pagal vietovės kodą.

        :param code: Vietovės kodas.
        :return: Orų prognozės duomenys.
        """

        if self._code_valid(code):
            url = f"{self.base_url}/v1/places/{code}/forecasts/long-term"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                forecast_records = [
                    {
                        'time': fcast.get('forecastTimeUtc'),
                        'temperature': fcast.get('airTemperature'),
                        'precipitation': fcast.get('totalPrecipitation'),
                        'relativeHumidity': fcast.get('relativeHumidity')
                    }
                    for fcast in data.get('forecastTimestamps', [])
                    if 'forecastTimeUtc' in fcast
                ]
            else:
                print(f"Nepavyko gauti duomenų. Statusas: {response.status_code}")

            self.df_forecast = pd.DataFrame(forecast_records)

            self.df_forecast['time'] = pd.to_datetime(self.df_forecast['time'], utc=True)
            self.df_forecast.set_index('time', inplace=True)

            return self.df_forecast
        else:
            raise ValueError(f"Netinkamas vietovės kodas: {code=}.")

    def _code_valid(self, code: str) -> bool:
        """
        Patikrina ar vietovė egzistuoja metaduomenyse.

        :param code: Vietovės kodas.
        :return: True, jei kodas rastas, False, jei ne.
        """

        if code in list(self.places.keys()):
            return True
        return False

    def _station_valid(self, station: str) -> bool:
        """
        Patikrina ar stoties kodas egzistuoja metaduomenyse.

        :param station: Stoties kodas.
        :return: True, jei kodas rastas, False, jei ne.
        """

        if station in list(self.stations.keys()):
            return True
        return False
