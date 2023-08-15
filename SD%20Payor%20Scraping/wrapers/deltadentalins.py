import json
import re
import pandas as pd
from datetime import datetime
import sys
import sys
import os
from mapPDF import mapEligibilityPatientVerification
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from local import kickoff as kick


def AlternativeBenefitProvision(Benefits):
    for obj in Benefits:
        if (obj['procedureCode'] =="D2391" or obj['procedureCode'] =="D2392" or obj['procedureCode'] =="D2393" or obj['procedureCode'] =="D2394"):
            return "No"
    return "Yes"    
            
        
    
    


def TreatmentHistorySummary(treatmenthistory):
    df=pd.DataFrame(treatmenthistory)
    df3 = df.groupby(['ProcedureCode', 'ServiceDate'])['ToothCode'].apply(','.join).reset_index()
    def sort_date(servicedate):
        df1 = pd.DataFrame()
        count= 0
        for each in servicedate:
            each1sort = each.split(',')
            each1sort.sort(key=lambda date: datetime.strptime(date.strip(), "%m/%d/%Y"), reverse=True)
            new_row = {'ServiceDateSorted':','.join(each1sort)} 
            df2['ServiceDateSorted'] = pd.DataFrame(new_row, index=[0])
            df1 = pd.concat([df1,df2] , axis=0, ignore_index=True)
            count = count+1
        return df1

    summary_df = pd.DataFrame(columns=['ProcedureCode','ProcedureCodeDescription','LimitationText','LimitationAlsoAppliesTo','History'])
    df2 = pd.DataFrame()
    df2=sort_date(df.ServiceDate)
    df['ServiceDateSorted'] = df2
    unique_proc_code = df['ProcedureCode'].unique()
            
    for each_proc_code in unique_proc_code:
        df = df.drop_duplicates(subset=["ProcedureCode", "ServiceDate"], keep='first')
        each_loc = df[df.ProcedureCode == each_proc_code][['ServiceDateSorted','ToothCode', 'ServiceDate']].iloc
        data= {'ProcedureCode':each_proc_code, 'ProcedureCodeDescription':df[df.ProcedureCode == each_proc_code]['ProcedureCodeDescription'].iloc[0],
            'LimitationText':df[df.ProcedureCode == each_proc_code]['LimitationText'].iloc[0],
            'LimitationAlsoAppliesTo': df[df.ProcedureCode == each_proc_code]['LimitationAlsoAppliesTo'].iloc[0]}

        historytext = ''
        for each in each_loc:
            for each_date in each.ServiceDateSorted.split(','):
                toothcode = ''
                #historytext = (historytext + each_date + toothcode.strip())
                toothcode = ''.join(df3[(df3['ProcedureCode'] == each_proc_code) & (df3['ServiceDate'] == each.ServiceDate)]['ToothCode'])
                if len(each.ToothCode)!=0: 
                    historytext = (historytext + each_date + ':'+ f"({toothcode})")
                else:
                    historytext = (historytext + each_date) 
                
        data['History'] = historytext.strip(",")
        df_2 = pd.DataFrame(data,index=[1])
        summary_df = pd.concat([summary_df,df_2])           
        
        # reset index
        summary_df.reset_index(drop=True, inplace=True)
        
    return summary_df.to_dict("records")
def addressmaker(address):
  address = address.split("\n")
  address.remove("Claim mailing address")
  for ads in address:
    if ads.startswith("Claim payer ID"):
      ClaimPayerID=ads.split(":")[-1].strip()
     
      address.remove(ads)
  ClaimMailingAddress=" ".join(address)
 
  return ClaimMailingAddress,ClaimPayerID

def OONBenefits(benefits):
    for obj in benefits:
        if obj["NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel"]!="":
            return "Yes"
        else:
            return "No"


