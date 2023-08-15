import sys

sys.path.append('imapsetup')
from WraperHandler import WraperHandler
import traceback

from azure_queue import QueueHandler
from login import Login
from Search import Search
from Scraper import Scraper
import json
from Clinic import ClinicSwitch
from base64 import b64encode,b64decode
from blob import create_blob_from_message
from downloader import  upload_to_blob
from wrapers import requesthandler
from azure.storage.blob import BlobServiceClient
from DDscrap import main as ddscrap
import datetime
import os
import random
import string
import requests
from time import sleep
from common.functions import screenshot,upload_image_to_azure

from constants import ELIGIBILITY_FILE_CONTEXT_NAME, CLAIM_FILE_CONTEXT_NAME

if not os.path.exists('download'):  
  os.makedirs('download')

#s  
def getdata(key):
    with open("config.json", "r") as f:
        data = json.loads(f.read())
        return data[key]
def responsemaker(InputParameters,final_data,message_id):    
    date_time = datetime.datetime.now()    
    date=''.join(random.choices(string.ascii_uppercase +string.digits, k=10))
    filename=f"{InputParameters['AppName']}/{InputParameters['PayorName']}/{date}/{message_id}.txt"       
    url =create_blob_from_message(InputParameters,filename, json.dumps(final_data,indent=4), 'text') 
    return url    
def api_post(ScheduleId,InputParameters):
    
    url =getdata(InputParameters['AppName']).get("ApiUrl")
    print("urllllllllllllllllllllllllllllll",url)
    payload = {"RequestData": None, "ScheduleId": ScheduleId, "JobStatus": "Completed",
            "Exception": None}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI5YTFhODQ3YS1mZjY3LTQ5MDctOGZlMC0wZDcyZWU0MjZlN2MiLCJ1bmlxdWVfbmFtZSI6ImV2VXNlcjEiLCJhdXRoX3RpbWUiOiI5LzYvMjAyMiA2OjMwOjM0IEFNIiwianRpIjoiZWRkYjM5NzUtZmVjOC00NDEwLTkzZGMtN2RlMzU3ODBmMWIyIiwiYXVkIjpbIlNpbXBsaWZpRGVudGlzdHJ5LmNvbSIsIlNpbXBsaWZpRGVudGlzdHJ5LmNvbSJdLCJpc3MiOiJCUEtUZWNoLmNvbSIsIklzc3VlZEF0IjoiMTIvNS8yMDIyIDU6Mzg6NDYgQU0iLCJDcmVhdGVkRGF0ZSI6IjkvNi8yMDIyIDY6MzA6MzQgQU0iLCJJc0FjdGl2ZSI6IlRydWUiLCJDbGllbnRJZCI6Ijg4YjgwNTAwLWQ1YTktNGM0MC1hNzUzLTM0ZTQzNjk1YzY5ZSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkNsaWVudFVzZXIiLCJuYmYiOjE2NzAyMTg3MjYsImV4cCI6MTY3MDIyNTkyNn0.IXdHFIqjhCg4AM7sAIVTGhQe-JAK4Uf_3q8oJU2koU0',
        'Content-Type': 'application/json',
        'Cookie': 'ARRAffinity=22a7daa836b64a8ce56c907737553d08297ff2e76cd06a1f52c29956b9a85c17; ARRAffinitySameSite=22a7daa836b64a8ce56c907737553d08297ff2e76cd06a1f52c29956b9a85c17'
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response)

def ErrorPoster(InputParameters,error_message,inputurl,queuename):
    
    handler =QueueHandler(InputParameters['AppName'])
    handler.queue_name =queuename
    error_message["InputURL"] =inputurl
    error_message["PayorName"]=InputParameters.get("PayorName")
    handler.send_message(b64encode(bytes(json.dumps(error_message,indent=4), 'utf-8')).decode('utf-8'))

def close_other_tabs(driver):
    num_tabs = len(driver.window_handles)
    if num_tabs > 1:
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()
        driver.switch_to.window(driver.window_handles[0])

