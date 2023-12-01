import requests, time
from ..utils.helper_functions import validate_response_status_code
from .logger import set_logger


class MyAppAPI(object):
    def __init__(self, app_url: str):
        '''
        Init an API Wrapper object to work with a given running container that runs my app
        :param app_url: the app url of the application that runs on the container, for example localhost:5000
        '''
        self.app_url = app_url
        self.logger = set_logger(self.__class__.__name__)

    def get_template(self, endpoint: str, params: dict = None):
        '''
        A template for invoking a baisc HTTP get request of our app
        :param endpoint: endpoint name
        :param params: Request Params as a dict
        :return:
        '''
        self.logger.debug(f"performing HTTP GET request to f'{self.app_url}/{endpoint}' with param {params}")
        response = requests.get(f'{self.app_url}/{endpoint}', params=params)
        return response

    def wait_for_app_service_to_up(self, timeout_sec:int=5):
        '''
        waits for the application flask service to be ready and running on the docker container.
        by checking the status endpoint
        :param timeout_sec: the time to wait for app to be ready
        :return: Exception if the app is still down after the timeout_sec
        '''
        self.logger.info(f"waiting for service to up within {timeout_sec}  seconds")
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            response = self.get_template(endpoint='status')
            try:
                validate_response_status_code(response)
                self.logger.info("service is up.")
                return
            except Exception:
                pass
            time.sleep(0.1)  # Wait for a short interval before checking again
        self.logger.info(f"service is still down after {timeout_sec} seconds.")
        raise Exception(f"app is not up and running status within {timeout_sec} seconds")

    def reverse_get(self, in_param: str, expect_fail: bool = False):
        '''
        simple wrapper to invoke the reverse GET API
        :param in_param: the "in" param that is passed to the reverse API
        :param expect_fail: when True we do not check that teh response status_code is OK
        :return: the response of the API Call
        '''
        self.logger.info(f"Invoking the reverse api with in param {in_param}")
        response = self.get_template(endpoint='reverse', params={'in': in_param})
        if not expect_fail:
            validate_response_status_code(response)
        return response

    def restore_get(self, expect_fail: bool = False):
        '''
        simple wrapper for the restore GET API
        :param expect_fail: expect_fail: when True we do not check that teh response status_code is OK
        :return: the response of the API Call
        '''
        self.logger.info(f"Invoking the restore api")
        response = self.get_template(endpoint='restore')
        if not expect_fail:
            validate_response_status_code(response)
        return response
