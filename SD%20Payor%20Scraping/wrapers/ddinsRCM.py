import re
def get_status(data_status,Enrollee_ClaimId):
    for obj in data_status:
        
        if obj.get("ClaimId")==Enrollee_ClaimId:
            print("hellllllllllll")
            return obj.get("Status")
def main(data):
    data_status=[]
    claimmaster=[]
    url=""
    for obj in data["RcmEobClaimMaster"]:
        if obj.get("status"):
            data_status=obj.get("status")
            url=obj.get("url")
        else:
            claimmaster.append(obj)    
    del data["RcmEobClaimMaster"][0]["status"]        
    data["RcmEobClaimMaster"]=claimmaster
    Enrollee_ClaimId = data["RcmEobClaimMaster"][0].get("Enrollee_ClaimId")
    data["RcmEobClaimMaster"][0]["url"]=url
    Enrollee_ClaimId = re.sub('[^0-9]', '', Enrollee_ClaimId)
    print(Enrollee_ClaimId)
    claim_status =get_status(data_status,Enrollee_ClaimId)
    print(claim_status)
    if "Processed" in claim_status:
        claim_status="Processed"
   
    if "Denied" in claim_status:
        claim_status="Denied"
    if "Processing" in claim_status:
        claim_status="Processing"

    print(data["RcmEobClaimMaster"])      
    data["RcmEobClaimMaster"][0]["Claim_Status"]  =claim_status
    data["RcmEobClaimMaster"][0]["Enrollee_ClaimId"]=Enrollee_ClaimId

    for obj in data["RcmEobClaimDetail"]:
        if obj.get("DateOfService"):
            if obj.get("DateOfService")=="-":
                obj["DateOfService"] =None

    
    
    return data
