import json
import logging

from sqlmodel import Session, select

from apps.sprocket import models

logger = logging.getLogger(__name__)


def load_data_from_json(
    factory_file_path: str, sprocket_file_path: str, session: Session
) -> str:
    try:
        with (
            open(factory_file_path, "r") as factory_file,
            open(sprocket_file_path, "r") as sprocket_file,
        ):
            factory_data = json.load(factory_file)
            sprocket_data = json.load(sprocket_file)

        stmt = select(models.InitialDataLoad).where(
            models.InitialDataLoad.loaded == True
        )
        results = session.exec(stmt)
        initial_data_load = results.first()
        if initial_data_load is None:
            for factory in factory_data["factories"]:
                chart_data_info = factory["factory"]["chart_data"]
                chart_data = models.ChartData(
                    sprocket_production_actual=chart_data_info[
                        "sprocket_production_actual"
                    ],
                    sprocket_production_goal=chart_data_info[
                        "sprocket_production_goal"
                    ],
                    time=chart_data_info["time"],
                )
                session.add(chart_data)
                session.flush()
                factory_obj = models.Factory(
                    chart_data_id=chart_data.id, chart_data=chart_data
                )
                session.add(factory_obj)

            for sprocket in sprocket_data["sprockets"]:
                sprocket_obj = models.SPRocket(
                    teeth=sprocket["teeth"],
                    pitch_diameter=sprocket["pitch_diameter"],
                    outside_diameter=sprocket["outside_diameter"],
                    pitch=sprocket["pitch"],
                )
                session.add(sprocket_obj)

            session.add(models.InitialDataLoad(loaded=True))
            session.commit()
            return "Initial data load completed successfully."
        else:
            return "Initial data already loaded. Skipping data load."

    except Exception as e:
        logger.error(f"Error during data loading: {e}")
        raise
