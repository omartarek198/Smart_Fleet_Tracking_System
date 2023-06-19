import flask_login
from dataclasses import dataclass
from typing import Optional
import mysql.connector

import flask_login


@dataclass
class User(flask_login.UserMixin):
    id: int
    user_type: str 
    email: str
    passwd: str
    fname: str
    lname: str

    @staticmethod
    def get(id: int, connection: mysql.connector.MySQLConnection) -> "User":
        cursor = connection.cursor()
        cursor.execute(
            f"""
            SELECT *
            FROM user
            WHERE user_id=%s
        """, (id,),
        )
        params = cursor.fetchone()
        return User(*params)

    def insert(self, connection: mysql.connector.MySQLConnection) -> "User":
        cursor = connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO user (user_type, email, passwd, fname, lname)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (self.user_type, self.email, self.passwd, self.fname, self.lname),
        )
        connection.commit()

        cursor.execute(
            """
            SELECT LAST_INSERT_ID()
        """
        )
        id = cursor.fetchone()[0]

        self.id = id
        return self

    def update(self, connection: mysql.connector.MySQLConnection) -> "User":
        cursor = connection.cursor()
        cursor.execute(
            f"""
            UPDATE user
            SET email=%s, passwd=%s, fname=%s, lname=%s
            WHERE user_id=%s
        """,
            (self.email, self.passwd, self.fname, self.lname, self.id),
        )
        connection.commit()
        return self

    @staticmethod
    def get_by_email_and_password(
        email: str, password: str, connection: mysql.connector.MySQLConnection
    ) -> Optional["User"]:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT user_id, email, passwd, fname, lname
            FROM User
            WHERE email=%s AND passwd=%s
        """,
            (email, password),
        )
        params = cursor.fetchone()
        if params is None:
            return None
        return User(*params)

    @staticmethod
    def get_by_email(
        email: str, connection: mysql.connector.MySQLConnection
    ) -> Optional["User"]:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT user_id, email, passwd, fname, lname
            FROM User
            WHERE email=%s
        """,
            (email,),
        )
        params = cursor.fetchone()
        if params is None:
            return None
        return User(*params)


@dataclass
class Driver(User):
    bus: "Bus"
    pass


class Admin(User):
    pass


class Passenger(User):
    pass


@dataclass
class Model:
    name: str
    emission_rate: float
    fuel_rate: float

    @staticmethod
    def get(id: int, connection: mysql.connector.MySQLConnection) -> Optional["Model"]:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            SELECT name, emission_rate, fuel_rate
            FROM model
            WHERE model_id=%s
        """,
            (id,),
        )
        params = cursor.fetchone()
        return Model(*params) if params else None

    def insert(self, connection: mysql.connector.MySQLConnection) -> None:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO model (name, emission_rate, fuel_rate)
            VALUES (%s, %s, %s)
        """,
            (self.name, self.emission_rate, self.fuel_rate),
        )
        connection.commit()

    def update(self, connection: mysql.connector.MySQLConnection) -> None:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            UPDATE model
            SET name=%s, emission_rate=%s, fuel_rate=%s
            WHERE model_id=%s
        """,
            (self.name, self.emission_rate, self.fuel_rate, self.id),
        )
        connection.commit()


@dataclass
class Bus:
    model: Model
    driver: Optional[Driver]
    capacity: int

    @staticmethod
    def get(id: int, connection: mysql.connector.MySQLConnection) -> "Bus":
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT model_id, driver_id, n_passengers
            FROM bus
            WHERE bus_id=%s
        """,
            (id,),
        )
        (model_id, driver_id, capacity) = cursor.fetchone()
        model = Model.get(model_id, connection)
        driver = User.get(driver_id, connection)
        return Bus(model, driver, capacity)

    def insert(self, connection: mysql.connector.MySQLConnection) -> None:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO bus (model_id, driver_id, n_passengers)
            VALUES (%s, %s, %s)
        """,
            (self.model.id, self.driver.id, self.capacity),
        )
        connection.commit()

    def update(self, connection: mysql.connector.MySQLConnection) -> None:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            UPDATE bus
            SET model_id=%s, driver_id=%s, n_passengers=%s
            WHERE bus_id=%s
        """,
            (self.model.id, self.driver.id, self.capacity, self.id),
        )
        connection.commit()
