from Utilities.pdf_utils import *
from FileDownload import Downloader
from mapPDF import mapEligibilityPatientVerification
from typing import Iterable
import re
from collections import defaultdict

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



def main(Scraperdata, request):

    patientdata = request.get("PatientData")[0]
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityDEductible = Scraperdata.get("EligibilityDeductible")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions")


    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]
  
    patientdata = request.get("PatientData")[0]
    details_to_merge = Scraperdata["EligibilityPatientVerification"][-1]
    
    # PatientName = patientdata.get("FirstName")+", "+patientdata.get("LastName")
    # patient_name = PatientName.upper()
    
    # matching_dict = next((entry for entry in Scraperdata["EligibilityPatientVerification"] if entry.get("Name") == patient_name), None)

    PBirthdate = patientdata.get("BirthDate")
    
    matching_dict = next((entry for entry in Scraperdata["EligibilityPatientVerification"] if entry.get("Birthdate") == PBirthdate), None)

    if matching_dict is not None:
        matching_dict.update(details_to_merge)
        print(matching_dict)
    else:
        # Handle the case when matching_dict is None
        print("No matching dictionary found.")

    EligibilityPatientVerification.update(
        {
        "FamilyMemberId":patientdata.get("SubscriberId", ''),
        "SubscriberId":patientdata.get("SubscriberId"),
        "SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName"),
        "FamilyMemberName":patientdata.get("LastName")+", "+patientdata.get("FirstName").upper(),
        "FamilyMemberDateOfBirth":patientdata.get("BirthDate"),
        "Relationship":matching_dict.get("Group/Relationship"),
        "SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate"),
        "FamilyMemberEffectiveDate":matching_dict.get("EffectiveDate").replace("Effective Date for Coordination of Benefits: ",""),
        "CoordinationofBenefitsType":matching_dict.get("EffectiveDate").replace("Effective Date for Coordination of Benefits: ",""),
        "GroupName":EligibilityMaximiums[0].get("Status").replace("Group ",""),
        "GroupNumber":EligibilityMaximiums[0].get("NextEligibleDate").replace("Group No ",""),
        "InNetworkOutNetwork":"In Network",
        "oonBenefits":"Yes",
        "CoordinationofBenefits": "Yes",
        "EligibilityStatus":"Active",
        "PlanType":matching_dict.get("Plantype").replace("Plan Type: ",""),
        "ProgramType":EligibilityMaximiums[0].get("Benefit"),
        "InsuranceFeeScheduleUsed":matching_dict.get("Plantype").replace("Plan Type: ","")
        }
    )
    

    try:
        for alterbenefit in EligibilityBenefitsData:
            if "Medically" in alterbenefit.get('Specialcomments',""):
                value = alterbenefit.get('Specialcomments',"")
                if "Medically" in value:
                    medicalvalue = value.split('Medically')[1].split('.')[0]

                EligibilityPatientVerification.update({"MedicallyNecessaryonly":"Medically"+medicalvalue})
    except:
        pass    

    try:
        for alterbenefit in EligibilityBenefitsData:
            if "POSTERIOR COMPOSITES" == alterbenefit.get('Category'):
                EligibilityPatientVerification.update({"AlternativeBenefitProvision":alterbenefit.get("FrequencyLimits")})
    except:
        pass

    
    try:
        for benefit in EligibilityBenefitsData:
            if benefit.get('Category') == "ORTHODONTICS":
                agelimit = benefit.get('MaxAge')
                EligibilityPatientVerification.update({"OrthodonticAgeLimits":agelimit})
    except:
        pass 
    
    try:
        index_of_orthodontic = -1
        for i in range(len(EligibilityMaximiums)):
            if EligibilityMaximiums[i].get("Benefit") == "Ortho Max":
                index_of_orthodontic = i
                break
        # Get the required value
        if index_of_orthodontic != -1:
            value = EligibilityMaximiums[index_of_orthodontic].get("Status")
            
            pattern = r"\$(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)"
            matches = re.findall(pattern, value)
            value1 = "$" + matches[0]
            value2 = "$" + matches[1]

            EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":value1})
            EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":value2})

            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":value1})
            EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":value2})            
            
        else:
            print("IndividualLifetimeBenefitsUsedtoDate :- Orthodontic not found")     
    except:
        pass

    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":getsum(EligibilityPatientVerification.get("OrthodonticLifetimeBenefitUsedtoDate").strip(),EligibilityPatientVerification.get("OrthodonticLifetimeRemainingBenefit").strip())})
    EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":getsum(EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate").strip(),EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit").strip())})


    try:
        index_of_orthodontic = -1
        for i in range(len(EligibilityMaximiums)):
            if EligibilityMaximiums[i].get("Benefit") == "Ind Max Out-Of-Pocket (MOOP)":
                index_of_orthodontic = i
                break
        # Get the required value
        if index_of_orthodontic != -1:
            value = EligibilityMaximiums[index_of_orthodontic].get("Status")
            InsuranceCalendarOrFiscalPolicyYearvalue = EligibilityMaximiums[index_of_orthodontic].get("NextEligibleDate")
            pattern = r"\$(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)"
            matches = re.findall(pattern, value)
            value1 = "$" + matches[0]
            value2 = "$" + matches[1]

            EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":value1})
            EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":value2}) 
            EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":InsuranceCalendarOrFiscalPolicyYearvalue})         
            
        else:
            print("IndividualAnnualBenefitsUsedtoDate :- Ind Max Out-Of-Pocket (MOOP) not found") 
    except:
        pass  

    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":getsum(EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate").strip(),EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip())})  
   

    try:
        index_of_orthodontic = -1
        for i in range(len(EligibilityMaximiums)):
            if EligibilityMaximiums[i].get("Benefit") == "Fam Max Out-Of-Pocket (MOOP)":
                index_of_orthodontic = i
                break
        # Get the required value
        if index_of_orthodontic != -1:
            value = EligibilityMaximiums[index_of_orthodontic].get("Status")
            
            pattern = r"\$(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)"
            matches = re.findall(pattern, value)
            value1 = "$" + matches[0]
            value2 = "$" + matches[1]

            EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":value1})
            EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":value2})         
            
        else:
            print("FamilyAnnualBenefitsUsedtoDate :- Fam Max Out-Of-Pocket (MOOP) not found") 
    except:
        pass  

    EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":getsum(EligibilityPatientVerification.get("FamilyAnnualBenefitsUsedtoDate").strip(),EligibilityPatientVerification.get("FamilyAnnualRemainingBenefit").strip())})  
    EligibilityPatientVerification.update({"IndividualAnnualDeductible":"0"})
    EligibilityPatientVerification.update({"FamilyAnnualDeductible":"0"})
    EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":"NONE"})


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



    codes = [
            {"code":"D0150","search":"EXAMINATIONS"},
            {"code":"D0120","search":"EXAMINATIONS"},
            {"code":"D0140","search":"EXAMINATIONS"}, 
            {"code":"D0170","search":"E-EVALUATION - LIMITED PROBLEM FOCUSED"}, # no found decsription
            {"code":"D9110","search":"PALLIATIVE (EMERGENCY) TREATME"}, # no found decsription
            {"code":"D0220","search":"INTRAORAL"}, # no found decsription
            {"code":"D0230","search":"INTRAORAL - PERIAPICAL EACH ADD RADIOGRAPH IMAGE"}, 
            {"code":"D0272","search":"BITEWING X-RAYS >= 15 YEARS"},
            {"code":"D0274","search":"BITEWING X-RAYS < 15 YEARS"},
            {"code":"D0210","search":"FULL MOUTH X-RAYS"},
            {"code":"D0330","search":"FULL MOUTH X-RAYS"},
            {"code":"D0240","search":"INTRAORAL - OCCLUSAL RADIOGRAPHIC IMAGE"}, 
            {"code":"D1110","search":"CLEANINGS (CLNG)"},
            {"code":"D1120","search":"CLEANINGS (CLNG)"},
            {"code":"D1206","search":"FLUORIDE"},
            {"code":"D1208","search":"FLUORIDE"},
            {"code":"D1351","search":"SEALANTS - PER PERMANENT MOLAR"},
            {"code":"D1354","search":"Other drugs and/or medicaments"},
            {"code":"D1516","search":"SPACE MAINTAINERS"},
            {"code":"D1517","search":"SPACE MAINTAINERS"},
            {"code":"D2140","search":"Amalgam"},
            {"code":"D2150","search":"Amalgam"},
            {"code":"D2160","search":"Amalgam"},
            {"code":"D2161","search":"Amalgam"},
            {"code":"D2391","search":"Amalgam"},
            {"code":"D2392","search":"Amalgam"},
            {"code":"D2393","search":"Amalgam"},
            {"code":"D2394","search":"Amalgam"},     
            {"code":"D7140","search":"Simple Extractions"}, 
            {"code":"D3220","search":"REMV PULP CORONAL DENTINOCEMENTL JUNC"}, 
            {"code":"D2930","search":"CROWNS AND GOLD RESTORATION"}, 
            {"code":"D2933","search":"IMPLANT"}, 
            {"code":"D2934","search":"CROWNS AND GOLD RESTORATION"}, 
            {"code":"D9230","search":"INHALATION OF NITROUS OXIDE/ANALGESIA ANXIOLYSIS"} 
        ]
    

    translation_table = str.maketrans('', '', ' -')
    #  To get uniques procedure codes from EligibilityTreatmentHistory  
    result = defaultdict(lambda: defaultdict(list))   

    for benefit in EligibilityTreatmentHistory:
    
        procedure = benefit['Procedure'] 
        if len(procedure) == 3:
            benefit['Procedure'] = 'D0'+ procedure
        elif len(procedure) == 4:
            benefit['Procedure'] = 'D' + procedure

        procedure = benefit['Procedure'] 

        if procedure not in result:
            result[procedure] = {'Tooth': [], 'Surface': [], 'ServiceDate': []}
    
        result[procedure]['Tooth'].append(benefit['Tooth'])
        result[procedure]['Surface'].append(benefit['Surface'])
        result[procedure]['ServiceDate'].append(benefit['ServiceDate'])    
           

    final_results = []

    for procedure, entries in result.items():
        tooth_list = ', '.join(entries['Tooth'])
        surface_list = ', '.join(entries['Surface'])
        service_date_list = ', '.join(str(date) + ' (' + procedure + ')' + ' - Tth: ' + tooth + ' Surface(s): ' + surface for date, tooth, surface in zip(entries['ServiceDate'], entries['Tooth'], entries['Surface']))


        final_result = {
            'Tooth': tooth_list,
            'Surface': surface_list,
            'Procedure': procedure,
            'ServiceDate': service_date_list
        }

        final_results.append(final_result)

        # To append ProcedureCodeDescription and frequency from EligibilityBenefitsData
    for itemss in final_results:
        procedure_code = itemss.get("Procedure")
        code_description = ""
        frequency_limits = ""
        
        # Find code description from codes dictionary
        for code in codes:
            if code["code"] == procedure_code:
                code_description = code["search"]
                break
        
        # Find frequency limits from EligibilityBenefits
        for eligibility in EligibilityBenefitsData:
            if eligibility.get("Category","").translate(translation_table) == code_description.translate(translation_table):
                frequency_limits = eligibility.get("FrequencyLimits","")
                break
        
        # Update the current itemss dictionary with code description and frequency limits
        itemss["ProcedureCodeDescription"] = code_description
        itemss["FrequencyLimits"] = frequency_limits