def FamilyCalenderDeductible(Deductibles):
    if len(Deductibles)!=0:
        for obj in Deductibles:
            if obj['Type'] =="Calendar Family Deductible" or obj['Type']=="Contract Family Deductible" or obj['Type']=="Carryover Family Deductible":
                if "Delta Dental DPO" in obj['Network'] or  "Delta Dental PPO" in  obj['Network'] or "In-Network" in  obj['Network']:
                    return float(fixna(obj['Amount']).replace("$",""))
              
    else:
        return None        
def FamilyDeductibleMet(Deductibles):
    if len(Deductibles)!=0:
        for obj in Deductibles:
            if obj['Type'] =="Calendar Family Deductible" or obj['Type']=="Contract Family Deductible" or obj['Type']=="Carryover Family Deductible":
                if "Delta Dental DPO" in obj['Network'] or  "Delta Dental PPO" in  obj['Network'] or "In-Network" in  obj['Network']:
                    return   float(fixna(obj['Amount']).replace("$","")) - float(fixna(obj['Remaining']).replace("$",""))
    else:
        return None
def IndividualAnnualDeductible(Deductibles):
    count=0
    for obj in Deductibles:
        if obj['Type'] =='Calendar Individual Deductible':
            count+=1
    if count ==2:
        for obj in Deductibles:
            if obj.get("Type") =="Calendar Individual Deductible":
                if "Delta Dental DPO" in obj['Network'] or  "Delta Dental PPO" in  obj['Network']:
                    return float(fixna(obj['Amount']).replace("$",""))
                                                                
    for obj in Deductibles:
        if obj['Type'] =="Calendar Individual Deductible" or obj['Type']=="Contract Individual Deductible" or obj['Type']=="Carryover Individual Deductible":
            return  float(fixna(obj['Amount']).replace("$",""))
        
def IndividualAnnualDeductibleApplies(Deductibles):
    count=0
    for obj in Deductibles:
        if obj['Type'] =='Calendar Individual Deductible':
            count+=1
    if count ==2:
        for obj in Deductibles:
            if obj.get("Type") =="Calendar Individual Deductible":
                if "Delta Dental DPO" in obj['Network'] or  "Delta Dental PPO" in  obj['Network']:
                    return obj['Amount']
                                                                
    for obj in Deductibles:
        if obj['Type'] =="Calendar Individual Deductible" or obj['Type']=="Contract Individual Deductible" or obj['Type']=="Carryover Individual Deductible":
            return  obj['Amount']
            
def IndividualDeductibleMet(Deductibles):
    count=0
    for obj in Deductibles:
        if obj['Type'] =='Calendar Individual Deductible':
            count+=1
    if count ==2:
        for obj in Deductibles:
            if "Delta Dental DPO" in obj['Network'] or  "Delta Dental PPO" in  obj['Network']:
                return   float(fixna(obj['Amount']).replace("$","")) - float(fixna(obj['Remaining']).replace("$",""))
    for obj in Deductibles:
        if obj['Type'] =="Calendar Individual Deductible" or obj['Type']=="Contract Individual Deductible" or obj['Type']=="Carryover Individual Deductible":
                
            return   float(fixna(obj['Amount']).replace("$","")) - float(fixna(obj['Remaining']).replace("$",""))
        
def AdultOrthodonticCovered(agelimitation):
    
    for obj in agelimitation:
        if obj['AgeLimit'] =='No Age Limit':
            return "Yes"
        if int(''.join(filter(str.isdigit, obj['AgeLimit'])))   <18:
            return "No"
        else:
            "Yes"
def LifetimeMaximumBenefits(maximums):
    for obj in maximums:
        if obj['Type'] =='Lifetime Individual Maximum' and "PPO" in obj['Network']:
            return  float(fixna(obj['Amount']).replace("$",""))
        
def BenefitsUsedtoDate(maximums):
     for obj in maximums:
        if obj['Type'] =='Lifetime Individual Maximum' and "PPO" in obj['Network']:
            return   float(fixna(obj['Amount']).replace("$","")) -  float(fixna(obj['Remaining']).replace("$",""))
        
