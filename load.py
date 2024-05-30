from sqlmodel import Session

from apps.database import database
from apps.sprocket import tasks as sprocket_tasks


def run() -> None:
    with Session(database.engine) as session:
        log = sprocket_tasks.load_data_from_json(
            factory_file_path="data/seed_factory_data.json",
            sprocket_file_path="data/seed_sprocket_types.json",
            session=session,
        )
        print(f"{'*'*50} {log} {'*'*50}")


run()