# print(unique_benefits)   


    

    for code in codes:
        if code.get("code") and code.get("search"):  # only proceed if both fields are present
            limitation = ""
            Benefits = ""
            Agelimit = ""
            waitperiod = ""
            deductible = ""
            agelimit = ""
            # corrected variable name
            for searchItem in EligibilityBenefitsData:
                if code.get("search").translate(translation_table) == searchItem.get("Category","").translate(translation_table) and searchItem.get("Category", ""):
                    limitation = limitation +", "+searchItem.get("FrequencyLimits","")
                    Benefits = Benefits +", "+searchItem.get("Copay","")
                    Agelimit = Agelimit +", "+searchItem.get("MaxAge","")
                    waitperiod = waitperiod +", "+searchItem.get("WaitPeriod","")
                    deductible = deductible +", "+ searchItem.get("IndividualDeductible","")
                    agelimit = str(limitation.strip(', ')+", "+ Agelimit.strip(', ')).replace(" N/A","")
                    
                    if 'NONE' in waitperiod:
                        waitperiod = ""

                    if '0' in deductible:
                        deductible = "No"
                    else:
                        deductible = "Yes"        
            
            EligibilityBenefits.append({
                "ProcedureCode": code.get("code").strip(),
                "ProcedureCodeDescription": code.get("search"),
                "Amount": "",
                "Type": "",
                "limitation": agelimit.strip(', '),
                "DeductibleApplies": deductible.strip(),
                "Copay": "",
                "Benefits": Benefits.strip(', '),
                "WaitingPeriod": waitperiod.strip(', ')
            })
        # print(EligibilityBenefits)     


    for itemss in final_results:
        if itemss.get("Procedure") != "" and itemss.get("Procedure", None):
            limitation = ""
            limitapplies = ""
            
            for codees in codes:
                if itemss.get("Procedure").translate(translation_table) == codees.get("code").translate(translation_table):
                    for searchitems in EligibilityTreatmentHistory:
                        limitation = searchitems.get("Frequency")
                        limitapplies = searchitems.get("LimitationORNotes")
                        
                
            EligibilityServiceTreatmentHistory.append({
                "ProcedureCode": itemss.get("Procedure"),
                "LimitationText": itemss.get("FrequencyLimits"),
                "History": itemss.get("ServiceDate"),
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": itemss.get("ProcedureCodeDescription")                
                })
              
            TreatmentHistorySummary.append({
                "ProcedureCode": itemss.get("Procedure"),
                "LimitationText": itemss.get("FrequencyLimits"),
                "History": itemss.get("ServiceDate"),
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": itemss.get("ProcedureCodeDescription")                
                })        

        
        if itemss.get("Proccode") == "D2391":
            EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":itemss.get("WaitingPeriod")})



    output={}

    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output
