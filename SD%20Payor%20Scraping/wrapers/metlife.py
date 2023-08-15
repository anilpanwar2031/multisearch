import json, datetime
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
    return f'${float(a)-float(b)}'
def main(data):
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityPatientVerification.update({
        "PlanType": data.get("EligibilityPatientVerification")[0].get("Network"),
        "FamilyMemberName": data.get("EligibilityPatientVerification")[0].get("Patient"),
        "GroupNumber": data.get("EligibilityPatientVerification")[0].get("Group#"),
        "GroupName": data.get("EligibilityPatientVerification")[0].get("GroupName"),
    })
    # for x in data.get("EligibilityPatientVerification")[0]:
    #     print(x, ':', data.get("EligibilityPatientVerification")[0].get(x))
        

    for x in data.get("EligibilityPatientVerification")[1]:
        if(x=="Address"):
            temp=data.get("EligibilityPatientVerification")[1].get(x)
            EligibilityPatientVerification.update({"ClaimMailingAddress":temp[temp.index("Mail Claims to:\n")+16:temp.index("\nOr Fax to:")].replace("\n", " ")})
        for y in data.get("EligibilityPatientVerification")[1].get(x).split('\n'):
            temp=y.split(':')
            if(len(temp)==2 and temp[1].strip!=""):
                # print(temp[0].strip(), ':', temp[1].strip())
                if(temp[0]=="Plan Benefit start date"):
                    EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":temp[1]})
                elif(temp[0]=="Subscriber's Name"):
                    EligibilityPatientVerification.update({"SubscriberName":temp[1]})
        
    temp={}
    for x in data.get("EligibilityMaximums")[0].get("BasicPlanInfo"):
        if(x.get("Type")=="Plan Maximum"):
            a=temp.get("Maximum")
            if(not a): a={}
            
            a.update({
                "IndividualAnnualAmount":changeNone(x.get("BenefitPeriodIndividual")),
                "IndividualLifetimeAmount":changeNone(changeNone(x.get("LifetimeIndividual"))),
                "FamilyAnnualAmount":changeNone(x.get("BenefitPeriodFamily")),
                "FamilyLifetimeAmount":changeNone(x.get("LifetimeFamily"))
            })
            
            temp.update({"Maximum":a})
            
        elif(x.get("Type")=="Maximum Used to Date"):
            a=temp.get("Maximum")
            if(not a): a={}
            a.update({
                "IndividualRemainingAnnualAmount":changeNone(x.get("BenefitPeriodIndividual")),
                "IndividualRemainingLifetimeAmount":changeNone(changeNone(x.get("LifetimeIndividual"))),
                "FamilyRemainingAnnualAmount":changeNone(x.get("BenefitPeriodFamily")),
                "FamilyRemainingLifetimeAmount":changeNone(x.get("LifetimeFamily"))
            })
            temp.update({"Maximum":a})
        elif(x.get("Type")=="Plan Deductible"):
            a=temp.get("Deductible")
            if(not a): a={}
            a.update({
                "IndividualAnnualAmount":changeNone(x.get("BenefitPeriodIndividual")),
                "IndividualLifetimeAmount":changeNone(changeNone(x.get("LifetimeIndividual"))),
                "FamilyAnnualAmount":changeNone(x.get("BenefitPeriodFamily")),
                "FamilyLifetimeAmount":changeNone(x.get("LifetimeFamily"))
            })
            temp.update({"Deductible":a})
            
        elif(x.get("Type")=="Deductible Satisfied to Date"):
            a=temp.get("Deductible")
            if(not a): a={}
            a.update({
                "IndividualRemainingAnnualAmount":changeNone(x.get("BenefitPeriodIndividual")),
                "IndividualRemainingLifetimeAmount":changeNone(changeNone(x.get("LifetimeIndividual"))),
                "FamilyRemainingAnnualAmount":changeNone(x.get("BenefitPeriodFamily")),
                "FamilyRemainingLifetimeAmount":changeNone(x.get("LifetimeFamily"))
            })
            temp.update({"Deductible":a})

    for x in data.get("EligibilityMaximums")[1].get("Orthodontics"):
        if(x.get("Type")=="Plan Maximum"):
            a=temp.get("Maximum")
            if(not a): a={}
            a.update({
                "IndividualOrthodonticsAnnualAmount":changeNone(x.get("BenefitPeriodIndividual")),
                "IndividualOrthodonticsLifetimeAmount":changeNone(changeNone(x.get("LifetimeIndividual"))),
                "FamilyOrthodonticsAnnualAmount":changeNone(x.get("BenefitPeriodFamily")),
                "FamilyOrthodonticsLifetimeAmount":changeNone(x.get("LifetimeFamily"))
            })
            temp.update({"Maximum":a})
            
        elif(x.get("Type")=="Maximum Used to Date"):
            a=temp.get("Maximum")
            if(not a): a={}
            a.update({
                "IndividualOrthodonticsRemainingAnnualAmount":changeNone(x.get("BenefitPeriodIndividual")),
                "IndividualOrthodonticsRemainingLifetimeAmount":changeNone(changeNone(x.get("LifetimeIndividual"))),
                "FamilyOrthodonticsRemainingAnnualAmount":changeNone(x.get("BenefitPeriodFamily")),
                "FamilyOrthodonticsRemainingLifetimeAmount":changeNone(x.get("LifetimeFamily"))
            })
            temp.update({"Maximum":a})
            print(a)
        elif(x.get("Type")=="Plan Deductible"):
            a=temp.get("Deductible")
            if(not a): a={}
            a.update({
                "IndividualOrthodonticsAnnualAmount":changeNone(x.get("BenefitPeriodIndividual")),
                "IndividualOrthodonticsLifetimeAmount":changeNone(changeNone(x.get("LifetimeIndividual"))),
                "FamilyOrthodonticsAnnualAmount":changeNone(x.get("BenefitPeriodFamily")),
                "FamilyOrthodonticsLifetimeAmount":changeNone(x.get("LifetimeFamily"))
            })
            temp.update({"Deductible":a})
            
        elif(x.get("Type")=="Deductible Satisfied to Date"):
            a=temp.get("Deductible")
            if(not a): a={}
            a.update({
                "IndividualOrthodonticsRemainingAnnualAmount":changeNone(x.get("BenefitPeriodIndividual")),
                "IndividualOrthodonticsRemainingLifetimeAmount":changeNone(changeNone(x.get("LifetimeIndividual"))),
                "FamilyOrthodonticsRemainingAnnualAmount":changeNone(x.get("BenefitPeriodFamily")),
                "FamilyOrthodonticsRemainingLifetimeAmount":changeNone(x.get("LifetimeFamily"))
            })
            temp.update({"Deductible":a})
            
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    temp1=[[], []]
    for x in temp:
        if(x=="Maximum"): 
            type="Maximums"
            count=0
            
        elif(x=="Deductible"): 
            type="Deductibles"
            count=1
        
        temp1[count].append({
            "Type": f"Annual {type}",
            "Network": "",
            "Amount": changeNone(temp.get(x).get("IndividualAnnualAmount")),
            "Remaining": changeNone(temp.get(x).get("IndividualRemainingAnnualAmount")),
            "ServiceCategory": "BasicPlanInfo",
            "Family_Individual": "Individual"
        })
        temp1[count].append({
            "Type": f"Annual {type}",
            "Network": "",
            "Amount": changeNone(temp.get(x).get("FamilyAnnualAmount")),
            "Remaining": changeNone(temp.get(x).get("FamilyRemainingAnnualAmount")),
            "ServiceCategory": "BasicPlanInfo",
            "Family_Individual": "Family"
        })
        temp1[count].append({
            "Type": f"Lifetime {type}",
            "Network": "",
            "Amount": changeNone(temp.get(x).get("IndividualLifetimeAmount")),
            "Remaining": changeNone(temp.get(x).get("IndividualRemainingLifetimeAmount")),
            "ServiceCategory": "BasicPlanInfo",
            "Family_Individual": "Individual"
        })
        temp1[count].append({
            "Type": f"Lifetime {type}",
            "Network": "",
            "Amount": changeNone(temp.get(x).get("FamilyLifetimeAmount")),
            "Remaining": changeNone(temp.get(x).get("FamilyRemainingLifetimeAmount")),
            "ServiceCategory": "BasicPlanInfo",
            "Family_Individual": "Family"
        })

        # temp1[count].append({
        #     "Type": f"Annual {type}",
        #     "Network": "",
        #     "Amount": changeNone(temp.get(x).get("IndividualOrthodonticsAnnualAmount")),
        #     "Remaining": changeNone(temp.get(x).get("IndividualOrthodonticsRemainingAnnualAmount")),
        #     "ServiceCategory": "Orthodontics",
        #     "Family_Individual": "Individual"
        # })
        # temp1[count].append({
        #     "Type": f"Annual {type}",
        #     "Network": "",
        #     "Amount": changeNone(temp.get(x).get("FamilyOrthodonticsAnnualAmount")),
        #     "Remaining": changeNone(temp.get(x).get("FamilyOrthodonticsRemainingAnnualAmount")),
        #     "ServiceCategory": "Orthodontics",
        #     "Family_Individual": "Family"
        # })
        temp1[count].append({
            "Type": f"Lifetime {type}",
            "Network": "",
            "Amount": changeNone(temp.get(x).get("IndividualOrthodonticsLifetimeAmount")),
            "Remaining": changeNone(temp.get(x).get("IndividualOrthodonticsRemainingLifetimeAmount")),
            "ServiceCategory": "Orthodontics",
            "Family_Individual": "Individual"
        })
        temp1[count].append({
                "Type": f"Lifetime {type}",
                "Network": "",
                "Amount": changeNone(temp.get(x).get("FamilyOrthodonticsLifetimeAmount")),
                "Remaining": changeNone(temp.get(x).get("FamilyOrthodonticsRemainingLifetimeAmount")),
                "ServiceCategory": "Orthodontics",
                "Family_Individual": "Family"
            })

    EligibilityMaximums, EligibilityDeductiblesProcCode=temp1[0], temp1[1]
    EligibilityBenefits=[]
    for x in data.get('Eligibilitylimitaiton'):
        if(x.get("Notes")): continue
        limitation=x.get("Frequency/AgeLimitlastDateOfService")
        LastDateOfService=""
        try: 
            if(x.get("Frequency/AgeLimitlastDateOfService").split(' ')[-1][0].isnumeric()):
                if("/" in x.get("Frequency/AgeLimitlastDateOfService").split(' ')[-1]):
                    LastDateOfService=x.get("Frequency/AgeLimitlastDateOfService").split(' ')[-1]
                limitation=limitation[:limitation.rfind(LastDateOfService)].strip()
        except: pass
        temp={
                "ProcedureCode": "",
                "ProcedureCodeDescription": "",
                "NetworkFee": "",
                "PlanBenefit": "",
                "PatientObligation": "",
                "Category":x.get("ProcedureDescription"),
                "limitation":limitation,
                "LastDateOfService":LastDateOfService,
                "BenefitLevel":x.get("BenefitLevel"),
                "Deductible":x.get("Deductible")
            }
        EligibilityBenefits.append(temp)
    for x in data.get('EligibilityBenefits'):
        if(x.get("0")!="Procedure Code*" and x.get("0")!="" and x.get("1")!="" and len(x.get("3"))>0):
            temp={
                "ProcedureCode": x.get("0"),
                "ProcedureCodeDescription": x.get("1"),
                "NetworkFee": x.get("2"),
                "PlanBenefit": x.get("3"),
                "PatientObligation": x.get("4"),
                "Category":"",
                "limitation":"",
                "LastDateOfService":"",
                "BenefitLevel":"",
                "Deductible":""
            }
            EligibilityBenefits.append(temp)
    EligibilityServiceTreatmentHistory=[]
    for x in EligibilityBenefits:
        if(x.get("LastDateOfService")!=""):
            EligibilityServiceTreatmentHistory.append({
                "Category":x.get("Category"),
                "limitation":x.get("limitation"),
                "LastDateOfService":x.get("LastDateOfService"),
                "BenefitLevel":x.get("BenefitLevel"),
                "Deductible":x.get("Deductible")
            })
    for x in EligibilityMaximums:
        if(x.get("Type")=="Annual Maximums" and x.get("Family_Individual")=="Individual" and x.get("ServiceCategory")=="BasicPlanInfo"):
            IndividualAnnualMaximumBenefits=x.get("Amount")
            IndividualAnnualRemainingBenefit=x.get("Remaining")
        elif(x.get("Type")=="Annual Maximums" and x.get("Family_Individual")=="Family" and x.get("ServiceCategory")=="BasicPlanInfo"):
            FamilyAnnualMaximumBenefits=x.get("Amount")
            FamilyAnnualRemainingBenefit=x.get("Remaining")
        elif(x.get("Type")=="Lifetime Maximums" and x.get("Family_Individual")=="Individual" and x.get("ServiceCategory")=="BasicPlanInfo"):
            IndividualLifetimeMaximumBenefits=x.get("Amount")
            IndividualLifetimeRemainingBenefit=x.get("Remaining")
        elif(x.get("Type")=="Lifetime Maximums" and x.get("Family_Individual")=="Family" and x.get("ServiceCategory")=="BasicPlanInfo"):
            FamilyLifetimeMaximumBenefits=x.get("Amount")
            FamilyLifetimeRemainingBenefit=x.get("Remaining")
        elif(x.get("Type")=="Lifetime Maximums" and x.get("Family_Individual")=="Individual" and x.get("ServiceCategory")=="Orthodontics"):
            OrthodonticMaximumBenefit=x.get("Amount")
            OrthodonticRemainingBenefit=x.get("Remaining")

    for x in EligibilityDeductiblesProcCode:
        if(x.get("Type")=="Annual Deductibles" and x.get("Family_Individual")=="Individual" and x.get("ServiceCategory")=="BasicPlanInfo"):
            IndividualAnnualDeductible=x.get("Amount")
            IndividualAnnualDeductibleRemaining=x.get("Remaining")
        elif(x.get("Type")=="Annual Deductibles" and x.get("Family_Individual")=="Family" and x.get("ServiceCategory")=="BasicPlanInfo"):
            FamilyAnnualDeductible=x.get("Amount")
            FamilyAnnualDeductibleRemaining=x.get("Remaining")
        elif(x.get("Type")=="Lifetime Deductibles" and x.get("Family_Individual")=="Individual" and x.get("ServiceCategory")=="BasicPlanInfo"):
            IndividualLifetimeDeductible=x.get("Amount")
            IndividualLifetimeRemainingDeductible=x.get("Remaining")
        elif(x.get("Type")=="Lifetime Deductibles" and x.get("Family_Individual")=="Family" and x.get("ServiceCategory")=="BasicPlanInfo"):
            FamilyLifetimeDeductible=x.get("Amount")
            FamilyLifetimeRemainingDeductible=x.get("Remaining")
    templist=[]
    for x in data.get("EligibilityOtherProvisions"):
        tempdict={}
        for y in x:
            if(y=="Name"):
                tempdict.update({"Name":x.get(y).split("\u00a0")[0].replace(" SSN or ID#", "").replace("XXXXXXXXX\n", "")})
                tempdict.update({"DateOfBirth":x.get(y).split("\u00a0")[-1].replace(" SSN or ID#", "").replace("XXXXXXXXX\n", "")})
                # for z in x.get(y).split("\u00a0"):
                #     if(z!="Birth Date"):
                #         print(z.replace(" SSN or ID#", "").replace("XXXXXXXXX\n", ""))
            elif(y=="Address"):
                tempdict.update({"Address":x.get(y).replace("\u00a0", " ")})
            elif(y=="PatientInformation"):
                temp=x.get(y).split("\u00a0")[1]
                tempdict.update({"Relationship":temp[:temp.index("\n")]})
            elif(y=="EligibilityDates"):
                temp=x.get(y).split("\u00a0")[1]
                tempdict.update({"EffectiveDate":temp[:temp.index("\n")]})
                if(x.get(y).split('\n')[-1]=="Cancellation Date"):
                    tempdict.update({"EligibilityStatus":"Active"})
                else:
                    try:
                        canceldate=x.get(y).split("\n")[-1].split("\u00a0")[1]
                        if(datetime.datetime.now().date()>datetime.datetime.strptime(canceldate, "%m/%d/%Y").date()):
                            tempdict.update({"EligibilityStatus":""})
                        else:
                            tempdict.update({"EligibilityStatus":"Active"})
                    except:
                        tempdict.update({"EligibilityStatus":"Active"})
        templist.append(tempdict)
    

    for x in templist:
        if(x.get("Name")==EligibilityPatientVerification.get("FamilyMemberName")):
            
            EligibilityPatientVerification.update({"FamilyMemberName":x.get("Name")})
            EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":x.get("DateOfBirth")})
            EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":x.get("EffectiveDate")})
            EligibilityPatientVerification.update({"ClaimsAddress":x.get("Address")})
            EligibilityPatientVerification.update({"EligibilityStatus":x.get("EligibilityStatus")})
        if(x.get("Relationship")=="Self"):
            EligibilityPatientVerification.update({"SubscriberName":x.get("Name")})
            EligibilityPatientVerification.update({"SubscriberDateOfBirth":x.get("DateOfBirth")})
            EligibilityPatientVerification.update({"SubscriberEffectiveDate":x.get("EffectiveDate")})
            EligibilityPatientVerification.update({"SubscriberEligibilityStatus":x.get("EligibilityStatus")})
            # EligibilityPatientVerification.update({"FamilyMemberName":x.get("Name")})
            # EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":x.get("DateOfBirth")})
            # EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":x.get("EffectiveDate")})
            # EligibilityPatientVerification.update({"ClaimsAddress":x.get("Address")})
        elif(x.get("Relationship")=="Subscriber"):
            EligibilityPatientVerification.update({"SubscriberName":x.get("Name")})
            EligibilityPatientVerification.update({"SubscriberDateOfBirth":x.get("DateOfBirth")})
            EligibilityPatientVerification.update({"SubscriberEffectiveDate":x.get("EffectiveDate")})
            EligibilityPatientVerification.update({"SubscriberEligibilityStatus":x.get("EligibilityStatus")})
        
    
    EligibilityPatientVerification.update({"FamilyAnnualDeductible":changeNone(FamilyAnnualDeductible)})
    EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":changeNone(calculate_difference(FamilyAnnualDeductible, FamilyAnnualDeductibleRemaining))})
    EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":changeNone(FamilyAnnualDeductibleRemaining)})

    EligibilityPatientVerification.update({"FamilyLifetimeDeductible":changeNone(FamilyLifetimeDeductible)})
    EligibilityPatientVerification.update({"FamilyLifetimeDeductibleMet":changeNone(calculate_difference(FamilyLifetimeDeductible, FamilyLifetimeRemainingDeductible))})
    EligibilityPatientVerification.update({"FamilyLifetimeRemainingDeductible":changeNone(FamilyLifetimeRemainingDeductible)})

    EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":changeNone(FamilyLifetimeMaximumBenefits)})
    EligibilityPatientVerification.update({"FamilyLifetimeBenefitsUsedtoDate":changeNone(calculate_difference(FamilyLifetimeMaximumBenefits, FamilyLifetimeRemainingBenefit))})
    EligibilityPatientVerification.update({"FamilyLifetimeRemainingBenefit":changeNone(FamilyLifetimeRemainingBenefit)})

    EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":changeNone(FamilyAnnualMaximumBenefits)})
    EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":changeNone(calculate_difference(FamilyAnnualMaximumBenefits, FamilyAnnualRemainingBenefit))})
    EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":changeNone(FamilyAnnualRemainingBenefit)})

    EligibilityPatientVerification.update({"IndividualAnnualDeductible":changeNone(IndividualAnnualDeductible)})
    EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":changeNone(calculate_difference(IndividualAnnualDeductible, IndividualAnnualDeductibleRemaining))})
    EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":changeNone(IndividualAnnualDeductibleRemaining)})

    EligibilityPatientVerification.update({"IndividualLifetimeDeductible":changeNone(IndividualLifetimeDeductible)})
    EligibilityPatientVerification.update({"IndividualLifetimeDeductibleMet":changeNone(calculate_difference(IndividualLifetimeDeductible, IndividualLifetimeRemainingDeductible))})
    EligibilityPatientVerification.update({"IndividualLifetimeRemainingDeductible":changeNone(IndividualLifetimeRemainingDeductible)})

    EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":changeNone(IndividualLifetimeMaximumBenefits)})
    EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":changeNone(calculate_difference(IndividualLifetimeMaximumBenefits, IndividualLifetimeRemainingBenefit))})
    EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":changeNone(IndividualLifetimeRemainingBenefit)})

    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":changeNone(IndividualAnnualMaximumBenefits)})
    EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":changeNone(calculate_difference(IndividualAnnualMaximumBenefits, IndividualAnnualRemainingBenefit))})
    EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":changeNone(IndividualAnnualRemainingBenefit)})

    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":changeNone(OrthodonticMaximumBenefit)})
    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":changeNone(calculate_difference(OrthodonticMaximumBenefit, OrthodonticRemainingBenefit))})
    EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":changeNone(OrthodonticRemainingBenefit)})
    TreatmentHistorySummary=[]
    for x in EligibilityServiceTreatmentHistory:
        TreatmentHistorySummary.append({
            "ProcedureCode":x.get("Category"),
            "ProcedureCodeDescription":"",
            "LimitationText":x.get("limitation"),
            "LimitationAlsoAppliesTo":"",
            "History":x.get("LastDateOfService")
        })

    
    output={}
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
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
    
    return output


# data=json.load(open(r"C:\Users\saran\Downloads\output5000 (1).json", 'r'))
# output=main(data)
# with open("Metliferes.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)