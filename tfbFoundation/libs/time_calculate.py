from datetime import datetime, timezone
def time_calculate(record_time):

    # Example timestamp from the database
    user_creation_time = datetime.fromisoformat(str(record_time))

    # Get the current time in UTC
    current_time = datetime.now(timezone.utc)

    # Calculate the difference in time
    time_difference = current_time - user_creation_time

    # Convert the time difference to minutes
    minutes_difference = time_difference.total_seconds() / 60

    # If you want to get the absolute difference (positive value)
    minutes_difference = abs(minutes_difference)

    return int(minutes_difference)