from datetime import datetime


def create_notification(title, message):
    """
    Create a notification object for the prototype.
    """

    return {
        "title": title,
        "message": message,
        "created_at": datetime.now()
    }


def baggage_status_notification(baggage_tag, status):
    """
    Generate a notification when baggage status changes.
    """

    return create_notification(
        "Baggage Status Updated",
        f"Baggage {baggage_tag} is now '{status}'."
    )


def delay_notification(baggage_tag, delay_risk):
    """
    Generate a notification when baggage delay risk changes.
    """

    if delay_risk == "HIGH":
        message = (
            f"Baggage {baggage_tag} has a high delay risk. "
            "Please contact airport assistance if required."
        )
    elif delay_risk == "MEDIUM":
        message = (
            f"Baggage {baggage_tag} has a medium delay risk."
        )
    else:
        message = (
            f"Baggage {baggage_tag} is currently progressing normally."
        )

    return create_notification(
        "Baggage Delay Alert",
        message
    )