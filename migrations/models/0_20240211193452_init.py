from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chat" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL,
    "watched" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "channel" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL,
    "chat_id" BIGINT REFERENCES "chat" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "autopost" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT,
    "start_date" DATE,
    "end_date" DATE,
    "chat_id" BIGINT NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "postdate" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "time" TIMETZ,
    "post_id" INT NOT NULL REFERENCES "autopost" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "userchat" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "warnings" INT NOT NULL  DEFAULT 0,
    "admin" BOOL NOT NULL  DEFAULT False,
    "chat_id" BIGINT NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_channel" (
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "channel_id" BIGINT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
