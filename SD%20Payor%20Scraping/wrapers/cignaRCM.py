def main(data):
    items_to_remove = []

    for i in range(len(data['RcmEobClaimDetail'])):
        if data['RcmEobClaimDetail'][i]["DatesOfService"] == "Totals":
            del data['RcmEobClaimDetail'][i]["DatesOfService"]
            del data['RcmEobClaimDetail'][i]["CdtCodes*/TypeOfService"]
            if "RemarkCodes" not in data['RcmEobClaimDetail'][i]:
                pass
            else:
                del data['RcmEobClaimDetail'][i]["RemarkCodes"]
        items_to_remove.append(data['RcmEobClaimDetail'][i])

    key_lst = []
    final_dict = {}
    for i in range(len(items_to_remove)):
        if "DatesOfService" not in items_to_remove[i]:
            for k, v in items_to_remove[i].items():
                if k not in ["ClientId", "EligibilityVerificationId", "RcmGridViewId"]:
                    key = "{}Total".format(k)
                    key_lst.append(key)
                    final_dict = dict(zip(key_lst, list(items_to_remove[i].values())))
    data['RcmEobClaimMaster'][0].update(final_dict)

    # n = len(data['RcmEobClaimDetail'])
    #
    # if 'Status' not in data['RcmEobClaimDetail'][n - 1]:
    #     del data['RcmEobClaimDetail'][n - 1]
    # else:
    #     pass


    for k,v in data['RcmEobClaimMaster'][0].items():
        if type(v) == str:
            if ":\n" in v:
                val = v.split(":\n")
                val = val[1]
                data['RcmEobClaimMaster'][0][k] = val



    for k,v in data["RcmEobClaimMaster"][0].items():
        if k == "PatientName":
            data["RcmEobClaimMaster"][0]["PatientName"] = data["RcmEobClaimMaster"][0]["PatientName"].split("|")[0].strip()
    CDTCodes = ""
    TypeOfService = ""
    for i in range(len(data['RcmEobClaimDetail'])):
        for key,values in data['RcmEobClaimDetail'][i].items():
            if key == "DatesOfService":
                if data['RcmEobClaimDetail'][i]['DatesOfService'] == "--":
                    data['RcmEobClaimDetail'][i]['DatesOfService'] = ''
            if key == "CdtCodes*/TypeOfService":
                cdtcodes_type_of_service = values
                try:
                    CDTCodes, TypeOfService = cdtcodes_type_of_service.split(" - ",1)
                except:
                    CDTCodes=cdtcodes_type_of_service

        data['RcmEobClaimDetail'][i]["CDTCodes"] = CDTCodes
        data['RcmEobClaimDetail'][i]["TypeOfService"] = TypeOfService
        if data['RcmEobClaimDetail'][i].get("CdtCodes*/TypeOfService"):
            del data['RcmEobClaimDetail'][i]["CdtCodes*/TypeOfService"]
       
    return data