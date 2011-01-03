from .abstract import X10Controller

__author__ = "fabriceb@theodo.fr"
__date__ = "2010-12-31"

class MockX10Controller(X10Controller):
    """
    Mock class to be able to test python code dependent on a python-x10 controller

    # Create a mock controller and use ack or do
    >>> mock_controller = MockX10Controller(None)
    >>> mock_controller.ack()
    True
    >>> mock_controller.do('ON', 'A1')
    """

    def ack(self):
        return True

    def do(self, function, x10addr=None, amount=None):
        pass
