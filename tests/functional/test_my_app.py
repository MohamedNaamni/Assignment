import pytest
from ..common.base_test_class import BaseTestClass
from ..common.fixtures.conftest import my_app
from ..common.utils.helper_functions import validate_expected_result
from ..common.utils.logger import set_logger
from http import HTTPStatus
import allure

@pytest.mark.app("my_app")
class TestMyApp(BaseTestClass):
    def __int__(self):
        super(BaseTestClass,self).__init__()
        self.logger = set_logger(self.__class__.__name__)
    @staticmethod
    def _test_basic_reverse_restore(app,input_string="One Two Three",expected_result="Three Two One"):
        '''
        basic validation of restore after reverse , will be reused in many test cases
        :param app: the tested app wrapper module
        :param input_string: the reverse input string
        :param expected_result: the restore expected result
        :return: the restore api GET response
        '''
        with allure.step("calling and validating reverse"):
            reverse_response=app.reverse_get(in_param=input_string)
            validate_expected_result(response=reverse_response, expected_result=expected_result)
        with allure.step("calling and validating restore"):
            restore_response = app.restore_get()
            validate_expected_result(response=restore_response, expected_result=expected_result)
        return restore_response

    @pytest.mark.sanity
    @pytest.mark.p1
    def test_reverse_functionality(self,my_app):
        '''
        test basic reverse functionally
        :param my_app: the tested app wrapper module
        '''
        input_string = "The quick brown fox jumps over the lazy dog"
        expected_result = "dog lazy the over jumps fox brown quick The"
        with allure.step("calling and validating reverse"):
            reverse_response = my_app.reverse_get(in_param=input_string)
            validate_expected_result(response=reverse_response,expected_result=expected_result)

    @pytest.mark.sanity
    @pytest.mark.p1
    def test_restore_functionality(self,my_app):
        '''
        test basic restore functionally
        :param my_app: the tested app wrapper module
        '''
        input_string = "The quick brown fox jumps over the lazy dog"
        expected_result = "dog lazy the over jumps fox brown quick The"
        self._test_basic_reverse_restore(app=my_app,input_string=input_string,expected_result=expected_result)


    @pytest.mark.sanity
    @pytest.mark.p1
    def test_restore_twice(self, my_app):
        '''
        test restore twice after reverse , should return the same result twice
        :param my_app: the tested app wrapper module
        '''
        response_rever_restore = self._test_basic_reverse_restore(my_app)
        with allure.step("calling and validating reverse for the second time"):
            response_restore = my_app.restore_get()
            expected_result = response_rever_restore.json().get('result')
            validate_expected_result(response=response_restore, expected_result=expected_result)

    @pytest.mark.sanityHTTPStatus
    @pytest.mark.p1
    def test_twice_reverse_one_restore(self, my_app):
        '''
        testing twice reverse and one restore, restore should return the latest reversed string
        :param my_app: the tested app wrapper module
        '''
        with allure.step("reverse for the first time"):
            input_string_1 = "Not Relevant"
            my_app.reverse_get(in_param=input_string_1)
        with allure.step("second reverse and restore"):
            self._test_basic_reverse_restore(my_app)

    @pytest.mark.sanity
    @pytest.mark.p1
    def test_restore_after_reverse_twice(self, my_app):
        '''
        testing restore and reverse twice
        :param my_app: the tested app wrapper module
        :return:
        '''
        with allure.step("reverse and restore for the first time"):
            self._test_basic_reverse_restore(app=my_app)
        with allure.step("reverse and restore for the second time"):
            input_string = "The quick brown fox jumps over the lazy dog"
            expected_result = "dog lazy the over jumps fox brown quick The"
            self._test_basic_reverse_restore(app=my_app,input_string=input_string,expected_result=expected_result)


    @pytest.mark.integration
    @pytest.mark.p2
    def test_integration_invalid_input(self,my_app):
        '''
        testing a successful reverse and then a failure reverse and then a restore.
        restore should return the first reverse result
        :param my_app: the tested app wrapper module
        :return:
        '''
        input_string_1 = "One Two Three"
        expected_result = "Three Two One"
        with allure.step("reverse for the first time, should be successful"):
            my_app.reverse_get(in_param=input_string_1)
        with allure.step("reverse for the second time, should fail"):
            response_reverse_empty = my_app.reverse_get(in_param='',expect_fail=True)
            assert response_reverse_empty.status_code == HTTPStatus.BAD_REQUEST
        with allure.step("restore, should return the first reverse result"):
            response_restore = my_app.restore_get()
            validate_expected_result(response_restore,expected_result)

    @pytest.mark.edge_case
    @pytest.mark.p2
    def test_empty_string_reverse(self,my_app):
        '''
        testing a reverse on an empty string,should return BAD_REQUEST response
        :param my_app: the tested app wrapper module
        '''
        response_reverse_empty = my_app.reverse_get(in_param='',expect_fail=True)
        assert response_reverse_empty.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.edge_case
    @pytest.mark.p2
    def test_whitespace_only_string_reverse(self,my_app):
        '''
        testing reverse on a string that contains white spaces only
        should return an empty string
        :param my_app: the tested app wrapper module
        '''
        response_reverse_empty = my_app.reverse_get(in_param=' '*100,expect_fail=True)
        validate_expected_result(response=response_reverse_empty,expected_result="")

    @pytest.mark.negative
    @pytest.mark.p2
    def test_negative_restore(self,my_app):
        '''
        testing restore with no earlier reverse , should return BAD_REQUEST response
        :param my_app: the tested app wrapper module
        '''
        restore_response = my_app.restore_get(expect_fail=True)
        assert restore_response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.negative
    @pytest.mark.p2
    def test_negative_invalid_endpoint(self,my_app):
        '''
        testing invalid input , should return NOT_FOUND response
        :param my_app: the tested app wrapper module
        '''
        invalid_response = my_app.get_template(endpoint='invalid',params={})
        assert invalid_response.status_code == HTTPStatus.NOT_FOUND

