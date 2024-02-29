from datetime import datetime


def convert_date_time_format(input_date):
    # Parse the input string to a datetime object
    dt_object = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%S")

    # Format the datetime object as a string with HH:MM format
    formatted_datetime_str = dt_object.strftime("%d-%m-%Y %H:%M")
    return formatted_datetime_str
