from selenium import webdriver
#import undetected_chromedriver as webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from imapsetup import  OtpFetcher
from imapsetup import OtpFetch
import os
import json
import requests
import traceback
from time import sleep

from constants import DD_PAYOR_NAMES

# import otp_manager

def captcha_solver(browser,wait,iframexpath,aftercaptchaxpath):
    print('Captcha solving<<<<<<<<<<<<<<<<<<<<<<<<')
    limit =0
    if iframexpath != "":
        try:
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframexpath)))
        except:
            pass
    while True:
        status=""
        try:
            status=browser.find_element(By.XPATH,"//a[@class='status']").text
            print(status+str(limit))
        except:
            pass    
        if aftercaptchaxpath != "":
            try:
                browser.find_element(By.XPATH, aftercaptchaxpath)
                print('Login Successful')
                break
            except:
                pass
        if 'solved' in status.lower():
            sleep(2)            
            print('Captcha solved')
            break
        limit+=1
        print(limit)
        sleep(0.25)
        if 800 < limit:
            break
def OtpQueueChecker(payorname,otp_email):
    count=0
    round_ =0
    while True:
        if OtpFetch.AddOtp(payorname,otp_email):
            return True
        else:
            sleep(10)
            count+=10
        if count >=200:
            break
            #OtpFetch.DeleteOtp_(payorname,otp_email)
      





