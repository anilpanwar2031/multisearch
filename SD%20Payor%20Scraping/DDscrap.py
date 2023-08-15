from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from azure_queue import QueueHandler
from blob import create_blob_from_message
from downloader import upload_to_blob
from base64 import b64encode,b64decode
import json, datetime, os
from mapPDF import mapEligibilityPatientVerification
def changeZero(a):
    if(a=="0"):
        return "$0.0"
    else: return a
def changeNone(val):
    if(val==None or val=="N/A"):
        return ""
    else:
        return val
def get_remaining(type, category, servicecategory, t):
    for x in t:
        if(x.get("Type")==f"Remaining {type}" and x.get("ServiceCategory")==servicecategory):
            return x.get(category)
def getdata(key):
    with open("config.json", "r") as f:
        data = json.loads(f.read())
        return data[key]
def responsemaker(InputParameters,final_data,message_id):    
    date_time = datetime.datetime.now()    
    date=date_time.strftime("%d%m%Y%H%M%S")
 
    filename=f"{InputParameters['AppName']}/{InputParameters['PayorName']}/{date}/{message_id}.txt"       
    url =create_blob_from_message(InputParameters,filename, json.dumps(final_data,indent=4), 'text') 
    return url
def calculate_difference(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)-float(b)}'
def spawn_driver():
    chrome_options = webdriver.ChromeOptions()
    caps = DesiredCapabilities().CHROME
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver=webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=caps)
    driver.set_window_size(1920, 1080)
    return driver
def login(url,  username, password):
    driver=spawn_driver()
    driver.get(url)
    sleep(10)
    count=0
    while count<1000:
        try:
            driver.find_element(by=By.XPATH, value="//a[@href='#link-4']").click()
            break
        except:
            count+=1
            sleep(0.01)
    if(count==1000):
        return driver, 1
    while count<1000:
        try:
            driver.find_element(by=By.XPATH, value="//a[text()='Sign in']").click()
            break
        except:
            count+=1
            sleep(0.01)
    if(count==1000):
        return driver, 1
    while count<1000:
        try:
            driver.find_element(by=By.XPATH, value="//input[@name='username']").send_keys(username)
            driver.find_element(by=By.XPATH, value="//input[@name='password']").send_keys(password)
            # driver.find_element(by=By.XPATH, value="//input[@name='password']").send_keys(Keys.ENTER)
            break
        except:
            count+=1
            sleep(0.01)
    if(count==1000):
        return driver, 1
    sleep(2)
    driver.find_element(by=By.XPATH, value="//button[@id='btn-login']").click()
    return driver, 0
def search(driver, PatientData):
    # driver=webdriver.Chrome()
    SubscriberID=PatientData.get("SubscriberId")
    SubscriberFirstName=PatientData.get("SubscriberFirstName")
    SubscriberLastName=PatientData.get("SubscriberLastName")
    SubscriberBirthDate=PatientData.get("SubscriberBirthDate")
    # temp=SubscriberBirthDate.split('/')
    # SubscriberBirthDate=temp[1]+temp[0]+temp[2]
    LastName=PatientData.get("LastName")
    FirstName=PatientData.get("FirstName")
    BirthDate=PatientData.get("BirthDate")
    
    count=0
    while count<1000:
        try:
            driver.find_element(by=By.XPATH, value="//input[@id='BES-member_ID']").send_keys(SubscriberID)
            break
        except:
            count+=1
            sleep(0.01)
    if(count==1000):
        return driver, 1
    driver.find_element(by=By.XPATH, value="//input[@id='BES-member_DOB']").send_keys(SubscriberBirthDate)
    driver.find_element(by=By.XPATH, value="//input[@id='BES-member_firstname']").send_keys(SubscriberFirstName)
    driver.find_element(by=By.XPATH, value="//input[@id='BES-member_lastname']").send_keys(SubscriberLastName)
    if(BirthDate != ""):
        # try:
        #     temp=BirthDate.split('/')
        #     BirthDate=temp[1]+temp[0]+temp[2]
        # except:
        #     return driver, 1
        driver.find_element(by=By.XPATH, value="//label[@for='BES-benefits-yes']").click()
        sleep(5)
        driver.find_element(by=By.XPATH, value="//input[@id='BES-dependent_firstname']").send_keys(FirstName)
        driver.find_element(by=By.XPATH, value="//input[@id='BES-dependent_lastname']").send_keys(LastName)
        driver.find_element(by=By.XPATH, value="//input[@id='BES-dependent_DOB']").send_keys(BirthDate)
    driver.find_element(by=By.XPATH, value="//button[@class='btn']").click()
    sleep(10)
    if("The member information you have entered has generated multiple results." in driver.page_source):
        driver.find_element(by=By.XPATH, value="//table[@border='0']/tbody/tr[2]/td[1]").click()
        sleep(10)
    if("Member Company Providing Coverage" not in driver.page_source):
        return driver, 1
    return driver, 0

def PDFData(driver):
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityPatientVerification.update({
        "PlanType": driver.find_element(by=By.XPATH, value="//td[text()='Plan Type:']/following-sibling::td").text.replace("(", "").replace(")", ""),
        "SubscriberName": driver.find_element(by=By.XPATH, value="//td[text()='Member Name:']/following-sibling::td").text,
        "GroupNumber": driver.find_element(by=By.XPATH, value="//td[text()='Group Number:']/following-sibling::td").text,
        "GroupName": driver.find_element(by=By.XPATH, value="//td[text()='Group Name:']/following-sibling::td").text,
        "InsuranceName": driver.find_element(by=By.XPATH, value="//td[text()='Member Company Providing Coverage:']/following-sibling::td").text,
    })
    return EligibilityPatientVerification
    
def TableScrapBenefits(table):
    tabledata=table.find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.XPATH, value="./tr[@class='BODY']")
    
    instypes=[]
    for instype in tabledata[0].find_elements(by=By.TAG_NAME, value='td')[1:]:
        instypes.append(instype.text.replace("\n", "").replace(" ", ""))
    fields=[]
    for field in table.find_elements(by=By.XPATH, value=".//tr[@bgcolor='#F2F2F2']")[1].find_elements(by=By.TAG_NAME, value="td"):
        fields.append(field.text.replace("\n", "").replace(" ", ""))
    count=0
    fields[2]="PreApproval"
    for x in range(3, len(fields), 2):
        fields[x]=fields[x]+instypes[count]
        fields[x+1]=fields[x+1]+instypes[count]
        count+=1

    count=0
    temp1=[]
    temp2=[]
    if(len(tabledata)>2):
        for subtable in tabledata[2].find_elements(by=By.TAG_NAME, value='tbody'):
            temprow=subtable.find_elements(by=By.TAG_NAME, value='tr')
            for x in temprow:
                temp=[]
                for text in x.find_elements(by=By.TAG_NAME, value='td'):
                    temp.append(text.text.strip())
                if(count==0):
                    temp1.append(temp)
                else:
                    temp1[temprow.index(x)].extend(temp)
                
            count+=1
    
    if(len(tabledata)>4):
        temp2=[]
        fields2=[]
        for field in table.find_elements(by=By.XPATH, value=".//tr[@bgcolor='#F2F2F2']")[2].find_elements(by=By.TAG_NAME, value="td"):
            fields2.append(field.text.replace("\n", "").replace(" ", ""))
        count=0
        
        for x in range(1, len(fields2), 2):
            fields2[x]=fields2[x]+instypes[count]
            fields2[x+1]=fields2[x+1]+instypes[count]
            count+=1
        count=0
        for subtable in tabledata[4].find_elements(by=By.TAG_NAME, value='tbody'):
            
            temprow=subtable.find_elements(by=By.TAG_NAME, value='tr')
            for x in temprow:
                temp=[]
                for text in x.find_elements(by=By.TAG_NAME, value='td'):
                    temp.append(text.text.strip())
                if(count==0):
                    temp2.append(temp)
                else:
                    temp2[temprow.index(x)].extend(temp)
                
            count+=1
    
    templist=[]
    
    for x in temp1:
        tempdict={}
        for y in fields:
            tempdict.update({y:x[fields.index(y)]})
        templist.append(tempdict)
    if(len(temp2)):
        for x in temp2:
            tempdict={}
            for y in fields2:
                tempdict.update({y:x[fields2.index(y)]})
            templist.append(tempdict)
    
    return templist

