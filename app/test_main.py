import datetime
from unittest.mock import patch
from app.main import outdated_products


# Patch the MODULE 'datetime' in 'app.main'
@patch("app.main.datetime")
def test_outdated_products(mock_datetime):
    # Set the fixed "today" date
    fixed_today = datetime.date(2022, 2, 2)

    # Mock the .date.today() call chain
    mock_datetime.date.today.return_value = fixed_today

    # Crucial: Ensure when app.main calls datetime.date(y, m, d),
    # it returns a real date object for comparison
    mock_datetime.date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)

    products = [
        {
            "name": "salmon",
            "expiration_date": datetime.date(2022, 2, 10),  # Future
        },
        {
            "name": "chicken",
            "expiration_date": datetime.date(2022, 2, 2),  # Today
        },
        {
            "name": "duck",
            "expiration_date": datetime.date(2022, 2, 1),  # Outdated
        }
    ]

    # 1. Test basic filtering
    assert outdated_products(products) == ["duck"]

    # 2. Test empty list
    assert outdated_products([]) == []

    # 3. Test multiple outdated products (moving today forward)
    mock_datetime.date.today.return_value = datetime.date(2022, 2, 11)
    assert outdated_products(products) == ["salmon", "chicken", "duck"]
