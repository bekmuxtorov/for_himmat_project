from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone_number VARCHAR(255) NOT NULL,
        gender VARCHAR(100) NOT NULL,
        age VARCHAR(20) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_talks(self):
        sql = """
            CREATE TABLE IF NOT EXISTS talks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                links TEXT[] NOT NULL,
                updated_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """
        await self.execute(sql, execute=True)

    async def create_table_questions(self):
        sql = """
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                sender_user_id BIGINT NOT NULL,
                body TEXT NOT NULL,
                answer TEXT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_question(self, sender_user_id, body):
        sql = "INSERT INTO questions (sender_user_id, body) VALUES($1, $2) returning *"
        data = await self.execute(sql, sender_user_id, body, fetchrow=True)
        return data[0] if data else None

    async def select_question(self, **kwargs):
        sql = "SELECT * FROM questions WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        data = await self.execute(sql, *parameters, fetchrow=True)

        return {
            "id": data[0],
            "sender_user_id": data[1],
            "body": data[2],
            "answer": data[3],
            "created_at": data[4],
        } if data else None

    async def update_question_answer(self, answer, question_id):
        sql = "UPDATE questions SET answer=$1 WHERE id=$2"
        return await self.execute(sql, answer, question_id, execute=True)

    async def add_user(self, full_name, username, telegram_id, phone_number, gender, age):
        sql = "INSERT INTO users (full_name, username, telegram_id, phone_number, gender, age) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, full_name, username, telegram_id, phone_number, gender, age, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        data = await self.execute(sql, *parameters, fetchrow=True)

        return {
            "full_name": data[1],
            "username": data[2],
            "telegram_id": data[3],
            "phone_number": data[4],
            "gender": data[5],
            "age": data[6]
        } if data else None

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def count_man_users(self):
        sql = "SELECT COUNT(*) FROM users WHERE gender = 'Erkak';"
        return await self.execute(sql, fetchval=True)

    async def count_woman_users(self):
        sql = "SELECT COUNT(*) FROM users WHERE gender = 'Ayol';"
        return await self.execute(sql, fetchval=True)

    async def count_users_by_time(self):
        sql = "SELECT COUNT(*) FROM users WHERE created_at::DATE = NOW()::DATE;"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)

    async def add_talks(self, title, links, ):
        await self.create_table_talks()
        sql = "INSERT INTO talks (title, links) VALUES($1, $2) returning *"
        return await self.execute(sql, title, links, fetchrow=True)

    async def get_titles(self):
        sql = "SELECT * FROM talks;"
        data = await self.execute(sql, fetch=True)
        titles = {item[0]: item[1].strip() for item in data}
        return titles

    async def get_links(self, **kwargs):
        sql = "SELECT * FROM talks WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        data = await self.execute(sql, *parameters, fetchrow=True)
        return {
            "title": data[1],
            "links": data[2],
            "updated_at": data[3]
        } if data else None

    async def delete_talks(self):
        try:
            await self.execute("DELETE FROM talks WHERE TRUE;", execute=True)
        except Exception as e:
            print(f"Error in delete_talks: {e}")
