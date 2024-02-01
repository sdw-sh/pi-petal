from plant_register.plant import Plant


def plant_update(plant: Plant):
    sensor_valve = (
        plant.sensor
        if plant.sensor == plant.valve
        else f"{plant.sensor} / {plant.valve}"
    )
    return {
        "headline": plant.plant_name,
        "lines": [
            f"Threshold: {plant.irrigation_threshold}",
            f"Measured: {plant.moisture_level}",
            f"Measurement Time:",
            f"{plant.last_moisture_measurement}",
            f"Last Irrigation:",
            f"{plant.last_irrigation_event}",
            f"Sensor / Valve: {sensor_valve}",
        ],
    }
