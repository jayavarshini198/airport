 def calculate_priority(passenger):
    """
    Calculate passenger priority score based on
    accessibility, age, mobility needs and connection time.
    """

    score = 0

    # Age-based priority
    if passenger.age >= 75:
        score += 25
    elif passenger.age >= 65:
        score += 15

    # Assistance requirement
    if passenger.assistance_required:
        score += 25

    # Mobility requirement
    if passenger.mobility_required:
        score += 30

    # Short flight connection time
    if passenger.connection_minutes <= 30:
        score += 20
    elif passenger.connection_minutes <= 60:
        score += 10

    # Convert score into priority level
    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "NORMAL"

    return {
        "score": score,
        "level": level
    }


# Backward-compatible function name
def calculate_priority_score(passenger):
    return calculate_priority(passenger)

