# action_network_events_export
# Export Action Network Events to ICS calendar

Extracting Event Data from Action Network
for creating an ICS format calendar
for importing into Google Calendar

------------------
Written for Python 3

An API KEY is needed to run it, which is obtainable from the API & Sync section of Action Network.

You must change these in the SETTINGS section of the program to run it.

#api_key = 'ENTER YOUR API KEY HERE'
#TZID = ENTER YOUR TIME ZONE

Rename the file to remove the -NO_APIKEY suffix.

Run python3 AN-events_export-ics.py > calendar.ics to create the file.Running this in a cron job gives a 0 byte output file.I had to run it from a shell script in cron to get it to work.

Import calendar.ics into a calendar that supports ICS.


References:
----------- 

Action Network API Reference
https://actionnetwork.org/docs/v2/events

iCalendar specifications (RFC 5545)
https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/

iCalendar Validator
https://icalendar.org/validator.html

------------------

TO DO:
------

There is no DTEND (DATE END) in the Action Network export but there is a date end field in the Action Network event entry forms. ???

Automatically calculate these from entered TZID value:print ('TZOFFSETFROM:+1000')print ('TZOFFSETTO:+1000')print ('TZNAME:AEST')

The times from AN network are stated as Z (UTC) but are actually local times."start_date": "2019-11-29T16:00:00Z" is 16:00 AESTIt looks like the times that are entered into events are meant to be entered in UTC timeShould I modify to suit AN data entry errors?When viewed in the Next cloud calendar the internals of the events show times as local times but are labelled as UTC. The calendar event titles are then displayed as AEST + 10 hours.

