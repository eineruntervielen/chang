"""Object Relational Mapper"""
import sqlite3
import abc


class SQLiteManager:
    connection: sqlite3.Connection | None = None

    def dict_factory(cursor, row):
        col_names = [col[0] for col in cursor.description]
        return {key: value for key, value in zip(col_names, row)}

    @classmethod
    def set_connection(cls, settings):
        cls.connection = sqlite3.connect(settings)
        cls.connection.row_factory = cls.dict_factory

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls.connection._get_cursor()
        cursor.execute(query, params)

    def __init__(self, model_class: str) -> None:
        self.model_class = model_class

    def select(self, field_names: None | list[str] = None):
        fields = ", ".join(field_names) if field_names else "*"
        query = f"SELECT {fields} FROM {self.model_class.table_name}"
        cursor = self._get_cursor()
        result = cursor.execute(query).fetchall()
        return list(map(self.model_class, result))

    def insert(self, row: dict):
        fields = ", ".join(row.keys())
        values = ", ".join([f'\'{v}\'' for v in row.values()])
        query = f"INSERT INTO {self.model_class.table_name}({fields}) VALUES ({values})"
        print(query)
        cursor = self._get_cursor()
        cursor.execute(query)
        self.connection.commit()

    def update(self, new_data: dict):
        ...

    def delete(self, attribute, value):
        query = (
            f"DELETE FROM {self.model_class.table_name} WHERE {attribute} = {value};"
        )
        cursor = self._get_cursor()
        cursor.execute(query)
        self.connection.commit()


class MetaModel(type):
    """The MetaModel is necessary because the objects
    property woulnd be passed to the actual Model.
    Also it is responsible for giving ever actual Model a the SQLiteManager.
    """

    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        x.manager_class = SQLiteManager
        return x

    def _get_manager(self):
        return self.manager_class(model_class=self)

    @property
    def objects(self):
        return self._get_manager()


class BaseModel(metaclass=MetaModel):
    table = ""

    def __init__(self, row) -> None:
        """Quick and Dirty if you dont want to have any fields or stuff"""
        for field_name, value in row.items():
            setattr(self, field_name, value)


class Field(abc.ABC):
    """Descriptor and Validator for basic Fields"""

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(self.public_name, value)
        setattr(obj, self.private_name, value)

    @abc.abstractmethod
    def validate(self, public_name, value):
        ...


class NullField(Field):
    def validate(self, public_name, value):
        if not isinstance(value, None):
            raise TypeError(f"Expected {public_name} = {value} to be None")


class IntegerField(Field):
    def validate(self, public_name, value):
        if not isinstance(value, int):
            raise TypeError(f"Expected {public_name} = {value} to be an interger")


class TextField(Field):
    def validate(self, public_name, value):
        if not isinstance(value, str):
            raise TypeError(f"Expected {public_name} = {value} to be a string")
