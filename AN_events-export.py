#! python3.7
#
# Extracting Event Data from Action Network
# for creating an ICS format calendar
# for importing into Google Calendar
#
# Action Network API Reference
# https://actionnetwork.org/docs/v2/events
#
# iCalendar specifications (RFC 5545)
# https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/
#
# iCalendar Validator
# https://icalendar.org/validator.html
#
#********* You must enter your API KEY here **********
#api_key = 'ENTER YOUR API KEY HERE'


endpoint = 'https://actionnetwork.org/api/v2/events/'

import requests
import json
import datetime
import pytz

# Retrieve a collection of event resources (GET)
response = requests.get(endpoint,
 headers={
   "OSDI-API-Token": api_key,
 }
)
if response:
  #Request is successful

  #Read the output
  data = response.text
  
  #Parse JSON – convert the string to JSON
  parsed = json.loads(data)

  events = parsed["_embedded"]["osdi:events"]

  #Pretty Print (uncomment for pretty print)
  #print(json.dumps(events, indent=4))

  #----CALENDAR----
  print ('BEGIN:VCALENDAR')
  print ('PRODID:-//Teslations//Calendar//EN')
  print ('VERSION:2.0')
  print ('CALSCALE:GREGORIAN')
  print ('METHOD:PUBLISH')
  print ('X-WR-CALNAME:XR')
  print ('X-WR-TIMEZONE:Australia/Brisbane')

  #----TIMEZONE----  
  print ('BEGIN:VTIMEZONE')
  print ('TZID:Australia/Brisbane')
  print ('X-LIC-LOCATION:Australia/Brisbane')

  #----STANDARD----
  print ('BEGIN:STANDARD')
  print ('TZOFFSETFROM:+1000')
  print ('TZOFFSETTO:+1000')
  print ('TZNAME:AEST')
  print ('DTSTART:19700101T000000')
  print ('END:STANDARD')
  
  print ('END:VTIMEZONE')

  for i in events:
    #----VEVENT----
    print ('BEGIN:VEVENT')

    #3.8.2.4. Date-Time Start - when the calendar component begins
    orig_start_date = i['start_date']
    split_start_date = orig_start_date.split("T")
    mod_start_date = split_start_date[0].replace("-", "")
    print ('DTSTART;VALUE=DATE:' + mod_start_date)

    #3.8.2.2. Date-Time End - the date and time that a calendar component ends.
    #DTEND:20200422T150000Z
    #DTEND;VALUE=DATE:20200422
    #print ('DTEND;VALUE=DATE:' + mod_start_date)

    #3.8.5.3. Recurrence Rule
    #print ('RRULE:FREQ=WEEKLY;WKST=SU;UNTIL=20200508T135959Z;BYDAY=FR')

    #Current Date Time
    now = datetime.datetime.now()
    utc = pytz.utc.localize(datetime.datetime.utcnow())
    utcdate = utc.strftime("%Y%m%d")
    utctime = utc.strftime("%H%M%S")
    uid = utc.strftime("%Y%m%d%S%f")
    utcnow = utcdate + 'T' + utctime + 'Z'

    #3.8.7.2. Date-Time Stamp
    #DTSTAMP:20200418T001100Z
    print ('DTSTAMP:' + utcnow)

    #3.8.4.7. Unique Identifier
    print ('UID:' + uid + '@teslations.ddns.net')

    # 3.8.7.1. Date-Time Created
    # date and time that the calendar
    # information was created by the calendar user agent in the calendar store.
    #(The date the event was created)
    #Change format from 2019-12-05T04:03:06Z to 19960329T133000Z
    orig_created_date = i['created_date']
    x = orig_created_date.replace("-", "")
    mod_created_date = x.replace(":", "")
    print ('CREATED:' + mod_created_date)

    #3.8.1.5. Description
    #End lines with CRLF
    print ('DESCRIPTION:' + i['description'])

    #3.8.7.3. Last Modified
    orig_modified_date = i['modified_date']
    x = orig_modified_date.replace("-", "")
    mod_modified_date = x.replace(":", "")
    print ('LAST-MODIFIED:' + mod_modified_date)

    #3.8.1.7. Location (The venue of the calendar event)
    ### CHANGE to the Location,
    '''
    ----- Examples of this property
    LOCATION:Conference Room - F123\, Bldg. 002
    LOCATION;ALTREP="http://xyzcorp.com/conf-rooms/f123.vcf":
    Conference Room - F123\, Bldg. 002
    ----
                "location": {
                    "address_lines": [
                        "Extinction Park 3321 Carbon Rd, Rebellion Grove QLD 4000"
                    ],
                    "country": "AU",
                    "locality": "Brisbane",
                    "location": {
                        "accuracy": "Rooftop",
                        "latitude": -27.402343999999996,
                        "longitude": 152.93726100000003
                    },
                    "postal_code": "4000",
                    "venue": "Extinction Park, Rebellion Grove"
    '''
    print ('LOCATION:' + i['browser_url'])

    #3.8.7.4. Sequence Number
    # revision sequence number of the calendar component within a sequence of revisions.
    print ('SEQUENCE:0')

    #3.8.1.11. Status
    # overall status or confirmation for the calendar component.
    print ('STATUS:' + i['status'])

    #3.8.1.12. Summary
    # short summary or subject for the calendar component.
    print ('SUMMARY:' + i['title'])

    #3.8.2.7. Time Transparency
    # whether or not an event is transparent to busy time searches.
    print ('TRANSP:' + i['transparence'])

    #----VALARM----
    print ('BEGIN:VALARM')

    #3.8.6.1. Action
    # the action to be invoked when an alarm is triggered. (AUDIO or DISPLAY)
    print ('ACTION:DISPLAY')
    
    print ('DESCRIPTION:This is an event reminder')

    #3.8.6.3. Trigger - when an alarm will trigger.
    print ('TRIGGER:-P0DT4H0M0S')

    print ('END:VALARM')
    print ('END:VEVENT')
    
  print ('END:VCALENDAR')

else:
  print('Request returned an error.')
  print(response.status_code)

  


