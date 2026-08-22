import json
import pytest
from fare import calculate_fare

# Load test data from JSON
with open("test_data.json") as f:
    test_data = json.load(f)


@pytest.mark.parametrize("data", test_data)
def test_calculate_fare_from_json(data):
    result = calculate_fare(data["distance"], data["surge"])
    assert result == data["expected_fare"]


# --- Negative / Error Tests ---
def test_calculate_fare_invalid_distance_type():
    with pytest.raises(TypeError):
        calculate_fare("10", 1.0)


def test_calculate_fare_invalid_surge_type():
    with pytest.raises(TypeError):
        calculate_fare(10, "1.5")


def test_negative_distance_raises_error():
    with pytest.raises(ValueError):
        calculate_fare(-5, 1.0)