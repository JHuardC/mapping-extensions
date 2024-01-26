from mapext import FrozenKeys
import pytest

@pytest.fixture
def dummy1():
    # generate from kwargs
    return FrozenKeys(a = 1, b = 2, c = 3)

@pytest.fixture
def dummy2():
    # generate from iterable
    return FrozenKeys((('b', 3), ))

@pytest.fixture
def overlapping_dict():
    # generate a normal dictionary whose keys overlap with dummy1
    return dict(zip(list('abc'), range(1, 4)))

@pytest.fixture
def non_overlapping_dict():
    # generate a normal dictionary whose keys do not overlap with dummy1
    return dict(zip(list('def'), range(3)))

def test_init_using_kwargs():
    try:
        check = dummy1
    except Exception as e:
        assert False, f"Initializing FrozenKeys with kwargs failed: {e}"

def test_init_using_iterable():
    try:
        check = dummy2
    except Exception as e:
        assert False, f"Initializing FrozenKeys with kwargs failed: {e}"

def test_conversion_from_dict(overlapping_dict):
    try:
        check = FrozenKeys(overlapping_dict)
    except Exception as e:
        assert False, f"Converting dict to FrozenKeys failed: {e}"

def test_setitem_new_key(dummy1):
    try:
        dummy1['d'] = 4
    except Exception as e:
        assert False, f'setting a new item in FrozenDict failed: {e}'

def test_setitem_existing_key(dummy1):
    with pytest.raises(KeyError):
        dummy1['c'] = 5

def test_update_overlapping_map(dummy1, overlapping_dict):
    with pytest.raises(KeyError):
        dummy1.update(overlapping_dict)

def test_update_overlapping_kwarg(dummy1):
    with pytest.raises(KeyError):
        dummy1.update(c = 8)

def test_update_overlapping_map_and_kwarg(dummy1, non_overlapping_dict):
    with pytest.raises(KeyError):
        dummy1.update(non_overlapping_dict, **non_overlapping_dict)

def test_update_non_overlapping(dummy1, non_overlapping_dict):
    try:
        # test non-overlapping dict instance
        dummy1.update(non_overlapping_dict, g = 17)
    except Exception as e:
        err_msg = f'update method failed with non-overlapping args/kwargs: {e}'
        assert False, err_msg

def test_or(dummy1, non_overlapping_dict):
    try:
        check = dummy1 | non_overlapping_dict
    except Exception as e:
        err_msg = f'| operation failed: {e}'
        assert False, err_msg

    
def test_or_unsupported_type(dummy1):
    with pytest.raises(TypeError):
        dummy1 | None

def test_ior(dummy1, non_overlapping_dict):
    try:
        dummy1 |= non_overlapping_dict
    except Exception as e:
        err_msg = f'|= operation failed: {e}'
        assert False, err_msg

    
def test_ior_unsupported_type(dummy1):
    with pytest.raises(TypeError):
        dummy1 |= None