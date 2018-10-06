# import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,'flibia_aac/app'))

import pytest

from flibia_aac.app import create_app


@pytest.yield_fixture(scope='session')
def test_client():
    app = create_app('testing')

    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()
