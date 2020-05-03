Action Network event export to ICS calendar file to use with Nextcloud, Google or other calendars that support the ICS calendar format.

Written for Python 3
An API KEY is needed to run it, which is obtainable from the API & Sync section of Action Network.

**SETTINGS:**

To run this program modify the following in the program:

api_key = 'ENTER YOUR API KEY HERE'

TZID = ENTER YOUR TIME ZONE

('TZOFFSETFROM:+1000')

('TZOFFSETTO:+1000')

('TZNAME:AEST')

Rename the file to remove the -NO_APIKEY suffix.

Run python3 AN-events_export.py which creates the XRcalendar.ics file.

*Running this in a cron job gives a 0 byte output file.
I had to run it from a shell script in cron to get it to work.*

Import XRcalendar.ics into a calendar that supports ICS.

**TO DO:**

Automatically calculate these from entered TZID value:
Currently, these need to be entered manually. 
('TZOFFSETFROM:+1000')
('TZOFFSETTO:+1000')
('TZNAME:AEST')

Export individual events, so they can be exported into an existing calendar. 
As importing the full event list at each update, results in multiple copies of existing events in the existing calendar.
If a single purpose calendar is used, then new calendars can be created at each import, then the old calendar can be deleted. 

The times from exported from AN network are stated as Z (UTC) but are actually entered as local times.
"start_date": "2019-11-29T16:00:00Z" is 16:00 AEST
It looks like the times that are entered into events are meant to be entered in UTC time.
Should I modify to suit AN data entry errors?
When viewed in the Next cloud calendar the internals of the events show times as UTC. The calendar event titles are displayed as the local time set in the calendar.


**REFERENCES:**

Action Network API Reference

[https://actionnetwork.org/docs/v2/events](https://actionnetwork.org/docs/v2/events)

iCalendar specifications (RFC 5545)

[https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/](https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/)

iCalendar Validator

[https://icalendar.org/validator.html](https://icalendar.org/validator.html)
