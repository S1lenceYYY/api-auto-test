from framework import Context
import pytest
@pytest.fixture(scope="class")
def serial_context():
    context = Context()
    yield context
    context.data.clear()


@pytest.fixture(scope="function")
def parallel_context():
    context = Context()
    yield context
    context.data.clear()