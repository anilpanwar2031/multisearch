def main(data):
    print("<<<<<<<<<<<<<<<<<<<<<<In DNOA RCM>>>>>>>>>>>>>>>>>>>>>>>>>>")

    # Remove claim total and allowed value and key
    for i in range(len(data["RcmEobClaimDetail"])):

        if data["RcmEobClaimDetail"][i]["Tooth_Quadrant"] == "/":
            data["RcmEobClaimDetail"][i]["Tooth_Quadrant"] = ""
        if data["RcmEobClaimDetail"][i]["ClaimTotals"] == "Claim Totals":
            del data["RcmEobClaimDetail"][i]

        elif data["RcmEobClaimDetail"][i]["ClaimTotals"] == "Allowed":
            del data["RcmEobClaimDetail"][i]["ClaimTotals"]
        else:
            pass

    # Remove empty key value
    # print(len(data["RcmEobClaimMaster"]))
    newDict = {}
    if len(data["RcmEobClaimMaster"]) > 1:
        for item in data["RcmEobClaimMaster"]:
            if 'ClaimDetails' in item:
                claim_details = item['ClaimDetails']
                for claim in claim_details:
                    if claim[''] == '':
                        del claim['']
                    newDict.update(claim)
                    del item['ClaimDetails']

        dat = []
        final = {}
        backup_key = data["RcmEobClaimMaster"][0]["url"]  # Backup of url
        del data["RcmEobClaimMaster"][0]["url"]  # Delete of old url

        for i in data["RcmEobClaimMaster"][0].items():  # formating the unstructured data
            if "\n" in i[0]:
                d = i[0].replace("PatientName", "PatientName\n").split("\n")
                t = i[1].replace("PatientName", "PatientName\n").split("\n")
                dat.append(d)
                dat.append(t)
        for i in range(len(dat)):
            list_ = dat[i]
            final.update({list_[0].replace(" ", ""): list_[1]})
        del data["RcmEobClaimMaster"][0]
        final['url'] = backup_key
        data["RcmEobClaimMaster"].append(final.copy())  # copying final dict to main object
        data["RcmEobClaimMaster"].append(newDict.copy())  # copying newDict dict to main object
        data["RcmEobClaimMaster"][0].update(data["RcmEobClaimMaster"][1])
        del data["RcmEobClaimMaster"][1]
        data["RcmEobClaimMaster"][0].update(data["RcmEobClaimMaster"][1])
        del data["RcmEobClaimMaster"][1]
    else:
        pass
    
    return data



