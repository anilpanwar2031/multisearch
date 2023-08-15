
def main(data):


    temp_lst = []
    for i in range(len(data["RcmEobClaimDetail"])):
        if data["RcmEobClaimDetail"][i]['ApprovedProcCode'] != 'TOTALS':
            temp_lst.append(data["RcmEobClaimDetail"][i])

    del data["RcmEobClaimDetail"]
    data["RcmEobClaimDetail"] = []
    for i in temp_lst:
        data["RcmEobClaimDetail"].append(i)

    

    return data