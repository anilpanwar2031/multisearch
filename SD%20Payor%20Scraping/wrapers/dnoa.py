from mapPDF import mapEligibilityPatientVerification
import json

def FamilyMemberWaitingPeriod(benefits):
    for obj in benefits:
        if obj.get("procedureCode")=="D2392":
            return obj.get("WaitingPeriod","")
def NewDeductible(data):
  final=[]
  for obj in data:
    if obj.get("Type")=="Deductible - Benefit Period":
      if obj.get("InNetworkindividual"):
        remaining_obj=[x for x in data if x['Type']=="Deductible - Benefit Period Remaining"][0]
        remain=remaining_obj.get("InNetworkindividual")
        
     
        temp_dict1={
        "Type":"Deductible - Benefit Period",
        "Network":"InNetwork",
        "Amount":obj.get("InNetworkindividual",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Individual"
    }
        final.append(temp_dict1)
      if obj.get("InNetworkfamily"):
        remaining_obj=[x for x in data if x['Type']=="Deductible - Benefit Period Remaining"][0]
        remain=remaining_obj.get("InNetworkfamily")
        
     
        temp_dict2={
        "Type":"Deductible - Benefit Period",
        "Network":"InNetwork",
        "Amount":obj.get("InNetworkfamily",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Family"
    } 
        final.append(temp_dict2)
      if obj.get("OutOfNetworkindividual"):
    
        remaining_obj=[x for x in data if x['Type']=="Deductible - Benefit Period Remaining"][0]
        remain=remaining_obj.get("OutOfNetworkindividual")
        temp_dict3={
        "Type":"Deductible - Benefit Period",
        "Network":"OutOfNetwork",
        "Amount":obj.get("OutOfNetworkindividual",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Individual"
      } 
        final.append(temp_dict3)
      if obj.get("OutOfNetworkfamily"):
    
        remaining_obj=[x for x in data if x['Type']=="Deductible - Benefit Period Remaining"][0]
        remain=remaining_obj.get("OutOfNetworkfamily")
        temp_dict4={
        "Type":"Deductible - Benefit Period",
        "Network":"OutOfNetwork",
        "Amount":obj.get("OutOfNetworkfamily",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Family"
      }    
        final.append(temp_dict4)
  
 
      
  return final 
def NewMaximun(data):
  final=[]
  for obj in data:
    if obj.get("Type")=="Maximums - Benefit Period":
      if obj.get("InNetworkindividual"):
        remaining_obj=[x for x in data if x['Type']=="Maximums - Benefit Period Remaining"][0]
        remain=remaining_obj.get("InNetworkindividual")
        
     
        temp_dict1={
        "Type":"Maximums - Benefit Period",
        "Network":"InNetwork",
        "Amount":obj.get("InNetworkindividual",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Individual"
    }
        final.append(temp_dict1)
      if obj.get("InNetworkfamily"):
        remaining_obj=[x for x in data if x['Type']=="Maximums - Benefit Period Remaining"][0]
        remain=remaining_obj.get("InNetworkfamily")
        
     
        temp_dict2={
        "Type":"Maximums - Benefit Period",
        "Network":"InNetwork",
        "Amount":obj.get("InNetworkfamily",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Family"
    } 
        final.append(temp_dict2)
      if obj.get("OutOfNetworkindividual"):
    
        remaining_obj=[x for x in data if x['Type']=="Maximums - Benefit Period Remaining"][0]
        remain=remaining_obj.get("OutOfNetworkindividual")
        temp_dict3={
        "Type":"Maximums - Benefit Period",
        "Network":"OutOfNetwork",
        "Amount":obj.get("OutOfNetworkindividual",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Individual"
      } 
        final.append(temp_dict3)
      if obj.get("OutOfNetworkfamily"):
    
        remaining_obj=[x for x in data if x['Type']=="Maximums - Benefit Period Remaining"][0]
        remain=remaining_obj.get("OutOfNetworkfamily")
        temp_dict4={
        "Type":"Maximums - Benefit Period",
        "Network":"OutOfNetwork",
        "Amount":obj.get("OutOfNetworkfamily",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Family"
      }    
        final.append(temp_dict4)
  
    if obj.get("Type")=="Maximums - Lifetime":
      
      
      if obj.get("InNetworkindividual"):
        remaining_obj=[x for x in data if x['Type']=="Maximums - Lifetime Remaining"][0]
        remain=remaining_obj.get("InNetworkindividual")
        
     
        temp_dict1={
        "Type":"Maximums - Lifetime",
        "Network":"InNetwork",
        "Amount":obj.get("InNetworkindividual",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Individual"
    }
        final.append(temp_dict1)
      if obj.get("InNetworkfamily"):
        remaining_obj=[x for x in data if x['Type']=="Maximums - Lifetime Remaining"][0]
        remain=remaining_obj.get("InNetworkfamily")
        
     
        temp_dict2={
        "Type":"Maximums - Lifetime",
        "Network":"InNetwork",
        "Amount":obj.get("InNetworkfamily",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Family"
    } 
        final.append(temp_dict2)
      if obj.get("OutOfNetworkindividual"):
    
        remaining_obj=[x for x in data if x['Type']=="Maximums - Lifetime Remaining"][0]
        remain=remaining_obj.get("OutOfNetworkindividual")
        temp_dict3={
        "Type":"Maximums - Lifetime",
        "Network":"OutOfNetwork",
        "Amount":obj.get("OutOfNetworkindividual",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Individual"
      } 
        final.append(temp_dict3)
      if obj.get("OutOfNetworkfamily"):
    
        remaining_obj=[x for x in data if x['Type']=="Maximums - Lifetime Remaining"][0]
        remain=remaining_obj.get("OutOfNetworkfamily")
        temp_dict4={
        "Type":"Maximums - Lifetime",
        "Network":"OutOfNetwork",
        "Amount":obj.get("OutOfNetworkfamily",""),
        "Remaining":remain,
        "ServiceCategory":"",
        "Family_Individual":"Family"
      }    
        final.append(temp_dict4)


      
  return final 
def calculate_difference(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=str(a).replace(",", "").replace("N/A", "0").replace("$", "")
    b=str(b).replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)-float(b)}'
def changeNone(val):
    if(val==None):
        return ""
    else:
        return val

def mapdicts(a,b):
    for x in a:
        b.update({x:""})
    return b
def check_oon_flag(temp):
    for x in temp:
        try:
            if(float(temp.get(x).get("OutOfNetworkindividual").replace(",", "").replace("N/A", "0").replace("$", ""))):
                return "Yes"
        except: pass
    return "No"
def generate_codelist(code, tempdict):
    text=tempdict.get("Alternate Benefit Procedure").replace("\n", "")
    codelist=[]
    for x in range(len(text)):
        if(text[x]=="D" and text[x+1].isnumeric()):
            code="D"
            for y in text[x+1:]:
                if(not y.isnumeric() and y!="-"):  break
                code+=y
            x=x+len(code)
            codelist.append(code)
    x=0

    
    while x<len(codelist)-1:
        if(codelist[x][-1]=="-"):
            
            
            codelist[x]=codelist[x].replace("-", "")
            
            for y in range(int(codelist[x][1:])+1, int(codelist[x+1][1:])):
                if(y<10): codelist.insert(x+1, f"D000{y}")
                elif(y<100): codelist.insert(x+1, f"D00{y}")
                elif(y<1000): codelist.insert(x+1, f"D0{y}")
                elif(y<10000): codelist.insert(x+1, f"D{y}")
                x+=1
            x+=1
        x+=1
    codelist=list(set(codelist))
    try:codelist.remove(code)
    except: pass
    return codelist

def get_related_codes(code, master_codelist):
    temp=''
    for codes in master_codelist.get(code, ""):
        temp+=codes+', '
    # temp=str(list(set(temp)))[1:-1].replace("'", "")
    return temp.strip(', ')

def getbenefitsdata(code, templist):
    for x in templist:
        if(x.get("procedureCode")==code):
            return x.get("procedureCodeDescription"), x.get("limitation")
    return "", ""
def fixdate(text):
    t=""
    for x in text.split('/'): 
        t+=x.zfill(2)+"/"
    return t[:-1]
def main(data):
    output={}
    PDFData={}
    PDFData=mapEligibilityPatientVerification()
    PDFData.update({"InsuranceName":data.get('EligibilityPatientVerification')[-1].get('Payer')})
    for key in data.get('EligibilityPatientVerification')[-1]:
        if(key.startswith("ClaimsAddress")):
            # PDFData.update({"InsuranceMailingAddress":key[13:]+data.get('EligibilityPatientVerification')[-1].get(key).replace("Address1", "")})
            PDFData.update({"ClaimMailingAddress":key[13:]+data.get('EligibilityPatientVerification')[-1].get(key).replace("Address1", "")})
            break
    PDFData.update({"ClaimPayerID":data.get('EligibilityPatientVerification')[-1].get('PayerId')})
    PDFData.update({"SubscriberEffectiveDate":data.get('EligibilityPatientVerification')[1].get('Enrolled')})
    PDFData.update({"GroupName":data.get('EligibilityPatientVerification')[-1].get('GroupName')})
    PDFData.update({"GroupNumber":data.get('EligibilityPatientVerification')[-1].get('GroupNumber')})
    
    planinfodict={}
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    for temp1 in data.get('EligibilityMaximums')[0].get("Maximums"):
        if("Maximum" in temp1.get("Type")): 
            tempmapdict={
                "Type": "Lifetime Individual Maximum",
                "ProgramMaximum_AppliesToTheFollowingServices_": "Oral & Maxillofacial SurgeryOrthodontics",
                "Network": "Delta Dental DPO DentistDelta Dental Premier DentistNon-Delta Dental Dentist (Benefits based on contract allowance)",
                "Amount": "$3000.00",
                "Remaining": "$3000.00"
            }
            temp2={}
            temp2=mapdicts(tempmapdict, temp2)
            temp2.update(temp1)
            EligibilityMaximums.append(temp2)
        elif("Deductible" in temp1.get("Type")): 
            tempmapdict={
                "Type": "",
                "ProgramDeductible_AppliesToTheFollowingServices_": "",
                "Network": "",
                "Amount": "",
                "Remaining": ""
            }
            temp2={}
            temp2=mapdicts(tempmapdict, temp2)
            temp2.update(temp1)
            EligibilityDeductiblesProcCode.append(temp2)
        planinfodict.update({temp1.get("Type"):temp1})

    PDFData.update({"oonBenefits":check_oon_flag(planinfodict)})
    planinfodictortho={}
    try:
        for temp1 in data.get('EligibilityMaximums')[1].get("OrthodonticsMaximums"):
            planinfodictortho.update({temp1.get("Type"):temp1})
    except:
        pass
    # PDFData.update({"IndividualAnnualDeductible":planinfodict.get("Deductible - Benefit Period").get("InNetworkindividual")})
    # PDFData.update({"IndividualDeductibleMet":calculate_difference(planinfodict.get("Deductible - Benefit Period").get("InNetworkindividual"), planinfodict.get("Deductible - Benefit Period Remaining").get("InNetworkindividual"))})

    try: PDFData.update({"FamilyAnnualDeductible":changeNone(planinfodict.get("Deductible - Benefit Period").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyAnnualDeductible":""})
    try: PDFData.update({"FamilyAnnualDeductibleMet":calculate_difference(planinfodict.get("Deductible - Benefit Period").get("InNetworkfamily"), planinfodict.get("Deductible - Benefit Period Remaining").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyAnnualDeductibleMet":0.0})
    try: PDFData.update({"FamilyAnnualDeductibleRemaining":changeNone(planinfodict.get("Deductible - Benefit Period Remaining").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyAnnualDeductibleRemaining":""})

    try: PDFData.update({"FamilyLifetimeMaximumBenefits":changeNone(planinfodict.get("Maximums - Lifetime").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyLifetimeMaximumBenefits":""})
    try: PDFData.update({"FamilyLifetimeBenefitsUsedtoDate":calculate_difference(planinfodict.get("Maximums - Lifetime").get("InNetworkfamily"), planinfodict.get("Maximums - Lifetime Remaining").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyLifetimeBenefitsUsedtoDate":0.0})
    try: PDFData.update({"FamilyLifetimeRemainingBenefit":changeNone(planinfodict.get("Maximums - Lifetime Remaining").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyLifetimeRemainingBenefit":""})

    try: PDFData.update({"FamilyAnnualMaximumBenefits":changeNone(planinfodict.get("Maximums - Benefit Period").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyAnnualMaximumBenefits":""})
    try: PDFData.update({"FamilyAnnualBenefitsUsedtoDate":calculate_difference(planinfodict.get("Maximums - Benefit Period").get("InNetworkfamily"), planinfodict.get("Maximums - Benefit Period Remaining").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyAnnualBenefitsUsedtoDate":0.0})
    try: PDFData.update({"FamilyAnnualRemainingBenefit":changeNone(planinfodict.get("Maximums - Benefit Period Remaining").get("InNetworkfamily"))})
    except: PDFData.update({"FamilyAnnualRemainingBenefit":""})

    try: PDFData.update({"IndividualAnnualDeductible":changeNone(planinfodict.get("Deductible - Benefit Period").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualAnnualDeductible":""})
    try: PDFData.update({"IndividualAnnualDeductibleMet":calculate_difference(planinfodict.get("Deductible - Benefit Period").get("InNetworkindividual"), planinfodict.get("Deductible - Benefit Period Remaining").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualAnnualDeductibleMet":0.0})
    try: PDFData.update({"IndividualAnnualDeductibleRemaining":changeNone(planinfodict.get("Deductible - Benefit Period Remaining").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualAnnualDeductibleRemaining":""})

    try: PDFData.update({"IndividualLifetimeMaximumBenefits":changeNone(planinfodict.get("Maximums - Lifetime").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualLifetimeMaximumBenefits":""})
    try: PDFData.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(planinfodict.get("Maximums - Lifetime").get("InNetworkindividual"), planinfodict.get("Maximums - Lifetime Remaining").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualLifetimeBenefitsUsedtoDate":0.0})
    try: PDFData.update({"IndividualLifetimeRemainingBenefit":changeNone(planinfodict.get("Maximums - Lifetime Remaining").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualLifetimeRemainingBenefit":""})

    try: PDFData.update({"IndividualAnnualMaximumBenefits":changeNone(planinfodict.get("Maximums - Benefit Period").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualAnnualMaximumBenefits":""})
    try: PDFData.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(planinfodict.get("Maximums - Benefit Period").get("InNetworkindividual"), planinfodict.get("Maximums - Benefit Period Remaining").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualAnnualBenefitsUsedtoDate":0.0})
    try: PDFData.update({"IndividualAnnualRemainingBenefit":changeNone(planinfodict.get("Maximums - Benefit Period Remaining").get("InNetworkindividual"))})
    except: PDFData.update({"IndividualAnnualRemainingBenefit":""})

    try: PDFData.update({"OrthodonticLifetimeBenefit":changeNone(planinfodictortho.get("Maximums - Lifetime").get("InNetworkindividual"))})
    except: PDFData.update({"OrthodonticLifetimeBenefit":""})
    try: PDFData.update({"OrthodonticLifetimeRemainingBenefit":changeNone(planinfodictortho.get("Maximums - Lifetime Remaining").get("InNetworkindividual"))})
    except: PDFData.update({"OrthodonticLifetimeRemainingBenefit":0.0})
    try: PDFData.update({"OrthodonticLifetimeBenefitUsedtoDate":calculate_difference(planinfodictortho.get("Maximums - Lifetime").get("InNetworkindividual"), planinfodictortho.get("Maximums - Lifetime Remaining").get("InNetworkindividual"))})
    except: PDFData.update({"OrthodonticLifetimeBenefitUsedtoDate":""})
    
    # PDFData.update({"RemainingBenefit":planinfodict.get("Maximums - Lifetime Remaining").get("InNetworkindividual")})
    # PDFData.update({"AnnualMaximumBenefits":planinfodict.get("Maximums - Benefit Period").get("InNetworkindividual")})
    # PDFData.update({"BenefitsUsedToDate":calculate_difference(planinfodict.get("Maximums - Benefit Period").get("InNetworkindividual"), planinfodict.get("Maximums - Benefit Period Remaining").get("InNetworkindividual"))})
    # PDFData.update({"RemainingBenefit":planinfodict.get("Maximums - Benefit Period Remaining").get("InNetworkindividual")})

    PDFData.update({"MissingToothClause":data.get('EligibilityPatientVerification')[2].get('MissingToothProvision')})
    # PDFData.update({"CoordinationofBenefits":data.get('EligibilityPatientVerification')[2].get('CoordinationOfBenefits')})
    if(data.get('EligibilityPatientVerification')[2].get('CoordinationOfBenefits')):
        PDFData.update({"CoordinationofBenefits":"Yes"})
        PDFData.update({"CoordinationofBenefitsType":data.get('EligibilityPatientVerification')[2].get('CoordinationOfBenefits')})
    
    waitingperiods={}
    ProcedureCode=[]
    master_codelist={}
    # for templist in data.get('EligibilityBenefits'):
    #     ################## for tempdict in templist:
    #     if(True):
    #         tempdict=templist
    #         if(tempdict.get("Category")):
    #             if(tempdict.get("Category")=="Orthodontics"):
    #                 try:
    #                     PDFData.update({"OrthodonticLifetimeBenefit":templist[0].get("InNetworkindividual")})
    #                     PDFData.update({"OrthodonticRemainingBenefit":templist[1].get("InNetworkindividual")})
    #                     PDFData.update({"OrthodonticBenefitUsedtoDate":calculate_difference(templist[0].get("InNetworkindividual"), templist[1].get("InNetworkindividual"))})

    #                 except:
    #                     PDFData.update({"OrthodonticLifetimeBenefit":""})
    #                     PDFData.update({"OrthodonticRemainingBenefit":""})
                    
    #             waitingperiods.update({f'{tempdict.get("Category")}WaitingPeriod'.replace(" ", ""): tempdict.get("WaitingPeriod")})
    #             codelist=generate_codelist(tempdict)
    #             master_codelist.append(codelist)
    #             for code in codelist:
    #                 try: 
    #                     # abc=ProcedureCode.get(code)
    #                     # abc.extend([tempdict])
    #                     # ProcedureCode.update({code:abc})
    #                     abc={}
    #                     tempmapdict={
    #                         "procedureCode": "D0120",
    #                         "procedureCodeDescription": "Periodic oral evaluation - established patient",
    #                         "limitation": "Benefit is limited to two of any oral evaluation procedure within the contract period. Comprehensive evaluations are limited to once per provider.",
    #                         "PreApproval": "No",
    #                         "DeductibleApplicable": "No"
    #                     }
    #                     abc=mapdicts(tempmapdict, abc)
    #                     abc.update({"procedureCode":code})
    #                     abc["limitation"] = tempdict["FrequencyLimitationText"]
    #                     abc.update(tempdict)
                        
    #                     ProcedureCode.append(abc)
    #                 except: 
    #                     ProcedureCode.update({code:[tempdict]})
    # # abc=[]
    # for tempdict in ProcedureCode:
    #     abc.append({tempdict:ProcedureCode.get(tempdict)})
    EligibilityBenefits=[]
    for tempdict in data.get("EligibilityBenefits"):
        limitation=""
        Otherdict={
            'Waiting Period': '',
            'Up to Age 13': '',
            'Other Limitations':'',
            'Alternate Benefit Procedure':'',
            'AgeLimit':'',
            'AgeLimitationText':''
        }
        try:
            Other=tempdict.get("Other").split("\n")
        except: Other=[]
        for x in range(len(Other)):
            if(x<len(Other)-1 and ":" in Other[x] and ":" not in Other[x+1]):
                Otherdict.update({Other[x][:-1]:Other[x+1]})
                if("Up to Age" in Other[x]):
                    Otherdict.update({"AgeLimitationText":Other[x+1]})
                    Otherdict.update({"AgeLimit":Other[x+1].replace("Up to Age ", "")})
            elif(Other[x]=="Alternate Benefit Procedure:" and x<len(Other)-1):
                text=''
                limitation=Other[x+1][:-1]
                for y in range(len(Other[x+1:])):
                    text+=' '+Other[y+x+1]
                Otherdict.update({Other[x][:-1]:text})
                break
        master_codelist.update({tempdict.get("procedureCode").replace("Procedure Code: ", ""):generate_codelist(tempdict.get("procedureCode").replace("Procedure Code: ", ""), Otherdict)})
        codeUsed = tempdict.get("procedureCode").replace("Procedure Code: ", "")
        DescripitonForHitory = tempdict.get("codeDescription")
        if codeUsed in tempdict.get("Historydates"):
            LastDateOfServiceHistory = tempdict.get("Historydates").replace("\n"," ").replace(codeUsed,",").strip(",").replace(DescripitonForHitory,"-").strip("-")
        else:
            LastDateOfServiceHistory = ""
        temp={
            "procedureCode": tempdict.get("procedureCode").replace("Procedure Code: ", ""),
            "procedureCodeDescription":  tempdict.get("codeDescription"),
            # "limitation": limitation,
            "limitation": Otherdict.get("Alternate Benefit Procedure"),
            "PreApproval": "",
            "DeductibleApplicable": tempdict.get("InNetworkDeductible"),
            "Category": "",
            # "InNetwork": "",
            "InNetworkDeductible": tempdict.get("InNetworkDeductible"),
            # "Outofnetwork": "",
            # "OutNetworkDeductible": "",
            "LastDateOfService": LastDateOfServiceHistory,
            "FrequencyLimitationText": limitation.replace("consisting of codes", "").strip(),
            "FrequencyLimitations": Otherdict.get("Alternate Benefit Procedure"),
            "WaitingPeriod": tempdict.get("WaitingPeriod"),
            "AgeLimit": Otherdict.get("AgeLimit"),
            "AgeLimitationText": Otherdict.get("AgeLimitationText"),
            "OtherLimitations": Otherdict.get("Other Limitations"),
            "InNetworkCoinsurance": tempdict.get("InNetworkCoinsurance"),
            "procedureCovered": tempdict.get("InNetworkCoinsurance"),
            "Benefits":tempdict.get("InNetworkCoinsurance"),
            "OutOfNetworkCoinsurance": tempdict.get("OutOfNetworkCoinsurance"),
            "OutOfInNetworkDeductible": tempdict.get("OutOfNetworkDeductible"),
            "Copay":tempdict.get("Copay"),
            "AlternateBenefitProcedure":tempdict.get("AlternateBenefitProcedure")
        }
        EligibilityBenefits.append(temp)

    # PDFData.update(waitingperiods)
    
    
    temp=PDFData
    # temp.update(data.get("EligibilityPatientVerification")[0])
    x=data.get("EligibilityPatientVerification")[0]
    temp.update({"SubscriberEligibilityStatus":x.get("MemberStatus")})
    temp.update({"EligibilityStatus":x.get("MemberStatus")})
    temp.update({"SubscriberName":x.get("SubscriberName").replace(" Information cannot be retrieved at this time", "")})
    temp.update({"FamilyMemberDateOfBirth":x.get("DateOfBirth")})
    temp.update({"SubscriberId":x.get("SubscriberId")})
    temp.update({"FamilyMemberName":x.get("MemberName")})
    EnrolleeName=x.get("SubscriberName").replace(" Information cannot be retrieved at this time", "")
    

    # temp.update(data.get("EligibilityPatientVerification")[1])
    x=data.get("EligibilityPatientVerification")[1]
    temp.update({"FamilyMemberEffectiveDate":x.get("Enrolled")})
    # temp.update({"EligibilityStatus":x.get("MemberStatus")})
    # temp.update({"EligibilityStatus":x.get("MemberStatus")})

    # temp.update(data.get("EligibilityPatientVerification")[2])
    x=data.get("EligibilityPatientVerification")[2]
    temp.update({"AlternativeBenefitProvision":x.get("AlternativeBenefitProvision")})
    temp.update({"MissingToothProvision":x.get("MissingToothProvision")})
    if(x.get("CoordinationOfBenefits")):
        temp.update({"CoordinationofBenefits":"Yes"})
        temp.update({"CoordinationofBenefitsType":x.get("CoordinationOfBenefits")})
    # temp.update({"CoordinationofBenefits":x.get("CoordinationOfBenefits")})
    temp.update({"AssignmentOfBenefits":x.get("AssignmentOfBenefits")})
    temp.update({"FillingDowngrade":x.get("FillingDowngrade")})
    for x in data.get("EligibilityPatientVerification")[-1]:
        if('ClaimsAddress' in x or "PayerId" in x):
            continue
        temp.update({x:data.get("EligibilityPatientVerification")[-1].get(x)})
    temp.update({"InsuranceFeeScheduleUsed":changeNone(temp.get("PlanType"))})
    output.update({"EligibilityPatientVerification":[temp]})
    output.update({"EligibilityMaximums":NewMaximun(EligibilityMaximums)})
    output.update({"EligibilityDeductiblesProcCode":NewDeductible(EligibilityDeductiblesProcCode)})
    output.update({"EligibilityBenefits": EligibilityBenefits})
    EligibilityServiceTreatmentHistory=[]


    for x1 in EligibilityBenefits:
        tempmapdict={
            "ProcedureCode": "D0120",
            "ProcedureCodeDescription": "Periodic oral evaluation - established patient",
            "LimitationText": "Benefit is limited to two of any oral evaluation procedure within the contract period. Comprehensive evaluations are limited to once per provider.",
            "LimitationAlsoAppliesTo": "D0145, D0150, D0160, D0180, D0190, D0191, D9310",
            "ServiceDate": "12/09/2022, 06/24/2022, 12/17/2021, 07/05/2021, 01/04/2021, 07/24/2020, 01/03/2020, 07/26/2019, 12/21/2018, 05/25/2018, 11/21/2017",
            "ToothCode": "",
            "ToothDescription": "",
            "ToothSurface": ""
        }
        temp={}
        temp=mapdicts(tempmapdict, temp)
        #ProcedureCodeDescription, LimitationText =getbenefitsdata(x.get("ProcedureCode"), EligibilityBenefits)
        temp.update({"ProcedureCode": x1.get("procedureCode")})
        temp.update({"ToothCode": ""})
        temp.update({"ToothSurface": ""})
        temp.update({"Description": x1.get("procedureCodeDescription")})
        temp.update({"ServiceDate":x1.get("LastDateOfService")})
        temp.update({"LimitationText":x1.get("limitation")})
        temp.update({"ProcedureCodeDescription":x1.get("procedureCodeDescription")})
        temp.update({"LimitationAlsoAppliesTo":""})
        EligibilityServiceTreatmentHistory.append(temp)


    # for x in data.get("EligibilityServiceTreatmentHistory"):
    #     tempmapdict={
    #         "ProcedureCode": "D0120",
    #         "ProcedureCodeDescription": "Periodic oral evaluation - established patient",
    #         "LimitationText": "Benefit is limited to two of any oral evaluation procedure within the contract period. Comprehensive evaluations are limited to once per provider.",
    #         "LimitationAlsoAppliesTo": "D0145, D0150, D0160, D0180, D0190, D0191, D9310",
    #         "ServiceDate": "12/09/2022, 06/24/2022, 12/17/2021, 07/05/2021, 01/04/2021, 07/24/2020, 01/03/2020, 07/26/2019, 12/21/2018, 05/25/2018, 11/21/2017",
    #         "ToothCode": "",
    #         "ToothDescription": "",
    #         "ToothSurface": ""
    #     }
    #     temp={}
    #     temp=mapdicts(tempmapdict, temp)
    #     ProcedureCodeDescription, LimitationText =getbenefitsdata(x.get("ProcedureCode"), EligibilityBenefits)
    #     temp.update({"ProcedureCode": x.get("ProcedureCode")})
    #     temp.update({"ToothCode": x.get("Tooth_Quadrant")})
    #     temp.update({"ToothSurface": x.get("Surfaces")})
    #     temp.update({"Description": x.get("Description")})
    #     temp.update({"ServiceDate": fixdate(x.get("DateOfService"))})
    #     temp.update({"LimitationText":LimitationText})
    #     temp.update({"ProcedureCodeDescription":ProcedureCodeDescription})
    #     temp.update({"LimitationAlsoAppliesTo":get_related_codes(x.get("ProcedureCode"), master_codelist)})
    #     EligibilityServiceTreatmentHistory.append(temp)
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})




    GROUPINFO=[]
    temp={}
    for x in data.get("EligibilityPatientVerification"):
        if(x.get("Status")==""):
            temp={"Name":x.get("Name/Plans")}
            
        elif(x.get("Status")!=None):
            temp.update({"Plan":x.get("Name/Plans"), "Status":x.get("Status")})
            GROUPINFO.append(temp)
            temp={}
    output.update({"AssociatedMember":GROUPINFO})
    temp=[]
    for y in EligibilityServiceTreatmentHistory:
        temp.append({"ProcedureCode":y.get("ProcedureCode"), "ProcedureCodeDescription":y.get("Description"), "LimitationText":y.get("LimitationText") , "LimitationAlsoAppliesTo":"", "History":y.get("ServiceDate")})
    output.update({"TreatmentHistorySummary":temp})
    output.update({"EligibilityAgeLimitation": [
        {
            "FamilyMember": "",
            "AgeLimit": ""
        }
    ]})

    for x in GROUPINFO:
        
        if(x.get("Name")==EnrolleeName):
            temp=output.get("EligibilityPatientVerification")
            temp=temp[0]
            
            temp.update({"SubscriberEligibilityStatus":x.get("Status")})
            output.update({"EligibilityPatientVerification":[temp]})
            break
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
    output["EligibilityPatientVerification"][0]["FamilyMemberWaitingPeriod"]=FamilyMemberWaitingPeriod(output['EligibilityBenefits'])    
    return output

# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\dev 15 june all testing\dev 17 june\SD%20Payor%20Scraping\output_230628_124147_.json", 'r'))
# output=main(data)
# with open("Dnoares.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
       
