from mapext import KVDecor
import pytest

@pytest.fixture
def dummykv() -> KVDecor:
    return KVDecor()


@pytest.fixture
def dummyregistered(dummykv):
    @dummykv.register('test')
    class DummyClass:
        """A dummy class for testing KVDecor."""
        pass

    return dummykv


def test_registering(dummykv):
    try:
        @dummykv.register('test')
        class DummyClass:
            """A dummy class for testing KVDecor."""
            pass
    
    except Exception as e:
        assert False, f"Registering failed. Error raised: {e}"


def test_calling(dummyregistered):
    try:
        test = dummyregistered['test']
    except Exception as e:
        assert False, f"Calling failed. Error raised: {e}"


def test_mapping_to_same_key(dummyregistered):
    err_msg = f'test already registered to {dummyregistered["test"]}'
    with pytest.raises(KeyError, match = err_msg):
        @dummyregistered.register('test')
        class AnotherDummyClass:
            pass