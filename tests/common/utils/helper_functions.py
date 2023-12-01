from .logger import set_logger
logger = set_logger("HelperFunctions")

def validate_response_status_code(response):
    '''
    validates response status code
    '''
    logger.info("validating response has status code 200")
    assert response.ok , (f"status code of the response was {response.status_code} instead of 200,"
                                         f"Reason :{response.json().get('error')}")


def validate_expected_result(response, expected_result):
    '''
    validate response result to and expected result
    '''
    logger.info(f"validating response result is {expected_result}")
    assert response.json().get("result") == expected_result, (f"result of response was {response.json().get('result')}"
                                                              f" instead of {expected_result}")
