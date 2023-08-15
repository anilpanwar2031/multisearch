def remove_none_objects(RcmEobClaimDetail):
    """
        Removes dictionary objects from the given list 'RcmEobClaimDetail' that have 'SubmittedAmount' set to None.
        Args:
            RcmEobClaimDetail (list): A list of dictionaries representing claim details.
        Returns:
            list: A filtered list of dictionaries with 'SubmittedAmount' not equal to None.
    """

    filteredRcmEobClaimDetail1 = []
    for claim in RcmEobClaimDetail:
        if claim.get('SubmittedAmount') is not None:
            filteredRcmEobClaimDetail1.append(claim)
    filteredRcmEobClaimDetail = []
    for claim in filteredRcmEobClaimDetail1:
        if claim.get('DateOfService') != "Date of Service":
            filteredRcmEobClaimDetail.append(claim)

    replace_dash_with_empty(filteredRcmEobClaimDetail)

    return filteredRcmEobClaimDetail


def replace_dash_with_empty(filteredRcmEobClaimDetail):
    """
        Replaces any occurrence of the string "-" in the dictionaries of the given list 'filteredRcmEobClaimDetail'
        with an empty string "".
        Args:
            filteredRcmEobClaimDetail (list): A list of dictionaries representing filtered claim details.
        Returns:
            list: The modified list of dictionaries with "-" replaced by an empty string.
    """
    for claim in filteredRcmEobClaimDetail:
        for key, value in claim.items():
            if value == "-":
                claim[key] = ""

    return filteredRcmEobClaimDetail


def main(data):
    """
        Main function to process and modify the input data.
        Args:
            data (dict): The input data in the form of a dictionary containing claim details.
        Returns:
            dict: The modified data dictionary with 'RcmEobClaimDetail' filtered and '-' replaced with an empty string.
    """
    RcmEobClaimDetail = data["RcmEobClaimDetail"]

    data["RcmEobClaimDetail"] = remove_none_objects(RcmEobClaimDetail)

    return data
