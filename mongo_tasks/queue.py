from mongo_tasks.connection import Connection
from . import logger, ASCENDING, LOW

class Queue(Connection):
    def __init__(self, connection):
        # Parent class
        super().__init__(connection)

    def add_in_queue(self, service, arguments=(), priority=LOW , **kwargs):
        # Check arguments
        if type(arguments) != tuple:
            # Logging
            logger.error("[Queue] 'argument' isn't a tuple")

            # Raise error
            raise Exception("'argument' isn't a tuple")

        # Mount the payload
        payload = {
            "status": "pending",
            "service": service,
            "priority": priority,
            "arguments": [*arguments]
        }

        # Add document in connection
        task = self._connection.insert_one(payload)

        # Logging
        logger.info(f"[Queue] Task added: {task.inserted_id}")

        # Return inserted '_id'
        return str(task.inserted_id)

    def get_queue(self, status=None, priority=None, sort_by=ASCENDING, limit=0, offset=0):
        # Init sort
        sort = [("_id", sort_by)]

        # Init query
        query = {}

        # Check status
        if status is not None:
            # Add status in query
            query['status'] = status

        # Check priority
        if priority is not None:
            # Add priority in query
            query['priority'] = priority

        # Create parser function
        def parse(doc):
            # Transform oid to str
            doc['_id'] = str(doc['_id'])

            # Returns doc
            return doc

        # Get all tasks in queue
        tasks = [parse(doc) for doc in self._connection.find(query).sort(sort).skip(offset).limit(limit)]

        # Returns tasks
        return tasks
