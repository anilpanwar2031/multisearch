"""
It's a wrapper for output for claims for 'Delta Dental of Missouri' for 'Claims'
"""

import pandas as pd

from Utilities.pdf_utils import (
    file_download,
    get_data_in_format,
    extract_text_from_json_data,
)


def get_data_from_portal(data):
    """
    This function takes in a dictionary containing two lists:
        'RcmEobClaimMaster' and 'RcmEobClaimDetail'.
    It modifies keys of the RcmEobClaimDetail.

    Args:
    - data: A dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.

    Returns:
    - A modified 'data' dictionary with the changed keys in 'RcmEobClaimDetail'.
    """

    # Keys to modify in claim detail list
    keys = [
        "ProcessedToothCodeNumber",
        "ProcedureDescription",
        "ServiceDate",
        "SubmittedAmount",
        "PlanPays",
    ]
    temp = []
    for i in range(len(data["RcmEobClaimDetail"])):
        final_dict = dict(zip(keys, list(data["RcmEobClaimDetail"][i].values())))
        temp.append(final_dict)
    data["RcmEobClaimDetail"] = temp
    diff_keys = {
        "SubmittedCode": "",
        "ToothSurface": "",
        "AcceptedAmount": "",
        "AllowedAmount": "",
        "AppliedDeductible": "",
        "CoPay": "",
        "CoInsPercentage": "",
        "PatientPays": "",
        "AdjustmentNotice": "",
    }
    data["RcmEobClaimDetail"] = [
        {**item, **diff_keys} for item in data["RcmEobClaimDetail"]
    ]

    data["RcmEobClaimMaster"][0]["Notes"] = ""

    return data


