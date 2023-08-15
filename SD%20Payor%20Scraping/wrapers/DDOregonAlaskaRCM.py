# Claim Wrapper: Delta Dental Oregon and Alaska

def main(data):

    print(data["RcmEobClaimMaster"][0]["ReasonCode"])
    reason_codes = data["RcmEobClaimMaster"][0]["ReasonCode"].split(":")[1].strip()
    data["RcmEobClaimMaster"][0]["Notes"] = reason_codes
    del data["RcmEobClaimMaster"][0]["ReasonCode"]

    reason_code_hashmap = {}
    for reason_code in reason_codes.split("\n"):
        key, val = reason_code.split("-")
        reason_code_hashmap[key.strip()] = val.strip()
    
    new_data = []
    last_row = data["RcmEobClaimDetail"][-1]
    data["RcmEobClaimMaster"][0]["TotalBenefit"] = last_row["TotalBenefit"]
    # data["RcmEobClaimMaster"][0]["NonCoveredCharges"] = last_row["Non-CoveredCharges"]
    # data["RcmEobClaimMaster"][0]["Deduct"] = last_row["Deduct"]
    # data["RcmEobClaimMaster"][0]["ProviderDisc/Disallow"] = last_row["ProviderDisc/Disallow"]
    # data["RcmEobClaimMaster"][0]["RemainingCoveredCharges"] = last_row["RemainingCoveredCharges"]
    # data["RcmEobClaimMaster"][0]["Copay/Coins"] = last_row["Copay/Coins"]
    # data["RcmEobClaimMaster"][0]["PtResp"] = last_row["PtResp"]
    # data["RcmEobClaimMaster"][0]["BenefitPdToProv"] = last_row["BenefitPd ToProv"]
    # data["RcmEobClaimMaster"][0]["Codes"] = last_row["Codes"]
    del data["RcmEobClaimDetail"][-1]
    for index in range(0, len(data["RcmEobClaimDetail"]), 2):
        data["RcmEobClaimDetail"][index+1]["Dates"] = data["RcmEobClaimDetail"][index]["Dates"]
        data["RcmEobClaimDetail"][index+1]["ProcedureCode"] = data["RcmEobClaimDetail"][index]["Tooth"]
        data["RcmEobClaimDetail"][index+1]["ProcedureDescription"] = data["RcmEobClaimDetail"][index]["Tooth"]
        new_data.append(data["RcmEobClaimDetail"][index+1].copy())

    data["RcmEobClaimDetail"] = new_data
    for i, claim in enumerate(data["RcmEobClaimDetail"], start=1):
        desc, code= claim["ProcedureCode"].split("Code:")
        claim["ProcedureCode"] = code.strip()
        claim["ProcedureDescription"] = desc.strip()

        codes_str = ''
        for key in reason_code_hashmap.keys():
            if key in claim["Codes"]:
                if codes_str: 
                    codes_str = "\n".join([codes_str, key + " - " + reason_code_hashmap[key]])
                else:
                    codes_str = key + " - " + reason_code_hashmap[key]
        
        claim["Codes"] = codes_str

    return data