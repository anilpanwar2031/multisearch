from mapPDF import mapEligibilityPatientVerification
import json, datetime
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
    return f'${float(a)-float(b)}'
def getsum(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)+float(b)}'
def main(data):
    
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    try:
        # codelist=req.get("InputParameters").get("ProcCodes")
        temp=data.get("EligibilityPatientVerification")[0]
        EligibilityPatientVerification.update({"FamilyMemberName":temp.get("Name")})
        temp=data.get("EligibilityPatientVerification")[1]
        EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":temp.get("Date of birth")})
        EligibilityPatientVerification.update({"GroupName":temp.get("Group name")})
        EligibilityPatientVerification.update({"GroupNumber":temp.get("Group number")})
        EligibilityPatientVerification.update({"PlanType":temp.get("Plan").replace("The patient's plan is ", "")[:-1]})
        EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":temp.get("Plan").replace("The patient's plan is ", "")[:-1]})
        EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":temp.get("Dependent age limit")})
        effectivedate=data.get("EligibilityPatientVerification")[0].get("Prev")
        effectivedate=effectivedate[:-2]+"20"+effectivedate[-2:]
        EligibilityPatientVerification.update({"DependentStudentAgeLimit":temp.get("Student age limit")})
        EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":effectivedate})
        tempdate=temp.get("Benefit period")[temp.get("Benefit period").index(" to ")+4:]
        

        payorid = temp.get("PayorID")
        if 'Payer ID' in payorid:
            payorid = payorid.split('Payer ID')[1].split('.')[0].strip()
            print(payorid)

        EligibilityPatientVerification.update({"ClaimPayerID":payorid})

        datedict={
            "January":"01",
            "February":"02",
            "March":"03",
            "April":"04",
            "May":"05",
            "June":"06",
            "July":"07",
            "August":"08",
            "September":"09",
            "October":"10",
            "November":"11",
            "December":"12"
        }
        tempdate=f"{tempdate.split(' ')[-1]}/{datedict.get(tempdate.split(' ')[0])}/{datetime.date.today().year}"
        tempdate=datetime.datetime.strptime(tempdate, "%d/%m/%Y").date()
        
        if(datetime.date.today()<tempdate):
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
        
        address=temp.get("Claim Address")
        address=address[address.index("Mail us your claim"):]
        address=address.replace("Mail us your claim", "").replace("\n" ," ").strip()
        EligibilityPatientVerification.update({"ClaimMailingAddress":address})
        
    except: pass
    


    EligibilityMaximums=[]
    EligibilityMaximumChange = []
    try:
        coverageMaximum = ""
        MaximumData=data.get("EligibilityMaximums")
        for valDeduct in MaximumData:
            if valDeduct.get("Coverage") == "":
                ccc = coverageMaximum
            else:
                ccc = valDeduct.get("Coverage")

            EligibilityMaximumChange.append({
                "Type": "Annual Maximums",
                "Network": valDeduct.get("Network"),
                "Amount": valDeduct.get("YearlyPlanLimit"),
                "Remaining": calculate_difference(valDeduct.get("YearlyPlanLimit"), valDeduct.get("YearlyMetToDate")),
                "ServiceCategory": ccc,
                "Family_Individual": "Individual"
            })
            EligibilityMaximumChange.append({
                "Type": "Lifetime Maximums",
                "Network": valDeduct.get("Network"),
                "Amount": valDeduct.get("LifetimePlanLimit"),
                "Remaining": calculate_difference(valDeduct.get("LifetimePlanLimit"), valDeduct.get("LifetimeMetToDate")),
                "ServiceCategory": ccc,
                "Family_Individual": "Individual"
            })
            if valDeduct.get("Coverage") == "":
                continue
            coverageMaximum = valDeduct.get("Coverage")

    except:
        pass
    EligibilityMaximums = EligibilityMaximumChange










    EligibilityDeductiblesProcCode=[]
    try:    
        temp=data.get("EligibilityDeductiblesProcCode")
        for x in range(0, len(temp)):
            
            if("Dental" in temp[x].get("Coverage")):
                ServiceCategory="Dental"
                Type="Annual Deductible"
            elif("Ortho" in temp[x].get("Coverage")):
                ServiceCategory="Orthodontics"
                Type="Lifetime Deductible"
            if("Family" in temp[x].get("Coverage")):
                Family_Individual="Family"
            elif("Individual" in temp[x].get("Coverage")):
                Family_Individual="Individual"
                if(ServiceCategory=="Dental" and (temp[x].get("Network")=="Out of network" or temp[x].get("Network")=="NON-CONTRACTED")):
                    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
            Amount=temp[x].get("Deductible")
            MetToDate=temp[x].get("MetToDate")
            
            if("per family" in Amount): 
                Amount=int(Amount.replace(" per family", ""))
                if(temp[x].get("Network")=="In network" or temp[x].get("Network")=="DG Alliance"):
                    Amount*=float(innetworkamount[1:])
                    Amount=f'${Amount}'
                else:
                    Amount*=float(oonamount[1:])
                    Amount=f'${Amount}'
            else:
                if(temp[x].get("Network")=="In network" or temp[x].get("Network")=="DG Alliance"):
                    innetworkamount=Amount
                else:
                    oonamount=Amount

            
            EligibilityDeductiblesProcCode.append({
                "Type": Type,
                "Network": temp[x].get("Network"),
                "Amount": Amount,
                "Remaining": calculate_difference(Amount, MetToDate),
                "ServiceCategory": ServiceCategory,
                "Family_Individual": Family_Individual
            })
        
    except: pass

    #Deductibles Applies#
    EligibilityDeductiblesChange = []
    DeductiblesAppliedWaivedPreventive = ""
    DeductibleAmmount = ""
    try:
        coverageDeduct = ""
        DeductiblesData=data.get("EligibilityDeductiblesProcCode")
        for valDeduct in DeductiblesData:
            if valDeduct.get("Coverage") == "":
                cc = coverageDeduct
            else:
                cc = valDeduct.get("Coverage")

            EligibilityDeductiblesChange.append({
                "Coverage": cc,
                "Network": valDeduct.get("Network"),
                "Deductible": valDeduct.get("Deductible"),
                "WaivedForPreventive?": valDeduct.get("WaivedForPreventive?"),
                "MetToDate": valDeduct.get("MetToDate")
            })
            if valDeduct.get("Coverage") == "":
                continue
            coverageDeduct = valDeduct.get("Coverage")

        for newvalDeduct in EligibilityDeductiblesChange:
            if "Individual" in newvalDeduct.get("Coverage") and "In network" in newvalDeduct.get("Network"):
                DeductiblesAppliedWaivedPreventive = newvalDeduct.get("WaivedForPreventive?")
                DeductibleAmmount = newvalDeduct.get("Deductible")
            if ("Individual" in newvalDeduct.get("Coverage") and "DG Alliance" in newvalDeduct.get("Network")):
                DeductiblesAppliedWaivedPreventive = newvalDeduct.get("WaivedForPreventive?")
                DeductibleAmmount = newvalDeduct.get("Deductible")
    except:
        pass


    EligibilityBenefits=[]
    TreatmentHistorySummary=[]
    count=0
    try:
        for x in data.get("EligibilityBenefits"):
            if x.get("Coinsurance 1, Coinsurance2") == "":
                for item in data.get("EligibilityOtherProvisions"):
                    if item.get("Service") == x.get("Service"):
                        x.update({"Service":item.get("Service")})
                        x.update({"Network 1, Network 2":item.get("Network")})
                        x.update({"Category 1, Category 1":item.get("Category")})
                        x.update({"Coinsurance 1, Coinsurance2":item.get("Coinsurance")})
                        x.update({"Message":item.get("Message**")})
                        x.update({"Last visit":item.get("LastVisit*").replace("\n"," ")})

            if(x.get("Proccode")=="2391"):
                alternativeBenefit = x.get("Message")
                if "Amalgam" in x.get("Message"):
                    alternativeBenefit = x.get("Message").split("Amalgam")[0]
                EligibilityPatientVerification.update({"AlternativeBenefitProvision":alternativeBenefit})
            try:
                [Benefits1, Benefits2]=x.get("Coinsurance 1, Coinsurance2", "").split('%')[:2]
                # Benefits1=f'{100-int(Benefits1)}%'
                # Benefits2=f'{100-int(Benefits2)}%'
                Benefits1=f'{int(Benefits1)}%'
                Benefits2=f'{int(Benefits2)}%'
            except: Benefits1, Benefits2="", ""
            
            if(x.get("Proccode") in ['8080', '8030', '8040', '8090']):
                if('Adult Orthodontic Covered' in x.get("Message")):
                    EligibilityPatientVerification.update({"AdultOrthodonticCovered":"Yes"})
            
            DDeductible = ""
            if "Preventive" in x.get("Category 1, Category 1"):
                if DeductiblesAppliedWaivedPreventive == "Yes":
                    DDeductible = "No"
                else:
                    DDeductible = "Yes"
            elif "$0.00" not in DeductibleAmmount and x.get("Category 1, Category 1") != "":
                DDeductible = "Yes"

            if x.get("Category 1, Category 1") == "":
                if "Preventive" in x.get("Service"):
                    if DeductiblesAppliedWaivedPreventive == "Yes":
                        DDeductible = "No"
                    else:
                        DDeductible = "Yes"
                elif "$0.00" not in DeductibleAmmount and ("Basic" or "Major") in x.get("Service"):
                    DDeductible = "Yes"


            EligibilityBenefits.append({
                "Category":x.get("Category 1, Category 1").replace("PreventivePreventive","Preventive").replace("BasicBasic","Basic").replace("MajorMajor","Major"),
                "ProcedureCode": "D"+x.get("Proccode"),
                "ProcedureCodeDescription": x.get("Service"),
                "limitation": x.get("Message"),
                "DeductibleApplies": DDeductible,
                "Copay": "",
                "Benefits": Benefits1,
                "BenefitsOutOfNetwork": Benefits2,
            })
            TreatmentHistorySummary.append({
                "ProcedureCode": "D"+x.get("Proccode"),
                "LimitationText": x.get("Message"),
                "History": x.get("Last visit", ""),
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": x.get("Service")
            })
            count+=1
        
    except: pass
    EligibilityServiceTreatmentHistory=TreatmentHistorySummary
        
    try:
        for x in EligibilityMaximums:
            if("Annual" in x.get("Type") and ("In network" or "DG Alliance" in x.get("Network")) and "Dental" in x.get("ServiceCategory")):
                if(x.get("Family_Individual")=="Individual"):
                    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":x.get("Amount")})
                    EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                    EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":x.get("Remaining")})
                elif(x.get("Family_Individual")=="Family"):
                    EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":x.get("Amount")})
                    EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                    EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":x.get("Remaining")})
            elif("Lifetime" in x.get("Type") and ("In network" or "DG Alliance" in x.get("Network")) and "Dental" in x.get("ServiceCategory")):
                if(x.get("Family_Individual")=="Individual"):
                    EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":x.get("Amount")})
                    EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                    EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":x.get("Remaining")})
                elif(x.get("Family_Individual")=="Family"):
                    EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":x.get("Amount")})
                    EligibilityPatientVerification.update({"FamilyLifetimeBenefitsUsedtoDate":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                    EligibilityPatientVerification.update({"FamilyLifetimeRemainingBenefit":x.get("Remaining")})
            elif("Lifetime" in x.get("Type") and ("In network" or "DG Alliance" in x.get("Network")) and "Ortho" in x.get("ServiceCategory")):
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":x.get("Amount")})
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":x.get("Remaining")})
        
    except: pass
    try:
        for x in EligibilityDeductiblesProcCode:
            if("Annual" in x.get("Type") and ("In network" or "DG Alliance" in x.get("Network")) and "Dental" in x.get("ServiceCategory")):
                if(x.get("Family_Individual")=="Individual"):
                    EligibilityPatientVerification.update({"IndividualAnnualDeductible":x.get("Amount")})
                    EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                    EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":x.get("Remaining")})
                elif(x.get("Family_Individual")=="Family"):
                    EligibilityPatientVerification.update({"FamilyAnnualDeductible":x.get("Amount")})
                    EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                    EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":x.get("Remaining")})
            elif("Lifetime" in x.get("Type") and ("In network" or "DG Alliance" in x.get("Network"))  and "Dental" in x.get("ServiceCategory")):
                if(x.get("Family_Individual")=="Individual"):
                    EligibilityPatientVerification.update({"IndividualLifetimeDeductible":x.get("Amount")})
                    EligibilityPatientVerification.update({"IndividualLifetimeDeductibleMet":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                    EligibilityPatientVerification.update({"IndividualLifetimeRemainingDeductible":x.get("Remaining")})
                elif(x.get("Family_Individual")=="Family"):
                    EligibilityPatientVerification.update({"FamilyLifetimeDeductible":x.get("Amount")})
                    EligibilityPatientVerification.update({"FamilyLifetimeDeductibleMet":calculate_difference(x.get("Amount"), x.get("Remaining"))})
                    EligibilityPatientVerification.update({"FamilyLifetimeRemainingDeductible":x.get("Remaining")})
    except: pass
    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output


# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\dev 15 june all testing\dev 5 july\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data)
# with open("Guardianres.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)