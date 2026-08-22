# Fare Calculator Automation Test Suite

A Python-based test automation framework for verifying ride-share fare calculations, utilizing `pytest` and JSON-driven data parameterization.

## Features

- **Dynamic Fare Logic:** Calculates total trip fare using base rate, per-mile cost, and dynamic surge multipliers.
- **Data-Driven Testing:** Reads test scenarios directly from `test_data.json` to validate positive calculation cases.
- **Robust Exception Handling:** Rigorously tests negative scenarios including invalid data types and negative numeric inputs.

## Setup & Execution

### Prerequisites
- Python 3.x
- `pytest` library

### Running Tests
Execute the full test suite using:

```bash
pytest test_fare.py