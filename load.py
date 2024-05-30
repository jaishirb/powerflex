import asyncio

from apps.sprocket import tasks as sprocket_tasks


async def run():
    await sprocket_tasks.load_data_from_json(
        factory_file_path="seed_factory_data.json",
        sprocket_file_path="seed_sprocket_types.json",
    )
    print(f"{'*'*50} Data loaded successfully {'*'*50}")


asyncio.run(run())
