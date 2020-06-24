from pymongo.collection import Collection

class Connection:
    def __init__(self, connection):
        # Set collection instance
        if type(connection) == Collection:
            self.__connection = connection
        else:
            raise Exception("'connection' argument isn't 'Pymongo.Collection'")

    @property
    def _connection(self):
        return self.__connection

    