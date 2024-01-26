from mapext.descriptorregister import KVExtensionsRegistry
from mapext.descriptorregister._descriptorregister import KVDescriptor
import pytest
from dotenv import find_dotenv
from typing import Final
from pathlib import Path
import pickle
from os import makedirs

TEST_PATH: Final[Path] = Path(find_dotenv()).parent.joinpath('test')


@pytest.fixture
def emptydummyregistry():
    return KVExtensionsRegistry()


def test_build_descriptor_type(emptydummyregistry):
    assert isinstance(emptydummyregistry.build_descriptor(), KVDescriptor),\
        "KVExtentionsRegistry instance's build_descriptor method did not "\
        "return a KVDescriptor"


@pytest.fixture
def dummykey():
    return 'test'


registry = KVExtensionsRegistry()

@registry.register('test')
class DummyClass:
    pass


class HasDescriptor:
    test = registry.build_descriptor()

    def __init__(self, test: str):
        self.test = test


@pytest.fixture
def instance_with_kvdescriptor(dummykey):
    return HasDescriptor(dummykey)


def test_wrong_arg_passed_to_descriptor():
    wrong_arg = 'wrong_arg'
    with pytest.raises(KeyError, match = f"{wrong_arg} is unregistered"):
        check = HasDescriptor(wrong_arg)


def test_arg_passed_retrieval(instance_with_kvdescriptor, dummykey):
    assert (val := instance_with_kvdescriptor.test) == dummykey,\
        f"test attribute does not return the correct value: {val}"


def test_descriptor_adds_private_attribute(instance_with_kvdescriptor):
    assert hasattr(instance_with_kvdescriptor, '_test'),\
        'KVDescriptor has not added a protected version of the test attribute.'


def test_correct_arg_passed_returns_expected_class(instance_with_kvdescriptor):
    extension_class = getattr(instance_with_kvdescriptor, '_test')
    assert extension_class is DummyClass, f'KVDescriptor did not '\
        f'provide the correct extension class: _test returned '\
        f'{extension_class}'
    

def test_persistency(instance_with_kvdescriptor):
    tmpdir = 'temp',
    filename = 'temp_inst_w_kvdesc.pkl'
    try:
        if not (temp_path := TEST_PATH.joinpath(*tmpdir)).exists():
            makedirs(temp_path)

        with open((file_path := temp_path.joinpath(filename)), 'wb') as tmp:
            pickle.dump(instance_with_kvdescriptor, tmp)

        with open(file_path, 'rb') as tmp:
            loaded = pickle.load(tmp)

    except Exception as e:
        assert False, f"test failed due to following exception raised: {e}"

    try:
        extension_class = getattr(loaded, '_test', None)

        assert isinstance(extension_class, type), f'Extension class not '\
            f'returned correctly: {extension_class}'
        
        assert extension_class is DummyClass, f'Extension class returned is '\
            f'not the DummyClass: {extension_class}'
    
    finally:
        
        # cleanup temporary resources
        file_path.unlink()
