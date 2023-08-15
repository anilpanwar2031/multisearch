import zipfile
import pandas as pd
import logging
import json

def zip_processor(path1, path2):

    df_list = []

    archive1 = zipfile.ZipFile(path1, 'r')
    file_names1 = archive1.namelist()
    table_files1 = [name for name in file_names1 if name.startswith('tables/') and name.endswith(".xlsx")]

    #load extra info from benefit summary
    structureData = []
    mailingAdress = ""
    payorID = ""
    with zipfile.ZipFile(path1, "r") as zip_file:
        with zip_file.open("structuredData.json") as json_file:
            structureData = json.load(json_file)
    elements = structureData.get("elements")
    for item in elements:
        if item.get("Path") == "//Document/P/Sub":
            mailingAdress = mailingAdress + item.get("Text")
        elif item.get("Path") == "//Document/P/Sub[2]":
            mailingAdress = mailingAdress + item.get("Text")
        elif item.get("Path") == "//Document/P/Sub[3]":
            mailingAdress = mailingAdress + item.get("Text")
        elif item.get("Path") == "//Document/P/Sub[4]":
            mailingAdress = mailingAdress + item.get("Text")
        elif item.get("Path") == "//Document/P/Sub[5]":
            payorID = item.get("Text")

    archive2 = zipfile.ZipFile(path2, 'r')
    file_names2 = archive2.namelist()
    table_files2 = [name for name in file_names2 if name.startswith('tables/') and name.endswith(".xlsx")]
    
    data = {
        "EligibilityPatientVerification":[],
        "EligibilityMaximums":[],
        "EligibilityOtherProvisions":[],
        "EligibilityBenefits":[]
        }
    
    data["EligibilityPatientVerification"].append({"ClaimMailingAddress":mailingAdress})
    data["EligibilityPatientVerification"].append({"PayorID":payorID})

    for idx, name in enumerate(table_files1):
        with archive1.open(name) as file:
            try:
                df = pd.read_excel(file)
                if len(df.index) >= 1 or df.columns.str.contains('TOTAL', case=False).any():
                    if df.columns.str.contains('_x000D_', case=False).any():
                        df = df.replace('_x000D_', '', regex=True)
                    if any('_x000D_' in col for col in df.columns):
                        df = df.rename(columns=lambda x:x.replace("_x000D_", ""))

                    df_list.append(df)
            except pd.errors.ParserError as e:
                logging(f"Error parsing {name}: {e}")

    for idx, name in enumerate(table_files2):
        with archive2.open(name) as file:
            try:
                df = pd.read_excel(file)
                if len(df.index) >= 1 or df.columns.str.contains('TOTAL', case=False).any():
                    if df.columns.str.contains('_x000D_', case=False).any():
                        df = df.replace('_x000D_', '', regex=True)
                    if any('_x000D_' in col for col in df.columns):
                        df = df.rename(columns=lambda x:x.replace("_x000D_", ""))

                    df_list.append(df)
            except pd.errors.ParserError as e:
                logging(f"Error parsing {name}: {e}")
    
    for tables in df_list:
        ##Benefits Summary##
        if tables.columns.str.contains('Plan Member: ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Title', 'Detail']    
            data["EligibilityPatientVerification"].append({"PlanMember":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Coverage Status Information: ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Title', 'Detail']    
            data["EligibilityPatientVerification"].append({"Coverage":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Benefit Type/Plan Benefit: ', case=False).any():
            if len(tables.columns) == 4:
                tables.columns = ['Benefit Type/Plan Benefit', 'Percentage', 'value', 'Elimination Period']    
                data["EligibilityOtherProvisions"].append({"BenefitTypePlan":tables.to_dict(orient='records')})
            elif len(tables.columns) == 5:
                tables.columns = ['Benefit Type/Plan Benefit', 'Detail', 'Percentage', 'value', 'Elimination Period']    
                data["EligibilityOtherProvisions"].append({"BenefitTypePlan":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Orthodontics: ', case=False).any():
            tables.columns = ['Title', 'Detail']    
            data["EligibilityOtherProvisions"].append({"Orthodontics":tables.to_dict(orient='records')})
        elif (tables == "Contributing Procedures ").any(axis=1).any():
            tables.columns = ['Service', 'Benefit Type', 'Frequency', 'Contributing Procedures', 'Additional Information']    
            data["EligibilityBenefits"].append({"Benefits with proc":tables.to_dict(orient='records')})
        elif (tables == "Frequency ").any(axis=1).any() and len(tables.columns) == 4:
            tables.columns = ['Service', 'Benefit Type', 'Frequency', 'Additional Information']    
            data["EligibilityBenefits"].append({"Benefits":tables.to_dict(orient='records')})
        
        ##Patient Summary##
        elif tables.columns.str.contains('Benefit Type Percentage Type 1 - Preventive ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Title', 'Detail']   
            data["EligibilityMaximums"].append({"MaximumsAll":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Next Eligible ', case=False).any():
            tables.columns = ['Procedure', 'Next Eligible']   
            data["EligibilityBenefits"].append({"Procedure Dates":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Type 1 - Preventive ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Benefit Type', 'Percentage']   
            data["EligibilityMaximums"].append({"BenefitTypeByPercentage":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Preventive/Basic/Major ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Deductible', 'Detail']   
            data["EligibilityMaximums"].append({"Deductible":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Maximum ', case=False).any():
            tables.columns = ['Maximum', 'Detail']   
            data["EligibilityMaximums"].append({"Maximums":tables.to_dict(orient='records')})

    
    # json_data = json.dumps(data, indent=2)
    
    # with open ("outputRuhe.json", "w") as f:
    #     f.write(json_data)

    return data


