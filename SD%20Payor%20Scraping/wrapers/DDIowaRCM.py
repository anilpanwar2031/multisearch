"""
It's a wrapper for output for claims for 'Delta Dental Iowa' for 'Claims'
"""

def main(data):
    """
    This function takes in a dictionary containing two lists: 'RcmEobClaimMaster' and
    'RcmEobClaimDetail'. It modifies the 'ClaimSubmissionRecord', 'Status', and
    'PaymentDate' values in the 'RcmEobClaimMaster' list by splitting them on ':'
    and retaining the last part. It also removes any claim detail records where the
    'DateOfService' value contains the character '$'. Finally, it returns the modified
    'data' dictionary.

    Args:
    - data: A dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.

    Returns:
    - A modified 'data' dictionary with the 'ClaimSubmissionRecord', 'Status', and
    'PaymentDate' values in the 'RcmEobClaimMaster' list modified, and any claim detail
    records with a 'DateOfService' value containing the character '$' removed.
    """

    # Retrieve claim master and claim detail lists from data
    claim_master_list = data.get('RcmEobClaimMaster', [])
    claim_detail_list = data.get('RcmEobClaimDetail', [])

    # Keys to modify in claim master list
    keys_to_modify = ['ClaimSubmissionRecord', 'Status', 'PaymentDate']

    # Modify keys in claim master list
    for claim in claim_master_list:
        for key in keys_to_modify:
            value = claim.get(key, '')
            if isinstance(value, str) and value != '':
                # Split value on ':' and retain last part after split
                claim[key] = value.split(':')[-1].strip()

        claim['Notes'] = claim.get('Notes').replace('Reference Codes\n', '')
        claim['DentistSubmittedComments'] = claim.get('DentistSubmittedComments').replace('Dentist Submit Comments', '')

    for claim in claim_detail_list:
        if '$' in claim.get('DateOfService'):
            delta_dental_pays = claim.get('AllowedAmount')
            patient_pays = claim.get('FeeAdjust')

    claim_master_list[0].update({
        'DeltaDentalPays': delta_dental_pays,
        'PatientPays': patient_pays
    })


    # Remove items from claim detail list where 'DateOfService' key contains '$'
    claim_detail_list = \
        [claim for claim in claim_detail_list if '$' not in claim.get('DateOfService', '')]


    # Update data dictionary with modified lists
    data['RcmEobClaimMaster'] = claim_master_list
    data['RcmEobClaimDetail'] = claim_detail_list

    

    return data
