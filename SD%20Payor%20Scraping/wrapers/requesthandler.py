import json
import re
from datetime import datetime, timedelta
import pytz

def requestmaker(request):
    websiteid=request["InputParameters"].get("WebsiteId")
    AppName = request["InputParameters"].get("AppName")
    PayorName = request["InputParameters"].get("PayorName")



    if websiteid:                
        if websiteid =="GEHA_001":
            for patient in request["PatientData"]:
                BirthDate = patient["BirthDate"].split("/")
                patient["BirthDateMM"] = BirthDate[0]
                patient["BirthDateDD"] = BirthDate[1]
                patient["BirthDateYYYY"] = BirthDate[2]
            return request        

        if websiteid=="DENTALOFFICETOOLKIT001":
            for patient in request["PatientData"]:                                           
                if patient.get('SubscriberBirthDate'):
                    patient['SubscriberBirthDate'] =patient['SubscriberBirthDate'].replace("/","")
            
            procodes=request["InputParameters"].get("ProcCodes")
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])

                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request
            else:
                return request
            

        if websiteid=="DENTALDENTALOHIO_001":
            for patient in request["PatientData"]:                                            
                patient["FirstNameUpper"] = patient["FirstName"].upper()
                if patient.get('SubscriberBirthDate'):
                    patient['SubscriberBirthDate'] =patient['SubscriberBirthDate'].replace("/","")

            procodes=request["InputParameters"].get("ProcCodes")
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])

                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request
            else:
                return request


        elif websiteid =="DNOACONNECT_001":
            procodes=request["InputParameters"].get("ProcCodes")
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request

        elif websiteid =="UNITEDHEALTHCARE_001":
            for patient in request["PatientData"]:
                patientData = patient["ServiceDate"]= datetime.today().strftime('%m/%d/%Y')
            return request
        
        elif websiteid =="ILLINOIS_001":
            for patient in request["PatientData"]:
                if patient.get('FirstName'):
                    patient['FirstName'] =patient['FirstName'].upper()
            procodes=[]
            for code in request["InputParameters"].get("ProcCodes"):
                procodes.append(code.replace("D",""))
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
            return request        

        elif websiteid =="CONNECTICUT_001":
            for patient in request["PatientData"]:
                date_input = patient["BirthDate"]
                date_object = datetime.strptime(date_input, '%m/%d/%Y')
                patient["BirthDate"]=date_object.strftime('%b %d, %Y').replace(" 0"," ")
            procodes=[]
            for code in request["InputParameters"].get("ProcCodes"):
                procodes.append(code.replace("D",""))
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)            
            return request
        
        elif websiteid =="NEWJERSEY_001":
            print("NEWJERSEY_001")
            for patient in request["PatientData"]:                
                date_input = patient["BirthDate"]
                date_object = datetime.strptime(date_input, '%m/%d/%Y')
                patient["BirthDate"]=date_object.strftime('%b %d, %Y').replace(" 0"," ")
            procodes=[]
            for code in request["InputParameters"].get("ProcCodes"):
                procodes.append(code.replace("D",""))
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)            
            return request
        
        elif websiteid =="WASHINGTON_001":
            for patient in request["PatientData"]:
                date_input = patient["BirthDate"]
                date_object = datetime.strptime(date_input, '%m/%d/%Y')
                print(date_object.strftime('%b %d, %Y').replace(" 0"," "))
                patient["BirthDate"]=date_object.strftime('%b %d, %Y').replace(" 0"," ")
            procodes=[]
            for code in request["InputParameters"].get("ProcCodes"):
                procodes.append(code.replace("D",""))
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)            
            return request

        elif websiteid =="COLORADO_001":
            procodes=[]
            procodes=request["InputParameters"].get("ProcCodes")
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request 
            
        elif websiteid =="RHODEISLAND_001":
            procodes=request["InputParameters"].get("ProcCodes")
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits' or i['DataContextName'] =='EligibilityServiceTreatmentHistory':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request
            
        elif websiteid =="OKLAHOMA_001":
            procodes=request["InputParameters"].get("ProcCodes")
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request
        elif websiteid =="MISSOURI_001":
            for patient in request["PatientData"]:
                FirstName = patient["FirstName"]
                LastName = patient["LastName"]
                name_=    LastName.upper() + ', ' + FirstName.upper()
                patient["FullName"] = name_
      
            return request    

        elif websiteid =="PRINCIPAL_001":
            for patient in request["PatientData"]:
                FirstName = patient["FirstName"]
                name_=    FirstName.upper()
                patient["FName"] = name_
      
            return request   

        elif websiteid =="IOWA_001":
            procodes=request["InputParameters"].get("ProcCodes")
            procodesStrip=[]
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                    if i['DataContextName'] =='EligibilityServiceTreatmentHistory':
                        for code in request["InputParameters"].get("ProcCodes"):
                            procodesStrip.append(code.replace("D","").lstrip("0"))
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodesStrip
                        i['XPath']=json.dumps(data_)
                return request
            
        elif websiteid =="OREGONALASKA_001":
            procodes=request["InputParameters"].get("ProcCodes")
            procodesStrip=[]
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request
        
        elif websiteid =="NORTHEAST_001":
            procodes=[]
            for code in request["InputParameters"].get("ProcCodes"):
                procodes.append(code.replace("D",""))
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)            
            return request
        
        elif websiteid =="HAWAII_001":
            for patient in request["PatientData"]:
                BirthDate = patient["BirthDate"].split("/")
                patient["BirthDateMM"] = BirthDate[0]
                patient["BirthDateDD"] = BirthDate[1]
                patient["BirthDateYYYY"] = BirthDate[2]
            return request 

        elif websiteid =="ENVOLVE_001":
            for patient in request["PatientData"]:
                patient["LastName"]=patient["LastName"].upper()
                patient["FirstName"]=patient["FirstName"].upper()
                patient["FullName"]=patient["FirstName"]+' '+patient["LastName"]
            return request
        
        elif websiteid =="DENTAQUEST_001":
            for patient in request["PatientData"]:
                FirstName = patient["FirstName"]
                LastName = patient["LastName"]
                name_=    FirstName.upper() + ' ' + LastName.upper()
                patient["FullName"] = name_

                providername = patient["ProviderFirstName"]
                location = patient["ClinicZip"].strip()
                if '-' in location:
                    location = location.split('-')[0]
                patient["location"] = location
                patient["providername"] = providername
      
            return request  

        elif websiteid =="AETNA_001":
            procodes=request["InputParameters"].get("ProcCodes")
            procodesStrip=[]
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                    if i['DataContextName'] =='EligibilityOtherProvisions':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request
            
        elif websiteid =="DDVIRGINIA_001":
            procodes=request["InputParameters"].get("ProcCodes")
            procodesStrip=[]
            if procodes:
                for i in request['Xpaths']:
                    if i['DataContextName'] =='EligibilityBenefits':
                        data_=json.loads(i['XPath'])
                        data_['MultiplElements']['Searchlist']=procodes
                        i['XPath']=json.dumps(data_)
                return request
        
        else:
            return request



    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental Toolkit" and request.get('PatientData')[0].get('SubscriberBirthDate'):
        for patient in request["PatientData"]:
            if " " in patient["ProviderLastName"]:
                patient["ProviderLastName"] = patient["ProviderLastName"].split(" ")[0]
            patient['SubscriberBirthDate'] = patient['SubscriberBirthDate'].replace("/", "")
            #patient['DateOfService'] = patient['DateOfService'].replace("/", "")
            fullname =patient['ProviderLastName']+", "+         patient['ProviderFirstName']
            patient['ProviderFullName'] = fullname.upper()
            patient['FullName1'] =patient['FullName'].upper()
            patient['SmallFullName'] =patient['FullName'].title()
            patient['ProviderLastName']  = patient['ProviderLastName'].upper()
            patient['ProviderFirstName'] =patient['ProviderFirstName'].upper()
            DateOfService = patient['DateOfService']
            date_object = datetime.strptime(DateOfService, "%m/%d/%Y")
            days_to_add = 7
            current_date = datetime.now()
            converted_date = date_object + timedelta(days=days_to_add)
            if current_date.date() < converted_date.date():
                converted_date = min(converted_date, datetime.now())
            converted_date_string = converted_date.strftime("%m/%d/%Y")
            patient['DateOfService1'] = converted_date_string 

        return request                        
    elif AppName == "Revenue Cycle Management" and PayorName == "United Concordia":
        for patient in request["PatientData"]:
            patient["FirstName"] = patient["FirstName"].upper()
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Dental Network of America":
        for patient in request["PatientData"]:
            patient["fullNameUpper"] = patient["FullName"].upper()
            DateOfService = patient["DateOfService"]
            month, day, year = map(int, DateOfService.split('/'))
            DateOfService = "{:d}/{:d}/{:d}".format(month, day, year)
            patient["DateOfService"] = DateOfService
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Cigna":
        for patient in request["PatientData"]:
            DateOfService = patient["DateOfService"]
            DateOfService = "{}-{}".format(DateOfService, DateOfService)
            patient["DateOfService"] = DateOfService
            LastName = patient["LastName"]
            patient["LastName"] = re.sub(r'[^a-zA-Z0-9]+', '', LastName)
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta dental":
        for patient in request["PatientData"]:
            patientData = patient
            if patientData['SubscriberFirstName'] == patientData['FirstName']:
                searchparmas = json.loads(request['SearchParameters'][0]['JsonSettings'])
                searchparmas['Search']['Settings']['PreSteps']['Clicks'] = []
                request['SearchParameters'][0]['JsonSettings'] = json.dumps(searchparmas)
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "United Healthcare":
        for patient in request["PatientData"]:
            FirstName = patient["FirstName"]
            LastName = patient["LastName"]
            name_=    LastName + ', ' + FirstName
            patient["FullName"] = name_.upper()
        return request


    elif AppName == "Revenue Cycle Management" and PayorName == "Government Employees Health Association":
        for patient in request["PatientData"]:
            BirthDate = patient["BirthDate"].split("/")
            patient["BirthDateMM"] = BirthDate[0]
            patient["BirthDateDD"] = BirthDate[1]
            patient["BirthDateYYYY"] = BirthDate[2]
            DateOfService = patient["DateOfService"]
            patient["DateOfService1"] = DateOfService
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental Ins":
        for patient in request["PatientData"]:       
            amount =patient["ClaimAmount"]
            patient["ClaimAmount"] ="{:,.2f}".format(float(amount))
        
        return request
    elif AppName == "Revenue Cycle Management" and PayorName == "Principal":
        for patient in request["PatientData"]:
            patient["DateOfService"]     =       patient["DateOfService"].replace("/","")   
            patient["BirthDate"]         =patient["BirthDate"].replace("/","")             
            patient["ProviderTIN"] ="4771"        
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental Illinois":
        for patient in request["PatientData"]:
            FirstName = patient["FirstName"]
            LastName = patient["LastName"]
            name_=    FirstName + ' ' + LastName 
            patient["FullName"] = name_
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental Connecticut":
        for patient in request["PatientData"]:
            input_date_str = patient["DateOfService"]
            input_date = datetime.strptime(input_date_str, '%m/%d/%Y')
            output_date_str = input_date.strftime('%b{}{}, %Y'.format(' ' if input_date.day <= 10 else ' ', input_date.day))
            patient["DateOfService1"] = output_date_str
            ClinicDetails = request["InputParameters"]["ClinicDetails"]["SearchKey"][0]
            patient["Location"] = ClinicDetails
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental of New Jersey":
        for patient in request["PatientData"]:
            input_date_str = patient["DateOfService"]
            input_date = datetime.strptime(input_date_str, '%m/%d/%Y')
            output_date_str = input_date.strftime('%b{}{}, %Y'.format(' ' if input_date.day <= 10 else ' ', input_date.day))
            patient["DateOfService1"] = output_date_str
            ClinicDetails = request["InputParameters"]["ClinicDetails"]["SearchKey"][0]
            patient["Location"] = ClinicDetails
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental of Washington":
        for patient in request["PatientData"]:
            input_date_str = patient["DateOfService"]
            input_date = datetime.strptime(input_date_str, '%m/%d/%Y')
            output_date_str = input_date.strftime('%b{}{}, %Y'.format(' ' if input_date.day <= 10 else ' ', input_date.day))
            patient["DateOfService1"] = output_date_str
            ClinicDetails = request["InputParameters"]["ClinicDetails"]["SearchKey"][0]
            patient["Location"] = ClinicDetails
            patient['FullName1'] = patient['FullName'].upper()
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental of Oklahoma":
        for patient in request["PatientData"]:
            ClinicDetails = request["InputParameters"]["ClinicDetails"]["SearchKey"][0]
            patient["Location"] = ClinicDetails
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental Iowa":
        for patient in request["PatientData"]:
            us_timezone = pytz.timezone('US/Eastern')
            today = datetime.now(us_timezone).date()
            mmddyyyy_format = today.strftime("%m/%d/%Y")
            patient["DateOfService1"] = mmddyyyy_format
            ClinicDetails = request["InputParameters"]["ClinicDetails"]["SearchKey"][0]
            patient["Location"] = ClinicDetails
            patient_first_name = patient["FirstName"]
            patient_last_name = patient["LastName"]
            patient_name = f'{patient_last_name}, {patient_first_name}'
            patient["PatientName1"] = patient_name
        return request

    elif AppName == "Revenue Cycle Management" and PayorName in ["Delta Dental of Oregon", "Delta Dental Alaska"]:
        # Expecting ["PatientData"][0]["DateOfService"] as '%m/%d/%Y' eg. 07/08/2023
        for patient in request['PatientData']:
            date_of_service = datetime.strptime(patient["DateOfService"], '%m/%d/%Y')
            patient["DateOfService1"] = \
                str(date_of_service.month)+"/"+str(date_of_service.day)+"/"+\
                str(date_of_service.year)[2:]
            patient["BirthMonth"]=patient["BirthDate"].split('/')[0]
            patient["BirthDate"]=patient["BirthDate"].split('/')[1]
            patient["BirthYear"]=patient["BirthDate"].split('/')[2]
        return request
    
    elif AppName == "Revenue Cycle Management" and PayorName == "Lincoln Financial":
        for patient in request['PatientData']:
            input_ProviderSID=patient['SubscriberId']
            input_ProviderSID=input_ProviderSID[-4:]
            patient['SubscriberId']=input_ProviderSID
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental of Missouri":
        for patient in request['PatientData']:
            input_ProviderFirstName=patient['ProviderFirstName'].upper()
            patient['ProviderFirstName']=input_ProviderFirstName
            input_ProviderLastName=patient['ProviderLastName'].upper()
            patient['ProviderLastName']=input_ProviderLastName
            input_FirstName=patient['FirstName'].upper()
            patient['FirstName']=input_FirstName
            input_LastName=patient['LastName'].upper()
            patient['LastName']=input_LastName
            patient['DateRange']="200"
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Ameritas":

        for patient in request["PatientData"]:
            clinic_details = request["InputParameters"].get("ClinicDetails")
            if clinic_details and clinic_details.get("SearchKey")[0]:
                patient["Location"] = clinic_details["SearchKey"][0]
            else:
                print("Request Handler: Location is required.")

            date = patient['DateOfService']
            month, day, year = date.split('/')
            short_year = year[-2:]
            converted_date = f"{month}/{day}/{short_year}"
            patient["DateOfService1"] = converted_date
        return request
        
    
    elif AppName == "Revenue Cycle Management" and PayorName == "Sun Life":
        for patient in request["PatientData"]:
            input_f_name=patient['FirstName']
            input_f_name=input_f_name.upper()
            patient['FirstName']=input_f_name
        return request
    
    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental of Massachusetts":
        for patient in request["PatientData"]:
            input_f_name=patient['FirstName']
            input_f_name=input_f_name.upper()
            patient['CapsFirstName']=input_f_name
        return request

    elif AppName == "Revenue Cycle Management" and PayorName == "Delta Dental of Wisconsin":
        for patient in request["PatientData"]:
            input_f_name=patient['FirstName']
            input_f_name=input_f_name.upper()
            patient['CapsFirstName']=input_f_name
        return request
        
    else:
        return request



