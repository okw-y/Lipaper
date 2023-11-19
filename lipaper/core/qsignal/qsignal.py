import typing


class QSignal(object):
    def __init__(self) -> None:
        self._methods = []

    def connect(self, function: typing.Callable) -> None:
        self._methods.append(function)

    def emit(self, argument: typing.Any = None) -> None:
        for function in self._methods:
            try:
                if argument:
                    function(argument)
                else:
                    function()
            except Exception as _:
                del _
