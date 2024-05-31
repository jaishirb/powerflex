import json
import logging
from datetime import datetime

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
            sprocket_types = []
            for sprocket in sprocket_data["sprockets"]:
                sprocket_obj = models.SPRocketType(
                    teeth=sprocket["teeth"],
                    pitch_diameter=sprocket["pitch_diameter"],
                    outside_diameter=sprocket["outside_diameter"],
                    pitch=sprocket["pitch"],
                )
                session.add(sprocket_obj)
                session.flush()
                sprocket_types.append(sprocket_obj)

            for factory in factory_data["factories"]:
                chart_data_info = factory["factory"]["chart_data"]

                sprocket_productions = []
                for actual, goal, timestamp in zip(
                    chart_data_info["sprocket_production_actual"],
                    chart_data_info["sprocket_production_goal"],
                    chart_data_info["time"],
                ):
                    sprocket_production = models.SPRocketProduction(
                        sprocket_production_actual=actual,
                        sprocket_production_goal=goal,
                        time=datetime.fromtimestamp(timestamp),
                        sprocket_types=sprocket_types,
                    )
                    session.add(sprocket_production)
                    session.flush()
                    sprocket_productions.append(sprocket_production)

                chart_data = models.ChartData(sprocket_productions=sprocket_productions)
                session.add(chart_data)
                session.flush()

                factory_obj = models.Factory(
                    chart_data_id=chart_data.id, chart_data=chart_data
                )
                session.add(factory_obj)

            session.add(models.InitialDataLoad(loaded=True))
            session.commit()
            return "Initial data load completed successfully."
        else:
            return "Initial data already loaded. Skipping data load."

    except Exception as e:
        logger.error(f"Error during data loading: {e}")
        raise
