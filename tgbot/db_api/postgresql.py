from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from tgbot.config import load_config

config = load_config(".env")


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            database=config.db.database,
            max_inactive_connection_lifetime=3
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):

        async with self.pool.acquire() as connection:
            connection: Connection()
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

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Zommer_users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    @staticmethod
    def format_args2(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=2)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, telegram_id):
        sql = "INSERT INTO Zommer_users (full_name, telegram_id) VALUES($1, $2) returning *"
        return await self.execute(sql, full_name, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Zommer_users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Zommer_users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_user(self, telegram_id, **kwargs):
        sql = "UPDATE Zommer_users SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, *parameters, execute=True)

    async def count_users(self):
        return await self.execute("SELECT COUNT(*) FROM Zommer_users;", fetchval=True, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Zommer_users", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Zommer_admins (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE, 
        name VARCHAR(255) NULL,
        password VARCHAR(255) NULL,
        level INT NOT NULL,
        regions JSON NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_administrator(self, telegram_id, name, password, level, regions):
        sql = "INSERT INTO Zommer_admins (telegram_id, name, password, level, regions) VALUES ($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, telegram_id, name, password, level, regions, fetchrow=True)

    async def select_all_admins(self):
        sql = "SELECT * FROM Zommer_admins"
        return await self.execute(sql, fetch=True)

    async def select_id_admins(self):
        sql = "SELECT telegram_id FROM Zommer_admins"
        return await self.execute(sql, fetch=True)

    async def select_admin(self, **kwargs):
        sql = "SELECT * FROM Zommer_admins WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_admin(self, telegram_id, **kwargs):
        sql = "UPDATE Zommer_admins SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, *parameters, execute=True)

    async def delete_admin(self, telegram_id):
        await self.execute("DELETE FROM Zommer_admins WHERE telegram_id=$1", telegram_id, execute=True)

    async def drop_admins(self):
        await self.execute("DROP TABLE Zommer_admins", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_members(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Zommer_members (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE, 
        full_name VARCHAR(255) NOT NULL,
        number BIGINT NOT NULL,
        location VARCHAR(255) NOT NULL,
        memder_manager VARCHAR(255) NOT NULL,
        group_of_drugs TEXT NOT NULL, 
        birthday VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_member(self, telegram_id, full_name, number, location, memder_manager, group_of_drugs, birthday):
        sql = "INSERT INTO Zommer_members (telegram_id, full_name, number, location, memder_manager, " \
              "group_of_drugs, birthday) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, telegram_id, full_name, number, location, memder_manager, group_of_drugs, birthday, fetchrow=True)

    async def select_all_members(self):
        sql = "SELECT * FROM Zommer_members"
        return await self.execute(sql, fetch=True)

    async def select_member(self, **kwargs):
        sql = "SELECT * FROM Zommer_members WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_member(self, telegram_id, **kwargs):
        sql = "UPDATE Zommer_members SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, *parameters, execute=True)

    async def count_members(self):
        return await self.execute("SELECT COUNT(*) FROM Zommer_members;", fetchval=True, execute=True)

    async def drop_members(self):
        await self.execute("DROP TABLE Zommer_members", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_records(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Zommer_records (
            id SERIAL PRIMARY KEY,
            state_type VARCHAR(255) NOT NULL,
            telegram_id BIGINT NOT NULL,
            spokesman VARCHAR(255) NOT NULL,
            spokesman_number BIGINT NOT NULL,
            doctor_name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            institution VARCHAR(255) NOT NULL,
            speciality VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            group_of_drugs TEXT NOT NULL,
            doctor_phone BIGINT,
            birthday VARCHAR(255),
            period_capacity TEXT,
            calculation TEXT,
            number_of_drugs INTEGER,
            term VARCHAR(255),
            total_points INTEGER
        );
        """
        await self.execute(sql, fetch=True)

    async def add_record(self, state_type, telegram_id, spokesman, spokesman_number, doctor_name, location,
                         institution, speciality, category, group_of_drugs, doctor_phone, birthday,
                         period_capacity, calculation, number_of_drugs, term, total_points):
        sql = "INSERT INTO Zommer_records (state_type, telegram_id, spokesman, spokesman_number, doctor_name, " \
              "location, institution, speciality, category, group_of_drugs, doctor_phone, birthday, " \
              "period_capacity, calculation, number_of_drugs, term, total_points) " \
              "VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17) returning *"
        return await self.execute(sql, state_type, telegram_id, spokesman, spokesman_number, doctor_name,
                                  location, institution, speciality, category, group_of_drugs, doctor_phone,
                                  birthday, period_capacity, calculation, number_of_drugs, term, total_points,
                                  fetchrow=True)

    async def select_all_records(self):
        sql = "SELECT * FROM Zommer_records"
        return await self.execute(sql, fetch=True)

    async def select_records(self, **kwargs):
        sql = "SELECT * FROM Zommer_records WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_record(self, **kwargs):
        sql = "SELECT * FROM Zommer_records WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_record(self, telegram_id, **kwargs):
        sql = "UPDATE Zommer_records SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, *parameters, execute=True)

    async def count_records(self):
        return await self.execute("SELECT COUNT(*) FROM Zommer_records;", fetchval=True, execute=True)

    async def drop_records(self):
        await self.execute("DROP TABLE Zommer_records", execute=True)