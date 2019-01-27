"""Unit test(s) for 'tasks' module."""

import mock
import pytest

import tasks


@pytest.mark.positive
def test_task_send():
    """Unit test for the send function using mock."""
    with mock.patch('tasks.tasks.send') as send_mock:
        tasks.tasks.send(dict())
        assert send_mock.called