def BenefitLevels(table, driver):

    tabledata=table.find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.XPATH, value="./tr[@class='BODY']")
    instypes=[]
    for instype in tabledata[0].find_elements(by=By.TAG_NAME, value='td')[1:]:
        instypes.append(instype.text.replace("\n", "").replace(" ", ""))
    fields=[]
    if("Out-of-Network" in table.find_elements(by=By.XPATH, value=".//tr[@bgcolor='#F2F2F2']")[0].find_elements(by=By.TAG_NAME, value="td")[-1].text):
        oonflag=1
    else:
        oonflag=0
    for field in table.find_elements(by=By.XPATH, value=".//tr[@bgcolor='#F2F2F2']")[1].find_elements(by=By.TAG_NAME, value="td"):
        fields.append(field.text.replace("\n", "").replace(" ", ""))
    count=0
    fields[2]="PreApproval"
    for x in range(3, len(fields), 2):
        fields[x]=instypes[count]+fields[x]
        fields[x+1]=instypes[count]+fields[x+1]
        count+=1
    
    count=0
    temp1=[]
    
    for subtable in tabledata[1].find_elements(by=By.TAG_NAME, value='tbody'):
        temprow=subtable.find_elements(by=By.TAG_NAME, value='tr')
        for x in temprow:
            temp=[]
            tds=x.find_elements(by=By.TAG_NAME, value='td')
            for text in tds:
                proccodelist=[]
            
                if(tds.index(text)==0 and tabledata[1].find_elements(by=By.TAG_NAME, value='tbody').index(subtable)==0):

                    # if("[Details]" in text.text.strip()): 
                    #     sleep(100)
                    #     link=text.find_element(by=By.XPATH, value='.//a[@class="PARTICIPATION"]').click()
                    #     driver.switch_to.window(driver.window_handles[1])
                    #     driver.maximize_window()
                    #     errorcount=0
                        
                    #     if("Messages" in driver.page_source):
                    #         errorcount=1000
                    #     while errorcount<1000:
                    #         try:
                               
                    #             # print("Messages" in driver.page_source)
                    #             maintable=driver.find_element(by=By.XPATH, value="//table[@id='BenefitDetailsTable']")
                    #             break
                    #         except: 

                    #             if("Messages" in driver.page_source):
                    #                 errorcount=1000
                    #                 break
                    #             errorcount+=1
                    #             sleep(0.01)
                    #     if(errorcount!=1000):

                    #         insurancetype=maintable.find_element(by=By.XPATH, value=".//span[@class='h3']").text
                            
                    #         columns=maintable.find_element(by=By.XPATH, value=".//tr[@class='GridViewHeader']")
                    #         columnlist=[]
                            
                    #         for _ in columns.find_elements(by=By.TAG_NAME, value="th"):
                    #             columnlist.append(_.text.replace("\n", "").replace(" ", ""))
                    #         for row in maintable.find_elements(by=By.XPATH, value=".//tr[@class='GridViewRow']"):
                    #             cells=row.find_elements(by=By.TAG_NAME, value="td")                            
                    #             proccodelist.append({
                    #                 "ProcedureCode":cells[0].text.replace("\n", " "),
                    #                 "procedureCodeDescription":cells[1].text.replace("\n", " "),
                    #                 "DeltaDentalPPOPays":cells[2].text.replace("\n", " "),
                    #                 "MinimumAge":cells[3].text.replace("\n", " "),
                    #                 "MaximumAge":cells[4].text.replace("\n", " "), 
                    #                 "WaitingPeriod":cells[5].text.replace("\n", " "),
                    #                 "NextServiceDate":cells[6].text.replace("\n", " "),
                    #                 "DeltaDentalPPODeductibleApplies":cells[7].text.replace("\n", " ")
                    #             })
                    #             print(cells[6].text.replace("\n", " "))
                            
                    #     driver.close()
                    #     driver.switch_to.window(driver.window_handles[0])
                    
                    temp.append(proccodelist)
                
                temp.append(text.text.replace("[Details]", "").strip())
                

            
                

            if(count==0):
                temp1.append(temp)
            else:
                temp1[temprow.index(x)].extend(temp)
            
        count+=1
    
    temp2=[]
    count=0
    if(len(tabledata)>3):
        for subtable in tabledata[3].find_elements(by=By.TAG_NAME, value='tbody'):
            temprow=subtable.find_elements(by=By.TAG_NAME, value='tr')
            for x in temprow:
                temp=[]
                tds=x.find_elements(by=By.TAG_NAME, value='td')
                for text in tds:
                    proccodelist=[]
                    if(tds.index(text)==0 and tabledata[3].find_elements(by=By.TAG_NAME, value='tbody').index(subtable)==0):
                        temp.append(proccodelist)    
                    temp.append(text.text.strip())

                if(count==0):
                    temp2.append(temp)
                else:
                    temp2[temprow.index(x)].extend(temp)
                
            count+=1
    
    temp1.extend(temp2)
    templist=[]


    
    for x in temp1:
        if(len(x[0])!=0):
            for proccodelist in x[0]:
                tempdict={
                    "ServiceType":"",
                    "WaitingPeriod":proccodelist.get("WaitingPeriod"),
                    "PriorAuthorization":"",
                    "DeltaDentalPPOPays":"",
                    "DeltaDentalPremierPatientPays":"",
                    "DeltaDentalPremierDeductibleApplies":"",
                    "OutofNetworkPatientPays":"",
                    "OutofNetworkDeductibleApplies":"",
                    "limitation":"",
                    "AgeLimitationText":"",
                    "LastDateOfService":"",
                    "ProcedureCode":proccodelist.get("ProcedureCode").strip(),
                    "procedureCodeDescription":proccodelist.get("procedureCodeDescription").replace("\u2013", "-"),
                    "DeltaDentalPPOPays":proccodelist.get("DeltaDentalPPOPays"),
                    "MinimumAge":proccodelist.get("MinimumAge"),
                    "MaximumAge":proccodelist.get("MaximumAge"),
                    "NextServiceDate":proccodelist.get("NextServiceDate"),
                    "DeltaDentalPPODeductibleApplies":proccodelist.get("DeltaDentalPPODeductibleApplies")
                }
                print(proccodelist.get("NextServiceDate"))
                for y in fields:
                    tempdict.update({y:x[fields.index(y)+1]})
                templist.append(tempdict)
        else:
            tempdict={
                "ServiceType":"",
                "WaitingPeriod":"",
                "PreApproval":"",
                "DeltaDentalPPOPays":"",
                "DeltaDentalPPODeductibleApplies":"",
                "DeltaDentalPremierPatientPays":"",
                "DeltaDentalPremierDeductibleApplies":"",
                "OutofNetworkPatientPays":"",
                "OutofNetworkDeductibleApplies":"",
                "limitation":"",
                "AgeLimitationText":"",
                "LastDateOfService":"",
                "ProcedureCode":"",
                "procedureCodeDescription":"",
                "DeltaDentalPPOPays":"",
                "MinimumAge":"",
                "MaximumAge":"",
                "NextServiceDate":"",
                
            }
            for y in range(len(fields)):
                if(fields[y]=='DeltaDentalPPOPatientPays'):
                    fields[y]="DeltaDentalPPOPays"
            for y in fields:
                print(y, x[fields.index(y)+1].replace("\u2013", "-"))
                if(y=="DeltaDentalPPOPays"):
                    calc=x[fields.index(y)+1].replace("\u2013", "-")[:-1]
                    tempdict.update({y:f'{100-int(calc)}%'})
                else:    
                    tempdict.update({y:x[fields.index(y)+1].replace("\u2013", "-")})
            templist.append(tempdict)
    

    
    
    return templist, oonflag
    
