

def main(data):
    """
        This function takes in a dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.
        It modifies keys of the RcmEobClaimDetail.

        Args:
        - data: A dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.

        Returns:
        - A modified 'data' dictionary with the changed keys in 'RcmEobClaimDetail'.
    """

    # Keys to modify in claim detail list
    keys=["TTH","DateofService","Proccode","Description","SubmittedAmount","ApprovedAmount","AllowedAmount","AppliedToDeduct","PercentageCoPay","OVCoPay","PatientPay","DeltaDentalPayment","ProcessingPolicy_1","ProcessingPolicy_2","ProcessingPolicy_3"]
    temp=[]
    for i in range(len(data['RcmEobClaimDetail'])):
        final_dict = dict(zip(keys, list(data['RcmEobClaimDetail'][i].values())))
        temp.append(final_dict)
    data['RcmEobClaimDetail']=temp
    policy_code_des=[]
    for i in data['RcmEobClaimDetail']:
        if i['ProcessingPolicy_1']!='':
            policy_code_des.append(i['ProcessingPolicy_1'])
    data['RcmEobClaimMaster'][0]['ProcessingPolicy_1']=policy_code_des
    for i in range(len(data['RcmEobClaimDetail'])):
        try:
            data['RcmEobClaimDetail'][i]['ProcessingPolicy_1']=data['RcmEobClaimDetail'][i]['ProcessingPolicy_1'].split('Policy Code')[1].split('-')[0].strip()
        except:
            pass

    
    return data








