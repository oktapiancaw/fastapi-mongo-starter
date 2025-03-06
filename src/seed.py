import argparse


import faker

from src.configs import LOGGER, CustomLogLevel
from src.connections.pmongo import MainMongo
from src.models.post import Post


parser = argparse.ArgumentParser(description="A simple argument parser example.")

parser.add_argument("--num", type=int, required=False, default=10, help="Num data")
args = parser.parse_args()

mongo = MainMongo()
try:
    fake = faker.Faker()
    mongo.connect()
    payloads = []
    for _ in range(args.num):
        payloads.append(
            Post(
                _id=str(fake.uuid4()),
                title=fake.file_name(),
                content=fake.text(),
                published=True,
                status="active",
                createdAt=int(fake.date_time(tzinfo=None).timestamp() * 1000),
                updatedAt=int(fake.date_time(tzinfo=None).timestamp() * 1000),
            ).model_dump(by_alias=True)
        )

    mongo._db["post"].insert_many(payloads)
    LOGGER.log(CustomLogLevel.SUCCESS, f"Success add {args.num} fake data")
except Exception as e:
    LOGGER.exception(e)
finally:
    mongo.close()
