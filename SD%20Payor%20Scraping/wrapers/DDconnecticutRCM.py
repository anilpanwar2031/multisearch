import json
import re

def main(data):

    if data["RcmEobClaimMaster"][0].get("ProcessingPolicies"):
        rawStr = data["RcmEobClaimMaster"][0]["ProcessingPolicies"]
        pattern = r"\d+"
        data["RcmEobClaimMaster"][0]["ProcessingPolicies"] = re.sub(pattern, r"\g<0>-", rawStr)

    proc_code_description = {}
    proc_code_str = data["RcmEobClaimMaster"][0].get("ProcedureCodes")
    if proc_code_str:
        proc_code_desc = proc_code_str.split("\n")
        proc_code_desc.pop(0)
        for index in range(0, len(proc_code_desc), 2):
            proc_code_description[proc_code_desc[index]] = proc_code_desc[index + 1]
        del data["RcmEobClaimMaster"][0]["ProcedureCodes"]

    lst = []
    for i in range(len(data["RcmEobClaimDetail"])):
        if None not in data["RcmEobClaimDetail"][i].values():
            lst.append(data["RcmEobClaimDetail"][i])

    filtered_data = {}
    if data["RcmEobClaimDetail"][1].get("ClientId") != None:
        filtered_data = {
            "ClientId": data["RcmEobClaimDetail"][1].get("ClientId"),
            "EligibilityVerificationId": data["RcmEobClaimDetail"][1].get("EligibilityVerificationId"),
            "PatientId": data["RcmEobClaimDetail"][1].get("PatientId"),
            "RcmGridViewId": data["RcmEobClaimDetail"][1].get("RcmGridViewId"),
            "PMSSubscriberId": data["RcmEobClaimDetail"][1].get("PMSSubscriberId")
        }

    del data["RcmEobClaimDetail"]
    data["RcmEobClaimDetail"] = []

    for i in lst:
        data["RcmEobClaimDetail"].append(i)

    data_list = list(data["RcmEobClaimDetail"][0].values())
    sublists = [data_list[i:i + 6] for i in range(0, len(data_list), 6)]
    del data["RcmEobClaimDetail"][0]

    for row in sublists:
        data["RcmEobClaimDetail"].append({
            'Tooth': row[0],
            'Procedure': row[1]+"-"+proc_code_description[row[1]],
            'DateOfService': row[2],
            'Submitted': row[3],
            'Paid': row[4],
            'ProcessingPolicies': row[5]
        })

    n = len(data["RcmEobClaimDetail"])
    for i in range(n):
        for k,v in filtered_data.items():
            data["RcmEobClaimDetail"][i][k] = v

    

    return data