from flask import Flask, render_template
from src.production.pv_model import PVPlant
import json

app = Flask(__name__)


@app.route('/')
def index():

    with open("config.json", "r") as file:
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

    hourly_production = [[int(ts.timestamp() * 1000), round(power / 1000, 1)] for ts, power in data.itertuples()]

    context = {
        "total_production_24": round(data["power"].sum() / 1000, 1),
        "production_next_hour": round(data["power"].iloc[1] / 1000, 1),
        "production_actual": round(data["power"].iloc[0] / 1000, 1),
        "production_next_3hours": round(data["power"].iloc[:3].sum() / 1000, 1),
        "hourly_production": hourly_production,
        "index_labels": data.index.strftime("%H:%M").tolist()
    }

    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
