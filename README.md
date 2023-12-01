## Prepare the enviroment
#### 1. make sure python , PIP and docker are installed
#### 2. clone the repo and prepare your environment
```bash
git clone <repository_url>
cd <repository_name>
python -m venv venv
source venv/bin/activate
pip install -r tests/requirements.txt 
```

## Running Tests
#### Use pytest to run the test
```bash
pytest        # to run all tests in order
pytet -n auto # to run all tests in parallel
pytest -m <mark> # to run test that are marked wih some mark ( see available marks in pytest.ini)
pytest -k  <keyword> # Run Tests that Match a Keyword Expression in their name
Example :
pytest -n auto -m sanity  
```


## View Results
##### After running the tests a folder name "results " will be created that contains the junit xml result and data to generate an allure report
```commandline
open the file results/junit-results/test-results.xml
```
#### Allure is an open-source framework designed to create detailed and visual test reports.
#### The allure report contains logs files and can attach the application under tests logs also. ( extra work)

## Generating allure report

#### One Time:
```bash
sudo apt-get update
sudo apt install npm
sudo npm install -g allure-commandline
```
#### After Every Tests Run:
```bash
allure generate ../results/allure-results -o ./results/allure-report
open the file ./results/allure-report/index.html with a web browser

```

## Adding a test
#### adding a test should be very simple , please view the test suite tests/functional/test_my_app.py
#### Test Case Example
```python
@pytest.mark.sanity  # A test mark ndicates that the test of sanity category
@pytest.mark.p1      # A test mark indicates that the test in Priorty 1
def test_reverse_functionality(self,my_app):
    '''
    test basic reverse functionally
    :param my_app: the tested app wrapper module
    '''
    input_string = "The quick brown fox jumps over the lazy dog"
    expected_result = "dog lazy the over jumps fox brown quick The"
    with allure.step("calling and validating reverse"): # allure step that can be seen in allure report
        reverse_response = my_app.reverse_get(in_param=input_string)
        validate_expected_result(response=reverse_response,expected_result=expected_result)
```
```
Note: 
my_app is a fixture the deliveres to the test case an Interface Moudle to a ruuning application on a container
```
