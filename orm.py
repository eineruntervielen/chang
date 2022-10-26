"""
IDEA but in bad https://levelup.gitconnected.com/how-i-built-a-simple-orm-from-scratch-in-python-18b50108cfa3

zu lesen
                        https://speakerdeck.com/lig/your-own-orm-in-python-how-and-why?slide=10
wie gehen metclasses:   https://realpython.com/python-metaclasses/
wie gehen descriptors:  https://docs.python.org/3/howto/descriptor.html
"""
import sqlite3
import abc


class BaseManager:
    connection: sqlite3.Connection | None = None

    @classmethod
    def set_connection(cls, settings):
        cls.connection = sqlite3.connect(settings)

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls.connection._get_cursor()
        cursor.execute(query, params)

    def __init__(self, model_class: str) -> None:
        self.model_class = model_class

    def create(self, rows: list):
        ...
        # query = f"INSERT INTO {self.model_class.table_name} ({}) VALUES {}"

    def read(self, *field_names):
        if field_names:
            fields = ", ".join(field_names)
        else:
            fields = "*"
        query = f"SELECT {fields} FROM {self.model_class.table_name}"
        cursor = self._get_cursor()
        res = cursor.execute(query)
        # get the column names aka attributes of instance
        attributes_list = list(map(lambda x: x[0], res.description))
        result = res.fetchall()
        toreturn = []
        for tup in result:
            toreturn.append(self.model_class(*tup))
        return toreturn

    def update(self, new_data: dict):
        ...

    def delete(self):
        ...


class MetaModel(type):
    """The MetaModel is necessary because the objects
    property woulnd be passed to the actual Model.
    Also it is responsible for giving ever actual Model a the BaseManager.
    """

    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        x.manager_class = BaseManager
        return x

    def _get_manager(self):
        return self.manager_class(model_class=self)

    @property
    def objects(self):
        return self._get_manager()


class BaseModel(metaclass=MetaModel):
    table = ""

    def __init__(self, **row_data) -> None:
        """Quick and Dirty if you dont want to have any fields or stuff"""
        for field_name, value in row_data.items():
            setattr(self, field_name, value)


class Field(abc.ABC):
    """Descriptor and Validator for basic Fields"""

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        # do useful stufpf
        return value

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


class Task(BaseModel):
    table_name = "task"
    task_id = IntegerField()
    label = TextField()

    def __init__(self, task_id, label) -> None:
        self.task_id = task_id
        self.label = label

    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, label={self.label})"

    def __str__(self) -> str:
        return f"Task(id={self.task_id}, label={self.label})"