def RemainingBenefitAvailable(maximums):
    for obj in maximums:
        if obj['Type'] =='Lifetime Individual Maximum' and "PPO" in obj['Network']:
            return  float(fixna(obj['Remaining']).replace("$",""))
        
def  cob(EligibilityOtherProvisions):
    data=EligibilityOtherProvisions.get('CobRule')
    if data:
        CoordinationofBenefitsType =""
        
        if ":" in  data:
            CoordinationofBenefitsType =data.split(":")[0]
        if "-" in data:
            CoordinationofBenefitsType =data.split("-")[0]
            
        CoordinationofBenefits    ="Yes" 
        return CoordinationofBenefitsType,CoordinationofBenefits
    else:
        CoordinationofBenefitsType ="No"
        CoordinationofBenefits     =""
        return CoordinationofBenefitsType,CoordinationofBenefits
               
        
def AgelimitShow(age_obj):
    if len(age_obj)!=0:
        string=""
        for obj in age_obj:
            memeber=obj['FamilyMember']
            limit   =obj['AgeLimit']
            string+=f"{memeber} : {limit}\n"
        return string.strip("\n")  
    else:
        return None
        
        
    
            
     

def WaitingPeriods(waiting_periods):
    
    count = 0
    for i in waiting_periods:
        if all(value == "" for value in i.values()):
            count += 1
            
    if len(waiting_periods) == count:
        return "No"
    else:
        return "Yes"
def Orthodontic(maximums):
    if  len(maximums)!=0:
        for obj in maximums:
            if obj['Type'] =='Lifetime Individual Maximum':
                if "Orthodontics".lower() in  obj['ProgramMaximum_AppliesToTheFollowingServices_'].lower():
                    OrthodonticIndividualLifetimeBenefit ="Yes"
                    amount=float(fixna(obj['Amount']).replace("$",""))
                    remaining=float(fixna(obj['Remaining']).replace("$",""))
                    return OrthodonticIndividualLifetimeBenefit , amount , remaining
            else:
                return None, None, None   
    else:
        return None, None, None 
                     

def DeductibleApplicable(Benefits,IndividualAnnualDeductible):
    if len(Benefits)!=0:
        for obj in Benefits:
            # if "$" in str(IndividualAnnualDeductible):
            #     obj['DeductibleApplicable'] ="Yes"
            # else:
            #     obj['DeductibleApplicable'] ="No"
        
            if "1" in obj['DeltaDentalPPOTMDentistContractBenefitLevel'].split("%")[1]:
                print(obj['DeltaDentalPPOTMDentistContractBenefitLevel'].split("%")[1])
                print(obj['DeltaDentalPPOTMDentistContractBenefitLevel'])
            
                obj['DeductibleApplicable'] ="No"
            else:
                obj['DeductibleApplicable'] ="Yes"
                
            for i in obj:
                
                if "%" in obj[i]:
                
                    obj[i] =obj[i].split("%")[0]+"%"
                
        return Benefits
    else:
        return  None       
            
def AnnualMaximumBenefits(maximums):
    if len(maximums)!=0:
        
        for obj in maximums:
            if (obj['Type'] =='Calendar Individual Maximum' or obj['Type']=="Contract Individual Maximum" or obj['Type']=="Carryover Individual Maximum") and ("PPO" in obj['Network'] or "DPO" in obj['Network'] or "In-Network" in obj['Network']) and "Restorative" in obj['ProgramMaximum_AppliesToTheFollowingServices_']:
                return  float(fixna(obj['Amount']).replace("$",""))
    else:
        return None    
def AnnualBenefitsUsedtoDate(maximums):
     if len(maximums)!=0:
        for obj in maximums:
            if (obj['Type'] =='Calendar Individual Maximum' or obj['Type']=="Contract Individual Maximum" or obj['Type']=="Carryover Individual Maximum") and ("PPO" in obj['Network'] or "DPO" in obj['Network'] or "In-Network" in obj['Network']) and "Restorative" in obj['ProgramMaximum_AppliesToTheFollowingServices_']:
                return   float(fixna(obj['Amount']).replace("$","")) -  float(fixna(obj['Remaining']).replace("$",""))
     else:
         return None       
        
