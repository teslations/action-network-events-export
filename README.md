Action Network event export to ICS calendar file to use with Nextcloud, Google or other calendars that support the ICS calendar format.

Written for Python 3

An API KEY is needed to run it, which is obtainable from the API & Sync section of Action Network.

To run this program modify the following in the SETTINGS section of the program:
api_key = 'ENTER YOUR API KEY HERE'
TZID = ENTER YOUR TIME ZONE

Rename the file to remove the -NO_APIKEY suffix.

Run python3 AN-events_export.py which creates the XRcalendar.ics file.

Running this in a cron job gives a 0 byte output file.
I had to run it from a shell script in cron to get it to work.

Import XRcalendar.ics into a calendar that supports ICS.

TO DO:

Automatically calculate these from entered TZID value:Currently, these need to be entered manually. 

('TZOFFSETFROM:+1000')
('TZOFFSETTO:+1000')
('TZNAME:AEST')

Export individual events, so they can be exported into an existing calendar. As importing the full event list at each update, results in multiple copies of existing events in the existing calendar.If a single purpose calendar is used, then new calendars can be created at each import, then the old calendar can be deleted. I still have to work out how to automate this process.

The times from AN network are stated as Z (UTC) but are actually local times."start_date": "2019-11-29T16:00:00Z" is 16:00 AESTIt looks like the times that are entered into events are meant to be entered in UTC timeShould I modify to suit AN data entry errors?When viewed in the Nextcloud calendar the internals of the events show times as local times but are labelled as UTC. The calendar event titles are then displayed as AEST + 10 hours.When entering date-times into Action Network. The TimeZone selection pull-down list is only available, when no physical location is selected. It normally defaults to UTC/Z time.

REFERENCES:

Action Network API Reference

https://actionnetwork.org/docs/v2/events

iCalendar specifications (RFC 5545)

https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/

iCalendar Validator

https://icalendar.org/validator.html
