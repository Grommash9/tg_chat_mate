from copy import deepcopy


class FakeDB:
    """
    This class will be used to mock the database in tests.
    To use you need to pass a list of documents to the constructor.
    Also, use side_effect=FakeDB(documents) when patching.

    :param list documents: a list of documents to be returned.
    """

    def __init__(self, documents):
        self.documents = documents

    def __getitem__(self, *args):
        return FakeCollection(deepcopy(self.documents))


class FakeCollection:
    def __init__(self, documents):
        self.documents = documents

    def __getitem__(self, *args):
        return FakeCollection(self.documents)

    def aggregate(self, *args):
        return AsyncIterable(self.documents)


class AsyncIterable:
    """
    This class implements the async iterable protocol.
    Use it to mock async iterable objects.

    :param list items: a list of items to be returned.
    """

    def __init__(self, items):
        self.items = items

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.items:
            raise StopAsyncIteration
        return self.items.pop(0)
