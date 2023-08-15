from login import Login
from Search import Search
from Scraper import Scraper
from urllib.parse import urlparse
import json
from Clinic import ClinicSwitch
from blob import create_blob_from_message
import datetime
def getdata(key):
    with open("config.json", "r") as f:
        data = json.loads(f.read())
        return data[key]
def responsemaker(InputParameters,final_data,message_id):    
    date_time = datetime.datetime.now()    
    date=date_time.strftime("%d-%m-%Y")
 
    filename=f"{InputParameters['AppName']}/{InputParameters['PayorName']}/{date}/{message_id}.txt"       
    url =create_blob_from_message(filename, json.dumps(final_data,indent=4), 'text') 
    return url    
   
def start(data,message_id,browser,patient):
    InputParameters =data['InputParameters']
    payorname         =  InputParameters.get("PayorName")
    website=data['Login']
    url                  =      website['Url']
    username             =      website['LoginId']
    password             =      website['Password']
    OtpRequired          =      website['OtpRequired']
    print(OtpRequired)
    OtpEmail             =      website['OtpEmail']
    OtpEmailPassword     =      website.get('OtpEmailPassword',"")
    EmailProvierUrl      =      website.get('EmailProvierUrl',"")
    WebsiteId__          =      InputParameters.get("WebsiteId","")
    
    ScrapingXpaths =[json.loads(x['XPath'])['Xpaths'] for x in data['Xpaths'] if  x['DataContextName']=='EligibilityLogin'][0][0]
    OtpInstructions         =         ScrapingXpaths.get('OtpInstructions',{})    
    OtpEmail                =         OtpInstructions.get('OtpEmail')
    OtpEmailPassword        =         OtpInstructions.get('OtpEmailPassword')
    FromEmail               =         OtpInstructions.get('FromEmail')
    #OtpRegex                =         str(OtpInstructions.get('OtpRegex'))
    
    EmailTitle_              =         OtpInstructions.get('EmailTitle')
    tenantID                =         OtpInstructions.get("tenantID")
    clientID                =         OtpInstructions.get("clientID")
    clientSecret            =         OtpInstructions.get("clientSecret")
    ImapSecret               =       {"tenantID":tenantID,"clientID":clientID,"clientSecret":clientSecret}
    SMTPAddress             =         OtpInstructions.get("SMTPAddress")
    EncryptionType          =         OtpInstructions.get("EncryptionType")
    ImapType                   =         OtpInstructions.get("ImapType")
    otpwait                 =         OtpInstructions.get("OtpWait")
    
    username_xpath       =         ScrapingXpaths['UsernameXpath']   
    password_xpath       =         ScrapingXpaths['PasswordXpath'] 
    login_button_xpath   =         ScrapingXpaths['LoginButtonXpath']
    Otp_input_button_xpath  =      ScrapingXpaths['OtpInputXpath']
    Otp_submit_button_xpath =      ScrapingXpaths['OtpSubmitXpath']
    otp_preSteps           =       ScrapingXpaths['PreSteps']
    
    otp_postSteps          =       ScrapingXpaths['PostSteps']
    otp_xpath              =       ScrapingXpaths['OtpXpath']
    LoginAdditionalInfo    =       ScrapingXpaths.get("AdditionalInfo",{})

    search_main=data['SearchParameters'][0]['JsonSettings']
   
    search=json.loads(search_main)['Search']['Settings']
    pre_steps            =      search['PreSteps']
    search_button_xpath  =      search['SearchButtonXpath']
    post_step            =      search['PostSteps']
    search_filters       =      search.get('SearchFilter',{})
    
      
    ScrapingXpaths_=[x for x in data['Xpaths'] if  x['DataContextName'] not in ['EligibilityLogin','ClinicSwitch'] ] #[x for x in data['ScrapingXpaths'] if x['DataContextName']!='EligibilityLogin']
          
    scraper_=Scraper(browser,ScrapingXpaths_,InputParameters,message_id,patient)

    scraped_data=scraper_.Scrap()
    
    return scraped_data
        


def kickoff(message,message_id,browser,patient):      
    return start(message,message_id,browser,patient)
