from Utilities.pdf_utils import *
from FileDownload import Downloader
from mapPDF import mapEligibilityPatientVerification
from typing import Iterable
import re
import tabula


def changeNone(text):
    if(text=="None" or text=="N/A" or text==None):
        return ""
    else:
        return text
def calculate_difference(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    difference=f'${float(a)-float(b)}'
    if(difference=="$0.00"): return "0.00"
    return f'${round(float(a)-float(b) , 2)}'
def getsum(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)+float(b)}'



def PDFScrape(data):

    file_path =''.join(random.choices(string.ascii_uppercase +string.digits, k=10)) + ".pdf"
    print(file_path)
    input_file = data["EligibilityPatientVerification"][0]["url"].replace("%20", " ")
    Downloader('Eligibility',file_path,input_file)
    # file_path ="DDMi_2.pdf"

    # file_path = 'IdahoPDF.pdf'
    data_frames, work_dict = get_data_in_format(file_path) 

    dftabula = tabula.read_pdf(file_path,guess=False, pages='1', stream=True , encoding="utf-8",area = 
                         (697.2936712646484,19.584004669189454, 741.1336712646485,587.4490046691894))
    dftabula=dftabula[0]

    address = f"Delta Dental Idaho {dftabula.columns[0].split(',')[0]}"
    payor_id = dftabula.columns[0].split('Payor ID')[1].strip()


    for i,item in enumerate(work_dict.get('elements')):
        text = item.get('Text')
        if text is not None:
            if "Today's Date:" in text:
                date = text.split(':')[1].replace('Patient Information ",','')  
                date = date.replace('Patient Information','').strip()
                # print(date)
            if 'Dependents' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                dependent = sub_text.split(':')[-1].strip()
                # print(dependent)
            if 'Orthodontic Services Child Only' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+3]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                searvicechild = sub_text.split(':')[-1].strip().replace('Orthodontic Services Child Only ','')
                # print(searvicechild)    
            if "Missing" in text:
                missingtoothclouse = text.split('Missing')[1].split('.')[0]
                missingtoothclouse = 'Missing ' + missingtoothclouse.replace('Patient Information','').strip()
                print(missingtoothclouse)    
            if "Composite fillings"  in text:
                composite = text.split('Composite')[1].split('.')[0]
                composite = 'Composite ' + composite.replace('Patient Information','').strip() 

    data["EligibilityPatientVerification"][0].update(
        {'DependentStudentAgeLimit': str(dependent),
         'Orthodoncticservicechild': str(searvicechild),
         'address': str(address),
         'Payorid': str(payor_id),
         'missingtoothclouse': str(missingtoothclouse),
         'composite': str(composite)
        }
        )   

    
    if 'EligibilityMaximums' not in data:
        data['EligibilityMaximums'] = []     
    if 'EligibilityServiceTreatmentHistory' not in data:
        data['EligibilityServiceTreatmentHistory'] = []
    if 'EligibilityOtherProvisions' not in data:
        data['EligibilityOtherProvisions'] = []

        # dataframe 0 
        ele_patient_verification = ['Patient Information ', 'Unnamed: 1']

# DAtaframe 1 ---------------------------------------
    Elig_patient_max_columnone = ["Today's Date: " + date +" Patient Information ",
            'Unnamed: 1',
            'Benefit Information ',
            'PPO ',
            'Premier ',
            'Non-Par ']  
    Elig_patient_max_column = ['Patient Information ', 'Unnamed: 1', 'Benefit Information ', 'PPO ',
       'Premier ', 'Non-Par ']
    Elig_patient_max_column_next = ['Benefit Information ', 'PPO ', 'Premier ', 'Non-Par ']
# ---------------------------------------------------------------------------- 
    
    # dataframe 2 ________________________________________________________
    Proccode = ['Procedure Code ', 'Procedure Code Description ', 'Last Service Date ',
       'Tooth or Quadrant ', 'Age Restriction ']   
