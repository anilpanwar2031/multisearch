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
                         (698.8275,18.7425, 738.6075,597.8475))
    # print(dftabula)
    dftabula=dftabula[0]

    address_ = f"Delta Dental Wyoming {dftabula.columns[0].split(',')[0]}"
    print(address_)
    payor_id = dftabula.columns[0].split('Payer ID')[1].strip()
    print(payor_id)


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
                # print('searchvicevalue :- ',searvicechild)    

    data["EligibilityPatientVerification"][0].update(
        {'DependentStudentAgeLimit': str(dependent),
         'Orthodoncticservicechild': str(searvicechild),
         'address': str(address_),
         'Payorid': str(payor_id),
        }
        )   

    
    if 'EligibilityMaximums' not in data:
        data['EligibilityMaximums'] = []     
    if 'EligibilityServiceTreatmentHistory' not in data:
        data['EligibilityServiceTreatmentHistory'] = []
    if 'EligibilityOtherProvisions' not in data:
        data['EligibilityOtherProvisions'] = []

    Elig_patient_verification_columnone = ["Today's Date: " + date +" Patient Information ",
                'Unnamed: 1',
                'Benefit Information ',
                'Premier ',
                'Non-Par ']  
    Elig_patient_verification_column = ['Patient Information ', 'Unnamed: 1', 'Benefit Information ', 'PPO ',
       'Premier ', 'Non-Par ']
    Proccode = ['Procedure Code ', 'Procedure Code Description ', 'Last Service Date ',
       'Tooth or Quadrant ', 'Age Restriction ']   

    Plansummary = ['Plan Summary ', 'Unnamed: 1', 'Unnamed: 2']      



    for df in data_frames:
        if all(col in df.columns for col in Elig_patient_verification_columnone):
            df.columns = ['Keys', 'values', 'Benefit Information',
         'Premier', 'NonPar']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityMaximums'].append(record)
        elif all(col in df.columns for col in Elig_patient_verification_column):
            df.columns = ['Keys', 'values', 'Benefit Information',
    'PPO', 'Premier', 'NonPar']
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
            df.columns = ['Plansummary', 'Premier', 'Nonparticipating']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityOtherProvisions'].append(record)            
        # print(df.to_dict('records'))

    return data



#     with open("newJsonwyomingPDFoutput.json", "w") as jsonFile:
#         json.dump(data, jsonFile,indent=4)


