"""
This script contains the functions that model the photovoltaic production using the PVGIS tool
(https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis_en).
For the project, the APIs have been developed
and stored in the pvlib library (https://pvlib-python.readthedocs.io/en/stable/_modules/pvlib/iotools/pvgis.html), which
are used in this script.
"""

from pvlib.pvsystem import PVSystem, FixedMount, Array
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from src.api.open_weather import get_weather_forecast
import pandas as pd
import datetime


class PVPlant:
    """
    Class that models the Photovoltaic Plant
    """

    def __init__(self):
        self.location = None
        self.pvsystem = None
        self.array_list = []
        self.model_chain = None
        self.weather = None
        self.pv_production = None

    def get_location(self, latitude: float, longitude: float):
        """
        Method that gets the location of the PVPlant. It initializes the Location object of the 'pvlib' library.
        :param latitude: the latitude of the plant.
        :param longitude: the longitude of the plant.
        :return:
        """

        self.location = Location(latitude=latitude, longitude=longitude)

    def get_array(self, surface_tilt: float, surface_azimuth: float, module_type: str, pdc0_module: float,
                  gamma_pdc_module: float, module_per_string: int, strings: int):

        """
        Define an array of the class Array from the 'pvlib' library. It appends this object to the array_list, which is
        an attribute of the PVPlant object.
        :param surface_tilt: Angle of tilt of the modules
        :param surface_azimuth: Angle of azimuth of the modules
        :param module_type: Material of the module sandwich: possible choices are 'glass_glass' or 'polymer_glass'.
        :param pdc0_module: Power of the module at 1000 W/m2.
        :param gamma_pdc_module: Temperature coefficient in °C^-1- From -0.002 to -0.005.
        :param module_per_string: Number of modules for each string.
        :param strings: Number of strings.
        """

        self.array_list.append(Array(
            mount=FixedMount(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth),
            name=f"array{len(self.array_list)}",
            module_type=module_type,
            module_parameters={"pdc0": pdc0_module, "gamma_pdc": gamma_pdc_module},
            temperature_model_parameters=TEMPERATURE_MODEL_PARAMETERS["pvsyst"]["freestanding"],
            modules_per_string=module_per_string,
            strings=strings
        ))

    def get_pvsystem(self, pdc0_inverter: float):
        """
        Initializes the PVSystem object, which contains the information about the arrays and the inverter.
        :param pdc0_inverter: Nominal power of the inverter
        :return:
        """

        self.pvsystem = PVSystem(
            arrays=self.array_list,
            inverter_parameters={"pdc0": pdc0_inverter}
        )

    def get_modelchain(self):
        """
        Defines the model_chain.
        """
        self.model_chain = ModelChain(
            location=self.location,
            system=self.pvsystem,
            aoi_model='physical',
            spectral_model='no_loss'
        )

    def get_weather_forecast(self, forecasting_days: int = 1):
        """
        Gets the weather forecasts from the APIs
        :param forecasting_days: Number of days to forecast
        """
        start_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        end_time = start_time + datetime.timedelta(days=forecasting_days)
        start_hour = start_time.strftime("%Y-%m-%dT%H:%M")
        end_hour = end_time.strftime("%Y-%m-%dT%H:%M")
        self.weather = get_weather_forecast(self.location.latitude, self.location.longitude, start_hour, end_hour)
        self.weather.set_index("timestamp", inplace=True)
        self.weather.index = pd.to_datetime(self.weather.index)

    def get_pvplant_production(self):
        """
        Obtains the hourly annual dataframe with the photovoltaic plant production in the "power" column.
        """

        if (self.location is not None and self.pvsystem is not None and self.model_chain is not None and
                self.weather is not None):
            self.model_chain.run_model(self.weather)
            self.pv_production = pd.DataFrame(data=self.model_chain.results.ac.astype(float))
            self.pv_production.columns = ["power"]
            self.pv_production.index = pd.to_datetime(self.pv_production.index)


if __name__ == "__main__":
    import json

    # Load the configuration file
    with open("../../config.json", "r") as file:
        config = json.load(file)

    pv_plant = PVPlant()
    pv_plant.get_location(latitude=config["latitude"], longitude=config["longitude"])

    for array in config["array_list"]:
        pv_plant.get_array(**array)

    pv_plant.get_pvsystem(pdc0_inverter=config["pdc0_inverter"])
    pv_plant.get_modelchain()
    pv_plant.get_weather_forecast()
    pv_plant.get_pvplant_production()
    data = pv_plant.pv_production

