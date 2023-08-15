import json, datetime
from re import search
from mapPDF import mapEligibilityPatientVerification
def changeNone(val):
    if(val==None or val=="N/A"):
        return ""
    else:
        return val
def main(data):
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityPatientVerification.update({"FamilyAnnualDeductible":"0.0"})
    EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":"0.0"})
    EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":"0.0"})
    EligibilityPatientVerification.update({"IndividualAnnualDeductible":"0.0"})
    EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":"0.0"})
    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":"0.0"})
    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":"0.0"})
    EligibilityPatientVerification.update({"FamilyLifetimeDeductible":"0.0"})
    EligibilityPatientVerification.update({"IndividualLifetimeDeductible":"0.0"})
    
    try:
        print(data.get("EligibilityPatientVerification")[1].get("Network"))
        print(data.get("EligibilityPatientVerification")[1].get("Group Network"))
        DentalPlan=data.get("EligibilityPatientVerification")[1].get("Dental Plan").replace("\n", "").replace("Dental Plan", "")
        temp=data.get("EligibilityPatientVerification")[1].get("Group")
        [GroupName, GroupNumber]=temp.split("\n")[1].split(' / ')
        print(GroupName, GroupNumber)
        Network=data.get("EligibilityPatientVerification")[1].get("Network")
        temp=data.get("EligibilityPatientVerification")[1].get("Carrier & Service Type").replace("\n\n", "\n")
        CarrierType, ServiceType=temp.split("\n")[1],temp.split("\n")[-1]
        print(CarrierType, ServiceType)
        temp=data.get("EligibilityPatientVerification")[1].get("Holder Name & Mailing Adress").replace("\n\n", "\n")
        HolderName, ClaimMailingAddress=temp.split("\n")[1], ''
        for x in temp.split("\n")[3:]:
            ClaimMailingAddress+=x+' '
            ClaimMailingAddress=ClaimMailingAddress.strip()
        ClaimMailingAddress=data.get("EligibilityPatientVerification")[1].get("ClaimMailingAddress").replace("\n", " ").replace("Find Claim Forms", "").strip()
        print(HolderName, ClaimMailingAddress)
        temp=data.get("EligibilityPatientVerification")[1].get("Coverage Effective")
        EffectiveDate=temp[:temp.index(" - ")]
        EndDate=temp[temp.index(" - "):temp.index("|")]

        status = data.get("EligibilityPatientVerification")[1].get("Eligibility Status")
        if status == "ACTIVE":
             EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
        else:
            EligibilityPatientVerification.update({"EligibilityStatus":""})

        EligibilityPatientVerification.update({
            "GroupName": GroupName,
            "GroupNumber": GroupNumber,
            "FamilyMemberEffectiveDate":EffectiveDate,
            "ClaimMailingAddress":ClaimMailingAddress,
            "SubscriberName":HolderName,
            "PlanType":DentalPlan,
            "FamilyMemberName":data.get("EligibilityPatientVerification")[1].get("Member Name"),
            "FamilyMemberDateOfBirth":data.get("EligibilityPatientVerification")[0].get("Dob")
        })
    except: pass
    try:
        for x in data.get("EligibilityMaximums")[0].get("Benefits"):
            temp=x.get("FamilyDeductible")
            # if("Per Calendar Year" in temp): 
                
            try: 
                temp=temp[temp.index("$"):temp.index(" ")] 
                # temp=temp.replace("Per Calendar Year", "").strip()
                EligibilityPatientVerification.update({"FamilyAnnualDeductible":temp})
            except:pass
            temp=x.get("IndividualDeductible")
            # if("Per Calendar Year" in temp): 
            try: 
                temp=temp[temp.index("$"):temp.index(" ")] 
                # temp=temp.replace("Per Calendar Year", "").strip()
                EligibilityPatientVerification.update({"IndividualAnnualDeductible":temp})
            except: pass
            temp=x.get("IndividualMaximum")
            if search("Ortho related",temp) == None: 
                try: 
                    print(temp)
                    temp=temp[temp.index("$"):temp.index(" ")] 
                    # temp=temp.replace("Per Calendar Year", "").strip()
                    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":temp})
                except: pass
    except: pass
    EligibilityBenefits=[]
    for x in data.get("EligibilityBenefits"):
        if(x.get("Covered")=="Not Covered"):
            EligibilityBenefits.append({
                "ProcedureCode": x.get("Procedure Code"),
                "ProcedureCodeDescription": x.get("Procedure Name").replace("\u00a0>", ""),
                "Amount": "",
                "limitation": "",
                "DeductibleApplies": "",
                "Copay":"",          
                "Benefits":"Not Covered"
            })
          
        elif("$" in x.get("Coverage % or Copay $")):
            EligibilityBenefits.append({
                "ProcedureCode": x.get("Procedure Code"),
                "ProcedureCodeDescription": x.get("Procedure Name").replace("\u00a0>", ""),
                "Amount": x.get("Allowance"),
                "limitation": x.get("Limitation").replace("|", "").replace("More...", "").strip(),
                "DeductibleApplies": x.get("Applied to Deductible"),
                "Copay":x.get("Coverage % or Copay $"),          ###############,
                "Benefits":""
            })
            if(x.get("Procedure Code")=="D2391"):
                EligibilityPatientVerification.update({"AlternativeBenefitProvision": x.get("Limitation").replace("More...", "").strip()})
                # if("Alternate Benefit Provision ~ Will Apply" in x.get("Limitation").replace("|", "").replace("More...", "").strip()):
                #     EligibilityPatientVerification.update({"AlternativeBenefitProvision":"Yes"})
                # else:
                #     EligibilityPatientVerification.update({"AlternativeBenefitProvision":"No"})

        elif("%" in x.get("Coverage % or Copay $")):
            EligibilityBenefits.append({
                "ProcedureCode": x.get("Procedure Code"),
                "ProcedureCodeDescription": x.get("Procedure Name").replace("\u00a0>", ""),
                "Amount": x.get("Allowance"),
                "limitation": x.get("Limitation").replace("|", "").replace("More...", "").strip(),
                "DeductibleApplies": x.get("Applied to Deductible"),
                "Copay":"",
                "Benefits":x.get("Coverage % or Copay $")
            })
            if(x.get("Procedure Code")=="D2391"):
                EligibilityPatientVerification.update({"AlternativeBenefitProvision": x.get("Limitation").replace("More...", "").strip()})
                # if("Alternate Benefit Provision ~ Will Apply" in x.get("Limitation").replace("|", "").replace("More...", "").strip()):
                #     EligibilityPatientVerification.update({"AlternativeBenefitProvision":"Yes"})
                # else:
                #     EligibilityPatientVerification.update({"AlternativeBenefitProvision":"No"})
    EligibilityMaximums, EligibilityDeductibles=[],[]
    # try:
    #     temp=data.get("EligibilityMaximums")[0].get("Benefits")[0]
    
    #     if(temp.get("IndividualMaximum")):
    #         try:
    #             abc=temp.get("IndividualMaximum")
    #             abc=abc[abc.index("$"):abc.index(" ")] 
    #             EligibilityMaximums.append({
    #                 "Type":"Annual Maximums",
    #                 "Network":Network,
    #                 "Amount":abc,
    #                 "Remaining":"",
    #                 "ServiceCategory":ServiceType,
    #                 "Family_Individual":"Individual"
    #             })
    #         except: pass
    #     if(temp.get("IndividualDeductible")):
    #         try:
    #             abc=temp.get("IndividualDeductible")
    #             abc=abc[abc.index("$"):abc.index(" ")] 
    #             EligibilityDeductibles.append({
    #                 "Type":"Annual Deductible",
    #                 "Network":Network,           ###########
    #                 "Amount":abc,
    #                 "Remaining":"",
    #                 "ServiceCategory":ServiceType,
    #                 "Family_Individual":"Individual"
    #             })
    #         except: pass
    #     if(temp.get("FamilyDeductible")):
    #         try:
    #             abc=temp.get("FamilyDeductible")
    #             abc=abc[abc.index("$"):abc.index(" ")]
    #             EligibilityDeductibles.append({
    #                 "Type":"Annual Deductible",
    #                 "Network":Network,           ########
    #                 "Amount":abc,
    #                 "Remaining":"",
    #                 "ServiceCategory":ServiceType,
    #                 "Family_Individual":"Family"
    #             })
    #         except: pass

    # except: pass
    EligibilityServiceTreatmentHistory=[]
    try:
        for x in data.get("EligibilityServiceTreatmentHistory")[0].get("Tooth History"):
            flag=0
            History=x.get("End")
            if(x.get("Tooth")):
                History+='('
                for tooth in x.get("Tooth"):
                    History+=tooth+","
                History=History[:-1]+')'
            if(x.get("Surface")):
                History+='('
                for surface in x.get("Surface"):
                    History+=surface+","
                History=History[:-1]+')'

            for y in data.get("EligibilityBenefits"):
                if(x.get("Procedure")==y.get("Procedure Code")):
                    EligibilityServiceTreatmentHistory.append({
                        "ProcedureCode": x.get("Procedure"),
                        "LimitationText": y.get("Limitation").replace(" | More...", ""),
                        "History": History,
                        "Tooth": x.get("Tooth"),
                        "Surface": x.get("Surface"),
                        "LimitationAlsoAppliesTo":"",
                        "ProcedureCodeDescription": y.get("Procedure Name").replace("\u00a0>", "")
                    })
                    flag=1
                    break
            if(flag==0):
                EligibilityServiceTreatmentHistory.append({
                    "ProcedureCode": x.get("Procedure"),
                    "LimitationText": "",
                    "History": History,
                    "Tooth": x.get("Tooth"),
                    "Surface": x.get("Surface"),
                    "LimitationAlsoAppliesTo":"",
                    "ProcedureCodeDescription": ""
                    })
    except: pass
    try:
        COB=data.get("EligibilityOtherProvisions")[1].get("Benefit")
        if("Cob Primary Determination" in COB):
            COB=COB[COB.index("|")+2:]
            EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})
            EligibilityPatientVerification.update({"CoordinationofBenefitsType":COB})
    except: pass
    try:
        for p in data.get("EligibilityMaximums"):
            if ("Per Contract Year" in p.get("Coverage") and "$" in p.get("Coverage")):
                policyyear = p.get("Coverage").split(" ",1)[1]
                EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":policyyear})
                break
            else:
                EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":"Per Calendar Year"})
    except:
        pass
    try:
        for x in data.get("EligibilityMaximums"):
            if("Ortho" in x.get("Coverage")):
                ServiceCategory="Orthodontics"
            else:
                ServiceCategory=ServiceType
            if("Lifetime" in x.get("Coverage")):
                if("Maximum" in x.get("Benefit")):
                    Type="Lifetime Maximums"
                    if("Family" in x.get("Benefit")):
                        abc=x.get("Coverage")
                        try:abc=abc[abc.index("$"):abc.index(" ")]
                        except: abc=abc
                        Family_Individual="Family"
                        EligibilityMaximums.append({
                            "Type":Type,
                            "Network":Network,
                            "Amount":abc,
                            "Remaining":"",
                            "ServiceCategory":ServiceCategory,
                            "Family_Individual":Family_Individual
                        })
                    elif("Individual" in x.get("Benefit")):
                        abc=x.get("Coverage")
                        try:abc=abc[abc.index("$"):abc.index(" ")]
                        except: abc=abc
                        Family_Individual="Individual"
                        EligibilityMaximums.append({
                            "Type":Type,
                            "Network":Network,
                            "Amount":abc,
                            "Remaining":"",
                            "ServiceCategory":ServiceCategory,
                            "Family_Individual":Family_Individual
                        })
            
                elif("Deductible" in x.get("Benefit")):
                    Type="Lifetime Deductibles"
                    if("Family" in x.get("Benefit")):
                        abc=x.get("Coverage")
                        try:abc=abc[abc.index("$"):abc.index(" ")]
                        except: abc=abc
                        Family_Individual="Family"
                        EligibilityDeductibles.append({
                            "Type":Type,
                            "Network":Network,
                            "Amount":abc,
                            "Remaining":"",
                            "ServiceCategory":ServiceCategory,
                            "Family_Individual":Family_Individual
                        })
                    elif("Individual" in x.get("Benefit")):
                        abc=x.get("Coverage")
                        try:abc=abc[abc.index("$"):abc.index(" ")]
                        except: abc=abc
                        Family_Individual="Individual"
                        EligibilityDeductibles.append({
                            "Type":Type,
                            "Network":Network,
                            "Amount":abc,
                            "Remaining":"",
                            "ServiceCategory":ServiceCategory,
                            "Family_Individual":Family_Individual
                        })
            
            else:
                if("Maximum" in x.get("Benefit")):
                    Type="Annual Maximums"
                    if("Family" in x.get("Benefit")):
                        abc=x.get("Coverage")
                        try:abc=abc[abc.index("$"):abc.index(" ")]
                        except: abc=abc
                        Family_Individual="Family"
                        EligibilityMaximums.append({
                            "Type":Type,
                            "Network":Network,
                            "Amount":abc,
                            "Remaining":"",
                            "ServiceCategory":ServiceCategory,
                            "Family_Individual":Family_Individual
                        })
                    elif("Individual" in x.get("Benefit")):
                        abc=x.get("Coverage")
                        try:abc=abc[abc.index("$"):abc.index(" ")]
                        except: abc=abc
                        Family_Individual="Individual"
                        EligibilityMaximums.append({
                            "Type":Type,
                            "Network":Network,
                            "Amount":abc,
                            "Remaining":"",
                            "ServiceCategory":ServiceCategory,
                            "Family_Individual":Family_Individual
                        })
            
                elif("Deductible" in x.get("Benefit")):
                    Type="Annual Deductibles"
                    if("Family" in x.get("Benefit")):
                        abc=x.get("Coverage")
                        try:abc=abc[abc.index("$"):abc.index(" ")]
                        except: abc=abc
                        Family_Individual="Family"
                        EligibilityDeductibles.append({
                            "Type":Type,
                            "Network":Network,
                            "Amount":abc,
                            "Remaining":"",
                            "ServiceCategory":ServiceCategory,
                            "Family_Individual":Family_Individual
                        })
                    elif("Individual" in x.get("Benefit")):
                        abc=x.get("Coverage")
                        try:abc=abc[abc.index("$"):abc.index(" ")]
                        except: abc=abc
                        Family_Individual="Individual"
                        EligibilityDeductibles.append({
                            "Type":Type,
                            "Network":Network,
                            "Amount":abc,
                            "Remaining":"",
                            "ServiceCategory":ServiceCategory,
                            "Family_Individual":Family_Individual
                        })
            
            

        for x in EligibilityDeductibles:
            if(x.get("Type")=="Lifetime Deductibles" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Family"):
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("FamilyLifetimeDeductible")=="0.0"):
                    EligibilityPatientVerification.update({"FamilyLifetimeDeductible":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    EligibilityPatientVerification.update({"FamilyLifetimeDeductible":x.get('Amount')})        
            elif(x.get("Type")=="Lifetime Deductibles" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Individual"):
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("IndividualLifetimeDeductible")=="0.0"):
                    EligibilityPatientVerification.update({"IndividualLifetimeDeductible":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    EligibilityPatientVerification.update({"IndividualLifetimeDeductible":x.get('Amount')})        
            elif(x.get("Type")=="Annual Deductibles" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Family"):
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("FamilyAnnualDeductible")=="0.0"):
                    EligibilityPatientVerification.update({"FamilyAnnualDeductible":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    EligibilityPatientVerification.update({"FamilyAnnualDeductible":x.get('Amount')})        
            elif(x.get("Type")=="Annual Deductibles" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Individual"):
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("IndividualAnnualDeductible")=="0.0"):
                    EligibilityPatientVerification.update({"IndividualAnnualDeductible":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    EligibilityPatientVerification.update({"IndividualAnnualDeductible":x.get('Amount')})        
            

        for x in EligibilityMaximums:
            if(x.get("Type")=="Lifetime Maximums" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Family"):
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("FamilyLifetimeMaximumBenefits")=="0.0"):
                    EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":x.get('Amount')})        
            elif(x.get("Type")=="Lifetime Maximums" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Individual"):
                
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits")=="0.0"):
                    EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    
                    EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":x.get('Amount')})        
            elif(x.get("Type")=="Annual Maximums" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Family"):
                
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("FamilyAnnualMaximumBenefits")=="0.0"):
                    EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":x.get('Amount')})        
            elif(x.get("Type")=="Annual Maximums" and x.get("ServiceCategory")==ServiceType and x.get("Family_Individual")=="Individual"):
                
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits")=="0.0"):
                    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":x.get('Amount')})        
            elif(x.get("Type")=="Lifetime Maximums" and x.get("ServiceCategory")=="Orthodontics" and x.get("Family_Individual")=="Individual"):
                
                if(x.get("Amount")=="None" and EligibilityPatientVerification.get("OrthodonticLifetimeBenefit")=="0.0"):
                    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":x.get('Amount')})        
                elif(x.get("Amount")!="None"):
                    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":x.get('Amount')})        
    except: pass  

    try:
        # temp=data.get("OtherBenefits")[0].get("Policy Dollar Max")
        temp=data.get("EligibilityOtherProvisions")[-1].get("Policy Dollar Max", "")
        if search("Remaining", temp) and search("Orthodontics", temp) == None:
            temp=temp.split("\n")
            for x in temp:
                if("Applied" in x):
                    EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":x.replace("Applied", "").strip()})        
                elif(x=="Total"):
                  EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":temp[temp.index(x)+1]})   
                if("Remaining" in x):
                    EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":x.replace("Remaining", "").strip()})               
        # else:
        #     EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":"0.0"})        
        #     EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":"0.0"})   
        #     EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":"0.0"})               
    except: pass
    try:
        # temp=data.get("OtherBenefits")[0].get("Policy Dollar Max")
        temp=data.get("EligibilityOtherProvisions")[-1].get("Policy Dollar Ded Family", "")
        if("Remaining" in temp):
            temp=temp.split("\n")
            for x in temp:
                if("Applied" in x):
                    EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":x.replace("Applied", "").strip()})        
                elif(x=="Total"):
                  EligibilityPatientVerification.update({"FamilyAnnualDeductible":temp[temp.index(x)+1]})   
                if("Remaining" in x):
                    EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":x.replace("Remaining", "").strip()})               
        # else:
        #     EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":"0.0"})        
        #     EligibilityPatientVerification.update({"FamilyAnnualDeductible":"0.0"})   
        #     EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":"0.0"})               
    except: pass
    try:
        # temp=data.get("OtherBenefits")[0].get("Policy Dollar Max")
        temp=data.get("EligibilityOtherProvisions")[-1].get("Policy Dollar Ded Individual", "")
        if("Remaining" in temp):
            temp=temp.split("\n")
            for x in temp:
                if("Applied" in x):
                    EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":x.replace("Applied", "").strip()})        
                elif(x=="Total"):
                  EligibilityPatientVerification.update({"IndividualAnnualDeductible":temp[temp.index(x)+1]})   
                if("Remaining" in x):
                    EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":x.replace("Remaining", "").strip()})               
        # else:
        #     EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":"0.0"})        
        #     EligibilityPatientVerification.update({"IndividualAnnualDeductible":"0.0"})   
        #     EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":"0.0"})               
    except: pass
    # try:
    #     # temp=data.get("OtherBenefits")[0].get("Policy Dollar Max")
    #     temp=data.get("EligibilityOtherProvisions")[-1].get("Deductibles", "")
    #     if("No deductible applied to the current benefit period" in temp and EligibilityPatientVerification.get("IndividualAnnualDeductible", "") in ["", "0.0"]):
    #             # EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":"0.0"})        
    #             EligibilityPatientVerification.update({"IndividualAnnualDeductible":"0.0"})   
    #             # EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":x.replace("Remaining", "").strip()})               
    # except: pass

    # allcodeslist1 = ""
    # EligibilityBenefits1 =[]
    # for dictionary  in EligibilityBenefits:
    #     if dictionary.get("ProcedureCode") in allcodeslist1:
    #         # for historyitems in EligibilityBenefits1:
    #         #     if dictionary.get("ProcedureCode") in historyitems.get("ProcedureCode"):
    #         #         historyitems.update({"History":historyitems.get("History")+", "+dictionary['History']})
    #         #         break
    #         continue
    #     EligibilityBenefits1.append(dictionary)
    #     allcodeslist1 = allcodeslist1 +" "+dictionary['ProcedureCode']

    # EligibilityBenefits = EligibilityBenefits1


    
    allcodeslist = ""
    EligibilityServiceTreatmentHistory1 =[]
    for dictionary  in EligibilityServiceTreatmentHistory:
        if dictionary.get("ProcedureCode") in allcodeslist:
            for historyitems in EligibilityServiceTreatmentHistory1:
                if dictionary.get("ProcedureCode") in historyitems.get("ProcedureCode"):
                    historyitems.update({"History":historyitems.get("History")+", "+dictionary['History']})
                    break
            continue
        EligibilityServiceTreatmentHistory1.append(dictionary)
        allcodeslist = allcodeslist +" "+dictionary['ProcedureCode']

    EligibilityServiceTreatmentHistory = EligibilityServiceTreatmentHistory1


    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":changeNone(EligibilityPatientVerification.get("PlanType"))})
    output={}
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductibles})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":EligibilityServiceTreatmentHistory})
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
    return output
# import json
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\united concordia\New Framework\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data)
# with open("UCres.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)