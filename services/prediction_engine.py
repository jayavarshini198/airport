 def calculate_eta(status):
    """
    Estimate baggage delivery time based on baggage status.
    This is a prototype prediction model for demonstration.
    """

    eta_values = {
        "Checked In": 15,
        "Processing": 12,
        "Loaded": 8,
        "Arrived": 5,
        "Claim Ready": 2,
        "Collected": 0
    }

    return eta_values.get(status, 10)


def calculate_delay_risk(status):
    """
    Estimate baggage delay risk.
    """

    risk_values = {
        "Checked In": "MEDIUM",
        "Processing": "MEDIUM",
        "Loaded": "LOW",
        "Arrived": "LOW",
        "Claim Ready": "LOW",
        "Collected": "NONE"
    }

    return risk_values.get(status, "MEDIUM")


def predict_baggage(status):
    """
    Returns both ETA and delay risk.
    """

    return {
        "eta_minutes": calculate_eta(status),
        "delay_risk": calculate_delay_risk(status)
    }