def AnnualRemainingBenefitAvailable(maximums):
    if len(maximums) != 0:
        for obj in maximums:
            if (obj['Type'] =='Calendar Individual Maximum' or obj['Type']=="Contract Individual Maximum" or obj['Type']=="Carryover Individual Maximum") and ("PPO" in obj['Network'] or "DPO" in obj['Network'] or "In-Network" in obj['Network']) and "Restorative" in obj['ProgramMaximum_AppliesToTheFollowingServices_']:
                return  float(fixna(obj['Remaining']).replace("$",""))  
    return None     
            
def limitationsSoter(benefits,proccodes):
    
    CodesRequireScraping=[]
    for obj in benefits:
        if obj['procedureCode'] in proccodes:
            if "[Limitations Apply]" in obj['limitation']:
                CodesRequireScraping.append(obj['procedureCode'] )
    return CodesRequireScraping            
                
def limitationsUpdater(limitations,benefits):
    result = {}
    for d in limitations:
        result.update(d)
    for obj in limitations:
        
        obj=list(obj.keys())[0]
        for j in benefits:
            if j['procedureCode'].lower() ==obj.lower():
                finaltext =""
                for k in result[obj]:
                    limitationstxt = k['Limitation']
                    Age             = k['Age']
                    tooth_code      = k['ToothCode']
                    if len(tooth_code)==0:
                        tooth_code="N/A "
                    if len(Age)==0:
                        Age  ="N/A"
                    finaltext+=f"Limitations: {limitationstxt},  Age limitation: {Age}, Tooth_code: {tooth_code}\n"
                finaltext=finaltext.strip("\n").strip()        
                j['limitation']=j['limitation'].replace("[Limitations Apply]",f" {finaltext}")    
    return  benefits          
def limitationsUpdaterTreatmentHistory(limitations,benefits):
    result = {}
    for d in limitations:
        result.update(d)
    for obj in limitations:
        
        obj=list(obj.keys())[0]
        for j in benefits:
          
            if j['ProcedureCode'].lower() ==obj.lower():
                finaltext =""
                for k in result[obj]:
                    limitationstxt = k['Limitation']
                    Age             = k['Age']
                    tooth_code      = k['ToothCode']
                    if len(tooth_code)==0:
                        tooth_code="N/A "
                    if len(Age)==0:
                        Age  ="N/A "                        
                    finaltext+=f"Limitations: {limitationstxt},  Age limitation: {Age}, Tooth_code: {tooth_code}\n"
                finaltext=finaltext.strip("\n").strip()     
                j['LimitationText']=j['LimitationText'].replace("[Limitations Apply]",f" {finaltext}")    
    return  benefits                          
def getrequestprocodes(request):
    codes=request['InputParameters'].get('ProcCodes')
    if codes!=None:
        return codes                                         
    else:
        return []                  
