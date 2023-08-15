from AzureTable import AzureTable
from time import sleep
import os

# otptable =AzureTable(con,tablename)


def InsertTable(state,website,email_id,otptable):
    otptable.InsetEntity({
        u'PartitionKey': website,
        u'RowKey':email_id,
        u'Status': state,
        u'Email':email_id
        })

def AddOtp(website,email_id):
    con              =       os.environ['ConnectionString']
    tablename        =       os.environ['IMAPTableName']
    otptable          =     AzureTable(con,tablename)
    data =otptable.SelectEntity(f"PartitionKey eq '{website}' and Email eq '{email_id}' and Status eq 'Pending'")

    print(len(data))
    if len(data)   == 0:
        try:
            InsertTable("Pending",website,email_id,otptable)
            return True
        except:
            return False
        #data =otptable.SelectEntity("Status eq 'Pending'")
    else:
        print("Email Pending in queue")
        return False
def CheckOtp(website,email_id):
    con              =       os.environ['ConnectionString']
    tablename        =       os.environ['IMAPTableName']
    data =AzureTable(con,tablename).SelectEntity(f"PartitionKey eq '{website}' and Email eq '{email_id}' and Status eq 'Pending'")
    print(len(data))
    if len(data)   == 0:
        return True
        #data =otptable.SelectEntity("Status eq 'Pending'")
    else:
        print("Email Pending in queue")
        return False

def DeleteOtp_(website,email_id):
    con              =       os.environ['ConnectionString']
    tablename        =       os.environ['IMAPTableName']
    otptable =AzureTable(con,tablename)      
    otptable.DeleteEntity(website,email_id)
    return True

def DeleteOtp(website,email_id,otptable):
    otptable.DeleteEntity(website,email_id)
    return True
def update_status(website,email_id,status,otptable):
    otptable.UpdateEntity(website,email_id,{"Status":status})



def OtpFetch(website,email_id,OtpHandler):
    con              =       os.environ['ConnectionString']
    tablename        =       os.environ['IMAPTableName']
    final_otp  =OtpHandler.otp_fetch_with_imap()
    DeleteOtp(website,email_id,AzureTable(con,tablename) )
    print(final_otp)           
    return final_otp            
    
        