#  ------------------------------------------------------------------------------------------


    Plansummary = ['Plan Summary ', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3']        



    for df in data_frames:
        # print(df.columns)
        if all(col in df.columns for col in ele_patient_verification):
            df.columns = ['Keys', 'values']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityMaximums'].append(record)

        if all(col in df.columns for col in Elig_patient_max_columnone):
            df.columns = ['Keys', 'values', 'Benefit Information',
                'PPO', 'Premier', 'NonPar']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityMaximums'].append(record)
        elif all(col in df.columns for col in Elig_patient_max_column):
            df.columns = ['Keys', 'values', 'Benefit Information',
                'PPO', 'Premier', 'NonPar']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityMaximums'].append(record)
        elif all(col in df.columns for col in Elig_patient_max_column_next):
            df.columns = ['Benefit Information','PPO', 'Premier', 'NonPar']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityMaximums'].append(record)        

        if all(col in df.columns for col in Proccode):
            df.columns = ['Procedurecode', 'Procedurecodedescription', 'Lastservicedate',
                'Tooth', 'Agerestriction']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityServiceTreatmentHistory'].append(record)   

        if all(col in df.columns for col in Plansummary):
            df.columns = ['Plansummary', 'PPO', 'Premier', 'Nonparticipating']
            df.fillna('',inplace=True)
            data['EligibilityOtherProvisions'].append(df.to_dict('records'))                
        # print(df.to_dict('records'))

    # return data



#     with open("newJson_57742_new.json", "w") as jsonFile:
#         json.dump(data, jsonFile,indent=4)


# with open("output_57742.json", "r") as jsonFile:
#     data = json.load(jsonFile)
# PDFScrape(data)




def main(Scraperdata, request):

    pdf_data = PDFScrape(Scraperdata)

    patientdata = request.get("PatientData")[0]
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityDEductible = Scraperdata.get("EligibilityDeductible")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions")
   

    #print(EligibilityPatient)

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]
  

    # relationship_value = ""  
    try: 
        
        for item in EligibilityMaximiums:
            # print(item.get("Keys"))
            if "Group Name:" in item.get("Keys"):
                # print('found')
                group_name_dict = next(item for item in EligibilityMaximiums if "Group Name:" in item.get("Keys"))
                group_name_value = group_name_dict.get("values")
                # print(group_name_value)
            if "Group Number:" in item.get("Keys"):
                group_number_dict = next(item for item in EligibilityMaximiums if "Group Number:" in item.get("Keys"))
                group_number_value = group_number_dict.get("values")
                # print(group_number_value)
            if "Subscriber Name:" in item.get("Keys"):
                Subscriber_Name_dict = next(item for item in EligibilityMaximiums if "Subscriber Name:" in item.get("Keys"))
                Subscriber_Name_value = Subscriber_Name_dict.get("values")
                # print(Subscriber_Name_value)
            if "Patient Name:" in item.get("Keys"):  
                Patient_name_dict = next(item for item in EligibilityMaximiums if "Patient Name:" in item.get("Keys"))
                patient_name_value = Patient_name_dict.get("values")
                # print(patient_name_value)
            if "Relationship:" in item.get("Keys"):
                relationship_dict = next(item for item in EligibilityMaximiums if "Relationship:" in item.get("Keys"))
                relationship_value = relationship_dict.get("values")
                # print(relationship_value)
            if  "Effective Date:" in item.get("Keys"):
                effective_date_dict = next(item for item in EligibilityMaximiums if "Effective Date:" in item.get("Keys"))
                effectivedate_value = effective_date_dict.get("values")
                # print(effectivedate_value)
            if "Termination Date:" in item.get("Keys"):     
                termination_date_dict = next(item for item in EligibilityMaximiums if "Termination Date:" in item.get("Keys"))
                terminationdate_value = termination_date_dict.get("values")
                # print(terminationdate_value)
            if  "Wait Period Ends:" in item.get("Keys"):   
                witperiodends_dict = next(item for item in EligibilityMaximiums if "Wait Period Ends:" in item.get("Keys"))
                witperiodends_value = witperiodends_dict.get("values")
                # print(witperiodends_value)
            if "Benefit Year:" in item.get("Keys"):
                benefityear_dict = next(item for item in EligibilityMaximiums if "Benefit Year:" in item.get("Keys"))
                benefityear_value = benefityear_dict.get("values")
                values = benefityear_value.split('No')[0].strip()
                # print(values)

        

        

    except:
        pass 



    EligibilityPatientVerification.update(
        {
        
        "FamilyMemberId":patientdata.get("SubscriberId", ''),
        "SubscriberId":patientdata.get("SubscriberId"),
        "SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName"),
        # "InsuranceIDnumber":EligibilityPatient[0].get("Payorid").replace('#',''),
        "FamilyMemberName":patient_name_value,
        "FamilyMemberDateOfBirth":patientdata.get("BirthDate"),
        "Relationship":relationship_value,
        "SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate"),
        "FamilyMemberEffectiveDate":effectivedate_value,
        "FamilyMemberEndDate":terminationdate_value,
        "FamilyMemberWaitingPeriod":witperiodends_value,
        # "InsuranceFeeScheduleUsed":EligibilityPatient[0].get("Programtype"),
        "GroupName":group_name_value,
        "GroupNumber":group_number_value,
        "DependentChildCoveredAgeLimit":EligibilityPatient[0].get("DependentStudentAgeLimit"),
        # "DependentChildCoveredAgeLimit":EligibilityPatient[0].get("Orthodoncticservicechild").split('.')[0].split('Eligible')[1],
        "InsuranceCalendarOrFiscalPolicyYear":values,
        "InNetworkOutNetwork":"In Network",
        "oonBenefits":"Yes",
        # "MedicallyNecessaryonly":"Yes",
        # "CoordinationofBenefitsType":EligibilityPatient[0].get("COBtype"),
        "AlternativeBenefitProvision":EligibilityPatient[0].get("composite"),        
        "ClaimsAddress":EligibilityPatient[0].get("address"),
        "ClaimMailingAddress":EligibilityPatient[0].get("address"),
        "ClaimPayerID":EligibilityPatient[0].get("Payorid").replace('#',''),
        "MissingToothClause":EligibilityPatient[0].get("missingtoothclouse"),       
        }
    )

    if EligibilityPatientVerification.get("FamilyMemberEffectiveDate", None):
        EligibilityPatientVerification.update({"EligibilityStatus":"Active"}) 
    
    
    try:
      
        EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":"PPO"})
    except:
        pass


    for items in Scraperdata["EligibilityMaximums"]:
            if "Benefit Information" in items:
                benefit_name = items["Benefit Information"].strip()
                # print(benefit_name)
                if benefit_name:
                    if "Individual Annual Deductible:" in benefit_name:
                        individualannualdeductibleremainingvalue = items.get("Premier")
                        print(individualannualdeductibleremainingvalue)
                        IndividualAnnualdeductible_value = items.get("PPO")
                        print(IndividualAnnualdeductible_value)

                    if "Family Annual Deductible:" in  benefit_name:
                        familyannualdeductibleremainingvalue = items.get("Premier")
                        print(familyannualdeductibleremainingvalue)
                        familyAnnualdeductible_value = items.get("PPO")
                        print(familyAnnualdeductible_value)

                    if "Individual Annual Max:"  in  benefit_name:  
                        individualannualmaximumemainingvalue = items.get("Premier")
                        print(individualannualmaximumemainingvalue)
                        individualannualmax_value = items.get("PPO")
                        print(individualannualmax_value)

                    if "Ortho Lifetime Max:"  in  benefit_name:  
                        ortholifetimevalue = items.get("Premier")
                        print(ortholifetimevalue)
                        ortholifetime_value = items.get("PPO")
                        print(ortholifetime_value)    


    EligibilityPatientVerification.update({"IndividualAnnualDeductible":IndividualAnnualdeductible_value.strip()})    
    EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":individualannualdeductibleremainingvalue.strip()}) 
    EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining").strip())})                                     
    
    EligibilityPatientVerification.update({"FamilyAnnualDeductible":familyAnnualdeductible_value.strip()})    
    EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":familyannualdeductibleremainingvalue.strip()}) 
    EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining").strip())})               
   
    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":individualannualmax_value.strip()})   
    EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":individualannualmaximumemainingvalue.strip()})     
    EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip())})                                    
   
    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":ortholifetime_value})
    EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":ortholifetimevalue})
    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":calculate_difference(EligibilityPatientVerification.get("OrthodonticLifetimeBenefit").strip(),EligibilityPatientVerification.get("OrthodonticLifetimeRemainingBenefit").strip())})                                    
    
    EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":ortholifetime_value})    
    EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":ortholifetimevalue})   
    EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit").strip())})                                    



    try:
        EligibilityPatientVerification.update({"OrthodonticAgeLimits":EligibilityPatient[0].get("Orthodoncticservicechild").split('.')[0].split('Eligible')[1]})
    except:
        pass    

   
    EligibilityMaximums.append({
                "Type":  "Lifetime Maximum",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits"),
                "Remaining": EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })
    EligibilityMaximums.append({
                "Type":  "Annual Maximum",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits"),
                "Remaining": EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })     
    EligibilityMaximums.append({
                "Type":  "Orthodontic Lifetime",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("OrthodonticLifetimeBenefit"),
                "Remaining": EligibilityPatientVerification.get("OrthodonticLifetimeRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("OrthodonticLifetimeBenefitUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })  
       


    EligibilityDeductiblesProcCode.append({
                "Type":  "Annual Deductible",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualAnnualDeductible"),
                "Remaining": EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining"),
                "Used": EligibilityPatientVerification.get("IndividualAnnualDeductibleMet"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            }) 
    EligibilityDeductiblesProcCode.append({
                "Type":  "Annual Deductible",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("FamilyAnnualDeductible"),
                "Remaining": EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining"),
                "Used": EligibilityPatientVerification.get("FamilyAnnualDeductibleMet"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            }) 


    EligibilityBenefits = []  # initialize the list of benefits
    EligibilityServiceTreatmentHistory = []
    TreatmentHistorySummary = []

    for searchItem in EligibilityBenefitsData:
        procedure = searchItem.get("ProcCode").strip()
        if procedure.startswith("0"):
            procedure = procedure.replace("0", "D", 1)
    
        EligibilityBenefits.append({
            "ProcedureCode": procedure.strip(),
            "ProcedureCodeDescription": searchItem.get("ProcedureDescription"),
            "Amount": "",
            "Type": "",
            "limitation": searchItem.get("FrequencyAndLimitations"),
            "DeductibleApplies": "",
            "Copay": "",
            "Benefits": searchItem.get("DeltaPays"),
            "WaitingPeriod": searchItem.get("WaitPeriod")
        })
        EligibilityServiceTreatmentHistory.append({
        "ProcedureCode": procedure,
        "LimitationText": searchItem.get("FrequencyAndLimitations"),
        "History": searchItem.get("LastDateofService"),
        "Tooth": "",
        "Surface": "",
        "LimitationAlsoAppliesTo": "",
        "ProcedureCodeDescription": searchItem.get("ProcedureDescription")                
        })  
        TreatmentHistorySummary.append({
            "ProcedureCode": procedure,
            "LimitationText": searchItem.get("FrequencyAndLimitations"),
            "History": searchItem.get("LastDateofService"),
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": searchItem.get("ProcedureDescription")                
        }) 


    # for itemss in EligibilityBenefitsData:        
    #     procedure = searchItem.get("ProcCode").strip()
    #     if procedure.startswith("0"):
    #         procedure = procedure.replace("0", "D", 1)

       

        
        if searchItem.get("Proccode") == "D2391":
            EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":searchItem.get("WaitPeriod")})



    output={}

    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output



# request=json.load(open(r"C:\BPK\Eligibility_Python\VSCODE\26_07_04_12\SD Payor Scraping\Idaho.json", 'r'))
# data=json.load(open(r"C:\BPK\Eligibility_Python\VSCODE\26_07_04_12\SD Payor Scraping\output_57742.json", 'r'))
# output=main(data, request)
# with open("Idaho_57742_.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)

