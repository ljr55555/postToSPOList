import datetime
from requests_toolbelt.utils import dump
import json
from config import strListDataURI, strContextURL, strConnectURL, strUsername, strPassword, strFilePath

import sharepy
#https://github.com/JonathanHolvey/sharepy

strContentType = "application/json;odata=verbose"
dateNow = datetime.datetime.now().replace(microsecond=0).isoformat()

s = sharepy.connect(strConnectURL,strUsername,strPassword)

## Get items from list
#r = s.get(strListDataURI)
#jsonReply = json.loads(r.text)
#print(jsonReply)
#jsonData = jsonReply['d']
##
#for key,value in jsonData.items():
#    print("key: {} | value: {}\n".format(key, value))

r = s.post(strContextURL)

# Get digest value for use in POST
jsonDigestRaw = json.loads(r.text)
jsonDigestValue = jsonDigestRaw['d']['GetContextWebInformation']['FormDigestValue']

with open(strFilePath) as f:
    for strRecord in f:
        strRecordList = strRecord.split("\t")
		
        strBody = {"__metadata": { "type": "SP.Data.Teams_x0020_InteroperabilityListItem"}, "Title": "None", "User": strRecordList[0], "Mail": strRecordList[1], "Interoperability_x0020_Level": "UpgradeToTeams", "Status": "Initial Creation", "Date": dateNow}
        strBody  = json.dumps(strBody);


        postRecord = s.post(strListDataURI,headers={"Content-Length": str(len(json.dumps(strBody))), 'accept': strContentType, 'content-Type': strContentType, "X-RequestDigest": jsonDigestValue}, data=strBody)
        #data = dump.dump_all(postRecord)
        #print("Session data:\t%s" % data.decode('utf-8'))
        #print("HTTP Status Code:\t%s\nResult code content:\t%s" % (postRecord.status_code, postRecord.content))
        print("HTTP Status Code:\t%s" % postRecord.status_code)

# Research references
#https://sharepoint.stackexchange.com/questions/105380/adding-new-list-item-using-rest?newreg=70a88b49ad694022a867ac3a6e434380
#https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest

# ListItemEntityTypeFullName is SP.Data.Teams_x0020_InteroperabilityListItem

