from sqlalchemy.exc import IntegrityError
from exceptions import ResourceExists
from models import User
from passlib.hash import pbkdf2_sha256 as sha256


class UserRepository:
    @staticmethod
    def create(username: str, avatar_url: str, password: str) -> dict:
        """ Create user """
        result: dict = {}
        try:
            user = User(
                username=username,
                avatar_url=avatar_url,
                password=UserRepository.generate_hash(password),
                active=True
            )
            user.save()
            result = {
                "username": user.username,
                "avatar_url": user.avatar_url,
                "date_created": str(user.date_created),
                "message": "User {} was created".format(user.username)
            }

        except IntegrityError:
            User.rollback()
            raise ResourceExists("user already exists")

        return result

    @staticmethod
    def update_avatar(username: str, avatar_url: str) -> dict:
        """ Update user """
        result: dict = {}
        try:
            user = User.query.filter_by(username=username).first_or_404()
            if user:
                user.avatar_url = avatar_url
                user.save()
                result = {
                    "message": "User updated successfully",
                    "username": user.username,
                    "avatar_url": user.avatar_url,
                    "date_created": str(user.date_created)
                }
            else:
                result = {
                    "message": "User not found. Check username spelling please."
                }
        except IntegrityError:
            User.rollback()
            raise ResourceExists("Update didn't work")

        return result

    @staticmethod
    def delete(username: str) -> dict:
        """ Delete user """
        result: dict = {}
        try:
            user = User.query.filter_by(username=username).first_or_404()
            if user:
                user.active = False
                user.save()
                result = {
                    "username": user.username,
                    "active": user.active,
                    "date_created": str(user.date_created)
                }
            else:
                result = {
                    "message": "User not found. Check username spelling please."
                }
        except IntegrityError:
            User.rollback()
            raise ResourceExists("Deletion didn't work")

        return result

    @staticmethod
    def update_password(username: str, password: str) -> dict:
        """ Update user password """
        result: dict = {}
        try:
            user = User.query.filter_by(username=username).first_or_404()
            if user:
                user.password = UserRepository.generate_hash(password)
                user.save()
                result = {
                    "username": user.username,
                    "message": "Password updated successfully",
                }
            else:
                result = {
                    "message": "User not found. Check username spelling please."
                }
        except IntegrityError:
            User.rollback()
            raise ResourceExists("Update didn't work")

        return result

    @staticmethod
    def get(username: str) -> dict:
        """ Query a user by username """
        user: dict = {}
        user = User.query.filter_by(username=username).first_or_404()
        user = {
            "username": user.username,
            "date_created": str(user.date_created),
            "avatar_url": str(user.avatar_url),
            "password": str(user.password),
            "active": user.active
        }
        return user

    @staticmethod
    def all() -> list:
        users = []
        users = User.query.all()
        return users

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
