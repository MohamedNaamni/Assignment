import pytest
from subprocess import Popen, PIPE
import time, os
import requests
import docker
from ..utils.my_app_utils import MyAppAPI
import socket
from ..utils.logger import set_logger

logger = set_logger("Conftest")


def wait_for_container_up(container, timeout_sec=5):
    '''
    waits for the container to br in arunning state
    :return:
    '''
    logger.info(f"waiting to container to be ready within {timeout_sec} seconds")
    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        container.reload()
        if container.status == "running":
            return
        time.sleep(0.2)  # Wait for a short interval before checking again
    raise Exception(f"Container Did not manage to be in running status within {timeout_sec} seconds")


def find_available_port():
    '''
    finds an available port to be allocated for the test container
    useful when running in parallel
    '''
    logger.info(f"finding an available port")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    _, port = s.getsockname()
    s.close()
    logger.info(f"port found is {port}")
    return port


def create_a_container(request):
    '''
    finds the dockerfile relevant to our app under test
    builds a docker image
    creates a container from it with exposing the app port to random viable port on our machine
    :param request: contains the "app" mark that help us locate the matching docker file for our app in the repo
    :return: container python object and the assigned port
    '''
    logger.info(f"creating a container for the test")
    app_marker = request.node.get_closest_marker("app")
    if not app_marker:
        raise ValueError("Test is missing the 'my_app' marker.")

    app_name = app_marker.args[0]
    docker_build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', app_name))


    # Build the Docker image
    logger.info(f"Building a docker image from the docker file at {docker_build_path}")
    client = docker.from_env()
    image, _ = client.images.build(path=docker_build_path, tag=app_name)

    # Run the Docker container
    logger.info(f"Run the Docker container")
    port = find_available_port()
    container = client.containers.run(image, detach=True, ports={'5000': port})
    time.sleep(1)
    wait_for_container_up(container)
    return container, port


@pytest.fixture
def my_app(request):
    '''
    the most important fixture.
    this fixture assure that every test case that uses it will have a container running the
    APP under test ready before the test star and will be given an python object as a parameter to
    simple communicate with the container Application API.
    this will also assure to delete the container after the test is finished.
    '''
    logger.info(f"inside my_app fixture")
    container, port = create_a_container(request)
    my_app_url = f'http://localhost:{port}'
    my_app_api = MyAppAPI(my_app_url)
    my_app_api.wait_for_app_service_to_up()
    logger.info(f"container and app is ready at {my_app_url}")
    yield MyAppAPI(my_app_url)
    logger.info(f"Deleting the container")
    container.stop()
    container.remove()
