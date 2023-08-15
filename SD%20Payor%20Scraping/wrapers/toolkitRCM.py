import json



def main(data):
    n = len(data["RcmEobClaimDetail"])
    backup_lst = data["RcmEobClaimDetail"][n-1]
    lst =[]
    lst.append(data["RcmEobClaimDetail"][n-1])
    del data["RcmEobClaimDetail"][n - 1]
    for obj in lst[0]:
        print(obj)
        if obj == "Total":
            lst[0]["Total"] = ""


    temp = []
    for obj in data["RcmEobClaimDetail"]:
        if obj["DateOfService"] != None:
            temp.append(obj)
    temp.append(backup_lst)
    data["RcmEobClaimDetail"] = temp

    for i in range(len(data["RcmEobClaimDetail"])):
        for j in data["RcmEobClaimDetail"][i].items():
            if 'Total1' in j:
                data["RcmEobClaimMaster"][0].update(data["RcmEobClaimDetail"][i])
                del data["RcmEobClaimDetail"][i]

    

    return data



