import sqlite3
from rlogger import Log
from sqlalchemy.orm import sessionmaker, relationship, Query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

DATABASE_NAME = "database.db"


engine = create_engine(f"sqlite:///{DATABASE_NAME}", echo=False)
Base = declarative_base()
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from utils import Utilities

import uuid


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    description = Column(String)


class Claims(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    description = Column(String)
    active = Column(Boolean)


class UserClaims(Base):
    __tablename__ = "user_claims"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), primary_key=True)


Base.metadata.create_all(engine)


class Database:
    def __init__(self):
        self.session = sessionmaker(bind=engine)()
        self.utilities = Utilities()
        self.log = Log("Database")
        self.traceback_code = uuid.uuid4()

    def add_role(self, description: str) -> bool:
        if description == "":
            self.log.add_warning("Description is empty", self.traceback_code)
            self.log.add_debug(f"DESCRIPTION: {description}", self.traceback_code)
            return False
        else:
            try:
                roles = Roles(description=description)
                self.session.add(roles)
                self.session.commit()
                self.log.add_info("Role added successfully", self.traceback_code)
                status = True
            except Exception as e:
                self.session.rollback()
                self.session.flush()
                self.log.add_error("Error adding role", self.traceback_code)
                self.log.add_debug(f"EXCEPTION ERROR {e}", self.traceback_code)
                status = False
            finally:
                self.session.close()
                self.log.add_info("Session closed", self.traceback_code)
                return status

    def add_claim(self, description: str) -> bool:
        if description == "":
            self.log.add_warning("Description is empty", self.traceback_code)
            self.log.add_debug(f"DESCRIPTION: {description}", self.traceback_code)
            return False
        else:
            try:
                claims = Claims(description=description, active=True)
                self.session.add(claims)
                self.session.commit()
                self.log.add_info("Claim added successfully", self.traceback_code)
                status = True
            except Exception as e:
                self.session.rollback()
                self.session.flush()
                self.log.add_error("Error adding claim", self.traceback_code)
                self.log.add_debug(f"EXCEPTION ERROR {e}", self.traceback_code)
                status = False
            finally:
                self.session.close()
                self.log.add_info("Session closed", self.traceback_code)
                return status

    def add_user(self, name: str, email: str, password: str, role_id: int) -> bool:
        if name == "" or email == "" or role_id == "":
            self.log.add_warning("One or more fields are empty", self.traceback_code)
            self.log.add_debug(
                f"NAME: {name} EMAIL: {email} ROLE_ID: {role_id}",
                self.traceback_code,
            )
            return False
        else:
            try:
                users = Users(
                    name=name,
                    email=email,
                    password=password,
                    role_id=role_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                self.session.add(users)
                self.session.commit()
                self.log.add_info("User added successfully", self.traceback_code)
                status = True
            except Exception as e:
                self.session.rollback()
                self.session.flush()
                self.log.add_error("Error adding user", self.traceback_code)
                self.log.add_debug(f"EXCEPTION ERROR {e}", self.traceback_code)
                status = False
            finally:
                self.session.close()
                self.log.add_info("Session closed", self.traceback_code)
                return status

    def get_user_role(self, user_id: int) -> int:
        if user_id == "":
            self.log.add_warning("User ID is empty", self.traceback_code)
            self.log.add_debug(f"USER_ID: {user_id}", self.traceback_code)
            return False
        else:
            try:
                user = self.session.query(Users).filter_by(id=user_id).first()
                self.log.add_info(
                    "User role retrieved successfully", self.traceback_code
                )
                msg = {"status_code": 200, "data": user.role_id}
            except Exception as e:
                self.session.rollback()
                self.session.flush()
                self.log.add_error("Error retrieving user role", self.traceback_code)
                self.log.add_debug(f"EXCEPTION ERROR {e}", self.traceback_code)
                msg = {"status_code": 404, "data": None}
            finally:
                self.session.close()
                self.log.add_info("Session closed", self.traceback_code)
                return msg

    def question_query(self, user_name):

        query = (
            self.session.query(Users, Roles, Claims)
            .filter(Users.name == user_name)
            .filter(Users.role_id == Roles.id)
            .filter(UserClaims.user_id == Users.id)
            .filter(UserClaims.claim_id == Claims.id)
            .all()
        )

        return query
