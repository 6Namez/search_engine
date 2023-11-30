import search


def test_string_match__matches():
    assert search.string_match(document='red and blue', query='red') is True


def test_string_match__dont_match():
    assert search.string_match(document='yellow and blue', query='red') is False


def test_string_match__strange_match():
    assert search.string_match(document='predict color', query='red') is True


def test_boolean_term_match__matches():
    assert search.boolean_term_match(document='red and blue', query='red') is True


def test_boolean_term_match__dont_match():
    assert search.boolean_term_match(document='yellow and blue', query='red') is False


def test_boolean_term_match__fixes_strange_match():
    assert search.boolean_term_match(document='predict color', query='red') is False


def test_search():
    assert search.search(query='red', documents=['blue and yellow', 'red and green']) == ['red and green']
