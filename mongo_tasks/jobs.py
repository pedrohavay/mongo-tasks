import traceback
import time

from datetime import datetime
from functools import wraps

from mongo_tasks.connection import Connection
from . import ASCENDING, logger

class Jobs(Connection):
    def __init__(self, connection):
        # Parent class
        super().__init__(connection)

        # Module list
        self.services = {}

    def register(self, name):
        def decorator(f):
            # Registering function in list
            self.services[name] = f

            # Adding standlone  mode
            decorator._standlone = f

            # Logging
            logger.info(f"[Jobs] Service Registered: {name}")

            @wraps(f) 
            def task(*args, **kwargs):
                # When function is called, executes normally
                return f(*args, **kwargs)
            return task
        return decorator

    def execute(self, name):
        # Check if name exists
        if name in self.services.keys():
            # Returns module
            return self.services[name]
        else:
            # Returns None
            return None

    @property
    def all_services(self):
        # Return services list
        return [v for v in self.services.keys()]

    def __execute_task(self, task):
        # Get service internally
        service = self.execute(task['service'])

        # Define start timestamp
        started_at = datetime.now().isoformat()

        # Check if service exists
        if service is not None:
            try:
                # Execute service
                result = service(*task['arguments'])
                result = result if type(result) == dict else {}
            except Exception as error:
                # Logging
                logger.error(f"[Jobs] Error Task: {str(task['_id'])}")

                # Get traceback
                traceback_str = "\n".join(traceback.format_tb(error.__traceback__))

                # Adding string from exception
                traceback_str += f"\n[Main Error]{str(error)}"

                # Get exception not handled
                result = {
                    "status": "error",
                    "error": traceback_str,
                    "result": None
                }

            # Define end timestamp
            ended_at = datetime.now().isoformat()

            # Mount payload
            payload = {
                "status": "success",
                "started_at": started_at,
                "ended_at": ended_at,
                **result
            }
        else:
            # Mount payload
            payload = {
                "status": "unknown_service",
                "ended_at": started_at
            }

        # Update task
        self._connection.update_one({
            "_id": task['_id']
        }, {
            "$set": payload
        })


    def run(self, priority=None):
        # Logging
        logger.info("[Jobs] Starting tasks listener...")

        # Init sort
        sort = [("_id", ASCENDING)]

        # Check if priority is defined
        if priority is not None:
            # Define priority sort
            sort.append(("priority", priority))

        # Try for detect stop
        try:
            # Init loop for listener
            while True:
                # Get all task pending
                tasks = self._connection.find({
                    "status": "pending"
                }).sort(sort)

                # Iterate in each task
                for task in tasks:
                    # Logging
                    logger.info(f"[Jobs] Started task: {str(task['_id'])}")
                    
                    # Run task
                    self.__execute_task(task)

                    # Logging
                    logger.info(f"[Jobs] Ended task: {str(task['_id'])}")

                # Wait 1 second
                time.sleep(1)
        except KeyboardInterrupt:
            # Logging
            logger.info("[Jobs] Stopping tasks listerner...")
        except Exception as error:
            # Logging
            logger.error("[Jobs] Stopping tasks listerner...")

            # Get traceback
            traceback_str = "\n".join(traceback.format_tb(error.__traceback__))
            
            # Open error log
            error_file = open("./error.log", "a")

            # Write
            error_file.write(f"\n\nError Timestamp: {datetime.now().isoformat()}\n")
            error_file.write(traceback_str)
