import json

def main(data):

    n = data["RcmEobClaimDetail"][0]
    bkp_lst = []
    bkp_lst.append(n)
    del data["RcmEobClaimDetail"][0]
    output_lst =[]
    output_dict = {}
    output_dict1 = {}
    output_dict2 = {}
    output_dict3 = {}
    output_dict4 = {}
    lst = []


    for key, value in bkp_lst[0].items():
        if key.endswith('1'):
            output_dict1[key[:-1]] = value
            output_dict1['ClientId'] = bkp_lst[0]['ClientId']
            output_dict1['EligibilityVerificationId'] = bkp_lst[0]['EligibilityVerificationId']
            output_dict1['PatientId'] = bkp_lst[0]['PatientId']
            output_dict1['RcmGridViewId'] = bkp_lst[0]['RcmGridViewId']
            output_dict1['PMSSubscriberId'] = bkp_lst[0]['PMSSubscriberId']
            # data["RcmEobClaimDetail"].append(output_dict1)
        elif key.endswith('2'):
            output_dict2[key[:-1]] = value
            output_dict2['ClientId'] = bkp_lst[0]['ClientId']
            output_dict2['EligibilityVerificationId'] = bkp_lst[0]['EligibilityVerificationId']
            output_dict2['PatientId'] = bkp_lst[0]['PatientId']
            output_dict2['RcmGridViewId'] = bkp_lst[0]['RcmGridViewId']
            output_dict2['PMSSubscriberId'] = bkp_lst[0]['PMSSubscriberId']
            # data["RcmEobClaimDetail"].append(output_dict2)
        elif key.endswith('3'):
            output_dict3[key[:-1]] = value
            output_dict3['ClientId'] = bkp_lst[0]['ClientId']
            output_dict3['EligibilityVerificationId'] = bkp_lst[0]['EligibilityVerificationId']
            output_dict3['PatientId'] = bkp_lst[0]['PatientId']
            output_dict3['RcmGridViewId'] = bkp_lst[0]['RcmGridViewId']
            output_dict3['PMSSubscriberId'] = bkp_lst[0]['PMSSubscriberId']
            # data["RcmEobClaimDetail"].append(output_dict3)
        elif key.endswith('4'):
            output_dict4[key[:-1]] = value
            output_dict4['ClientId'] = bkp_lst[0]['ClientId']
            output_dict4['EligibilityVerificationId'] = bkp_lst[0]['EligibilityVerificationId']
            output_dict4['PatientId'] = bkp_lst[0]['PatientId']
            output_dict4['RcmGridViewId'] = bkp_lst[0]['RcmGridViewId']
            output_dict4['PMSSubscriberId'] = bkp_lst[0]['PMSSubscriberId']
            # data["RcmEobClaimDetail"].append(output_dict4)
        else:
            output_dict[key] = value
            # data["RcmEobClaimDetail"].append(output_dict)


    output_lst.append(output_dict)
    output_lst.append(output_dict1)
    output_lst.append(output_dict2)
    output_lst.append(output_dict3)
    output_lst.append(output_dict4)
    # print(output_lst)

    for i in range(len(output_lst)):
        if output_lst[i]["PayeeName"] != '':
            lst.append(output_lst[i])

    for i in lst:
        data["RcmEobClaimDetail"].append(i)
        
    return data

