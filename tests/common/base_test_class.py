from .utils.logger import set_logger


class BaseTestClass():
    logger = None

    def setup_class(cls):
        cls.logger = set_logger(cls.__name__)

    def setup_method(self,method):
        self.logger.info("inside setup_method")
        self.logger.info(f"Running test: {method.__name__}")

    def teardown_method(self,method):
        self.logger.info("inside teardown_method")
        self.logger.info(f"inside teardown_method for test: {method.__name__}")

    def teardown_class(cls):
        pass
