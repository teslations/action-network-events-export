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
#
# This document defines the iCalendar data format for representing
# and exchanging calendaring and scheduling information such as
# events, to-dos, journal entries, and free/busy information,
# independent of any particular calendar service or protocol.
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

  #unformatted output
  #print(response.json())

  #Read the output
  data = response.text
  
  #Parse JSON – convert the string to JSON
  parsed = json.loads(data)

  #Pretty print
  #print(json.dumps(parsed, indent=4))

  events = parsed["_embedded"]["osdi:events"]
  #print(json.dumps(events, indent=4))
  #print(events)

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
    #DTSTART:19970714T133000                         ; Local time
    #DTSTART:19970714T173000Z                        ; UTC time
    #DTSTART;TZID=America/New_York:19970714T133000   ; Local time and time zone reference
    #(Action Network format: start_date: 2019-11-24T12:00:00Z)
        
    orig_start_date = i['start_date']
    split_start_date = orig_start_date.split("T")
    mod_start_date = split_start_date[0].replace("-", "")
                                           
    print ('DTSTART;VALUE=DATE:' + mod_start_date)

    #DTEND;VALUE=DATE:20200422
    print ('DTEND;VALUE=DATE:' + mod_start_date)

    #Recurring event
    #RRULE:FREQ=WEEKLY;WKST=SU;UNTIL=20200508T135959Z;BYDAY=FR
    #print ('RRULE:FREQ=WEEKLY;WKST=SU;UNTIL=20200508T135959Z;BYDAY=FR')

    print ('DTSTAMP:20200418T001100Z')

    #Date time
    now = datetime.datetime.now()
    utc = pytz.utc.localize(datetime.datetime.utcnow())
    utcdate = utc.strftime("%Y%m%d")
    utctime = utc.strftime("%H%M%S")
    uid = utc.strftime("%Y%m%d%S%f")

    print ('UID:' + uid + '@google.com')

    print ('CREATED:' + i['created_date'])

    print ('DESCRIPTION:' + i['description'])
    
    # Now YYYYMMDDTHHMMSSZ
    print ('LAST-MODIFIED:' + i['modified_date'])

    print ('LOCATION:' + i['browser_url'])
    print ('SEQUENCE:0')
    print ('STATUS:CONFIRMED')
    print ('SUMMARY:' + i['title'])
    print ('TRANSP:OPAQUE')

    #----VALARM----
    print ('BEGIN:VALARM')
    print ('ACTION:DISPLAY')
    print ('DESCRIPTION:This is an event reminder')
    print ('TRIGGER:-P0DT4H0M0S')
    print ('END:VALARM')
    print ('END:VEVENT')
    
  print ('END:VCALENDAR')


else:
  print('Request returned an error.')
  print(response.status_code)

# Retrieve an individual event resource (GET)
#
#EVENT_ID=8a625981-67a4-4457-8b55-2e30b267b2c2
#https://actionnetwork.org/api/v2/events/$EVENT_ID OSDI-API-Token:$API_KEY
  


