#!/usr/bin/python3
#
# Extracts Event Data from Action Network
# for creating an ICS format calendar
# for importing into Google Calendar
#
# Action Network API Reference
# https://actionnetwork.org/docs/v2/events
# HAL+JSON format. It generally conforms to the Open Supporter Data Interface (OSDI) specification version 1.0.2
#
# iCalendar specifications (RFC 5545)
# https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/
#
# iCalendar Validator
# https://icalendar.org/validator.html
#
# You need to enter your API KEY and TZID in SETTINGS below to run this program

#****************SETTINGS****************
#******** Enter your API KEY here ********
api_key = 'ENTER YOUR API KEY HERE'


if api_key == 'ENTER YOUR API KEY HERE':
    api_key = input(' Enter your API KEY : ')
    print('''Enter your API KEY in the settings section
    of this program, to store it permanently.
    And your TimeZone ID (TZID). ''')

# **** Enter your TimeZone ID here ****
TZID = 'Australia/Brisbane'    
    
# **** ENDPOINT ****
endpoint = 'https://actionnetwork.org/api/v2/events/'
 
#For a collection of all events associated with your API key
# https://actionnetwork.org/api/v2/events
#
#For all events associated with a specific event campaign
# https://actionnetwork.org/api/v2/event_campaigns/[event_campaign_id]/events
#
#To address a specific event, use the identifier without the action_network: prefix to construct a URL, like
# https://actionnetwork.org/api/v2/events/[id]
# https://actionnetwork.org/api/v2/events/d91b4b2e-ae0e-4cd3-9ed7-d0ec501b0bc3
#****************************************

import requests
import json
import datetime
import pytz

response = requests.get(endpoint,
 headers={
   "OSDI-API-Token": api_key,
 }
)

if response:
  #Request is successful
  data = response.text
  parsed = json.loads(data)
  events = parsed["_embedded"]["osdi:events"]
  #print(json.dumps(events, sort_keys=True, indent=4))
  #write JSON file to disk
  with open('AN-events.json', 'w') as json_file:
    json.dump(parsed, json_file, sort_keys=True, indent=4)

  #----CALENDAR----
  print ('BEGIN:VCALENDAR')
  print ('PRODID:-//XR//Calendar//EN')
  print ('VERSION:2.0')
  print ('CALSCALE:GREGORIAN')
  print ('METHOD:PUBLISH')
  print ('X-WR-CALNAME:XR')
  print ('X-WR-TIMEZONE:' + TZID)

  #----TIMEZONE----  
  print ('BEGIN:VTIMEZONE')
  #3.2.19. Time Zone Identifier
  #  The "TZID" property parameter MUST NOT be applied to TIME
  #  properties whose time values are specified in UTC.
  print ('TZID:' + TZID)
  print ('X-LIC-LOCATION:' + TZID)

  #----STANDARD----
  print ('BEGIN:STANDARD')
  # 3.8.3.3. Time Zone Offset From. This property specifies the offset that is in use prior to this time zone observance. 
  print ('TZOFFSETFROM:+1000')
  #3.8.3.4. Time Zone Offset To . This property specifies the offset that is in use in this time zone observance.
  print ('TZOFFSETTO:+1000')
  #3.8.3.2.  Time Zone Name
  print ('TZNAME:AEST')
  print ('DTSTART:19700101T000000Z')
  print ('END:STANDARD')
  
  print ('END:VTIMEZONE')
  
#----EVENT-----------------------------------
  for i in events:

    #----VEVENT----
    print ('BEGIN:VEVENT')

    #3.8.2.4. Date-Time Start - when the calendar component begins
    # Dates are entered as local time in AN but exported as GMT(Z) time. ??
    orig_start_date = i['start_date']
    if str.endswith(orig_start_date,'Z'):
        d = datetime.datetime.strptime(orig_start_date, "%Y-%m-%dT%H:%M:%SZ")
        mod_start_date = d.strftime("%Y%m%dT%H%M%SZ")
        prefix_date=':'
    else:    
        prefix_date=';'+TZID+':'
    print ('DSTART'+prefix_date+mod_start_date)

    #3.8.2.2. Date-Time End - the date and time that a calendar component ends
    if 'end_date' in events:
        orig_end_date = i['end_date']
        if str.endswith(orig_end_date,'Z'):
            d = datetime.datetime.strptime(orig_end_date, "%Y-%m-%dT%H:%M:%S")
            mod_end_date = d.strftime("%Y%m%dT%H%M%S")
            prefix_date=':'
        else:    
            prefix_date=';'+TZID+':'
        print ('DSTART'+prefix_date+mod_start_date)
    else:
        #if no end date: end date = start date
        print('DTEND'+prefix_date+mod_start_date)

    #3.8.5.3. Recurrence Rule
# TO DO - Check if Action Network has recurring events
#    if 'rrule' in events:
#        print ('RRULE:FREQ=WEEKLY;WKST=SU;UNTIL=20200508T135959Z;BYDAY=FR')

    #----Current Date Time in 20200418T001100Z format
    now = datetime.datetime.now()
    utc = pytz.utc.localize(datetime.datetime.utcnow())
    utcnow = utc.strftime("%Y%m%dT%H%M%SZ")
    uid = utc.strftime("%Y%m%d%S%f")
    
    #3.8.7.2. Date-Time Stamp
    #DTSTAMP:20200418T001100Z
    print ('DTSTAMP:' + utcnow)

    #3.8.4.7. Unique Identifier
    print ('UID:' + uid + '@ausrebellion.earth')

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
    mod_description5 = mod_description4.replace("</a>", " ")
    mod_description6 = mod_description5.replace("<span>", " ")
    mod_description7 = mod_description6.replace("</span>", " ")
    mod_description8 = mod_description7.replace("<ul>", " ")
    mod_description9 = mod_description8.replace("</ul>", " ")
    mod_description10 = mod_description9.replace("<li>", " ")
    mod_description11 = mod_description10.replace("</li>", " ")
    mod_description12 = mod_description11.replace("<strong>", " ")
    mod_description13 = mod_description12.replace("</strong>", " ")
    mod_description14 = mod_description13.replace("&mdash;", " - ")    
    mod_description = mod_description14.replace("<br>", "\r")

# TO DO - Line length should not be longer than 75 characters.
# RFC 5545 3.1. Content Lines
# Nextcloud calendar description width is 47 characters.
# (Don't end lines with CRLF)?
#    print ('DESCRIPTION:', end='')
   
    print ('DESCRIPTION:' + mod_description + '\r' + i['browser_url'])

    #3.8.7.3. Last Modified
    #Change format from 2019-12-05T04:03:06Z to 19960329T133000Z
    orig_modified_date = i['modified_date']
    x = orig_modified_date.replace("-", "")
    mod_modified_date = x.replace(":", "")
    print ('LAST-MODIFIED:' + mod_modified_date)

    #3.8.1.7. Location (The venue of the calendar event)
    print ('LOCATION:' + i['location']['venue'],i['location']['address_lines'])

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
#--------------------------------------------
  print ('END:VCALENDAR')

else:
  print ('Request returned an error.')
  print (response.status_code)
