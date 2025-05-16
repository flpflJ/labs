from model.form_validation import validate_data

def test_validate_data():
    test_data = [
        {"product1": {"name": "habsd", "date": "12/04/2025", "count": 12}}
    ]
    expected = [True]
    for i, d in enumerate(test_data):
        assert expected[i] == validate_data(d)[0]
