from rlogger import Log


class Messages:
    def __init__(self, traceback_code: str) -> None:
        self.traceback_code = traceback_code
        self.log = Log("Returned_Messages")
        pass

    def message_return_400(self, message: str = "Bad Request"):
        self.log.add_info(message, self.traceback_code)
        return {"status_code": 400, "message": message}, 400

    def message_return_401(self, message: str = "Unauthorized"):
        self.log.add_info(message, self.traceback_code)
        return {"status_code": 401, "message": message}, 401

    def message_return_403(self, message: str = "Forbidden"):
        self.log.add_info(message, self.traceback_code)
        return {"status_code": 403, "message": message}, 403

    def message_return_404(self, message: str = "Not Found"):
        self.log.add_info(message, self.traceback_code)
        return {"status_code": 404, "message": message}, 404

    def message_return_200(self, message: str = "OK"):
        self.log.add_info(message, self.traceback_code)
        return {"status_code": 200, "message": message}, 200

    def message_return_201(self, message: str = "Created"):
        self.log.add_info(message, self.traceback_code)
        return {"status_code": 201, "message": message}, 201
