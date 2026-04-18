import datetime
from unittest.mock import patch, MagicMock
from app.main import outdated_products


@patch("app.main.datetime")
def test_outdated_products(mock_datetime: MagicMock) -> None:
    # Set the fixed "today" date
    fixed_today = datetime.date(2022, 2, 2)

    # Mock the .date.today() call chain
    mock_datetime.date.today.return_value = fixed_today

    # Fixed E501: Wrapped the long line to stay under 79 chars
    mock_datetime.date.side_effect = (
        lambda *args, **kwargs: datetime.date(*args, **kwargs)
    )

    products = [
        {
            "name": "salmon",
            "expiration_date": datetime.date(2022, 2, 10),
        },
        {
            "name": "chicken",
            "expiration_date": datetime.date(2022, 2, 2),
        },
        {
            "name": "duck",
            "expiration_date": datetime.date(2022, 2, 1),
        }
    ]

    # 1. Test basic filtering
    assert outdated_products(products) == ["duck"]

    # 2. Test empty list
    assert outdated_products([]) == []

    # 3. Test multiple outdated products
    mock_datetime.date.today.return_value = datetime.date(2022, 2, 11)
    assert outdated_products(products) == ["salmon", "chicken", "duck"]