def start(data,message_id,inputurl):
    

    data_req                                  =      data
    RequestReceivedFromQueue                  =      None
    loginStartTime                            =      None
    PatientSearchTimeStart                    =      None
    PatientSearchTimeEnd                      =      None
    ScrapingTimeStart                         =      None
    ScrapingTimeEnd                           =      None
    WraperStartTime                           =      None
    WraperEndTime                             =      None
    QueueTimeStart                            =      None
    QueueTimeEnd                              =      None
    RequestReceivedFromQueue                  =      datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data                                      =      requesthandler.requestmaker(data)
    InputParameters                           =      data['InputParameters']
    payorname                                 =      InputParameters.get("PayorName")
    os.environ['ConnectionString']            =      getdata(InputParameters["AppName"])["AZURE_STORAGE_CONNECTION_STRING"]
    os.environ['IMAPTableName']               =      getdata(InputParameters["AppName"])["IMAPTableName"]
    os.environ['container_name_blob']               =      getdata(InputParameters["AppName"])["container_name_blob"]
    website                                   =      data['Login']
    url                                       =      website['Url']
    username                                  =      website['LoginId']
    password                                  =      website['Password']
    OtpRequired                               =      website['OtpRequired']
    print(OtpRequired)
    is_topt_required                          =      website.get('IsTOTPRequired', False)
    OtpEmail                                  =      website['OtpEmail']
    OtpEmailPassword                          =      website.get('OtpEmailPassword',"")
    EmailProvierUrl                           =      website.get('EmailProvierUrl',"")
    WebsiteId__                               =      InputParameters.get("WebsiteId","")
    
    ScrapingXpaths                            =      [json.loads(x['XPath'])['Xpaths'] for x in data['Xpaths'] if  x['DataContextName']=='EligibilityLogin'][0][0]
    OtpInstructions                           =      ScrapingXpaths.get('OtpInstructions',{})    
    OtpEmail                                  =      OtpInstructions.get('OtpEmail')
    OtpEmailPassword                          =      OtpInstructions.get('OtpEmailPassword')
    FromEmail                                 =      OtpInstructions.get('FromEmail')
    
    EmailTitle_                               =      OtpInstructions.get('EmailTitle')
    tenantID                                  =      OtpInstructions.get("tenantID")
    clientID                                  =      OtpInstructions.get("clientID")
    clientSecret                              =      OtpInstructions.get("clientSecret")
    ImapSecret                                =      {"tenantID":tenantID,"clientID":clientID,"clientSecret":clientSecret}
    SMTPAddress                               =      OtpInstructions.get("SMTPAddress")
    EncryptionType                            =      OtpInstructions.get("EncryptionType")
    ImapType                                  =      OtpInstructions.get("ImapType")
    otpwait                                   =      OtpInstructions.get("OtpWait")
    
    username_xpath                            =      ScrapingXpaths['UsernameXpath']   
    password_xpath                            =      ScrapingXpaths['PasswordXpath'] 
    login_button_xpath                        =      ScrapingXpaths['LoginButtonXpath']
    Otp_input_button_xpath                    =      ScrapingXpaths['OtpInputXpath']
    Otp_submit_button_xpath                   =      ScrapingXpaths['OtpSubmitXpath']
    otp_preSteps                              =      ScrapingXpaths['PreSteps']
    
    otp_postSteps                             =       ScrapingXpaths['PostSteps']
    otp_xpath                                 =       ScrapingXpaths['OtpXpath']
    LoginAdditionalInfo                       =       ScrapingXpaths.get("AdditionalInfo",{})

    
    if InputParameters['AppName']==   "Eligibility":
        file_context_name = ELIGIBILITY_FILE_CONTEXT_NAME
    elif InputParameters['AppName']==   "Revenue Cycle Management":
        file_context_name = CLAIM_FILE_CONTEXT_NAME
    else:
        file_context_name = 'Files'

    loginStartTime =datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    login_                                    =         Login(      
                                                                    url  =url,
                                                                    userid=username,
                                                                    password=password,
                                                                    username_box_xpath= username_xpath,
                                                                    password_box_xpath=password_xpath,
                                                                    login_button_xpath= login_button_xpath,
                                                                    otp_required= OtpRequired,
                                                                    is_topt_required=is_topt_required,
                                                                    otp_email=  OtpEmail,
                                                                    otp_input_button_xpath= Otp_input_button_xpath,
                                                                    otp_submit_button_xpath= Otp_submit_button_xpath,
                                                                    otpemailpassword=OtpEmailPassword,
                                                                    imaphost= EmailProvierUrl,
                                                                    preSteps=  otp_preSteps,
                                                                    postSteps=  otp_postSteps,
                                                                    otp_xpath= otp_xpath,
                                                                    otp_wait=   otpwait,
                                                                    website_id=WebsiteId__,
                                                                    additionalInfo=LoginAdditionalInfo,
                                                                    EmailTitle =EmailTitle_,
                                                                    ImapSecret=ImapSecret,
                                                                    SMTPAddress=SMTPAddress,
                                                                    EncryptionType=EncryptionType,
                                                                    ImapType=ImapType,
                                                                    FromEmail=FromEmail,
                                                                    payorname=payorname
                                                             )
    browser=None
    is_loggedIn =None
  
    browser,is_loggedIn ,s,a   =         login_.performlogin()    
    if not is_loggedIn:        
        for patient in data['PatientData']:
            final = {
                        "ClientId": InputParameters['ClientId'],
                        "PayorId": InputParameters['PayorId'],
                        "AppName": InputParameters['AppName'],  
                        "BatchId": InputParameters.get("BatchId"),
                        "EligibilityVerificationId": patient['EligibilityVerificationId'],
                        "ClinicServerId": patient['ClinicServerId'],
                        'PatientId': patient.get('PatientId'),
                        "IsError":True,      
                        "Message" :"",                  
                        "ErrorMessage": "Login failed",
                        "ScrappingSource" : "SD",                    
                        "Data": None
                    }
            #QueueHandler(InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final,indent=4), 'utf-8')).decode('utf-8'))
            screenshot(browser)
            screenshot_url =upload_image_to_azure("combined_image.png", "files",getdata(InputParameters['AppName']).get("connect_str_blob") )
            final["screenshot"] = screenshot_url
            final[file_context_name] = {"ErrorScreenshots": [{"url": screenshot_url, "description":""}]}
            #ErrorPoster(InputParameters,final,inputurl,getdata(InputParameters['AppName']).get("ErrorQueue"))   
        browser.quit()    
        return    
    
    if(InputParameters.get("PayorName")=="Guardian"):
        sleep(100)
    loginEndTime=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")  
    if InputParameters.get('ClinicDetails'):
        data_clinic=[json.loads(x['XPath']) for x in data['Xpaths'] if  x['DataContextName']=='ClinicSwitch']
        if len(data_clinic)!=0:
            clinic_main=data_clinic[0]    
            clinic=clinic_main['Search']['Settings']
            
            pre_steps_            =      clinic['PreSteps']
            search_button_xpath_  =      clinic['SearchButtonXpath']
            post_step_           =      clinic['PostSteps']
            search_filters_       =      clinic['SearchFilter']    
            queries_=clinic_main['Search']['Queries']      
            s=ClinicSwitch(browser,pre_flow=pre_steps_,post_flow=post_step_,search_button_path=search_button_xpath_,queries=queries_,clinic_details=InputParameters['ClinicDetails'],search_filters=search_filters_)
            try:
                s.performS()
            except:
                final = {
                    "ClientId": InputParameters['ClientId'],
                    "PayorId": InputParameters['PayorId'],
                    "AppName": InputParameters['AppName'],
                    "IsError":True,
                    "ErrorMessage": "Clinic switch failed",
                    "Data": None}
                
          
                #QueueHandler(InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final,indent=4), 'utf-8')).decode('utf-8'))   
                
                                                
                
    PatientData = data['PatientData']
    ScrapingXpaths_=[x for x in data_req['Xpaths'] if  x['DataContextName'] not in ['EligibilityLogin','ClinicSwitch'] ]
    for patient in PatientData:
        PatientSearchTimeStart=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        found=False
        search_parameters = data['SearchParameters']
        for index, search_parameter in enumerate(search_parameters):
            json_settings = search_parameter['JsonSettings']
        
            search=json.loads(json_settings)['Search']['Settings']

            pre_steps                                 =      search['PreSteps']
            search_button_xpath                       =      search['SearchButtonXpath']
            post_step                                 =      search['PostSteps']
            search_filters                            =      search.get('SearchFilter',{})
            queries=json.loads(json_settings)['Search']['Queries']
            
            s1=Search(browser,  pre_steps , post_step, search_button_xpath, queries,patient,search_filters)
            is_searched, err_traceback = s1.performS()
            if is_searched:
                print("=====================Patient searched successfully.")
                found=True
                break
            print("=============================Iteration: ", index, "Could not search patient.")

        PatientSearchTimeEnd=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                      
        for contexts in ScrapingXpaths_:
            Xpaths=json.loads(contexts['XPath'])
            core=Xpaths.get("forCore")
            print(core)
            if core==False:
                ScrapingXpaths_.remove(contexts)

       
        if found:
            ScrapingTimeStart=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")          
            scraper_=Scraper(browser,ScrapingXpaths_,InputParameters,message_id,patient)
            try:
                scraped_data=scraper_.Scrap()
                name = patient.get("PatientId")
                with open(f"output_{name}.json", "w") as f:
                    f.write(json.dumps(scraped_data, indent=4))
            except Exception  as e:
                print("Scrapper Exception: ", e)
                final= {
                            "ClientId": InputParameters['ClientId'],
                            "PayorId": InputParameters['PayorId'],
                            "AppName": InputParameters['AppName'],
                             "BatchId": InputParameters.get("BatchId"),
                            "EligibilityVerificationId": patient['EligibilityVerificationId'],
                            "ClinicServerId": patient['ClinicServerId'],
                            'PatientId': patient.get('PatientId'),
                            "IsError":True,
                            "Message":"Core Scraping Failed",
                            "ErrorMessage": "Extraction Failed",
                            "ScrappingSource" : "SD",
                            "Data":None
                        }
                #QueueHandler(InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final,indent=4), 'utf-8')).decode('utf-8')) 
                final["DetailError"] = traceback.format_exc()  
                #ErrorPoster(InputParameters,final,inputurl,getdata(InputParameters['AppName']).get("ErrorQueue"))  
                
            
            for contexts in ScrapingXpaths_:
                datacontext = contexts["DataContextName"]
                Xpaths=json.loads(contexts['XPath'])
                Scraping=Xpaths.get("Scraping")
                if Scraping ==False:
                    del scraped_data[datacontext]

                
            ScrapingTimeEnd=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                     
            WraperStartTime =   datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") 
            try:
                scraped_data  = WraperHandler(InputParameters,data,scraped_data,patient,browser)
            except Exception as e:
                print("Wrapper Exception: ", e)      
                print(traceback.format_exc())                                                            
                final = {
                            "ClientId": InputParameters['ClientId'],
                            "PayorId": InputParameters['PayorId'],
                            "AppName": InputParameters['AppName'],
                            "BatchId": InputParameters.get("BatchId"),
                            "EligibilityVerificationId": patient['EligibilityVerificationId'],
                            "ClinicServerId": patient['ClinicServerId'],
                            'PatientId': patient.get('PatientId'),
                            "IsError":True,
                            "Message":"Wrapper Failed",
                            "ErrorMessage": "Extraction Failed",
                            "ScrappingSource" : "SD",
                            "Data":None
                        }

                #QueueHandler(InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final,indent=4), 'utf-8')).decode('utf-8'))   
                final["DetailError"] = traceback.format_exc()
                #ErrorPoster(InputParameters,final,inputurl,getdata(InputParameters['AppName']).get("ErrorQueue"))    
                
                

                                                
            WraperEndTime =datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")    
            QueueTimeStart =  datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            for i in scraped_data:
                count =0             
                for ctxt in scraped_data[i]:
                    if type(ctxt).__name__=="dict":
                        ctxt['ClientId']=InputParameters.get('ClientId')
                        ctxt['EligibilityVerificationId']=patient.get('EligibilityVerificationId')
                        if patient.get('PatientId'):
                            ctxt['PatientId']=patient.get('PatientId')
                        if patient.get("RcmGridViewId"):
                            ctxt['RcmGridViewId']=patient.get("RcmGridViewId")
                        if patient.get("PPGridViewId"):
                            ctxt['PPGridViewId']=patient.get("PPGridViewId")             
                        if InputParameters['AppName']==   "Revenue Cycle Management":
                            ctxt["PMSSubscriberId"]=patient.get("SubscriberId")  
                        ctxt['RecordId'] =count
                        count+=1

                    else:
                        count =0 
                        for dct in ctxt:
                            if InputParameters['AppName']==   "Revenue Cycle Management":
                                ctxt["PMSSubscriberId"]=patient.get("SubscriberId")                                                    
                            dct['ClientId']=InputParameters.get('ClientId')
                            dct['EligibilityVerificationId']=patient.get('EligibilityVerificationId')
                            if patient.get('PatientId'):
                                dct['PatientId']=patient.get('PatientId')
                            if patient.get("RcmGridViewId"):                
                                dct['RcmGridViewId']=patient.get("RcmGridViewId")
                            if patient.get("PPGridViewId"):
                                ctxt['PPGridViewId']=patient.get("PPGridViewId") 
                            ctxt['RecordId'] =count
                            count+=1

                          
                data_=[]                
                if type(scraped_data[i]).__name__=="dict":                    
                    data_= [scraped_data[i]]
                else:
                    data_=scraped_data[i]
 

                if InputParameters['AppName'] =='Eligibility':               
                    final_data = {               
                        "ClientId": InputParameters['ClientId'],
                        "DataContextName":i, 
                        "PayorId": InputParameters['PayorId'],
                        "AppName": InputParameters['AppName'],
                        "BatchId": InputParameters.get("BatchId"),
                        "EligibilityVerificationId": patient.get('EligibilityVerificationId'),
                        "ClinicServerId": patient.get('ClinicServerId'),
                        'PatientId': patient.get('PatientId'),
                        "IsError":False,

                        "Message":"",
                        "ErrorMessage": "",
                         "ScrappingSource" : "SD",
                        "Data": responsemaker(InputParameters,data_,f"{message_id}_{i}")}

                    #QueueHandler( InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final_data,indent=4), 'utf-8')).decode('utf-8'))
                    #ErrorPoster(InputParameters,final_data,inputurl,"testqueueoutgoing")
                    

                    
            if InputParameters.get("ScheduleId"):                
                ScheduleId=InputParameters.get("ScheduleId")                        
                if ScheduleId > 0:                    
                    api_post(ScheduleId,InputParameters)
                    
            if  InputParameters['AppName']==   "Revenue Cycle Management":              
                if InputParameters['PayorName'] == "Government Employees Health Association-GEHA":
                    from wrapers import GehaRcm
                    scraped_data=GehaRcm.main(scraped_data)    
                   
                final_data = {
                "ClientId": InputParameters['ClientId'],            
                "PayorId": InputParameters['PayorId'],
                "AppName": InputParameters['AppName'],
                "EligibilityVerificationId": patient['EligibilityVerificationId'],
                "ClinicServerId": patient['ClinicServerId'],
                'PatientId': patient.get('PatientId'),
                "IsError":False,
                "ErrorMessage": "",
                "Data": responsemaker(InputParameters,scraped_data,message_id)}                        
                print(final_data)
                name = patient.get("PatientId")
                with open(f"wrapper_{name}.json", "w") as f:
                    f.write(json.dumps(scraped_data, indent=4))        
                #QueueHandler( InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final_data,indent=4), 'utf-8')).decode('utf-8'))  
                if InputParameters.get("ScheduleId"):
                    ScheduleId=InputParameters.get("ScheduleId")
                    if ScheduleId > 0:
                        api_post(ScheduleId,InputParameters)  

        else:
            final = {
                "ClientId": InputParameters['ClientId'],
                "PayorId": InputParameters['PayorId'],
                "AppName": InputParameters['AppName'],
                "EligibilityVerificationId": patient['EligibilityVerificationId'],
                "BatchId": InputParameters.get("BatchId"),
                "ClinicServerId": patient['ClinicServerId'],
                'PatientId': patient.get('PatientId'),
                 "IsError":True,
                 "Message":"Search Failed",
                "ErrorMessage": "Patient not found",
                 "ScrappingSource" : "SD",
                "Data":None}
            ScrapingXpaths_copy =[]
            screenshot(browser)
            screenshot_url =upload_image_to_azure("combined_image.png", "files",getdata(InputParameters['AppName']).get("connect_str_blob") )
            final["screenshot"] = screenshot_url
            final[file_context_name] = {"ErrorScreenshots": [{"url": screenshot_url, "description":""}]}
            for contexts in ScrapingXpaths_:
                datacontext = contexts["DataContextName"]
                if "SearchDashboardFilter" ==contexts["DataContextName"]:
                    ScrapingXpaths_copy.append(contexts)
            if len(ScrapingXpaths_copy)>0:
                Scraper(browser,ScrapingXpaths_copy,InputParameters,message_id,patient).Scrap()     
                
            #QueueHandler(InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final,indent=4), 'utf-8')).decode('utf-8'))   
            # screenshot(browser)
            # screenshot_url =upload_image_to_azure("combined_image.png", "files",getdata(InputParameters['AppName']).get("connect_str_blob") )
            # final["screenshot"]=screenshot_url            
            #ErrorPoster(InputParameters,final,inputurl,getdata(InputParameters['AppName']).get("ErrorQueue"))    
                                            
        QueueTimeEnd=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        Audit = {"RequestReceivedFromQueue": RequestReceivedFromQueue,
                 "loginStartTime": loginStartTime, 
                 "loginEndTime": loginEndTime,
                 "SearchStartTime":PatientSearchTimeStart,
                 "SearchEndTime":PatientSearchTimeEnd,
                 "ScrapingTimeStart":ScrapingTimeStart,
                 "ScrapingTimeEnd":ScrapingTimeEnd,
                 "WrapperStartTime":WraperStartTime,
                 "WrapperEndTime":WraperEndTime,
                 "QueueResponseStartTime":QueueTimeStart,
                 "QueueResponeEndTime":QueueTimeEnd,
                 }
        print(json.dumps(Audit,indent=4))
        close_other_tabs(browser)
        print(json.dumps(Audit,indent=4))
        name = patient.get("PatientId")
        with open(f"wrapper_{name}.json", "w") as f:
            f.write(json.dumps(scraped_data,indent=4))
        
        
        # final_audit={   "ClientId": InputParameters['ClientId'],
        
        #     "PayorId": InputParameters['PayorId'],
        #     "AppName": InputParameters['AppName'],
        #     "PatientId":PatientData[0].get('PatientId'),
        #     "DataContextName":"TimeLogs",
        #     "MessageId":message_id,
        #     "IsError":False,
        #     "ErrorMessage": "",
        #     "Data": responsemaker(InputParameters,Audit,message_id)}
        # responsemaker(InputParameters,data_,f"{message_id}_{i}")
        # #QueueHandler(InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final_audit,indent=4), 'utf-8')).decode('utf-8'))
      
    browser.quit()


def kickoff(message,message_id,inputurl):
    print( message.get("InputParameters").get("WebsiteId"))
    if message.get(
        "InputParameters").get("WebsiteId","") =="DELTADENTAL_001":
        print("ss")
        ddscrap(message,message_id)
    else:
        start(message,message_id,inputurl)
       
            


def kickoff(message,message_id):
    start(message,message_id,"")

d=json.loads(open("ddwashinton.json","r").read())
kickoff(d,"8a7f3sd254221edssd")
