import json
import logging
from contextlib import contextmanager

from apps.database import database
from apps.sprocket import models

logger = logging.getLogger(__name__)


@contextmanager
def session_scope():
    session = database.SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


async def load_data_from_json(factory_file_path: str, sprocket_file_path: str):
    try:
        with open(factory_file_path, "r") as factory_file, open(
            sprocket_file_path, "r"
        ) as sprocket_file:
            factory_data = json.load(factory_file)
            sprocket_data = json.load(sprocket_file)

        async with session_scope() as session:
            if not session.query(models.InitialDataLoad).filter_by(loaded=True).first():
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
                    factory_obj = models.Factory(chart_data_id=chart_data.id, chart_data=chart_data)
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
                logger.info("Initial data load completed successfully.")
            else:
                logger.info("Initial data already loaded. Skipping data load.")

    except Exception as e:
        logger.error(f"Error during data loading: {e}")
        raise
