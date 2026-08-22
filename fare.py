def calculate_fare(distance, surge=1.0):
    # 1. Type Validation
    if not isinstance(distance, (int, float)) or isinstance(distance, bool):
        raise TypeError("Distance must be a number.")
    if not isinstance(surge, (int, float)) or isinstance(surge, bool):
        raise TypeError("Surge multiplier must be a number.")

    # 2. Value Validation
    if distance < 0:
        raise ValueError("Distance cannot be negative.")
    if surge < 0:
        raise ValueError("Surge multiplier cannot be negative.")

    # 3. Calculation
    base_fare = 5.0
    rate_per_mile = 2.0

    fare = (base_fare + (distance * rate_per_mile)) * surge
    return round(fare, 2)