def calculate_difference(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=str(a).replace(",", "").replace("N/A", "0").replace("$", "")
    b=str(b).replace(",", "").replace("N/A", "0").replace("$", "")
    return float(a)-float(b)
    
def fixna(val):
    if(val in [None, '', "N/A", "0"]):
        return "0.0"
    else: return val
def changeNone(val):
    if(val==None):
        return ""
    else:
        return val
def main(data,request,browser):
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    if data.get('EligibilityPatientVerification'):
        EligibilityPatientVerificationtemp=data.get("EligibilityPatientVerification")
        if EligibilityPatientVerificationtemp:
            EligibilityPatientVerification=mapEligibilityPatientVerification()
            
            EligibilityPatientVerification.update(EligibilityPatientVerificationtemp[0])
            

    EligibilityMaximums =[]        
    if data.get("EligibilityMaximums"):
        EligibilityMaximums                        = data["EligibilityMaximums"]
        
    EligibilityDeductiblesProcCode=[]
    if data.get("EligibilityDeductiblesProcCode"):
        EligibilityDeductiblesProcCode             = data["EligibilityDeductiblesProcCode"]
        
    EligibilityServiceTreatmentHistory=[]
    if data.get("EligibilityServiceTreatmentHistory"):
        EligibilityServiceTreatmentHistory         = data["EligibilityServiceTreatmentHistory"]
        
    EligibilityBenefits=[]   
    EligibilityBenefit1st=[]
    EligibilityBenefit2nd=[]
    if data.get('EligibilityBenefits'):
        repeatCodesChecker = ""
        for limCor in data.get("EligibilityBenefits"):
            if str(limCor.get("procedureCode")) in repeatCodesChecker:
                EligibilityBenefit2nd.append(limCor)
                continue
            EligibilityBenefit1st.append(limCor)
            repeatCodesChecker =repeatCodesChecker + str(limCor.get("procedureCode"))

        for limitationObj1 in EligibilityBenefit1st:
            for limitationObj2 in EligibilityBenefit2nd:
                if limitationObj1["procedureCode"] == limitationObj2["procedureCode"] and limitationObj2.get("DeltaDentalPPOTMDentistAgelimit") != "16 years and older":
                    limitationObj1["DeltaDentalPPOTMDentistAgelimit"] = limitationObj2["DeltaDentalPPOTMDentistAgelimit"]
                    limitationObj1["DeltaDentalPremierDentistAgelimit"] = limitationObj2["DeltaDentalPremierDentistAgelimit"]
                    limitationObj1["NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"] = limitationObj2["NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]
                    break
        EligibilityBenefits                        = EligibilityBenefit1st
        data["EligibilityBenefits"] = EligibilityBenefits
    # EligibilityBenefits=[]   
    # if data.get('EligibilityBenefits'):
    #     EligibilityBenefits                        = data["EligibilityBenefits"]

    EligibilityAgeLimitation =[]
    if data.get("EligibilityAgeLimitation"):
        EligibilityAgeLimitation                   = data["EligibilityAgeLimitation"]
        
    EligibilityOtherProvisions={}
    if data.get("EligibilityOtherProvisions"):
        EligibilityOtherProvisions                 = data["EligibilityOtherProvisions"][0]
        
    EligibilityPayorAddressDetails =None    
    if EligibilityPatientVerification:
        if len(EligibilityPatientVerification)!=0:
            EligibilityPayorAddressDetails             = data["EligibilityPatientVerification"][0].get('Address')
    EligibilityFamilyMembersWaitingPeriods=None
    if data.get("EligibilityFamilyMembersWaitingPeriods"):
        EligibilityFamilyMembersWaitingPeriods     = data["EligibilityFamilyMembersWaitingPeriods"]
    
    ClaimMailingAddress= None
    ClaimPayerID       = None
    if EligibilityPayorAddressDetails!=None:
        ClaimMailingAddress,ClaimPayerID                                  = addressmaker(EligibilityPayorAddressDetails)
    
    OONBenefits_=None        
    if len(EligibilityBenefits)!=0:
        OONBenefits_                                                      = OONBenefits(EligibilityBenefits)
        
    IndividualAnnualDeductible_=None
    IndividualDeductibleMet_=None
    IndividualAnnualDeductible_1 = ""
    if len(EligibilityDeductiblesProcCode)!=0:
        IndividualAnnualDeductible_                                       = changeNone(IndividualAnnualDeductible(EligibilityDeductiblesProcCode))
        IndividualAnnualDeductible_1                                      = changeNone(IndividualAnnualDeductibleApplies(EligibilityDeductiblesProcCode))
    
        IndividualDeductibleMet_                                          = changeNone(IndividualDeductibleMet(EligibilityDeductiblesProcCode))
    AdultOrthodonticCovered_=None    
    if len(EligibilityAgeLimitation)!=0 and len(EligibilityOtherProvisions)!=0:
        AdultOrthodonticCovered_                                          = "N/A" if EligibilityOtherProvisions["OrthodonticAgeLimit"]=="N/A" else  AdultOrthodonticCovered(EligibilityAgeLimitation)
    LifetimeMaximumBenefits_=None    
    BenefitsUsedtoDate_=None
    RemainingBenefitAvailable_=None
    if len(EligibilityMaximums)!=0:
        LifetimeMaximumBenefits_                                          =  changeNone(LifetimeMaximumBenefits(EligibilityMaximums))
    
        BenefitsUsedtoDate_                                               =  changeNone(BenefitsUsedtoDate(EligibilityMaximums))
    
        RemainingBenefitAvailable_                                        = changeNone(RemainingBenefitAvailable(EligibilityMaximums))
    
    EligibilityPatientVerification['OrthodonticPayment']              = EligibilityOtherProvisions.get('OrthodonticPayment')

    CoordinationofBenefitsType,CoordinationofBenefits                 =     cob(EligibilityOtherProvisions)
    if EligibilityFamilyMembersWaitingPeriods!=None:
        EligibilityFamilyMembersWaitingPeriods_                           =       WaitingPeriods(EligibilityFamilyMembersWaitingPeriods)
    else:
        EligibilityFamilyMembersWaitingPeriods_=None    
    EligibilityPatientVerification['DependentChildCoveredAgeLimit']   =     EligibilityOtherProvisions.get('ChildCoveredToAge')
    EligibilityPatientVerification["DependentStudentAgeLimit"]        =     EligibilityOtherProvisions.get('StudentCoveredToAge')
    EligibilityPatientVerification["ClaimMailingAddress"]             =      ClaimMailingAddress
    
    EligibilityPatientVerification['ClaimPayerID']                    =      ClaimPayerID
    
    EligibilityPatientVerification['oonBenefits']                     =      OONBenefits_
    
    
    EligibilityPatientVerification['CoordinationofBenefits']          =      CoordinationofBenefits
    
    EligibilityPatientVerification['CoordinationofBenefitsType']      =      CoordinationofBenefitsType
    
    EligibilityPatientVerification['AdultOrthodonticCovered']         =      AdultOrthodonticCovered_
    
    
  #  EligibilityPatientVerification['BenefitsPaid']                    =      BenefitsPaid_
    EligibilityPatientVerification['FamilyMembersWaitingPeriods']     =      EligibilityFamilyMembersWaitingPeriods_
    
    
    OrthodonticLifetimeBenefit ,OrthodonticMaximumBenefit,OrthodonticRemainingBenefit =Orthodontic(EligibilityMaximums)
    EligibilityPatientVerification['OrthodonticLifetimeBenefit']     =       changeNone(OrthodonticLifetimeBenefit)
    EligibilityPatientVerification['OrthodonticMaximumBenefit']      =       changeNone(OrthodonticMaximumBenefit)
    EligibilityPatientVerification['OrthodonticLifetimeRemainingBenefit']    =       changeNone(OrthodonticRemainingBenefit)
    EligibilityPatientVerification['FamilyAnnualDeductible']       =       changeNone(FamilyCalenderDeductible(EligibilityDeductiblesProcCode))
    EligibilityPatientVerification['FamilyAnnualDeductibleMet']    =        changeNone(FamilyDeductibleMet(EligibilityDeductiblesProcCode))
    
    EligibilityPatientVerification['FamilyAnnualDeductibleRemaining']    =      calculate_difference(changeNone(FamilyCalenderDeductible(EligibilityDeductiblesProcCode)), changeNone(FamilyDeductibleMet(EligibilityDeductiblesProcCode)))

    EligibilityPatientVerification['FamilyLifetimeMaximumBenefits']    =      ""
    EligibilityPatientVerification['FamilyLifetimeBenefitsUsedtoDate']    =      ""
    EligibilityPatientVerification['FamilyLifetimeRemainingBenefit']    =      ""

    EligibilityPatientVerification['FamilyAnnualMaximumBenefits']    =      ""
    EligibilityPatientVerification['FamilyAnnualBenefitsUsedtoDate']    =      ""
    EligibilityPatientVerification['FamilyAnnualRemainingBenefit']    =      ""
    
    EligibilityPatientVerification['IndividualAnnualDeductible']      =      IndividualAnnualDeductible_
    EligibilityPatientVerification['IndividualAnnualDeductibleMet']         =      IndividualDeductibleMet_
    EligibilityPatientVerification['IndividualAnnualDeductibleRemaining']         =     calculate_difference(IndividualAnnualDeductible_,IndividualDeductibleMet_)

    EligibilityPatientVerification['IndividualLifetimeMaximumBenefits']         =      LifetimeMaximumBenefits_
    EligibilityPatientVerification['IndividualLifetimeBenefitsUsedtoDate']              =      BenefitsUsedtoDate_
    EligibilityPatientVerification['IndividualLifetimeRemainingBenefit']       =      RemainingBenefitAvailable_
    
    EligibilityPatientVerification['IndividualAnnualMaximumBenefits'] = changeNone(AnnualMaximumBenefits(EligibilityMaximums))
    EligibilityPatientVerification["IndividualAnnualBenefitsUsedtoDate"] = changeNone(AnnualBenefitsUsedtoDate(EligibilityMaximums))
    EligibilityPatientVerification["IndividualAnnualRemainingBenefit"] = changeNone(AnnualRemainingBenefitAvailable(EligibilityMaximums))
    

    EligibilityPatientVerification["SpecialistOfficeVisitCopay"] = ""
    EligibilityPatientVerification["IsReferralNeeded"] = ""
    EligibilityPatientVerification["PreCertRequired"] = ""
    EligibilityPatientVerification["TreatmentinProgressCoverage"] = ""
    EligibilityPatientVerification["PreauthorizationRequired"] = ""
    EligibilityPatientVerification["MedicallyNecessaryonly"] = ""
    EligibilityPatientVerification["AutomaticPayments"] = ""
    EligibilityPatientVerification["ContinuationClaimNeeded"] = ""
    # EligibilityPatientVerification["EnrolleeID"]=EligibilityPatientVerification["EnrolleeId"]
    # del EligibilityPatientVerification["EnrolleeId"]
    # EligibilityPatientVerification["FamilyMemberID"]=EligibilityPatientVerification["FamilyMemberId"]
    # del EligibilityPatientVerification["FamilyMemberId"]

    EligibilityPatientVerification["SubscriberName"]=EligibilityPatientVerification["EnrolleeName"]
    del EligibilityPatientVerification["EnrolleeName"]
    EligibilityPatientVerification["SubscriberDateOfBirth"]=EligibilityPatientVerification["DateOfBirth"]
    del EligibilityPatientVerification["DateOfBirth"]
    EligibilityPatientVerification["SubscriberId"]=EligibilityPatientVerification["EnrolleeId"]
    del EligibilityPatientVerification["EnrolleeId"]
    EligibilityPatientVerification["SubscriberEffectiveDate"]=EligibilityPatientVerification["EffectiveDate"]
    del EligibilityPatientVerification["EffectiveDate"]
    EligibilityPatientVerification["SubscriberEndDate"]=EligibilityPatientVerification["EndDate"]
    del EligibilityPatientVerification["EndDate"]
    EligibilityPatientVerification["SubscriberEligibilityStatus"]=EligibilityPatientVerification["EligibilityStatus"]
    EligibilityPatientVerification["EligibilityStatus"]=EligibilityPatientVerification["FamilyMemberEligibilityStatus"]
    del EligibilityPatientVerification["FamilyMemberEligibilityStatus"]
    EligibilityPatientVerification["FamilyMemberWaitingPeriod"]=EligibilityPatientVerification["FamilyMembersWaitingPeriods"]
    del EligibilityPatientVerification["FamilyMembersWaitingPeriods"]
    EligibilityPatientVerification["OrthodonticLifetimeBenefit"]=EligibilityPatientVerification["OrthodonticMaximumBenefit"]
    del EligibilityPatientVerification["OrthodonticMaximumBenefit"]

    EligibilityPatientVerification["GroupName"]=EligibilityPatientVerification["PlanName"]
    
    EligibilityPatientVerification["GroupNumber"]=EligibilityPatientVerification["PlanNumber"]
    
    EligibilityPatientVerification["InsuranceFeeScheduleUsed"]=EligibilityPatientVerification["ProgramType"]
    EligibilityPatientVerification["PlanName"]=""
    EligibilityPatientVerification["PlanNumber"]=""
    EligibilityPatientVerification["PlanType"]=EligibilityPatientVerification["ProgramType"]
    


    
    EligibilityPatientVerification['OrthodonticAgeLimits']               =  AgelimitShow(EligibilityAgeLimitation)
   # EligibilityPatientVerification["FrequencyLimitationsExclusions"] = None
   # EligibilityPatientVerification["ExclusionsAgeRestrictionsMaximums"] = None
    if len(EligibilityBenefits)!=0:
        EligibilityBenefits                     =  DeductibleApplicable(EligibilityBenefits,IndividualAnnualDeductible_1)
    data["EligibilityBenefits"]= EligibilityBenefits
    data["EligibilityPatientVerification"]=[EligibilityPatientVerification]

    try:request_procodes=getrequestprocodes(request)
    except: request_procodes=[]
    print(request_procodes)
    if len(request_procodes)!=0:
        limitationsProCodes=limitationsSoter(EligibilityBenefits,request_procodes)
        print(limitationsProCodes,"here")
        if len(limitationsProCodes)!=0:
            
        
            for i in request['Xpaths']:
                if i['DataContextName'] =='Eligibilitylimitaiton':
                    print(list(set(limitationsProCodes)))
                    data_=json.loads(i['XPath'])
                    data_['Xpaths'][0]['MultiplElements']['multiple_elements_xpath']=list(set(limitationsProCodes))
                    i['XPath']=json.dumps(data_)
                    
                    
                    
        
            request['Xpaths']=[x for x in request['Xpaths'] if  x['DataContextName']  in  ['EligibilityLogin','Eligibilitylimitaiton'] ]
            limit=kick(request,"message_id",browser,request['PatientData'][0])
            data['Eligibilitylimitaiton']=        limit['Eligibilitylimitaiton']
            print(limit)
            # data['Eligibilitylimitaiton']= ""
            
            if len(EligibilityBenefits)!=0:
                data["EligibilityBenefits"]=limitationsUpdater(data['Eligibilitylimitaiton'],EligibilityBenefits)
            
            if len(data["EligibilityServiceTreatmentHistory"])!=0:
                data['EligibilityServiceTreatmentHistory']=limitationsUpdaterTreatmentHistory(data['Eligibilitylimitaiton'],data["EligibilityServiceTreatmentHistory"])
    if len(data["EligibilityServiceTreatmentHistory"])!=0:
        data['TreatmentHistorySummary']=TreatmentHistorySummary(data['EligibilityServiceTreatmentHistory'])    
    try:
        del data["EligibilityPatientVerification"][0]['Address']
    except:
        pass
    try:
        del data['Eligibilitylimitaiton']
    except:
        pass   
    EligibilityPatientVerification["AlternativeBenefitProvision"]=AlternativeBenefitProvision(data['EligibilityBenefits']) 
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

   
    # output=ast.literal_eval(str(data).replace("(", "_").replace(")", "_"))
    return output

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\ins\30 july\SD%20Payor%20Scraping\ins6.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\ins\30 july\SD%20Payor%20Scraping\output_22549.json", 'r'))
# browserr =""
# output=main(data, request, browserr)
# with open("deltadentalins-patient.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