class Login:
    
    def __init__(self,
                 url: str ,
                 userid: str,
                 password: str,
                 username_box_xpath: str,
                 password_box_xpath: str,
                 login_button_xpath: str,
                 otp_required: bool,
                 is_topt_required: bool,
                 otp_email:str,
                 otp_input_button_xpath: str,
                 otp_submit_button_xpath: str,
                 otpemailpassword:str,
                 imaphost:str,
                 otp_xpath:str,
                 otp_wait:int,
                 preSteps:list,
                 postSteps:list,
                 website_id:str,
                 additionalInfo:dict,
                 EmailTitle:str,
                 ImapSecret:dict,
                 SMTPAddress:str,
                 EncryptionType:str,
                 ImapType:str,
                 FromEmail:str,
                 payorname:str


              
               
                 ):
        
        self.url                = url
        self.userid             = userid
        self.password           = password        
        self.username_box_xpath = username_box_xpath
        self.password_box_xpath = password_box_xpath
        self.login_button_xpath = login_button_xpath
        self.is_topt_required = is_topt_required
        self.otp_required = otp_required
        self.otp_email = otp_email
        self.otp_input_button_xpath = otp_input_button_xpath
        self.otp_submit_button_xpath = otp_submit_button_xpath        
        self.otpemailpassword=otpemailpassword
        self.imaphost=imaphost
        self.preSteps = preSteps
        self.postSteps = postSteps
        self.otp_xpath=otp_xpath
        self.otp_wait = otp_wait  
        self.website_id=website_id 
        self.additionalInfo = additionalInfo
        self.EmailTitle   =EmailTitle
        self.ImapSecret   =ImapSecret
        self.SMTPAddress  =SMTPAddress
        self.EncryptionType =EncryptionType
        self.ImapType     =ImapType
        self.FromEmail       = FromEmail 
        self.payorname    =payorname
    
    def __str__(self):
        return f"{self.url}"
   
   # @log_decorator("login_Function")   
   #        
    def performlogin(self):  
        display =None    
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            # if self.payorname in DD_PAYOR_NAMES:
            #     chrome_options.add_argument("--proxy-server=2.56.119.93:5074")
            # if self.additionalInfo.get("headless")==False:
            #     from pyvirtualdisplay import Display
            #     display = Display(visible=0, size=(1024, 768))
            #     display.start()
            # else:
            #     chrome_options.add_argument('--headless')
                         
            path_=os.path.join(os.getcwd(), 'download')
            prefs = {"download.default_directory" : path_}
                
            chrome_options.add_argument('--disable-dev-shm-usage')
            settings = {
                "recentDestinations": [{
                    "id": "Save as PDF",
                    "origin": "local",
                    "account": "",
                }],
                "selectedDestinationId": "Save as PDF",
                "version": 2
            }
            prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
                    'savefile.default_directory': path_,
                    "download.prompt_for_download": False, "plugins.always_open_pdf_externally": True,
                    "download.default_directory": path_}
        
            chrome_options.add_experimental_option('prefs', prefs)
            if self.additionalInfo.get('IsCaptchaRequired'):
                ext_file=os.path.join(os.getcwd(), 'extensions','captcha')
                print(ext_file)
                chrome_options.add_argument(f"--load-extension={ext_file}")

            chrome_options.add_argument('--kiosk-printing')
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.set_window_size(1920, 1080)
            wait = WebDriverWait(browser,40) 
            browser.get(self.url)
            if self.additionalInfo.get("Script"):            
                Script=self.additionalInfo.get("Script")            
                if Script.get("AfterPageLoad"):
                    print(Script.get("AfterPageLoad").get("js"))
                    browser.execute_script(Script.get("AfterPageLoad").get("js"))

            if self.additionalInfo:
                if len(self.additionalInfo) != 0:
                    if self.additionalInfo.get("PreStepExceptionClicks"):
                        for step in self.additionalInfo.get("PreStepExceptionClicks").get("Click"):
                            print(step, "In Exception <<<<<<<<<<<<<<<<<<<<<<<")
                            try:
                                wait.until(EC.element_to_be_clickable((By.XPATH, step))).click()
                            except:
                                pass    
        

            if len(self.preSteps)!=0:
                for step in self.preSteps:
                    print(step,"<<<<<<<<<<<<<<<<<<<<<<<")                
                    wait.until(EC.element_to_be_clickable((By.XPATH,step))).click()
            
            wait.until(EC.element_to_be_clickable((By.XPATH,self.username_box_xpath))).send_keys(self.userid)
            if self.additionalInfo:
                if len(self.additionalInfo)!=0:
                    add_Info=self.additionalInfo
                    if add_Info.get("StepsAfterUsernameInput"):
                        if add_Info.get("StepsAfterUsernameInput").get("Click"):
                            for clk in add_Info.get("StepsAfterUsernameInput").get("Click"):
                                wait.until(EC.element_to_be_clickable((By.XPATH,clk))).click()
                            
                            SecurityQuestions =add_Info.get("Security")
                            
                            if SecurityQuestions:
                                SecurityQuestions =add_Info.get("Security").get("SecurityQuestions")
                                for qna in SecurityQuestions:
                                    Question     =     qna.get("Question")
                                    Answer       =     qna.get("Answer")
                                    Answer_Xapth =     qna.get("AnswerXpath")
                                    
                                    wait.until(EC.element_to_be_clickable((By.XPATH,Answer_Xapth))).send_keys(Answer)
                                    
                                PostClicks =add_Info.get("Security").get("PostClicks")     
                                for clk in PostClicks:                           
                                        wait.until(EC.element_to_be_clickable((By.XPATH,clk))).click()
                            
                                
                                
            wait.until(EC.element_to_be_clickable((By.XPATH,self.password_box_xpath))).send_keys(self.password)   
            # Generates and sends Time based otp(i.e. TOPT) to the input field.
            # if self.is_topt_required:
            #     browser.find_element(By.XPATH, self.login_button_xpath).click()
            #     sleep(3)
            #     otp_code = otp_manager.get_totp()
            #     wait.until((EC.element_to_be_clickable((By.XPATH,self.otp_input_button_xpath)))).send_keys(otp_code)
            #     wait.until((EC.element_to_be_clickable((By.XPATH,self.otp_submit_button_xpath)))).click()
            #     return browser,True,display,""
            
            iframexpath = ""
            aftercaptchaxpath = ""
            if self.additionalInfo.get('iframexpath'):
                if len(self.additionalInfo.get('iframexpath'))!=0:
                    iframexpath = self.additionalInfo.get('iframexpath')

            if self.additionalInfo.get('aftercaptchaxpath'):
                if len(self.additionalInfo.get('aftercaptchaxpath'))!=0:
                    aftercaptchaxpath = self.additionalInfo.get('aftercaptchaxpath')

            if self.additionalInfo.get('IsCaptchaRequired'):
                if self.additionalInfo.get("AfterCredentialsCaptcha"):                
                    print('Wait for captcha')
                    captcha_solver(browser,wait,iframexpath,aftercaptchaxpath) 
            if len(self.otp_input_button_xpath)>0:
                OtpQueueChecker(self.payorname,self.otp_email)             
            browser.find_element(By.XPATH, self.login_button_xpath).click()        
            if self.additionalInfo.get('IsCaptchaRequired'):
                if self.additionalInfo.get("AfterloginCaptcha"):                
                    print('Wait for captcha')
                    captcha_solver(browser,wait,iframexpath,aftercaptchaxpath)
                    
            if len(self.postSteps)!=0:
                for step in self.postSteps:
                    try:                                       
                        wait.until(EC.element_to_be_clickable((By.XPATH,step))).click()                         
                    except:                    
                        pass    

            print(self.otp_input_button_xpath)
            if self.otp_input_button_xpath:
                if len(self.otp_input_button_xpath)>0:
                    try:
                        WebDriverWait(browser,8).until(EC.element_to_be_clickable((By.XPATH,self.otp_input_button_xpath)))
                        self.otp_required=True
                    except:
                        self.otp_required=False
            
            
            if self.otp_required==True:                                          
                OtpHandler=OtpFetcher.OtpFetcher(

                    OtpXpath      =    self.otp_xpath,
                    EmailTitle    =    self.EmailTitle,
                    tenantID      =    self.ImapSecret["tenantID"],
                    clientID      =    self.ImapSecret["clientID"],
                    clientSecret  =    self.ImapSecret["clientSecret"],
                    username      =    self.otp_email,
                    sleep_time    =    self.otp_wait
                    
                )   
                
                otp_code=OtpFetch.OtpFetch(self.payorname,self.otp_email,OtpHandler)
                wait.until((EC.element_to_be_clickable((By.XPATH,self.otp_input_button_xpath)))).send_keys(otp_code)
                wait.until((EC.element_to_be_clickable((By.XPATH,self.otp_submit_button_xpath)))).click()
                try: OtpFetch.DeleteOtp_(self.payorname,self.otp_email)
                except: pass                
            try: OtpFetch.DeleteOtp_(self.payorname,self.otp_email)
            except: pass
            return browser,True,display,""
                
        except Exception as e:
            if len(self.otp_input_button_xpath)>0:
                try: OtpFetch.DeleteOtp_(self.payorname,self.otp_email)
                except: pass
                

            print(traceback.format_exc())

            return browser,False,display,traceback.format_exc()                         
        
            
            

                
