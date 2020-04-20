#!/usr/bin/python3
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
#****************************SETTINGS****************************
#**** API KEY
api_key = 'ENTER YOUR API KEY HERE'


endpoint = 'https://actionnetwork.org/api/v2/events/'

#**** TimeZone
TZID = 'Australia/Brisbane'
#*******************************************************************

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
  
  #Pretty Print
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
  print ('TZID:' + TZID)
  print ('X-LIC-LOCATION:' + TZID)

  #----STANDARD----
  print ('BEGIN:STANDARD')
  # ***** TO DO - Calculate these from TZID
  print ('TZOFFSETFROM:+1000')
  print ('TZOFFSETTO:+1000')
  print ('TZNAME:AEST')
  
  print ('DTSTART:19700101T000000Z')
  print ('END:STANDARD')
  
  print ('END:VTIMEZONE')

  for i in events:

    #----VEVENT----
    print ('BEGIN:VEVENT')

    #3.8.2.4. Date-Time Start - when the calendar component begins
    #"start_date": "2019-12-13T14:00:00Z" (Action Network)
    #DTSTART:20201213T140000Z (Google)
     #Change format from 2019-12-05T04:03:06Z to 20191205T040306Z
    orig_start_date = i['start_date']
    # Create datetime object
    d = datetime.datetime.strptime(orig_start_date, "%Y-%m-%dT%H:%M:%SZ")
    mod_start_date = d.strftime("%Y%m%dT%H%M%SZ")
    print ('DTSTART:' + mod_start_date)

    #3.8.2.2. Date-Time End - the date and time that a calendar component ends.
    #DTEND:20200422T150000Z
    #DTEND;VALUE=DATE:20200422
    #TO DO -There is no end_date key in Action Network exports

    #3.8.5.3. Recurrence Rule
    #print ('RRULE:FREQ=WEEKLY;WKST=SU;UNTIL=20200508T135959Z;BYDAY=FR')

    #----Current Date Time in 20200418T001100Z format
    now = datetime.datetime.now()
    utc = pytz.utc.localize(datetime.datetime.utcnow())
    utcnow = utc.strftime("%Y%m%dT%H%M%SZ")
    uid = utc.strftime("%Y%m%d%S%f")
    
    #3.8.7.2. Date-Time Stamp
    #DTSTAMP:20200418T001100Z
    print ('DTSTAMP:' + utcnow)

    #3.8.4.7. Unique Identifier
    print ('UID:' + uid + '@teslations.ddns.net')

    # 3.8.7.1. Date-Time Created
    # The date and time that the calendar information was 
    # created by the calendar user agent in the calendar store.
     #Change format from 2019-12-05T04:03:06Z to 20191205T040306Z
    orig_created_date = i['created_date']
    # Create datetime object
    d = datetime.datetime.strptime(orig_created_date, "%Y-%m-%dT%H:%M:%SZ")
    mod_created_date = d.strftime("%Y%m%dT%H%M%SZ")
    print ('CREATED:' + mod_created_date)

    #3.8.1.5. Description
    orig_description =  i['description']
    # Remove HTML formatting codes
    mod_description1 = orig_description.replace("<p>", "")
    mod_description2 = mod_description1.replace("</p>", " ")
    mod_description3 = mod_description2.replace('"', "")
    mod_description4 = mod_description3.replace("<a href=", "")
    mod_description5 = mod_description4.replace("'\">'", " ")
    mod_description = mod_description5.replace("</a>", " ")
    #mod_description = mod_description5.replace("<br>", "\r")
    print ('DESCRIPTION:' + mod_description)
    
    #3.8.7.3. Last Modified
    #Change format from 2019-12-05T04:03:06Z to 19960329T133000Z
    orig_modified_date = i['modified_date']
    x = orig_modified_date.replace("-", "")
    mod_modified_date = x.replace(":", "")
    print ('LAST-MODIFIED:' + mod_modified_date)

    #3.8.1.7. Location (The venue of the calendar event)
    # TO DO - CHANGE to the venue Location,
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
    print ('STATUS:' + i['status'].upper())

    #3.8.1.12. Summary
    # short summary or subject for the calendar component.
    print ('SUMMARY:' + i['title'])

    #3.8.2.7. Time Transparency
    # whether or not an event is transparent to busy time searches.
    print ('TRANSP:' + i['transparence'].upper())

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



