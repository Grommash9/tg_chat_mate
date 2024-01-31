from copy import deepcopy


class FakeDB:
    """
    This class will be used to mock the database in tests.
    To use you need to pass a list of documents to the constructor.
    Also, use side_effect=FakeDB(documents) when patching.

    :param list documents: a list of documents to be returned.
    """

    def __init__(self, documents, modified_count=1):
        self.documents = documents
        self.modified_count = modified_count

    def __getitem__(self, *args):
        return FakeCollection(deepcopy(self.documents), self.modified_count)


class FakeCollection:
    def __init__(self, documents, modified_count):
        self.documents = documents
        self.modified_count = modified_count

    def __getitem__(self, *args):
        return FakeCollection(self.documents, self.modified_count)

    def aggregate(self, *args):
        return AsyncIterable(self.documents)

    async def find_one(self, *args):
        return self.documents[0]

    async def update_one(self, *args):
        return FakeResult(self.modified_count)

    async def update_many(self, *args):
        return FakeResult(self.modified_count)


class FakeResult:
    def __init__(self, modified_count):
        self.modified_count = modified_count


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


class FakeRedis:
    """
    Use this class to mock redis in tests.

    :param bool exists: this value indicates whether the object exists in
     redis or not.
    """

    def __init__(self, exists=True):
        self.exists_value = exists

    async def exists(self, *args):
        return self.exists_value

    async def close(self):
        pass

    async def set(*args):
        pass