def TableScrap(table):
    tabledata=table.find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.XPATH, value="./tr[@class='BODY']")
    
    instypes=[]
    for instype in tabledata[0].find_elements(by=By.TAG_NAME, value='td')[1:]:
        instypes.append(instype.text.replace("\n", "").replace(" ", ""))
    fields=[]
    for field in table.find_elements(by=By.XPATH, value=".//tr[@bgcolor='#F2F2F2']")[1].find_elements(by=By.TAG_NAME, value="td"):
        fields.append(field.text.replace("\n", "").replace(" ", ""))
    count=0
    
    for x in range(1, len(fields), 2):
        fields[x]=fields[x]+instypes[count]
        fields[x+1]=fields[x+1]+instypes[count]
        count+=1

    count=0
    temp1=[]
    temp2=[]
    if(len(tabledata)>2):
        for subtable in tabledata[2].find_elements(by=By.TAG_NAME, value='tbody'):
            temprow=subtable.find_elements(by=By.TAG_NAME, value='tr')
            for x in temprow:
                temp=[]
                for text in x.find_elements(by=By.TAG_NAME, value='td'):
                    temp.append(text.text.strip())
                if(count==0):
                    temp1.append(temp)
                else:
                    temp1[temprow.index(x)].extend(temp)
                
            count+=1
    
    if(len(tabledata)>4):
        temp2=[]
        fields2=[]
        for field in table.find_elements(by=By.XPATH, value=".//tr[@bgcolor='#F2F2F2']")[2].find_elements(by=By.TAG_NAME, value="td"):
            fields2.append(field.text.replace("\n", "").replace(" ", ""))
        count=0
        
        for x in range(1, len(fields2), 2):
            fields2[x]=fields2[x]+instypes[count]
            fields2[x+1]=fields2[x+1]+instypes[count]
            count+=1
        count=0
        for subtable in tabledata[4].find_elements(by=By.TAG_NAME, value='tbody'):
            
            temprow=subtable.find_elements(by=By.TAG_NAME, value='tr')
            for x in temprow:
                temp=[]
                for text in x.find_elements(by=By.TAG_NAME, value='td'):
                    temp.append(text.text.strip())
                if(count==0):
                    temp2.append(temp)
                else:
                    
                    temp2[temprow.index(x)].extend(temp)
                
            count+=1
    
    templist=[]
    
    for x in temp1:
        tempdict={}
        for y in fields:
            tempdict.update({y:x[fields.index(y)]})
        templist.append(tempdict)
    if(len(temp2)):
        for x in temp2:
            tempdict={}
            for y in fields2:
                tempdict.update({y:x[fields2.index(y)]})
            templist.append(tempdict)
    
    return templist

def Limitations(table):
    templist=[]
    for row in table.find_elements(by=By.TAG_NAME, value="tr")[1:]:
        
        if(row.get_attribute("bgcolor")=="#F2F2F2"):
            fields=[]
            fields.append(row.find_elements(by=By.TAG_NAME, value="td")[0].text.replace("\n", "").replace(" ", ""))
            fields.append(row.find_elements(by=By.TAG_NAME, value="td")[1].text.replace("\n", "").replace(" ", ""))
            fields.append(row.find_elements(by=By.TAG_NAME, value="td")[2].text.replace("\n", "").replace(" ", ""))
            fields.append(row.find_elements(by=By.TAG_NAME, value="td")[3].text.replace("\n", "").replace(" ", ""))
        elif(row.get_attribute("bgcolor")=="#FFFFFF"):
            print(row.find_elements(by=By.TAG_NAME, value="td")[0].text.replace("\n", "").replace(" ", ""))
            limitationstext=''
            if(row.find_elements(by=By.TAG_NAME, value="td")[1].text.replace("\n", "").replace(" ", "")!=""):
                limitationstext=row.find_elements(by=By.TAG_NAME, value="td")[1].text+". "
            if(row.find_elements(by=By.TAG_NAME, value="td")[2].text.replace("\n", "").replace(" ", "")!=""):
                limitationstext+=f'Age Restrictions: {row.find_elements(by=By.TAG_NAME, value="td")[2].text}. '
            if("Service Date" in row.find_elements(by=By.TAG_NAME, value="td")[3].text):
                limitationstext+=row.find_elements(by=By.TAG_NAME, value="td")[3].text.replace("\n", " ")+"."
            templist.append({
                fields[0]:row.find_elements(by=By.TAG_NAME, value="td")[0].text,
                fields[1]:limitationstext.strip()
                # fields[2]:row.find_elements(by=By.TAG_NAME, value="td")[2].text,
                # fields[3]:row.find_elements(by=By.TAG_NAME, value="td")[3].text.replace("Last Service Date:", "").replace("\n", "").replace(" ", "")
            })
    print(templist)
    return templist

def TreatmentSummary(table, EligibilityBenefits):
    templist=[]
    for row in table.find_elements(by=By.TAG_NAME, value="tr")[1:]:
        
        if(row.get_attribute("bgcolor")=="#F2F2F2"):
            fields=[]
            fields.append(row.find_elements(by=By.TAG_NAME, value="td")[0].text.replace("\n", "").replace(" ", ""))
            fields.append(row.find_elements(by=By.TAG_NAME, value="td")[1].text.replace("\n", "").replace(" ", ""))
            fields.append(row.find_elements(by=By.TAG_NAME, value="td")[2].text.replace("\n", "").replace(" ", ""))
            fields.append(row.find_elements(by=By.TAG_NAME, value="td")[3].text.replace("\n", "").replace(" ", ""))
        elif(row.get_attribute("bgcolor")=="#FFFFFF"):
            print(row.find_elements(by=By.TAG_NAME, value="td")[0].text.replace("\n", "").replace(" ", ""))
            limitationstext=''
            if(row.find_elements(by=By.TAG_NAME, value="td")[1].text.replace("\n", "").replace(" ", "")!=""):
                limitationstext=row.find_elements(by=By.TAG_NAME, value="td")[1].text+". "
            if(row.find_elements(by=By.TAG_NAME, value="td")[2].text.replace("\n", "").replace(" ", "")!=""):
                limitationstext+=f'Age Restrictions: {row.find_elements(by=By.TAG_NAME, value="td")[2].text}. '
            if("Service Date" in row.find_elements(by=By.TAG_NAME, value="td")[3].text):
                limitationstext+=row.find_elements(by=By.TAG_NAME, value="td")[3].text.replace("\n", " ")+"."
            if("Service Date:" in row.find_elements(by=By.TAG_NAME, value="td")[3].text):
                templist.append({
                    fields[0]:row.find_elements(by=By.TAG_NAME, value="td")[0].text,
                    fields[1]:row.find_elements(by=By.TAG_NAME, value="td")[1].text,
                    fields[2]:row.find_elements(by=By.TAG_NAME, value="td")[2].text,
                    fields[3]:row.find_elements(by=By.TAG_NAME, value="td")[3].text.replace("\n", "").replace(" ", "").replace("LastServiceDate:", "LSD: ").replace("NextServiceDate:", "NSD: "),
                    "limitationtext":limitationstext
                })
    templist1=[]
    
    for x in templist:
        flag=0
        for y in EligibilityBenefits:
            if(x.get("Procedure")==y.get("ProcedureCode")):
                flag=1
                templist1.append({
                    "ProcedureCode":x.get("Procedure"),
                    "ProcedureCodeDescription":y.get("procedureCodeDescription"),
                    "LimitationText":x.get("limitationtext"),
                    "LimitationAlsoAppliesTo":"",
                    "History":x.get("Date")
                })
                break
        if(flag==0):
            templist1.append({
                "ProcedureCode":x.get("Procedure"),
                "ProcedureCodeDescription":"",
                "LimitationText":x.get("limitationtext"),
                "LimitationAlsoAppliesTo":"",
                "History":x.get("Date")
            })
            print(templist1, '1111111111111111')
    print(templist1)
    return templist1

