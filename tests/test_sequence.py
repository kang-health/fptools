from fptools.sequence import initial, last, pick


def test_initial():
    assert initial((1, 2, 3)) == (1, 2)


def test_last():
    assert last([]) is None
    assert last((1, 2)) is 2


def test_pick():
    assert pick({1, 2}, [1, 2, 3]) == [2, 3]
    assert pick({1, 2}, []) == []
    assert pick({1, 2}, [1, 2]) == [2]
