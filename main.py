import caldav
from caldav.elements import dav, cdav


def get_calendar_url():
    """
    Prompts the user to enter the URL of the Nextcloud CalDAV calendar and returns it as a string.
    """
    return input("Enter the URL of the Nextcloud CalDAV calendar: ")


def get_credentials():
    """
    Prompts the user to enter their username and password and returns them as a tuple of strings (username, password).
    """
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    return (username, password)


def get_calendars(client):
    """
    Returns a list of all the calendars in the user's account on the given CalDAV server.
    """
    principal = client.principal()
    return principal.calendars()


def change_events_privacy(calendar):
    """
    Changes the privacy setting of all events in the given calendar to private.
    """
    events = calendar.events()
    for event in events:
        event_data = event.data
        event.icalendar_component["class"] = "CONFIDENTIAL"
        event.save()


def main():
    """
    Prompts the user for the Nextcloud CalDAV server URL and their credentials, connects to the server, and prompts
    the user for each calendar whether to change its events' privacy setting to private.
    """
    # Get user input for the URL and credentials
    url = get_calendar_url()
    username, password = get_credentials()

    # Connect to the CalDAV server and retrieve the user's calendars
    client = caldav.DAVClient(url, username=username, password=password)
    calendars = get_calendars(client)

    # Prompt the user for each calendar whether to change its events' privacy setting
    for calendar in calendars:
        answer = input(
            f"Do you want to change the privacy setting of events in the calendar '{calendar.name}'? (y/n) "
        )
        if answer.lower() == "y":
            change_events_privacy(calendar)
            print(
                f"Privacy setting of events in the calendar '{calendar.name}' has been changed to 'CONFIDENTIAL'."
            )


if __name__ == "__main__":
    main()