def maxs(rawtext):
    
    text=rawtext
    instypes=[]       
    if("Delta Dental PPO Delta Dental Premier Out-of-Network" in text):
        instypes=["Delta Dental PPO", "Delta Dental Premier", "Out-of-Network"]
    elif("Delta Dental PPO Out-of-Network" in text):
        instypes=["Delta Dental PPO", "Out-of-Network"]
    elif("Delta Dental PPO Delta Dental Premier" in text):
        instypes=["Delta Dental PPO", "Delta Dental Premier"]
    if("Limitations" in text):

        text=text[text.index("Maximums for Benefit Year"):text.index("Limitations")]
        text=text.split('\n')
        t=[]
        for x in range(len(text)):
            temp={}
            if("Remaining Annual Maximums" in text[x]):
                ServiceCategory=text[x+1]
                temp.update({"Type":"Remaining Annual Maximums"})
                temp.update({"ServiceCategory":ServiceCategory})
                try:
                    if("$" in text[x+2] or 'N/A' in text[x+2]): temp1=text[x+2].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"PPO":temp1})
                try:
                    if("$" in text[x+3] or 'N/A' in text[x+3]): temp1=text[x+3].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"Premier":temp1})
                try:
                    if("$" in text[x+4] or 'N/A' in text[x+4]): temp1=text[x+4].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"OutofNetwork":temp1})
                t.append(temp)

            elif("Remaining Lifetime Maximums" in text[x]):
                ServiceCategory=text[x+1]
                temp.update({"Type":"Remaining Lifetime Maximums"})
                temp.update({"ServiceCategory":ServiceCategory})
                try:
                    if("$" in text[x+2] or 'N/A' in text[x+2]): temp1=text[x+2].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"PPO":temp1})
                try:
                    if("$" in text[x+3] or 'N/A' in text[x+3]): temp1=text[x+3].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"Premier":temp1})
                try:
                    if("$" in text[x+4] or 'N/A' in text[x+4]): temp1=text[x+4].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"OutofNetwork":temp1})
                t.append(temp)

            elif("Annual Maximums" in text[x]):
                ServiceCategory=text[x+1]
                temp.update({"Type":"Annual Maximums"})
                temp.update({"ServiceCategory":ServiceCategory})
                try:
                    if("$" in text[x+2] or 'N/A' in text[x+2]): temp1=text[x+2].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"PPO":temp1})
                try:
                    if("$" in text[x+3] or 'N/A' in text[x+3]): temp1=text[x+3].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"Premier":temp1})
                try:
                    if("$" in text[x+4] or 'N/A' in text[x+4]): temp1=text[x+4].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"OutofNetwork":temp1})
                t.append(temp)
                

            elif("Lifetime Maximums" in text[x]):
                ServiceCategory=text[x+1]
                temp.update({"Type":"Lifetime Maximums"})
                temp.update({"ServiceCategory":ServiceCategory})
                try:
                    if("$" in text[x+2] or 'N/A' in text[x+2]): temp1=text[x+2].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"PPO":temp1})
                try:
                    if("$" in text[x+3] or 'N/A' in text[x+3]): temp1=text[x+3].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"Premier":temp1})
                try:
                    if("$" in text[x+4] or 'N/A' in text[x+4]): temp1=text[x+4].split(' ')
                    else: temp1=['0.0', '0.0']
                except:
                    temp1=['0.0', '0.0']
                temp.update({"OutofNetwork":temp1})
                t.append(temp)
    else:
        text1=text[text.index("Annual Maximums Individual Family"):text.index("Lifetime Maximums Individual Family")].strip()
       
        text1=text1.split("\n")
        
        ServiceCategoryMax=[]
        for x in text1:
            if("N/A" in x or "$" in x):
                break
            ServiceCategoryMax.append(x)
        temp={}
        count=0
        for x in range(0, len(text1), 3):
            if("N/A" in x or "$" in x):
                ppo=text1[x].split(' ')
                premier=text1[x+1].split(' ')
                outofnetwork=text1[x+1].split(' ')
                temp.update({"Type":"Annual Maximums"})
                temp.update({"Network":"Delta Dental PPO"})
                temp.update({"Amount":ppo[0]})
                # temp.update({"Remaining":})
                temp.update({"ServiceCategory":ServiceCategoryMax[count]})
                temp.update({"Family_Individual":"Individual"})

                temp.update({"Type":"Annual Maximums"})
                temp.update({"Network":"Delta Dental PPO"})
                temp.update({"Amount":ppo[1]})
                # temp.update({"Remaining":})
                temp.update({"ServiceCategory":ServiceCategoryMax[count]})
                temp.update({"Family_Individual":"Family"})

                temp.update({"Type":"Annual Maximums"})
                temp.update({"Network":"Delta Dental Premier"})
                temp.update({"Amount":premier[0]})
                # temp.update({"Remaining":})
                temp.update({"ServiceCategory":ServiceCategoryMax[count]})
                temp.update({"Family_Individual":"Individual"})

                temp.update({"Type":"Annual Maximums"})
                temp.update({"Network":"Delta Dental Premier"})
                temp.update({"Amount":premier[1]})
                # temp.update({"Remaining":})
                temp.update({"ServiceCategory":ServiceCategoryMax[count]})
                temp.update({"Family_Individual":"Family"})

                temp.update({"Type":"Annual Maximums"})
                temp.update({"Network":"Out of Network"})
                temp.update({"Amount":outofnetwork[0]})
                # temp.update({"Remaining":})
                temp.update({"ServiceCategory":ServiceCategoryMax[count]})
                temp.update({"Family_Individual":"Individual"})

                temp.update({"Type":"Annual Maximums"})
                temp.update({"Network":"Out of Network"})
                temp.update({"Amount":outofnetwork[1]})
                # temp.update({"Remaining":})
                temp.update({"ServiceCategory":ServiceCategoryMax[count]})
                temp.update({"Family_Individual":"Family"})
                count+=1



    EligibilityMaximums=[]
    for x in t:
        if("Remaining" not in x.get("Type")):
            EligibilityMaximums.append({
                "Type":x.get("Type"),
                "Network":"DeltaDentalPPO",
                "Amount":changeZero(x.get('PPO')[0]),
                "Remaining":get_remaining(x.get("Type"), "PPO", x.get("ServiceCategory"), t)[0],
                "ServiceCategory":x.get("ServiceCategory"),
                "Family_Individual":"Individual"
            })

            EligibilityMaximums.append({
                "Type":x.get("Type"),
                "Network":"DeltaDentalPPO",
                "Amount":changeZero(x.get('PPO')[1]),
                "Remaining":get_remaining(x.get("Type"), "PPO", x.get("ServiceCategory"), t)[1],
                "ServiceCategory":x.get("ServiceCategory"),
                "Family_Individual":"Family"
            })

            EligibilityMaximums.append({
                "Type":x.get("Type"),
                "Network":"DeltaDentalPremier",
                "Amount":changeZero(x.get('Premier')[0]),
                "Remaining":get_remaining(x.get("Type"), "Premier", x.get("ServiceCategory"), t)[0],
                "ServiceCategory":x.get("ServiceCategory"),
                "Family_Individual":"Individual"
            })

            EligibilityMaximums.append({
                "Type":x.get("Type"),
                "Network":"DeltaDentalPremier",
                "Amount":changeZero(x.get('Premier')[1]),
                "Remaining":get_remaining(x.get("Type"), "Premier", x.get("ServiceCategory"), t)[1],
                "ServiceCategory":x.get("ServiceCategory"),
                "Family_Individual":"Family"
            })

            EligibilityMaximums.append({
                "Type":x.get("Type"),
                "Network":"OutofNetwork",
                "Amount":changeZero(x.get('OutofNetwork')[0]),
                "Remaining":get_remaining(x.get("Type"), "OutofNetwork", x.get("ServiceCategory"), t)[0],
                "ServiceCategory":x.get("ServiceCategory"),
                "Family_Individual":"Individual"
            })

            EligibilityMaximums.append({
                "Type":x.get("Type"),
                "Network":"OutofNetwork",
                "Amount":changeZero(x.get('OutofNetwork')[1]),
                "Remaining":get_remaining(x.get("Type"), "OutofNetwork", x.get("ServiceCategory"), t)[1],
                "ServiceCategory":x.get("ServiceCategory"),
                "Family_Individual":"Family"
            })
    FamilyAnnualMaximumBenefits=""
    FamilyAnnualRemainingBenefit=""
    IndividualAnnualMaximumBenefits=""
    IndividualAnnualRemainingBenefit=""
    FamilyLifetimeMaximumBenefits=""
    FamilyLifetimeRemainingBenefit=""
    IndividualLifetimeMaximumBenefits=""
    IndividualLifetimeRemainingBenefit=""
    OrthodonticMaximumBenefit=""
    OrthodonticRemainingBenefit=""
    
    for x in EligibilityMaximums:
        if(x.get("Type")=="Annual Maximums" and x.get("Network")=="DeltaDentalPPO" and x.get("Family_Individual")=="Family" and x.get("ServiceCategory")=="Dental Care"):
            FamilyAnnualMaximumBenefits=x.get("Amount")
            FamilyAnnualRemainingBenefit=x.get("Amount")
        elif(x.get("Type")=="Annual Maximums" and x.get("Network")=="DeltaDentalPPO" and x.get("Family_Individual")=="Individual" and x.get("ServiceCategory")=="Dental Care"):
            IndividualAnnualMaximumBenefits=x.get("Amount")
            IndividualAnnualRemainingBenefit=x.get("Amount")
        elif(x.get("Type")=="Lifetime Maximums" and x.get("Network")=="DeltaDentalPPO" and x.get("Family_Individual")=="Family" and x.get("ServiceCategory")=="Dental Care"):
            FamilyLifetimeMaximumBenefits=x.get("Amount")
            FamilyLifetimeRemainingBenefit=x.get("Amount")
        elif(x.get("Type")=="Lifetime Maximums" and x.get("Network")=="DeltaDentalPPO" and x.get("Family_Individual")=="Individual" and x.get("ServiceCategory")=="Dental Care"):
            IndividualLifetimeMaximumBenefits=x.get("Amount")
            IndividualLifetimeRemainingBenefit=x.get("Amount")
        elif(x.get("Type")=="Lifetime Maximums" and x.get("Network")=="DeltaDentalPPO" and x.get("Family_Individual")=="Individual" and x.get("ServiceCategory")=="Orthodontics"):
            OrthodonticMaximumBenefit=x.get("Amount")
            OrthodonticRemainingBenefit=x.get("Amount")

    return EligibilityMaximums, FamilyAnnualMaximumBenefits, FamilyAnnualRemainingBenefit, IndividualAnnualMaximumBenefits, IndividualAnnualRemainingBenefit, FamilyLifetimeMaximumBenefits, FamilyLifetimeRemainingBenefit, IndividualLifetimeMaximumBenefits, IndividualLifetimeRemainingBenefit, OrthodonticMaximumBenefit, OrthodonticRemainingBenefit

