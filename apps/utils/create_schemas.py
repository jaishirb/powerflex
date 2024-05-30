from tortoise import Tortoise, run_async

from apps.database.database import connect_to_database


async def main():
    await connect_to_database()
    await Tortoise.generate_schemas(safe=True)

if __name__ == '__main__':
    run_async(main())