def format_dataframe(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a pandas DataFrame, cleans it up, and standardizes the column names.
    It performs the following operations:
        - Fills NaN values with an empty string.
        - Sets DataFrame column names based on the row containing 'Service Date'.
        - Makes column names lowercase, removes periods and trims whitespace.
        - Transforms all DataFrame cell values to lowercase, removes periods and trims whitespace.
        - Drops rows in which all cell values match their respective column names.
        - Renames columns to standardized names.
        - Replaces any remaining NaN values with an empty string.

    Arguments:
    data_frame (pd.DataFrame): The input DataFrame to be cleaned and standardized.

    Returns:
    pd.DataFrame: The cleaned and standardized DataFrame.

    Raises:
    StopIteration: An error occurs if there is no row containing 'Service Date'.
    """

    try:
        data_frame.fillna("", inplace=True)
        header_row = next(
            i for i in data_frame.index if "Service Date" in data_frame.iloc[i, 0]
        )
        data_frame.columns = data_frame.iloc[header_row]
        data_frame = data_frame.iloc[(header_row + 1) :].reset_index(drop=True)
    except StopIteration:
        data_frame.columns = data_frame.iloc[0]
    # Make the column names lowercase and stripped of whitespace and periods for easier comparison
    data_frame.columns = (
        data_frame.columns.str.strip().str.replace(".", "", regex=True).str.lower()
    )

    # Do the same for the values in the dataframe
    formatted_df = data_frame.applymap(
        lambda x: str(x).strip().replace(".", "").lower()
    )

    # Compare the dataframe to its column names to get a boolean mask of matching values
    mask = formatted_df.eq(formatted_df.columns)

    # Find the index where all the row values are equal to the column names
    index_to_drop = mask.all(axis=1)

    # If any such row exists, perform the operations
    if index_to_drop.any():
        data_frame = data_frame.drop(data_frame[index_to_drop].index)

        # Rename columns
    data_frame.columns = [
        "ServiceDate",
        "SubmittedCode",
        "ProcessedToothCodeNumber",
        "ToothSurface",
        "SubmittedAmount",
        "AcceptedAmount",
        "AllowedAmount",
        "AppliedDeductible",
        "CoPay",
        "CoInsPercentage",
        "PatientPays",
        "PlanPays",
        "AdjustmentNotice",
    ]

    # Replace NaNs with empty string
    data_frame = data_frame.fillna("")

    return data_frame


def add_procedure_description(procedure_code_list: list, claim_details: list) -> list:
    """
    This function takes a list of procedure codes and their descriptions, and a list of
    claim details, and adds the corresponding procedure descriptions to the claim details
    based on the procedure codes.

    The function performs the following operations:
        - Converts the procedure code list to a dictionary for easy lookup.
        - Iterates over the claim details.
        - For each claim, if the submitted procedure code matches ProcedureCode in the dictionary,
          the corresponding procedure description is added to the claim details.
        - If there's no match, the function adds an empty string as the procedure description.

    Arguments:
    procedure_code_list (list): A list of dictionaries where each dictionary contains a
                                procedure code ('ProcedureCode') and
                                its description ('DescriptionOfCode').
    claim_details (list): A list of dictionaries where each dictionary contains details of a claim,
                          including a 'SubmittedCode'.

    Returns:
    list: The list of claim details with added 'ProcedureDescription' fields.

    """

    # Convert procedure_code_list to a dictionary for easy lookup
    procedure_code_dict = {
        item["ProcedureCode"].strip(): item["DescriptionOfCode"]
        for item in procedure_code_list
    }

    # Iterate over the claim details
    for claim_detail in claim_details:
        submitted_code = claim_detail["SubmittedCode"].strip()

        claim_detail["ProcedureDescription"] = procedure_code_dict.get(
            submitted_code, ""
        )

    return claim_details


def get_claim_details(data: dict, df_list: list, patien_name: str) -> tuple:
    """
    This function retrieves claim details for a specified patient from a list of DataFrames,
    along with procedure code list and a DataFrame of the last matching claim.

    The function performs the following operations:
        - Iterates over the list of DataFrames in reversed order.
        - For each DataFrame, checks if the patient's name appears in the column names.
        - If so, formats the DataFrame and checks if the 'PlanPays' field of the last record matches
          the 'AmountPaid' field from the input data.
        - If they match, appends all records from the DataFrame to the claim details.

    Arguments:
    data (dict): A dictionary containing key "RcmEobClaimMaster" which is a list of dictionaries
                 and the first item in the list contains key "AmountPaid".
    df_list (list): A list of pandas DataFrames, each containing claim data.
    patien_name (str): Name of the patient for which the claim details are being retrieved.

    Returns:
    tuple: A tuple containing three items: a list of claim details (each a dict of field values),
           an empty list (procedure_code_list, whose usage is not clear from the provided code),
           and a DataFrame of the last matching claim.

    """

    claim_details = []
    procedure_code_list = []

    for data_frame in reversed(df_list):
        columns = data_frame.columns
        for item in columns:
            if f"patient: {patien_name}" in item.lower():
                data_frame_copy = data_frame.copy()
                new_data_frame = format_dataframe(data_frame_copy)
                amount_paid = data.get("RcmEobClaimMaster", [{}])[0].get(
                    "AmountPaid", ""
                )
                if new_data_frame["PlanPays"].iloc[-1].strip() != amount_paid:
                    continue
                # for record in new_data_frame.to_dict('records'):
                #     claim_details.append(record)

                claim_details.extend(iter(new_data_frame.to_dict("records")))

    return claim_details, procedure_code_list, new_data_frame


def get_procedure_code_list(data_frame_list: list, combined_list: list) -> list:
    """
    This function scans a list of DataFrames for a DataFrame where the first column
    name contains any of the values from a given list (combined_list).
    If it finds such a DataFrame, it reformats the DataFrame and returns a list of its records.

    The function performs the following operations:
        - Iterates over the list of DataFrames.
        - For each DataFrame, checks if any of the values from combined_list
          is in the first column name.
        - If a match is found, adds the DataFrame's column names as a new row in the DataFrame,
          resets the DataFrame's index, and renames its columns.
        - Converts the DataFrame to a list of dictionaries and returns this list.

    Arguments:
    data_frame_list (list): A list of pandas DataFrames to be searched for procedure codes.
    combined_list (list): A list of strings. The function checks if any of these values is in
                          the first column name of each DataFrame.

    Returns:
    list: A list of dictionaries representing the records of a DataFrame where the first
          column name contained any of the values from combined_list.
          Each dictionary contains a procedure code ('ProcedureCode') and
          its description ('DescriptionOfCode').

    """

    procedure_code_list = []
    for data_frame in data_frame_list:
        if combined_list:
            print("start")
            if any(value in data_frame.columns[0] for value in combined_list):
                column_name = pd.DataFrame(
                    [data_frame.columns.to_list()], columns=data_frame.columns
                )
                procedure_df = pd.concat([column_name, data_frame], axis=0)
                procedure_df.reset_index(drop=True, inplace=True)
                procedure_df.columns = ["ProcedureCode", "DescriptionOfCode"]

                procedure_code_list = procedure_df.to_dict("records")
                print("procedure_code_list is ---------", procedure_code_list)
                break

    return procedure_code_list


def get_notes(data_frame: pd.DataFrame, note_list: list) -> str:
    """
    Function to extract notes corresponding to adjustment codes from a DataFrame.

    Args:
        data_frame: A pandas DataFrame containing an 'AdjustmentNotice' column.
        note_list: A list of possible notes.

    Returns:
        The extracted notes as a single string.

    Raises:
        TypeError: If the first argument is not a DataFrame.
        ValueError: If the 'AdjustmentNotice' column is not found in the DataFrame.
    """
    if not isinstance(data_frame, pd.DataFrame):
        raise TypeError(f"Expected DataFrame but got {type(data_frame).__name__}")
    if "AdjustmentNotice" not in data_frame.columns:
        raise ValueError("'AdjustmentNotice' column not found in data_frame")

    adjustment_notices = data_frame["AdjustmentNotice"].dropna().astype(str)
    updated_adjustments = {
        code.strip() for notice in adjustment_notices for code in notice.split()
    }
    notes = " ".join(
        note for note in note_list if any(code in note for code in updated_adjustments)
    )

    return f"Adjustment Notice {notes}" if notes else ""


def main(data: dict) -> dict:
    """
    This function retrieves data from a provided URL or portal,
    extracts and processes claim details,
    then adds these details to the input data and returns it.

    The function performs the following operations:
        - Retrieves the URL from the input data.
        - If no URL is provided, retrieves data from a portal
          (the get_data_from_portal function is not provided).
        - Retrieves a list of DataFrames and a work dictionary from the URL.
        - Extracts claim details and a procedure code list from the DataFrames.
        - Extracts a combined list of submitted codes and processed tooth code numbers.
        - Retrieves a procedure code list based on the combined list.
        - Extracts a list of notes from the work dictionary.
        - Cleans up the claim details.
        - Adds procedure descriptions to the claim details.
        - Strips whitespace from the ends of string values in the claim details.
        - Adds the claim details and notes to the input data.
        - Returns the updated input data.

    Arguments:
    data (dict): A dictionary containing keys 'RcmEobClaimDetail' (a list of dictionaries where the
                 first item contains key 'url') and 'RcmEobClaimMaster' (a list of dictionaries
                 where the first item contains keys 'Patient' and 'Notes').

    Returns:
    dict: The updated input data with additional claim details and notes.

    """

    eob_url = data.get("RcmEobClaimDetail", [{}])[0].get("url")

    if not eob_url:
        return get_data_from_portal(data)
    patient_name = data.get("RcmEobClaimMaster", [{}])[0].get("Patient", "").lower()
    print(eob_url)
    file_path = file_download(eob_url, "Revenue Cycle Management")

    df_list, work_dict = get_data_in_format(file_path)
    print(len(df_list))
    if not df_list:
        return get_data_from_portal(data)

    claim_details, procedure_code_list, new_data_frame = get_claim_details(
        data, df_list, patient_name
    )

    combined_series = list(
        set(
            pd.concat(
                [
                    new_data_frame["SubmittedCode"],
                    new_data_frame["ProcessedToothCodeNumber"],
                ]
            )
        )
    )
    print(combined_series)
    combined_list = [item.strip() for item in set(combined_series) if item != ""]
    print(combined_list)
    procedure_code_list = get_procedure_code_list(df_list, combined_list)

    note_list = extract_text_from_json_data(
        work_dict.get("elements"), "Adjustment Notice", "Procedure Code Description"
    )

    notes = get_notes(new_data_frame, note_list)

    claim_details = [
        detail
        for detail in claim_details
        if "Claim Totals:" not in detail.get("ToothSurface")
    ]
    claim_details = add_procedure_description(procedure_code_list, claim_details)
    claim_details = [
        {
            key: value.rstrip() if isinstance(value, str) else value
            for key, value in claim.items()
        }
        for claim in claim_details
    ]

    data["RcmEobClaimDetail"] = claim_details

    data["RcmEobClaimMaster"][0]["url"] = eob_url
    data["RcmEobClaimMaster"][0]["Notes"] = notes

    return data