def fixdata(a,b):
    temp=[]
    for x in a:
        
        if(x.get("AnnualMaximums")):
            if(x.get("IndividualDeltaDentalPPO")):
                temp.append({
                    "Type":"Annual Maximums",
                    "Network":"Delta Dental PPO",
                    "Amount":changeZero(x.get("IndividualDeltaDentalPPO")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualMaximums"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyDeltaDentalPPO")):
                temp.append({
                    "Type":"Annual Maximums",
                    "Network":"Delta Dental PPO",
                    "Amount":changeZero(x.get("FamilyDeltaDentalPPO")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualMaximums"),
                    "Family_Individual":"Family"
                })
            if(x.get("IndividualDeltaDentalPremier")):
                temp.append({
                    "Type":"Annual Maximums",
                    "Network":"Delta Dental Premier",
                    "Amount":changeZero(x.get("IndividualDeltaDentalPremier")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualMaximums"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyDeltaDentalPremier")):
                temp.append({
                    "Type":"Annual Maximums",
                    "Network":"Delta Dental Premier",
                    "Amount":changeZero(x.get("FamilyDeltaDentalPremier")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualMaximums"),
                    "Family_Individual":"Family"
                })
            if(x.get("IndividualOut-of-Network")):
                temp.append({
                    "Type":"Annual Maximums",
                    "Network":"Out of Network",
                    "Amount":changeZero(x.get("IndividualOut-of-Network")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualMaximums"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyOut-of-Network")):
                temp.append({
                    "Type":"Annual Maximums",
                    "Network":"Out of Network",
                    "Amount":changeZero(x.get("FamilyOut-of-Network")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualMaximums"),
                    "Family_Individual":"Family"
                })
        elif(x.get("LifetimeMaximums")):
            if(x.get("IndividualDeltaDentalPPO")):
                temp.append({
                    "Type":"Lifetime Maximums",
                    "Network":"Delta Dental PPO",
                    "Amount":changeZero(x.get("IndividualDeltaDentalPPO")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeMaximums"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyDeltaDentalPPO")):
                temp.append({
                    "Type":"Lifetime Maximums",
                    "Network":"Delta Dental PPO",
                    "Amount":changeZero(x.get("FamilyDeltaDentalPPO")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeMaximums"),
                    "Family_Individual":"Family"
                })
            if(x.get("IndividualDeltaDentalPremier")):
                temp.append({
                    "Type":"Lifetime Maximums",
                    "Network":"Delta Dental Premier",
                    "Amount":changeZero(x.get("IndividualDeltaDentalPremier")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeMaximums"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyDeltaDentalPremier")):
                temp.append({
                    "Type":"Lifetime Maximums",
                    "Network":"Delta Dental Premier",
                    "Amount":changeZero(x.get("FamilyDeltaDentalPremier")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeMaximums"),
                    "Family_Individual":"Family"
                })
            if(x.get("IndividualOut-of-Network")):
                temp.append({
                    "Type":"Lifetime Maximums",
                    "Network":"Out of Network",
                    "Amount":changeZero(x.get("IndividualOut-of-Network")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeMaximums"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyOut-of-Network")):
                temp.append({
                    "Type":"Lifetime Maximums",
                    "Network":"Out of Network",
                    "Amount":changeZero(x.get("FamilyOut-of-Network")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeMaximums"),
                    "Family_Individual":"Family"
                })
        elif(x.get("AnnualDeductibles")):
            if(x.get("IndividualDeltaDentalPPO")):
                temp.append({
                    "Type":"Annual Deductibles",
                    "Network":"Delta Dental PPO",
                    "Amount":changeZero(x.get("IndividualDeltaDentalPPO")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualDeductibles"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyDeltaDentalPPO")):
                temp.append({
                    "Type":"Annual Deductibles",
                    "Network":"Delta Dental PPO",
                    "Amount":changeZero(x.get("FamilyDeltaDentalPPO")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualDeductibles"),
                    "Family_Individual":"Family"
            })
            if(x.get("IndividualDeltaDentalPremier")):
                temp.append({
                    "Type":"Annual Deductibles",
                    "Network":"Delta Dental Premier",
                    "Amount":changeZero(x.get("IndividualDeltaDentalPremier")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualDeductibles"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyDeltaDentalPremier")):
                temp.append({
                    "Type":"Annual Deductibles",
                    "Network":"Delta Dental Premier",
                    "Amount":changeZero(x.get("FamilyDeltaDentalPremier")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualDeductibles"),
                    "Family_Individual":"Family"
                })
            if(x.get("IndividualOut-of-Network")):
                temp.append({
                    "Type":"Annual Deductibles",
                    "Network":"Out of Network",
                    "Amount":changeZero(x.get("IndividualOut-of-Network")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualDeductibles"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyOut-of-Network")):
                temp.append({
                    "Type":"Annual Deductibles",
                    "Network":"Out of Network",
                    "Amount":changeZero(x.get("FamilyOut-of-Network")),
                    "Remaining":"",
                    "ServiceCategory":x.get("AnnualDeductibles"),
                    "Family_Individual":"Family"
                })
        elif(x.get("LifetimeDeductibles")):
            if(x.get("IndividualDeltaDentalPPO")):
                temp.append({
                    "Type":"Lifetime Deductibles",
                    "Network":"Delta Dental PPO",
                    "Amount":changeZero(x.get("IndividualDeltaDentalPPO")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeDeductibles"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyDeltaDentalPPO")):
                temp.append({
                    "Type":"Lifetime Deductibles",
                    "Network":"Delta Dental PPO",
                    "Amount":changeZero(x.get("FamilyDeltaDentalPPO")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeDeductibles"),
                    "Family_Individual":"Family"
                })
            if(x.get("IndividualDeltaDentalPremier")):
                temp.append({
                    "Type":"Lifetime Deductibles",
                    "Network":"Delta Dental Premier",
                    "Amount":changeZero(x.get("IndividualDeltaDentalPremier")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeDeductibles"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyDeltaDentalPremier")):
                temp.append({
                    "Type":"Lifetime Deductibles",
                    "Network":"Delta Dental Premier",
                    "Amount":changeZero(x.get("FamilyDeltaDentalPremier")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeDeductibles"),
                    "Family_Individual":"Family"
                })
            if(x.get("IndividualOut-of-Network")):
                temp.append({
                    "Type":"Lifetime Deductibles",
                    "Network":"Out of Network",
                    "Amount":changeZero(x.get("IndividualOut-of-Network")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeDeductibles"),
                    "Family_Individual":"Individual"
                })
            if(x.get("FamilyOut-of-Network")):
                temp.append({
                    "Type":"Lifetime Deductibles",
                    "Network":"Out of Network",
                    "Amount":changeZero(x.get("FamilyOut-of-Network")),
                    "Remaining":"",
                    "ServiceCategory":x.get("LifetimeDeductibles"),
                    "Family_Individual":"Family"
                })
        
    for x in temp:
        for y in b:
            # if(x.get("Amount")):
            if(x.get("ServiceCategory")==y.get("RemainingAnnualMaximums") or x.get("ServiceCategory")==y.get("RemainingLifetimeMaximums") or x.get("ServiceCategory")==y.get("RemainingAnnualDeductibles") or x.get("ServiceCategory")==y.get("RemainingLifetimeDeductibles")):
                if(x.get("Network")=="Delta Dental PPO" and x.get("Family_Individual")=="Individual"):
                    x.update({"Remaining":changeZero(y.get("IndividualDeltaDentalPPO"))})
                elif(x.get("Network")=="Delta Dental PPO" and x.get("Family_Individual")=="Family"):
                    x.update({"Remaining":changeZero(y.get("FamilyDeltaDentalPPO"))})
                elif(x.get("Network")=="Delta Dental Premier" and x.get("Family_Individual")=="Individual"):
                    x.update({"Remaining":changeZero(y.get("IndividualDeltaDentalPremier"))})
                elif(x.get("Network")=="Delta Dental Premier" and x.get("Family_Individual")=="Family"):
                    x.update({"Remaining":changeZero(y.get("FamilyDeltaDentalPremier"))})
                elif(x.get("Network")=="Out of Network" and x.get("Family_Individual")=="Individual"):
                    x.update({"Remaining":changeZero(y.get("IndividualOut-of-Network"))})
                elif(x.get("Network")=="Out of Network" and x.get("Family_Individual")=="Family"):
                    x.update({"Remaining":changeZero(y.get("FamilyOut-of-Network"))})
                    
    return temp
def main(data, message_id):

    InputParameters=data.get("InputParameters")
    for patient in data.get("PatientData"):
        
        url, username, password=data.get("Login").get("Url"), data.get("Login").get("LoginId"), data.get("Login").get("Password")
        PatientData=patient
        driver, loginflag=login(url, username, password)
        if(loginflag):
            final= {        "ClientId": data.get("InputParameters").get('ClientId'),        "PayorId": data.get("InputParameters").get('PayorId'),        "AppName": data.get("InputParameters").get('AppName'),   "ScrappingSource": "SD",       "IsError":True,                    "ErrorMessage": "Login failed",        "Data": None, "EligibilityVerificationId": patient.get('EligibilityVerificationId'), "ClinicServerId": patient.get('ClinicServerId'),'PatientId': patient.get('PatientId')}
            print("Login failed")
            QueueHandler(data.get("InputParameters").get('AppName')).send_message(b64encode(bytes(json.dumps(final,indent=4), 'utf-8')).decode('utf-8'))
            driver.quit()
            continue
        driver, searchflag=search(driver, PatientData)
        if(searchflag):
            final= {        "ClientId": data.get("InputParameters").get('ClientId'),        "PayorId": data.get("InputParameters").get('PayorId'),     "ScrappingSource": "SD",    "AppName": data.get("InputParameters").get('AppName'),         "IsError":True,                    "ErrorMessage": "Patient not found",        "Data": None, "EligibilityVerificationId": patient.get('EligibilityVerificationId'), "ClinicServerId": patient.get('ClinicServerId'),'PatientId': patient.get('PatientId')}
            print("Patient Not Found")
            QueueHandler(data.get("InputParameters").get('AppName')).send_message(b64encode(bytes(json.dumps(final,indent=4), 'utf-8')).decode('utf-8'))
            driver.quit()
            continue
        sleep(15)                
        # driver = webdriver.Chrome()
        # html_file = r"C:\Users\saran\Downloads\config files\Delta4.html"
        # driver.get("file:///" + html_file)
        try:
            EligibilityPatientVerification=PDFData(driver)
        except:
            final= {        "ClientId": data.get("InputParameters").get('ClientId'),        "PayorId": data.get("InputParameters").get('PayorId'),        "AppName": data.get("InputParameters").get('AppName'),         "IsError":True,                    "ErrorMessage": "Patient not found",  "ScrappingSource": "SD",      "Data": None}
            print("Patient Not Found")
            QueueHandler(data.get("InputParameters").get('AppName')).send_message(b64encode(bytes(json.dumps(final,indent=4), 'utf-8')).decode('utf-8'))
            driver.quit()
            continue
        fields=[]
        fields1=[]
        for x in driver.find_elements(by=By.TAG_NAME, value="tbody"):
            try:
                if(x.find_element(by=By.XPATH, value=".//tr[@bgcolor='#41A928']").text.replace("\n", "").replace(" ", "")=="Patient"):
                    temp=x.find_element(by=By.XPATH, value=".//tr[@bgcolor='#F2F2F2']")
                    for y in temp.find_elements(by=By.TAG_NAME, value="td"):
                        
                        fields.append(y.text.replace("\n", "").replace(" ", ""))
                    patdata=[]
                    for temp in x.find_elements(by=By.XPATH, value=".//tr[@bgcolor='#FFFFFF']"):
                        count=0
                        patdict={}
                        for y in temp.find_elements(by=By.TAG_NAME, value="td"):
                            
                            patdict.update({fields[count]:y.text.replace("\n", "")})
                            count+=1
                        patdata.append(patdict)
            except: 
                pass

        for x in patdata:
            print(x.get("Relationship"), '-----------')
            if(x.get("Relationship")=="Self"):
                print(11111111111111111111)
                if(x.get("TerminationDate")==""):
                    EligibilityPatientVerification.update({
                        "FamilyMemberEffectiveDate":x.get("EffectiveDate"),
                        "FamilyMemberDateOfBirth":x.get("Birthday"),
                        "FamilyMemberName":x.get("Name"),
                        "EligibilityStatus":"Active",
                        "SubscriberEffectiveDate":x.get("EffectiveDate"),
                        "SubscriberDateOfBirth":x.get("Birthday"),
                        "SubscriberEligibilityStatus":"Active"
                        
                    })
                else:
                    EligibilityPatientVerification.update({
                        "FamilyMemberEffectiveDate":x.get("EffectiveDate"),
                        "FamilyMemberDateOfBirth":x.get("Birthday"),
                        "FamilyMemberName":x.get("Name"),
                        "EligibilityStatus":"",
                        "SubscriberEffectiveDate":x.get("EffectiveDate"),
                        "SubscriberDateOfBirth":x.get("Birthday"),
                        "SubscriberEligibilityStatus":""
                    })
                    
            else:
                if(x.get("TerminationDate")==""):
                    EligibilityPatientVerification.update({
                        "FamilyMemberEffectiveDate":x.get("EffectiveDate"),
                        "FamilyMemberDateOfBirth":x.get("Birthday"),
                        "EligibilityStatus":"Active",
                        "FamilyMemberName":x.get("Name")                
                    })
                else:
                    EligibilityPatientVerification.update({
                        "FamilyMemberEffectiveDate":x.get("EffectiveDate"),
                        "FamilyMemberDateOfBirth":x.get("Birthday"),
                        "EligibilityStatus":"",
                        "FamilyMemberName":x.get("Name")
                    })
    

        
        count=0
        while count<1000:
            try:
                tables=driver.find_element(by=By.XPATH, value="//table[@class='borderBlendHeader']")
                break
            except:
                count+=1
                sleep(0.01)
        tables=driver.find_elements(by=By.XPATH, value="//table[@class='borderBlendHeader']")
        flag=0
        EligibilityBenefits=[]
        TreatmentHistorySummary=[]
        AnnualDeductiblesDentalCareDeltaDentalPPOIndividual, RemainingAnnualDeductiblesDentalCareDeltaDentalPPOIndividual,AnnualDeductiblesDentalCareDeltaDentalPPOFamily,RemainingAnnualDeductiblesDentalCareDeltaDentalPPOFamily,LifetimeDeductiblesDentalCareDeltaDentalPPOIndividual,RemainingLifetimeDeductiblesDentalCareDeltaDentalPPOIndividual,LifetimeDeductiblesDentalCareDeltaDentalPPOFamily,RemainingLifetimeDeductiblesDentalCareDeltaDentalPPOFamily,IndividualAnnualMaximumBenefits,IndividualAnnualRemainingBenefit,FamilyAnnualMaximumBenefits,FamilyAnnualRemainingBenefit,IndividualLifetimeMaximumBenefits,IndividualLifetimeRemainingBenefit,FamilyLifetimeMaximumBenefits,FamilyLifetimeRemainingBenefit,OrthodonticMaximumBenefit,OrthodonticRemainingBenefit="", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
        for x in tables:
            tableheading=x.find_element(by=By.XPATH, value=".//tbody/tr[1]").text
            print(tableheading, '---------')
            if("Benefit Levels" in tableheading):
                EligibilityBenefits, oonflag=BenefitLevels(x, driver)
                
                if(oonflag):
                    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
                else:
                    EligibilityPatientVerification.update({"oonBenefits":"No"})
                if(EligibilityBenefits==[]):
                    EligibilityBenefits=TableScrapBenefits(x)
            if("Remaining Deductibles for Benefit Year" in tableheading):
                EligibilityRemainingDeductibles=TableScrap(x)
            elif("Deductibles for Benefit Year" in tableheading):
                EligibilityDeductibles=TableScrap(x)
            elif("Remaining Maximums for Benefit Year" in tableheading and "Limitations" not in x.text and flag!=2):
                EligibilityRemainingMaximums=TableScrap(x)
                flag=1
            elif("Maximums for Benefit Year" in tableheading and "Limitations" not in x.text):
                EligibilityMaximums=TableScrap(x)
            elif("Maximums for Benefit Year" in tableheading and "Limitations" in x.text and flag!=2):
                # EligibilityMaximums=TableScrap(x)
                EligibilityMaximums, FamilyAnnualMaximumBenefits, FamilyAnnualRemainingBenefit, IndividualAnnualMaximumBenefits, IndividualAnnualRemainingBenefit, FamilyLifetimeMaximumBenefits, FamilyLifetimeRemainingBenefit, IndividualLifetimeMaximumBenefits, IndividualLifetimeRemainingBenefit, OrthodonticMaximumBenefit, OrthodonticRemainingBenefit=maxs(x.text)
                flag=2
            elif("Limitations" in tableheading):
                EligibilityLimitations=Limitations(x)
                TreatmentHistorySummary=TreatmentSummary(x, EligibilityBenefits)
        EligibilityServiceTreatmentHistory=[]
        # for x in EligibilityLimitations:
        #     if(x.get("Date").replace("\n", "").replace(' ', '')!=""):
        #         EligibilityServiceTreatmentHistory.append(x)
        EligibilityDeductibles=fixdata(EligibilityDeductibles, EligibilityRemainingDeductibles)
        
        for x in EligibilityDeductibles:
            if(x.get("Type")=="Annual Deductibles" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Dental Care" and x.get("Family_Individual")=="Individual"):
                AnnualDeductiblesDentalCareDeltaDentalPPOIndividual=x.get("Amount")
                RemainingAnnualDeductiblesDentalCareDeltaDentalPPOIndividual=x.get("Remaining")
            elif(x.get("Type")=="Annual Deductibles" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Dental Care" and x.get("Family_Individual")=="Family"):
                AnnualDeductiblesDentalCareDeltaDentalPPOFamily=x.get("Amount")
                RemainingAnnualDeductiblesDentalCareDeltaDentalPPOFamily=x.get("Remaining")
            elif(x.get("Type")=="Lifetime Deductibles" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Dental Care" and x.get("Family_Individual")=="Family"):
                LifetimeDeductiblesDentalCareDeltaDentalPPOIndividual=x.get("Amount")
                RemainingLifetimeDeductiblesDentalCareDeltaDentalPPOIndividual=x.get("Remaining")
            elif(x.get("Type")=="Lifetime Deductibles" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Dental Care" and x.get("Family_Individual")=="Family"):
                LifetimeDeductiblesDentalCareDeltaDentalPPOFamily=x.get("Amount")
                RemainingLifetimeDeductiblesDentalCareDeltaDentalPPOFamily=x.get("Remaining")
        

        if(flag==1):
            EligibilityMaximums=fixdata(EligibilityMaximums, EligibilityRemainingMaximums)
        for x in EligibilityMaximums:
            if(x.get("Type")=="Annual Maximums" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Dental Care" and x.get("Family_Individual")=="Individual"):
                IndividualAnnualMaximumBenefits=x.get("Amount")
                IndividualAnnualRemainingBenefit=x.get("Remaining")
            elif(x.get("Type")=="Annual Maximums" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Dental Care" and x.get("Family_Individual")=="Family"):
                FamilyAnnualMaximumBenefits=x.get("Amount")
                FamilyAnnualRemainingBenefit=x.get("Remaining")
            elif(x.get("Type")=="Lifetime Maximums" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Dental Care" and x.get("Family_Individual")=="Family"):
                IndividualLifetimeMaximumBenefits=x.get("Amount")
                IndividualLifetimeRemainingBenefit=x.get("Remaining")
            elif(x.get("Type")=="Lifetime Maximums" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Dental Care" and x.get("Family_Individual")=="Family"):
                FamilyLifetimeMaximumBenefits=x.get("Amount")
                FamilyLifetimeRemainingBenefit=x.get("Remaining")
            elif(x.get("Type")=="Lifetime Maximums" and x.get("Network")=="Delta Dental PPO" and x.get("ServiceCategory")=="Orthodontics" and x.get("Family_Individual")=="Individual"):
                OrthodonticMaximumBenefit=x.get("Amount")
                OrthodonticRemainingBenefit=x.get("Remaining")
        
        
        EligibilityPatientVerification.update({"FamilyAnnualDeductible":AnnualDeductiblesDentalCareDeltaDentalPPOFamily})
        EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(AnnualDeductiblesDentalCareDeltaDentalPPOFamily, RemainingAnnualDeductiblesDentalCareDeltaDentalPPOFamily)})
        EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":RemainingAnnualDeductiblesDentalCareDeltaDentalPPOFamily})

        EligibilityPatientVerification.update({"FamilyLifetimeDeductible":LifetimeDeductiblesDentalCareDeltaDentalPPOFamily})
        EligibilityPatientVerification.update({"FamilyLifetimeDeductibleMet":calculate_difference(LifetimeDeductiblesDentalCareDeltaDentalPPOFamily, RemainingLifetimeDeductiblesDentalCareDeltaDentalPPOFamily)})
        EligibilityPatientVerification.update({"FamilyLifetimeRemainingDeductible":RemainingLifetimeDeductiblesDentalCareDeltaDentalPPOFamily})

        EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":FamilyLifetimeMaximumBenefits})
        EligibilityPatientVerification.update({"FamilyLifetimeBenefitsUsedtoDate":calculate_difference(FamilyLifetimeMaximumBenefits, FamilyLifetimeRemainingBenefit)})
        EligibilityPatientVerification.update({"FamilyLifetimeRemainingBenefit":FamilyLifetimeRemainingBenefit})

        EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":FamilyAnnualMaximumBenefits})
        EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":calculate_difference(FamilyAnnualMaximumBenefits, FamilyAnnualRemainingBenefit)})
        EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":FamilyAnnualRemainingBenefit})

        EligibilityPatientVerification.update({"IndividualAnnualDeductible":AnnualDeductiblesDentalCareDeltaDentalPPOIndividual})
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(AnnualDeductiblesDentalCareDeltaDentalPPOIndividual, RemainingAnnualDeductiblesDentalCareDeltaDentalPPOIndividual)})
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":RemainingAnnualDeductiblesDentalCareDeltaDentalPPOIndividual})

        EligibilityPatientVerification.update({"IndividualLifetimeDeductible":LifetimeDeductiblesDentalCareDeltaDentalPPOIndividual})
        EligibilityPatientVerification.update({"IndividualLifetimeDeductibleMet":calculate_difference(LifetimeDeductiblesDentalCareDeltaDentalPPOIndividual, RemainingLifetimeDeductiblesDentalCareDeltaDentalPPOIndividual)})
        EligibilityPatientVerification.update({"IndividualLifetimeRemainingDeductible":RemainingLifetimeDeductiblesDentalCareDeltaDentalPPOIndividual})

        EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":IndividualLifetimeMaximumBenefits})
        EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(IndividualLifetimeMaximumBenefits, IndividualLifetimeRemainingBenefit)})
        EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":IndividualLifetimeRemainingBenefit})

        EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":IndividualAnnualMaximumBenefits})
        EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(IndividualAnnualMaximumBenefits, IndividualAnnualRemainingBenefit)})
        EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":IndividualAnnualRemainingBenefit})

        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":OrthodonticMaximumBenefit})
        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":calculate_difference(OrthodonticMaximumBenefit, OrthodonticRemainingBenefit)})
        EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":OrthodonticRemainingBenefit})
        EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":changeNone(EligibilityPatientVerification.get("PlanType"))})
        for x in EligibilityLimitations:
            for y in EligibilityBenefits:
                if(x.get("Procedure")==y.get("ProcedureCode")): 
                    y.update({"limitation":x.get("Limitations")})
                elif(x.get("ServiceType")==y.get("ServiceType")): 
                    y.update({"limitation":x.get("Limitations")})
        # for x in EligibilityBenefits:
        #     x.update({"DeltaDentalPPODeductibleApplies":x.get("DeductibleAppliesDeltaDentalPPO")})

        for x in EligibilityBenefits:
            # if('Specific' not in x.get("NextServiceDate")):
            if(len(x.get("NextServiceDate"))):
                TreatmentHistorySummary.append({
                    "ProcedureCode":x.get("ProcedureCode"),
                    "ProcedureCodeDescription":x.get("procedureCodeDescription"),
                    "LimitationText":"",
                    "LimitationAlsoAppliesTo":"",
                    "History": f'NSD: {x.get("NextServiceDate")}'
                })

        output={}
        output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
        output.update({"EligibilityBenefits":EligibilityBenefits})
        output.update({"EligibilityMaximums":EligibilityMaximums})
        output.update({"EligibilityDeductiblesProcCode":EligibilityDeductibles})
        output.update({"EligibilityServiceTreatmentHistory":TreatmentHistorySummary})
        output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
        output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
        
        
        InputParameters=data.get("InputParameters")
        patient=data.get("PatientData")[0]
        for i in output:
                
            for ctxt in output[i]:
                if type(ctxt).__name__=="dict":
                    ctxt['ClientId']=InputParameters.get('ClientId')
                    ctxt['EligibilityVerificationId']=patient.get('EligibilityVerificationId')
                    if patient.get('PatientId'):
                        ctxt['PatientId']=patient.get('PatientId')
                    if patient.get("RcmGridViewId"):
                        ctxt['RcmGridViewId']=patient.get("RcmGridViewId")
                    if patient.get("PPGridViewId"):
                        ctxt['PPGridViewId']=patient.get("PPGridViewId")                                        
                else:
                    for dct in ctxt:                                                    
                        dct['ClientId']=InputParameters.get('ClientId')
                        dct['EligibilityVerificationId']=patient.get('EligibilityVerificationId')
                        if patient.get('PatientId'):
                            dct['PatientId']=patient.get('PatientId')
                        if patient.get("RcmGridViewId"):                
                            dct['RcmGridViewId']=patient.get("RcmGridViewId")
                        if patient.get("PPGridViewId"):
                            ctxt['PPGridViewId']=patient.get("PPGridViewId")                                
                            
            data_=[]                
            if type(output[i]).__name__=="dict":
                data_= [output[i]]
            else:
                data_=output[i]
       
                                
            if InputParameters['AppName'] =='Eligibility':               
                final_data = {               
                    "ClientId": InputParameters['ClientId'],
                    "DataContextName":i, 
                    "PayorId": InputParameters['PayorId'],
                    "AppName": InputParameters['AppName'],
                    "EligibilityVerificationId": patient.get('EligibilityVerificationId'),
                    "ClinicServerId": patient.get('ClinicServerId'),
                    'PatientId': patient.get('PatientId'),
                    "IsError":False,
                    "ErrorMessage": "",
                     "ScrappingSource": "SD",  
                    "Data": responsemaker(InputParameters,data_,f"{message_id}_{i}")}
                
                QueueHandler( InputParameters['AppName']).send_message(b64encode(bytes(json.dumps(final_data,indent=4), 'utf-8')).decode('utf-8'))
        

        driver.quit()

# data=json.load(open(r"C:\Users\saran\Downloads\config files\finaldns.json", 'r'))
# output=main(data, "123")
# with open("DDNEWres.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)