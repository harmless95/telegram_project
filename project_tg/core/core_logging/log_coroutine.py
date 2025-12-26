import asyncio


class LoggingTask(asyncio.Task):
    def __init__(self, coro):
        print(f"Start: {coro.__name__}, ID: {id(self)}")
        super().__init__(coro=coro)

    def __repr__(self):
        return f"<Task: {self.get_coro().__name__} - {self._state}"

    def cancel(self, *args, **kwargs):
        print(f"Cancel: {self.get_coro().__name__}")
        super().cancel(*args, **kwargs)


def loging_constructor(loop, coro):
    return LoggingTask(coro=coro)
