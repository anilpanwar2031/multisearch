import os,sys
import json
import string, random, PyPDF2
from mapPDF import mapEligibilityPatientVerification
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
    return f'${round(float(a)-float(b) , 2)}'

def CoordinationofBenefits(EligibilityPatientVerification):
    return EligibilityPatientVerification.get("OtherInsurance?")


def DeductibleAppliesNotcoveredservice(EligibilityBenefits):
    for obj in EligibilityBenefits:
        if obj.get("limitation"):
            if obj.get("limitation") =="Not a covered service":
                if obj.get("DeductibleApplies"):
                    obj["DeductibleApplies"] =""
    return  EligibilityBenefits              


def main(data):
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    try:temp=data.get("EligibilityPatientVerification")[0]
    except: temp={}
    try:
        EligibilityPatientVerification.update({"FamilyMemberName":temp.get("Name")})
        EligibilityPatientVerification.update({"FamilyMemberId":temp.get("PatientId")})
        EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":temp.get("DateOfBirth")})
        # EligibilityPatientVerification.update({"ClaimsAddress":temp.get("Address")})
        EligibilityPatientVerification.update({"SubscriberName":temp.get("Subscriber")})
        EligibilityPatientVerification.update({"SubscriberDateOfBirth":temp.get("SubscriberDateOfBirth")})
        EligibilityPatientVerification.update({"PlanType":temp.get("PlanType")})
        EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":temp.get("PlanType")})
        EligibilityPatientVerification.update({"GroupName":temp.get("AccountName")})
        EligibilityPatientVerification.update({"GroupNumber":temp.get("Account#")})
        EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":temp.get("PlanRenews", "")})
        EligibilityPatientVerification.update({"Relationship":temp.get("Relationship", "")})
        EligibilityPatientVerification.update({"CurrentCoverage":temp.get("CurrentCoverage", "")})
        EligibilityPatientVerification.update({"OtherInsurance?":temp.get("OtherInsurance?", "")})
        EligibilityPatientVerification["CoordinationofBenefits"]    =  CoordinationofBenefits(data.get("EligibilityPatientVerification")[0])
        try:
            EligibilityPatientVerification["CoordinationofBenefitsType"]    =  "OtherInsurance? "+CoordinationofBenefits(data.get("EligibilityPatientVerification")[0])
        except:
            pass

        Network=temp.get("Network")
        ClaimMailingAddress=''
        for x in temp.get("ClaimOfficeMailingAddress").split('\n')[2:]:
            ClaimMailingAddress+=x+' '
        EligibilityPatientVerification.update({"ClaimMailingAddress":ClaimMailingAddress.strip()})
        EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":temp.get("CurrentCoverage")[:temp.get("CurrentCoverage").index(" - ")]})
        if("Present" in temp.get("CurrentCoverage")):
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
    except: pass
    EligibilityBenefits, EligibilityMaximums, EligibilityDeductibles, EligibilityServiceTreatmentHistory=[], [], [], []
    TreatmentHistorySummary=[]
    Type = ""
    ServiceCategory = ""
    Amount = ""
    Remaining = ""
    Family_Individual =""
    try:    
        temp=data.get("EligibilityMaximums")[0].get("Maximums").split('\n')
        for x in range(len(temp)):
            if("Lifetime Maximum" in temp[x]):
                Type="Lifetime Maximums"
            elif("Calendar Year Maximum" in temp[x]):
                Type="Annual Maximums"
            elif("Policy Year Maximum" in temp[x]):
                Type="Annual Maximums"
            if('Ortho' in temp[x]):
                ServiceCategory="Orthodontics"
            elif('Dental' in temp[x]):
                ServiceCategory="Dental Care"
            elif(x==0):
                ServiceCategory=temp[x]
                Remaining=""
            if("Individual" in temp[x]):
                Family_Individual="Individual"
            elif("Family" in temp[x]):
                Family_Individual="Family"
            if("emaining" in temp[x]):
                Remaining=temp[x+1]
            
            if("Total" in temp[x]):
                Amount=temp[x].replace("Total: ", "")
                EligibilityMaximums.append({
                "Type": Type,
                "Network": Network,
                "Amount": Amount,
                "Remaining": Remaining,
                "ServiceCategory": ServiceCategory,
                "Family_Individual": Family_Individual
                })
    except: pass    
    try:
        temp=data.get("EligibilityDeductiblesProcCode")[0].get("Deductible").split('\n')
        for x in range(len(temp)):
            if(temp[x]=="Deductible Met"):
                Remaining="0.0"
            if("Lifetime Deductible" in temp[x]):
                Type="Lifetime Deductibles"
            elif("Calendar Year Deductible" in temp[x]):
                Type="Annual Deductibles"
            elif("Policy Year Deductible" in temp[x]):
                Type="Annual Deductibles"

            if('Ortho' in temp[x]):
                ServiceCategory="Orthodontics"
            elif(x==0):
                ServiceCategory=temp[x]
                Remaining=""
            if("Individual" in temp[x]):
                Family_Individual="Individual"
            elif("Family" in temp[x]):
                Family_Individual="Family"
            
            if(temp[x]=="Deductible Met"):
                Remaining="0.0"
            elif("emaining" in temp[x]):
                Remaining=temp[x+1]
                if(Remaining=="Deductible Met"):
                    Remaining=Amount
            if("Total" in temp[x]):
                Amount=temp[x].replace("Total: ", "")
                EligibilityDeductibles.append({
                "Type": Type,
                "Network": Network,
                "Amount": Amount,
                "Remaining": Remaining,
                "ServiceCategory": ServiceCategory,
                "Family_Individual": Family_Individual
                })
            
        
        
    except: pass
    try:
        for x in data.get("EligibilityBenefits"):
            proccode=x.get("Code")
            if(proccode=="D2391"):
                if("Tooth - 2" in x.get("Procedure") and "Alternate benefit may apply" in x.get("Procedure")):
                    EligibilityPatientVerification.update({"AlternativeBenefitProvision":"Yes"})

            proccodedesc=x.get("Procedure")[:x.get("Procedure").index("History**")]
            if("Tooth -" in proccodedesc):
                Tooth=proccodedesc.split("Tooth -")[-1].strip()
                proccodedesc=proccodedesc[:proccodedesc.index("Tooth -")]
            else: Tooth=""
            try:
                temp=x.get("Maximum").split(' Frequency ')[-1]
                
                if("Not Applicable" in temp):
                    if("Exclude after age" in temp):
                        limitation="Not Applicable. Exclude after age"
                        limitation+=temp[temp.index("Exclude after age")+17:temp.index(" Coinsurance")]
                        
                    else: limitation='Not Applicable'
                else:
                    temp=temp[temp.index("Amount Met:")+11:]
                    temp=temp[temp.index(" of ")+4:]
                    temp=temp[temp.index(" ")+1:temp.index(" Coinsurance")]
                    temp=temp.replace("Exclude", ". Exclude")
                    limitation=temp
            except: limitation=''

            #new limiation for cigna dhmo
            try:
                if ("Copay/Coinsurance" in x.get("Maximum") and "Frequency" in x.get("Maximum")):
                    if "Amount Met:" in x.get("Maximum").split("Frequency")[1]:
                        limitation = x.get("Maximum").split("Frequency")[1].replace("Amount Met:","").strip()
                        limitation = limitation[7:]
                    else:
                        limitation = x.get("Maximum").split("Frequency")[1].replace("Amount Met:","").strip()
            except:
                pass
            #new limiation for cigna dhmo
            
            try:
                temp=x.get("Maximum").split('Total: ')[1]
                Amount=temp[:temp.index("Notes")]
            except: Amount=''
            # if("Total" in temp):
            #     Amount=temp.replace("Total: ", "")
            try:temp=x.get("Maximum")
            except: temp=''
            if("Deductible " in temp):
                DeductibleApplies="Yes"
                if ("no deductibles" in temp):
                    DeductibleApplies="No"
            else: 
                DeductibleApplies="No"
            try:
                temp=x.get("Maximum").split('Member Responsibility  ')[-1]
                temp=temp[:temp.index(" Notes")]
            except: temp=''
            if("%" in temp):
                Benefits=f'{100-int(temp[:-1])}%'
            else: Benefits=''
            if("Copay" in x.get("Maximum") and "$" in x.get("Maximum") and "Deductible" in x.get("Maximum")):
                Benefits = x.get("Maximum").split("Deductible")[0].replace("(Network General Dentist)","Network General Dentist:").replace("(Specialist)",", Specialist:")
            try:
                History=x.get("Procedure")
                History=History[History.index("History**")+9:History.index("Alternate benefit may apply")].strip()
                
                if(len(History) and len(Tooth) and "history" not in History and "History" not in History):
                    History+=f'({Tooth})'
            except Exception as e: 
                History=''
            try:
                #cigna DHMO
                if(History == ''):
                    History=x.get("Procedure").split("History**")[1].replace("*","").strip()
                #cigna DHMO
            except:
                pass
            try:
                if("Not a covered service" in x.get("Maximum")):
                    Amount="N/A"
                    limitation="Not a covered service"
            except:
                pass
            proccodedesc=proccodedesc.replace("Arch -", " Arch -").replace("Tooth -", " Tooth -")
            if limitation == "Not a covered service":
                continue

            EligibilityBenefits.append({
                "ProcedureCode": proccode,
                "ProcedureCodeDescription": proccodedesc,
                "Amount": Amount,
                "limitation": limitation,
                "DeductibleApplies": DeductibleApplies,
                "Copay": "",
                "Benefits": Benefits 
            })
            TreatmentHistorySummary.append({
                "ProcedureCode": proccode,
                "LimitationText": limitation,
                "History": History,
                "Tooth": Tooth,
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": proccodedesc
            })

    except: pass 
    
    try:
   
        for x in EligibilityDeductibles:
            if x.get("ServiceCategory"):
                ServiceType=x.get("ServiceCategory")            
            if(x.get("Type")=="Lifetime Deductibles" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Family"):
                EligibilityPatientVerification.update({"FamilyLifetimeDeductible":x.get('Amount')})
                EligibilityPatientVerification.update({"FamilyLifetimeRemainingDeductible":x.get('Remaining')})
                EligibilityPatientVerification.update({"FamilyLifetimeDeductibleMet":calculate_difference(x.get("Amount"), x.get('Remaining'))})

            elif(x.get("Type")=="Lifetime Deductibles" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Individual"):
                EligibilityPatientVerification.update({"IndividualLifetimeDeductible":x.get('Amount')})
                EligibilityPatientVerification.update({"IndividualLifetimeRemainingDeductible":x.get('Remaining')})
                EligibilityPatientVerification.update({"IndividualLifetimeDeductibleMet":calculate_difference(x.get("Amount"), x.get('Remaining'))})

            elif(x.get("Type")=="Annual Deductibles" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Family"):
                EligibilityPatientVerification.update({"FamilyAnnualDeductible":x.get('Amount')})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":x.get('Remaining')})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(x.get("Amount"), x.get('Remaining'))})
            elif(x.get("Type")=="Annual Deductibles" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Individual"):
                EligibilityPatientVerification.update({"IndividualAnnualDeductible":x.get('Amount')})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":x.get('Remaining')})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(x.get("Amount"), x.get('Remaining'))})

    except: pass
    try:              
        for x in EligibilityMaximums:
            if x.get("ServiceCategory"):
                ServiceType=x.get("ServiceCategory")            
            if(x.get("Type")=="Lifetime Maximums" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Family"):
                EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":x.get('Amount')})
                EligibilityPatientVerification.update({"FamilyLifetimeRemainingBenefit":x.get('Remaining')})
                EligibilityPatientVerification.update({"FamilyLifetimeBenefitsUsedtoDate":calculate_difference(x.get("Amount"), x.get('Remaining'))})

            elif(x.get("Type")=="Lifetime Maximums" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Individual"):
                EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":x.get('Amount')})
                EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":x.get('Remaining')})
                EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(x.get("Amount"), x.get('Remaining'))})

            elif(x.get("Type")=="Annual Maximums" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Family"):
                EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":x.get('Amount')})
                EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":x.get('Remaining')})
                EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":calculate_difference(x.get("Amount"), x.get('Remaining'))})

            elif(x.get("Type")=="Annual Maximums" and x.get("ServiceCategory")==ServiceType and x.get("ServiceCategory")!="Orthodontics" and x.get("Family_Individual")=="Individual"):
                EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":x.get('Amount')})
                EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":x.get('Remaining')})
                EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(x.get("Amount"), x.get('Remaining'))})

            elif(x.get("Type")=="Lifetime Maximums" and x.get("ServiceCategory")=="Orthodontics" and x.get("Family_Individual")=="Individual"):
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":x.get('Amount')})
                EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":x.get('Remaining')})
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":calculate_difference(x.get("Amount"), x.get('Remaining'))})
    except: pass    
    # try:
        
    #     for x in data.get("EligibilityBenefits"):
    #         History=x.get("Procedure")
    #         History=History[History.get("History**")+9:History.get("Alternate benefit may apply")].strip()
    #         # if("No history on file for this member" in History or "History Not Applicable" in History):
    #         #     History=""
    #         temp=x.get("Deductible").split('\n')[-1]
    #         if("Not Applicable" not in temp and "Notes" not in temp):
    #             limitation=temp
    #         else: 
    #             limitation=""
    #         TreatmentHistorySummary.append({
    #             "ProcedureCode": x.get("Code"),
    #             "LimitationText": limitation,
    #             "History": History,
    #             "Tooth": "",
    #             "Surface": "",
    #             "LimitationAlsoAppliesTo": "",
    #             "ProcedureCodeDescription": x.get("Procedure")
    #         })

    # except: pass
    EligibilityServiceTreatmentHistory=TreatmentHistorySummary
    temp=[]
    codelist=[]
    try:
        for x in EligibilityServiceTreatmentHistory:
            ProcedureCode=x.get("ProcedureCode")
           
            if(ProcedureCode not in codelist):
                ProcedureCodeDescription=x.get("ProcedureCodeDescription")
                LimitationText=x.get("LimitationText")
                History=x.get("History")
                flag=0
                for y in EligibilityServiceTreatmentHistory:
                    if(x!=y and x.get("ProcedureCode")==y.get("ProcedureCode") and "history" not in x.get("History").lower() and "history" not in y.get("History").lower()):
                        codelist.append(ProcedureCode)
                        flag=1
                        History+=f' {y.get("History")}'
                    elif(x!=y and x.get("ProcedureCode")==y.get("ProcedureCode")):
                        codelist.append(ProcedureCode)
                        flag=1
                        History=f'{y.get("History")}'
                
                # if(flag):
                if(True):
                    History=History.replace("  ", " ").strip()
                    temp.append({
                        "ProcedureCode": ProcedureCode,
                        "ProcedureCodeDescription": ProcedureCodeDescription,
                        "LimitationText": LimitationText,
                        "LimitationAlsoAppliesTo": "",
                        "History": History
                    })
                
        TreatmentHistorySummary=temp
    except Exception as e: 
        print(e)
        pass
    t=[]
    for x in EligibilityBenefits:
        if(x not in t):
            t.append(x)
    EligibilityBenefits=t
    try:
        if(len(data.get("EligibilityDeductiblesProcCode")[0].get("url"))): 
            url=data.get("EligibilityDeductiblesProcCode")[0].get("url")
            current = os.path.dirname(os.path.realpath(__file__))
            parent = os.path.dirname(current)
            sys.path.append(parent)
            from FileDownload import Downloader
            file_path = ''.join(random.choices(string.ascii_uppercase +string.digits, k=10))
            file_path+='.pdf'
            Downloader("Eligibility",file_path,url)
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                templist=[]
                pageNumber=0
                pdf_page = pdf_reader.pages[pageNumber]
                text = pdf_page.extract_text().split("\n")[0]
                EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":text})
            os.remove(file_path)
    except: pass
    # for x in EligibilityBenefits:
    #     flag=0
    #     for y in TreatmentHistorySummary:
    #         if(y.get("ProcedureCode")==x.get("ProcedureCode")):
    #             flag=1
    #     if(flag==0):
    #         print(x)
    #         exit()
    try:
        for x in data.get("EligibilityAgeLimitation"):
            if(x.get("LimitationType")=="Student Age Limitation"):
                EligibilityPatientVerification.update({"DependentStudentAgeLimit":x.get("Age")})
            elif(x.get("LimitationType")=="Dependent Age Limitation"):
                EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":x.get("Age")})
            elif(x.get("LimitationType")=="Ortho Age Limitation"):
                if(x.get("Age")=="None"):
                    EligibilityPatientVerification.update({"AdultOrthodonticCovered":"Yes"})
                else:
                    EligibilityPatientVerification.update({"AdultOrthodonticCovered":"No"})
    except: pass
    try:
        for x in data.get("EligibilityAgeLimitation"):
            if(x.get("waiting period", None)):
                if "Waiting Period does not apply" in x.get("waiting period"):
                    EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":"Waiting Period does not apply"})
                if "Missing Tooth Limitation" in x.get("waiting period"):
                    EligibilityPatientVerification.update({"MissingToothClause":"No"})
    except: pass
    try:
        if(len(data.get("EligibilityDeductiblesProcCode")[0].get("OutofNetworkMaximums"))):
            EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    except: 
        pass
    if(EligibilityPatientVerification.get("oonBenefits")!="Yes"):
        EligibilityPatientVerification.update({"oonBenefits":"No"})
    output={}
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductibles})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    data=output
    output={}
    for x in data:
        temp1=[]
        for y in data.get(x):
            temp2={}
            for z in y:
                temp2.update({z.replace(")", "_").replace("(", "_"):y.get(z)})
                # del y[z]
            temp1.append(temp2)
        output.update({x:temp1})

    output["EligibilityBenefits"]   =  DeductibleAppliesNotcoveredservice(output.get("EligibilityBenefits",{}))    
    return output

# data=json.load(open("output.json", 'r'))
# output=main(data)
# with open("Cignares.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)