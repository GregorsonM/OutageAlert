# Outage Alert
# Application Server
# AppModelOutageMessages
#
# This script handles generating user messages for a set of outages.
#   
# ---------------------------------------------------------------------------------------

# Import custom modules
import AppTimeLib   # Custom date and time related functions for the OutageAlert application

# Import standard modules
import datetime     # Provides datetime object functions



def GenerateOutageMessages(existingOutageInfo, updatedOutageInfo):
    # Returns a list of outage tuples: [ ('key', int_priority, "message"), ('key', int_priority, "message"), ... ]
    # Each message string is a message to the user about a change in this specific power outage.
    # Each message is associated with a priority represented by an integer. The priority may be used to order/prioritize which messages go out first.

    outageMessages = [] # This is a list of strings for the current outage ID number. 

    for key in existingOutageInfo:
        oldValue = existingOutageInfo[key]
        newValue = updatedOutageInfo[key]


        # Generate generic power outage update messages for users

        if key == 'dateOn':
            priority = 1
            dateTimeOn = AppTimeLib.DateTimeFromJSToPython(newValue)
            dateTimeOn = AppTimeLib.PythonChangeTimeZone(dateTimeOn, 'America/Vancouver')
            if oldValue == None and newValue != None:
                outageMessages.append((key, priority, "Power restored on " + datetime.datetime.strftime(dateTimeOn, '%Y-%b-%d %I:%M:%S %p %Z')))
            elif oldValue != None and newValue == None:
                outageMessages.append((key, priority, "Power was restored, but has been lost again."))
            elif newValue != None:
                outageMessages.append((key, priority, "Power restoration time was updated to " + datetime.datetime.strftime(dateTimeOn, '%Y-%b-%d %I:%M:%S %p %Z')))
            break


        elif key == 'crewEta':
            priority = 2
            dateTimeCrewETA = AppTimeLib.DateTimeFromJSToPython(newValue)
            dateTimeCrewETA = AppTimeLib.PythonChangeTimeZone(dateTimeCrewETA, 'America/Vancouver')
            if oldValue == None and newValue != None:
                outageMessages.append((key, priority, "Power restoration crew ETA: " + datetime.datetime.strftime(dateTimeCrewETA, '%Y-%b-%d %I:%M:%S %p %Z')))
            elif oldValue != None and newValue == None:
                outageMessages.append((key, priority, "Power crew ETA has been cancelled."))
            elif newValue != None:
                outageMessages.append((key, priority, "Power restoration crew ETA updated to: " + datetime.datetime.strftime(dateTimeCrewETA, '%Y-%b-%d %I:%M:%S %p %Z')))
            break


        elif key == 'crewStatusDescription':
            priority = 3
            if oldValue == None and newValue != None:
                outageMessages.append((key, priority, "Power restoration crew status: " + newValue))
            elif newValue != None:
                outageMessages.append((key, priority, "Power restoration crew status updated from \'" + oldValue + "\' to \'" + newValue + "\'."))
            break


        elif key == 'cause':
            priority = 4
            if oldValue == None and newValue != None:
                outageMessages.append((key, priority, "Cause of power outage: " + newValue))
            elif newValue != None:
                outageMessages.append((key, priority, "Cause of power outage updated from \'" + oldValue + "\' to \'" + newValue + "\'."))
            break


        elif key == 'dateOff':
            priority = 5
            dateTimeOff = AppTimeLib.DateTimeFromJSToPython(newValue)
            dateTimeOff = AppTimeLib.PythonChangeTimeZone(dateTimeOff, 'America/Vancouver')
            if oldValue == None and newValue != None:
                outageMessages.append((key, priority, "Power outage began on " + datetime.datetime.strftime(dateTimeOff, '%Y-%b-%d %I:%M:%S %p %Z')))
            elif newValue != None:
                outageMessages.append((key, priority, "Power outage start time was updated to " + datetime.datetime.strftime(dateTimeOff, '%Y-%b-%d %I:%M:%S %p %Z')))
            break



        # OTHER DICTIONARY 'KEY' OPTIONS, saved in case we want to use them.
        # elif key == 'polygon':
        #     # need to check for newly affected customers, or newly restored customers if the polygon changes                 <----
        #     break
        # elif key == 'lastUpdated':
        #     # What do we do with this part? anything?                                                                        <----
        #     break
        # elif key == 'numCustomersOut':
        #     break
        # elif key == 'id':
        #     break
        # elif key == 'gisId':
        #     break
        # elif key == 'regionId':
        #     break
        # elif key == 'municipality':
        #     break
        # elif key == 'area':
        #     break
        # elif key == 'regionName':
        #     break
        # elif key == 'crewEtr':
        #     break
        # elif key == 'showEta':
        #     break
        # elif key == 'showEtr':
        #     break
        # elif key == 'latitude':
        #     break
        # elif key == 'longitude':
        #     break
    
    return outageMessages 




# NEW POWER OUTAGES ---------------------------------------------------------------------

def GenerateNewOutageMessages(outages):
    # Returns a list of outage tuples consisting of the outage ID number and a list of message tuples
    # [ (OutageIDNumber, [ ('key', int_priority, "message"), ('key', int_priority, "message"), ... ]),  ... ]

    blankOutage = {}        # A 'blank' outage skeleton
    newOutageAlerts = []    # This is a list of tuples consisting of the outage ID number, and all the related update messages for that outage ID

    if len(outages) > 0:
        # Create 'blank' outage
        for key in outages[0].keys():
            blankOutage[key] = None


        for i in range(len(outages)):
            newOutageAlerts.append((outages[i]['id'], GenerateOutageMessages(blankOutage, outages))) # Create a tuple consisting of the outage ID number, and all the related update messages for that outage ID

    return newOutageAlerts




# EXISTING POWER OUTAGES ----------------------------------------------------------------
    
def GenerateOutageUpdateMessages(udOutages):
    # Returns a list of outage tuples consisting of the outage ID number and a list of message tuples
    # [ (OutageIDNumber, [ ('key', int_priority, "message"), ('key', int_priority, "message"), ... ]),  ... ]

    updatedOutages = [] # Used to store outages that have changed and thus ones we need to notify users about
    updateAlerts = []   # This is a list of tuples consisting of the outage ID number, and all the related update messages for that outage ID

    if len(udOutages) > 0:
        # Figure out what changed with each outage so we can act on those changes
        for i in range(len(udOutages)):
            (outageID, oldOutageInfo, updatedOutageInfo) = udOutages[i] # Get the two outage dictionaries
            
            for key in oldOutageInfo.keys():                     # For each key in the dictionary...
                if updatedOutageInfo[key] == oldOutageInfo[key]: # If the key's values are the same...
                    updatedOutageInfo.pop(key)                   # Remove the key & value from these dictionaries
                    oldOutageInfo.pop(key)
                    continue
            if len(oldOutageInfo) != 0:    # If an outage dictionary still has keys, add it to the list of updated outages
                updatedOutages.append((outageID, oldOutageInfo, updatedOutageInfo))


        for i in range(len(updatedOutages)):
            (outageID, oldOutageInfo, updatedOutageInfo) = updatedOutages[i]

            updateAlerts.append((outageID, GenerateOutageMessages(oldOutageInfo, updatedOutageInfo))) # Create a tuple consisting of the outage ID number, and all the related update messages for that outage ID

    return updateAlerts





