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
# ENDPOINTS
#
#For a collection of all events associated with your API key
# https://actionnetwork.org/api/v2/events
#
#For all events associated with a specific event campaign
# https://actionnetwork.org/api/v2/event_campaigns/[event_campaign_id]/events
#
#To address a specific event, use the identifier without the action_network: prefix to construct a URL, like
# https://actionnetwork.org/api/v2/events/[id]
# https://actionnetwork.org/api/v2/events/d91b4b2e-ae0e-4cd3-9ed7-d0ec501b0bc3

import requests
import json
import datetime
import pytz


#*******************************************

def generate_ics(group, api_key):

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
    with open('XR-' + group +'.json', 'w') as json_file:
      json.dump(parsed, json_file, sort_keys=True, indent=4)
  
  
    #write calendar file
    output_file=open('XR-' + group + '.ics', 'w')
  
    #----CALENDAR----
    output_file.write ('BEGIN:VCALENDAR'+'\n')
    output_file.write ('PRODID:-//XR//Calendar//EN'+'\n')
    output_file.write ('VERSION:2.0'+'\n')
    output_file.write ('CALSCALE:GREGORIAN'+'\n')
    output_file.write ('METHOD:PUBLISH'+'\n')
    output_file.write ('X-WR-CALNAME:XR'+'\n')
    output_file.write ('X-WR-TIMEZONE:' + TZID+'\n')

    #----TIMEZONE----  
    output_file.write ('BEGIN:VTIMEZONE'+'\n')
    #3.2.19. Time Zone Identifier
    #  The "TZID" property parameter MUST NOT be applied to TIME
    #  properties whose time values are specified in UTC.
    output_file.write ('TZID:' + TZID+'\n')
    output_file.write ('X-LIC-LOCATION:' + TZID+'\n')

    #----STANDARD----
    output_file.write ('BEGIN:STANDARD'+'\n')
    # 3.8.3.3. Time Zone Offset From. This property specifies the offset that is in use prior to this time zone observance. 
    output_file.write ('TZOFFSETFROM:+1000'+'\n')
    #3.8.3.4. Time Zone Offset To . This property specifies the offset that is in use in this time zone observance.
    output_file.write ('TZOFFSETTO:+1000'+'\n')
    #3.8.3.2.  Time Zone Name
    output_file.write ('TZNAME:AEST'+'\n')
    output_file.write ('DTSTART:19700101T000000Z'+'\n')
    output_file.write ('END:STANDARD'+'\n')
  
    output_file.write ('END:VTIMEZONE'+'\n')
  
  #----EVENT-----------------------------------
    for i in events:
      #----VEVENT----

      output_file.write ('BEGIN:VEVENT'+'\n')

      #3.8.2.4. Date-Time Start - when the calendar component begins
      # Dates are entered as local time in AN but exported as GMT(Z+'\n') time. ??
      orig_start_date = i['start_date']
      if str.endswith(orig_start_date,'Z'):
          d = datetime.datetime.strptime(orig_start_date, "%Y-%m-%dT%H:%M:%SZ")
          mod_start_date = d.strftime("%Y%m%dT%H%M%SZ")
          prefix_date=':'
      else:    
          prefix_date=';'+TZID+':'
      output_file.write ('DTSTART'+prefix_date+mod_start_date+'\n')

      #3.8.2.2. Date-Time End - the date and time that a calendar component ends
      if 'end_date' in events:
          orig_end_date = i['end_date']
          if str.endswith(orig_end_date,'Z'):
              d = datetime.datetime.strptime(orig_end_date, "%Y-%m-%dT%H:%M:%SZ")
              mod_end_date = d.strftime("%Y%m%dT%H%M%SZ")
              prefix_date=':'
          else:    
              prefix_date=';'+TZID+':'
          output_file.write ('DTSTART'+prefix_date+mod_start_date+'\n')
      else:
          #if no end date: end date = start date
          output_file.write('DTEND'+prefix_date+mod_start_date+'\n')

      #3.8.5.3. Recurrence Rule
  # TO DO - Check if Action Network has recurring events
  #    if 'rrule' in events:
  #        output_file.write ('RRULE:FREQ=WEEKLY;WKST=SU;UNTIL=20200508T135959Z;BYDAY=FR')

      #----Current Date Time in 20200418T001100Z format
      now = datetime.datetime.now()
      utc = pytz.utc.localize(datetime.datetime.utcnow())
      utcnow = utc.strftime("%Y%m%dT%H%M%SZ")
      uid = utc.strftime("%Y%m%d%S%f")
    
      #3.8.7.2. Date-Time Stamp
      #DTSTAMP:20200418T001100Z
      output_file.write ('DTSTAMP:' + utcnow+'\n')

      #3.8.4.7. Unique Identifier
      output_file.write ('UID:' + uid + '@ausrebellion.earth'+'\n')

      # 3.8.7.1. Date-Time Created
      # The date and time that the calendar information was 
      # created by the calendar user agent in the calendar store.
      #Change format from 2019-12-05T04:03:06Z to 20191205T040306Z
      orig_created_date = i['created_date']
      # Create datetime object
      d = datetime.datetime.strptime(orig_created_date, "%Y-%m-%dT%H:%M:%SZ")
      mod_created_date = d.strftime("%Y%m%dT%H%M%SZ")
      output_file.write ('CREATED:' + mod_created_date+'\n')

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
      mod_description15 = mod_description14.replace("target=_blank>", " ")
      mod_description = mod_description15.replace("<br>", "\r")

  # TO DO - Line length should not be longer than 75 characters.
  # RFC 5545 3.1. Content Lines
  # Nextcloud calendar description width is 47 characters.
  # (Don't end lines with CRLF?
  #    output_file.write ('DESCRIPTION:', end='')
   
      output_file.write ('DESCRIPTION:' + mod_description + i['browser_url']+'\n')

      #3.8.7.3. Last Modified
      #Change format from 2019-12-05T04:03:06Z to 19960329T133000Z
      orig_modified_date = i['modified_date']
      x = orig_modified_date.replace("-", "")
      mod_modified_date = x.replace(":", "")
      output_file.write ('LAST-MODIFIED:' + mod_modified_date+'\n')

      #3.8.1.7. Location (The venue of the calendar event)
      #output_file.write ('LOCATION:' + i['location']['venue'],i['location']['address_lines']+'\n')

      #3.8.7.4. Sequence Number
      # revision sequence number of the calendar component within a sequence of revisions.
      output_file.write ('SEQUENCE:0'+'\n')

      #3.8.1.11. Status
      # overall status or confirmation for the calendar component.
      output_file.write ('STATUS:' + i['status'].upper()+'\n')

      #3.8.1.12. Summary
      # short summary or subject for the calendar component.
      output_file.write ('SUMMARY:' + i['title']+'\n')

      #3.8.2.7. Time Transparency
      # whether or not an event is transparent to busy time searches.
      output_file.write ('TRANSP:' + i['transparence'].upper()+'\n')

      #----VALARM----
      output_file.write ('BEGIN:VALARM'+'\n')

      #3.8.6.1. Action
      # the action to be invoked when an alarm is triggered. (AUDIO or DISPLAY)
      output_file.write ('ACTION:DISPLAY'+'\n')

      output_file.write ('DESCRIPTION:This is an event reminder'+'\n')

      #3.8.6.3. Trigger - when an alarm will trigger.
      output_file.write ('TRIGGER:-P0DT4H0M0S'+'\n')

      output_file.write ('END:VALARM'+'\n')
      output_file.write ('END:VEVENT'+'\n')
  #--------------------------------------------
    output_file.write ('END:VCALENDAR'+'\n')
    output_file.close()
  
  else:
    print ('Request returned an error.')
    print (response.status_code)

#***************************************************************
#**************************SETTINGS**************************
# Adjust these settings to run this program
#
# **** ENDPOINT ****
endpoint = 'https://actionnetwork.org/api/v2/events/'

# **** TimeZone ID ****
TZID = 'Australia/Brisbane'    

# **** GROUP NAMES: API KEYS ****
# api_keys = {
#'groupname':'apikey',
#'groupname':'apikey'
#}

for group in api_keys :
      print ('group='+group)
      print ('api_key='+api_keys[group])
      generate_ics(group, api_keys[group])
    