# with open("output.json", "r") as jsonFile:
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
  


    try:   
        group_name_dict = next(item for item in EligibilityMaximiums if "Group Name:" in item.get("Keys"))
        group_name_value = group_name_dict.get("values")
        # print(group_name_value)
        group_number_dict = next(item for item in EligibilityMaximiums if "Group Number:" in item.get("Keys"))
        group_number_value = group_number_dict.get("values")
        # print(group_number_value)
        Subscriber_Name_dict = next(item for item in EligibilityMaximiums if "Subscriber Name:" in item.get("Keys"))
        Subscriber_Name_value = Subscriber_Name_dict.get("values")
        # print(Subscriber_Name_value)
        Patient_name_dict = next(item for item in EligibilityMaximiums if "Patient Name:" in item.get("Keys"))
        patient_name_value = Patient_name_dict.get("values")
        # print(patient_name_value)
        relationship_dict = next(item for item in EligibilityMaximiums if "Relationship:" in item.get("Keys"))
        relationship_value = relationship_dict.get("values")
        # print(relationship_value)
        effective_date_dict = next(item for item in EligibilityMaximiums if "Effective Date:" in item.get("Keys"))
        effectivedate_value = effective_date_dict.get("values")
        # print(effectivedate_value)
        termination_date_dict = next(item for item in EligibilityMaximiums if "Termination Date:" in item.get("Keys"))
        terminationdate_value = termination_date_dict.get("values")
        # print(terminationdate_value)
        witperiodends_dict = next(item for item in EligibilityMaximiums if "Wait Period Ends:" in item.get("Keys"))
        witperiodends_value = witperiodends_dict.get("values")
        # print(witperiodends_value)
        benefityear_dict = next(item for item in EligibilityMaximiums if "Benefit Year:" in item.get("Keys"))
        benefityear_value = benefityear_dict.get("values")
        values = benefityear_value.split('No')[0].strip()
        # print(values)
    

        EligibilityPatientVerification.update(
        {
        "FamilyMemberId":patientdata.get("SubscriberId", ''),
        "SubscriberId":patientdata.get("SubscriberId"),
        "SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName"),
        "FamilyMemberName":patient_name_value,
        "FamilyMemberDateOfBirth":patientdata.get("BirthDate"),
        "Relationship":relationship_value,
        "SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate"),
        "FamilyMemberEffectiveDate":effectivedate_value,
        "FamilyMemberEndDate":terminationdate_value,
        "FamilyMemberWaitingPeriod":witperiodends_value,
        "GroupNumber":group_number_value,
        "GroupName":group_name_value,
        "DependentChildCoveredAgeLimit":EligibilityPatient[0].get("DependentStudentAgeLimit"),
        "InsuranceCalendarOrFiscalPolicyYear":values,
        "InNetworkOutNetwork":"In Network",
        "oonBenefits":"Yes",
        "ClaimsAddress":EligibilityPatient[0].get("address"),
        "ClaimMailingAddress":EligibilityPatient[0].get("address"),
        "ClaimPayerID":EligibilityPatient[0].get("Payorid").replace('#','')
        }
    )

    except:
        pass 
   

    if EligibilityPatientVerification.get("FamilyMemberEffectiveDate", None):
        EligibilityPatientVerification.update({"EligibilityStatus":"Active"})    

    missingvalue = ""
    missingvalue = ""
    for provision in EligibilityOtherProvisions:
        plansummary = provision.get("Plansummary")
        if "Missing" in plansummary:
            value = plansummary.split('Missing')[1].split('.')[0]
            missingvalue = 'Missing' + value
        # print(missingvalue)    
    EligibilityPatientVerification.update({"MissingToothClause":missingvalue})    
   
    try:
        alternatevalue = ""
        for provision_list in EligibilityOtherProvisions:
                plansummary = provision_list.get("Plansummary")
                if 'composite' in plansummary:
                    value = plansummary.split('composite')[1].split('.')[0]
                    alternatevalue = 'composite' + value
                # print(alternatevalue)        
        EligibilityPatientVerification.update({"AlternativeBenefitProvision":alternatevalue})
    except:
        pass
    try:
        orthodonticvalue = ""
        for provision_list in EligibilityOtherProvisions:
                plansummary = provision_list.get("Plansummary")
                if 'Comprehensive' in plansummary:
                    value = plansummary.split('Comprehensive')[1].split('.')[0]
                    orthodonticvalue = 'Comprehensive' + value
                # print(orthodonticvalue)        
        EligibilityPatientVerification.update({"OrthodonticAgeLimits":orthodonticvalue})
    except:
        pass

    try:
        # insurancevalue = ""
        # for provision_list in EligibilityOtherProvisions:
        #     for provision in provision_list:
        #         plansummary = provision.get("Plansummary")
        #         if 'Class I' in plansummary:
        #             insurancevalue = provision.get("PPO")
        EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":"Premier"})
    except:
        pass



    try:
        ppo_value = None
        found_individual_deductible = False
        individualannualdeductibleremainingvalue = ""

        for i in range(len(EligibilityMaximiums) - 1):
            if EligibilityMaximiums[i]["Benefit Information"] == "Individual Annual Deductible: ":
                found_individual_deductible = True
                ppo_value = EligibilityMaximiums[i + 1]["Premier"]
                break

        if found_individual_deductible:
            individualannualdeductibleremainingvalue = ppo_value
            print(individualannualdeductibleremainingvalue)
        else:
            print("Individual Annual Deductible not found.")  


        IndividualAnnualdeductible_dict = next(item for item in EligibilityMaximiums if "Individual Annual Deductible:" in item.get("Benefit Information"))
        IndividualAnnualdeductible_value = IndividualAnnualdeductible_dict.get("Premier")
        # print(IndividualAnnualdeductible_value)          

        EligibilityPatientVerification.update({"IndividualAnnualDeductible":IndividualAnnualdeductible_value.strip()})    
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":individualannualdeductibleremainingvalue.strip()}) 
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining").strip())})               
    except:
        pass

    try:
        ppo_value = None
        found_Family_Annual_deductible = False
        familyannualdeductibleremainingvalue = ""

        for i in range(len(EligibilityMaximiums) - 1):
            if EligibilityMaximiums[i]["Benefit Information"] == "Family Annual Deductible: ":
                found_Family_Annual_deductible = True
                ppo_value = EligibilityMaximiums[i + 1]["Premier"]
                break

        if found_Family_Annual_deductible:
            familyannualdeductibleremainingvalue = ppo_value
        else:
            print("Family Annual Deductible not found.")  


        familyAnnualdeductible_dict = next(item for item in EligibilityMaximiums if "Family Annual Deductible:" in item.get("Benefit Information"))
        familyAnnualdeductible_value = familyAnnualdeductible_dict.get("Premier")
        # print(IndividualAnnualdeductible_value)          

        EligibilityPatientVerification.update({"FamilyAnnualDeductible":familyAnnualdeductible_value.strip()})    
        EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":familyannualdeductibleremainingvalue.strip()}) 
        EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining").strip())})               
    except:
        pass



    try:

        ppo_value = None
        found_Individual_Annual_maximum = False
        individualannualmaximumemainingvalue = ""

        for i in range(len(EligibilityMaximiums) - 1):
            if EligibilityMaximiums[i]["Benefit Information"] == "Individual Annual Max: ":
                found_Individual_Annual_maximum = True
                ppo_value = EligibilityMaximiums[i + 1]["Premier"]
                break

        if found_Individual_Annual_maximum:
            individualannualmaximumemainingvalue = ppo_value
        else:
            print("Individual annual max not found.")  


        individualannualmax_dict = next(item for item in EligibilityMaximiums if "Individual Annual Max:" in item.get("Benefit Information"))
        individualannualmax_value = individualannualmax_dict.get("Premier")

        EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":individualannualmax_value.strip()})   
        EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":individualannualmaximumemainingvalue.strip()})     
        EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip())})                                    
    except:
        pass

    try:
        ppo_value = None
        found_Ortholifetime_maximum = False
        ortholifetimevalue = ""

        for i in range(len(EligibilityMaximiums) - 1):
            if EligibilityMaximiums[i]["Benefit Information"] == "Ortho Lifetime Max: ":
                found_Ortholifetime_maximum = True
                ppo_value = EligibilityMaximiums[i + 1]["Premier"]
                break

        if found_Ortholifetime_maximum:
            ortholifetimevalue = ppo_value
        else:
            print("Individual annual max not found.")  


        ortholifetimemax_dict = next(item for item in EligibilityMaximiums if "Ortho Lifetime Max:" in item.get("Benefit Information"))
        ortholifetime_value = ortholifetimemax_dict.get("Premier")
       
        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":ortholifetime_value})
        EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":ortholifetime_value})
        EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":ortholifetimevalue})
        EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":ortholifetimevalue})
        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":calculate_difference(EligibilityPatientVerification.get("OrthodonticLifetimeBenefit").strip(),EligibilityPatientVerification.get("OrthodonticLifetimeRemainingBenefit").strip())})                                    
        EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit").strip())})                                    
                        
    except:
        pass




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



