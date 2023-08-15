import json
# from thefuzz import fuzz
from re import search
from mapPDF import mapEligibilityPatientVerification

massachusetts_procedure_code_description = {
        # These procedure codes description is taken from payor page with the title 'Benefit Plan Summary of Benefits'
        # url https://onlineservices.deltadentalma.com/Router.jsp?source=HPMemberSummary&component=Members&action=BenefitDetails&rowNumber=1
        # These mapping needs to be done to fetch proper limitations from the payor site.
        
        # For Diagnostics
        "D0150":"Comprehensive Evaluation",
        "D0120":"Periodic Oral Exam",
        "D0210":"Full Mouth X-rays",
        "D0272":"Bitewing X-rays",
        "D0220":"Single Tooth X-rays",

        # For Preventives
        # "":"Teeth Cleaning",
        "D1206":"Fluoride Treatments.",
        "D1516":"Space Maintainers",
        "D1351":"Sealants",
        # "":"Chlorhexidine Mouthrinse",
        # "":"Fluoride Toothpaste",

        # For Restorative
        "D2930":"Stainless Steel Crowns",

        # For Endodontics
        "D1351":"Vital Pulpotomy"
    }

def main(Scraperdata, request):
    patientdata = request.get("PatientData")[0]
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification", [])
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums", [])
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits", [])
    EligibilityServiceTreatmentHistory =  Scraperdata.get("EligibilityServiceTreatmentHistory", [])
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions", [])


    EligibilityPatientVerification.update({"FamilyMemberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName")})
    EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":patientdata.get("BirthDate")})
    EligibilityPatientVerification.update({"SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate")})

    if EligibilityPatient:
        EligibilityPatientVerification.update({"FamilyMemberName":EligibilityPatient[0].get("MemberName")})
        EligibilityPatientVerification.update({"EligibilityStatus":EligibilityPatient[0].get("EligibilityStatus")})
        if EligibilityPatient[0].get("EligibilityStatus").lower() in ["ineligible", "not found"]:
            
            return {"EligibilityPatientVerification":[EligibilityPatientVerification]}
        
        
        EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":EligibilityPatient[0].get("InsuranceEffectiveDate")})
        EligibilityPatientVerification.update({"FamilyMemberEndDate":EligibilityPatient[0].get("TerminationDate")})
        EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":""})
        # EligibilityPatientVerification.update({"DependentStudentAgeLimit":EligibilityPatient.get("Studenteligibility")})

        try:
            EligibilityPatientVerification.update({"ProgramType":EligibilityBenefitsData[1]["data"][2][1]})
            EligibilityPatientVerification.update({"GroupName":EligibilityBenefitsData[1]["data"][0][1]})
            EligibilityPatientVerification.update({"GroupNumber":EligibilityBenefitsData[1]["data"][1][1]})    
            EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":EligibilityBenefitsData[1]["data"][5][1]})
            EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":EligibilityBenefitsData[1]["data"][4][1]})
            EligibilityPatientVerification.update({"InNetworkOutNetwork":"In Network"})
        except Exception as e:
            print("Exception Occured while getting benefit data.")

        EligibilityPatientVerification.update({"oonBenefits":"Yes"})
        EligibilityPatientVerification.update({"CoordinationofBenefitsType":""})
        EligibilityPatientVerification.update({"CoordinationofBenefits":EligibilityBenefitsData[1]["data"][6][1]})
    
    if EligibilityOtherProvisions:
        EligibilityPatientVerification.update({"ClaimMailingAddress":EligibilityOtherProvisions[0].get("Claimaddress").replace("\n"," ").replace("Claims Submission ","")})
        EligibilityPatientVerification.update({"AlternativeBenefitProvision":""})
        # EligibilityPatientVerification.update({"AlternativeBenefitProvision":"Multi Surface Posterior Composite restorations are a covered benefit."})

    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityBenefits=[]
    
    ####----Maximums and deductibles-----###
    for item in EligibilityMaximiums:
        if search("In", item.get("Network")) and item.get("Level")=="Individual" and search("Deductible", item.get("Type")):
            EligibilityPatientVerification.update({"IndividualAnnualDeductible":item.get("Limit")})
            EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":item.get("Remaining")})
            EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":item.get("Applied")})

            TypeDetail = item.get("Type").split("-",1)

            EligibilityDeductiblesProcCode.append({
                "Type": TypeDetail[0].strip(),
                "Network": "In Network",
                "Amount": item.get("Limit"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Applied"),
                "ServiceCategory": TypeDetail[1].strip(),
                "Period": item.get("Period"),
                "BenefitPeriod": item.get("BenefitPeriod"),
                "Family_Individual": "Individual"
            })

        if search("In", item.get("Network")) and item.get("Level")=="Family" and search("Deductible", item.get("Type")):
            EligibilityPatientVerification.update({"FamilyAnnualDeductible":item.get("Limit")})
            EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":item.get("Remaining")})
            EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":item.get("Applied")})

            TypeDetail = item.get("Type").split("-", 1)

            EligibilityDeductiblesProcCode.append({
                "Type": TypeDetail[0].strip(),
                "Network": "In Network",
                "Amount": item.get("Limit"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Applied"),
                "ServiceCategory": TypeDetail[1].strip(),
                "Period": item.get("Period"),
                "BenefitPeriod": item.get("BenefitPeriod"),
                "Family_Individual": "Family"
            })

        if search("Out", item.get("Network")) and item.get("Level")=="Individual" and search("Deductible", item.get("Type")):
            TypeDetail = item.get("Type").split("-", 1)

            EligibilityDeductiblesProcCode.append({
                "Type": TypeDetail[0].strip(),
                "Network": "Out of Network",
                "Amount": item.get("Limit"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Applied"),
                "ServiceCategory": TypeDetail[1].strip(),
                "Period": item.get("Period"),
                "BenefitPeriod": item.get("BenefitPeriod"),
                "Family_Individual": "Individual"
            })

        if search("Out", item.get("Network"))  and item.get("Level")=="Family" and search("Deductible", item.get("Type")):
            TypeDetail = item.get("Type").split("-", 1)

            EligibilityDeductiblesProcCode.append({
                "Type": TypeDetail[0].strip(),
                "Network": "Out of Network",
                "Amount": item.get("Limit"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Applied"),
                "ServiceCategory": TypeDetail[1].strip(),
                "Period": item.get("Period"),
                "BenefitPeriod": item.get("BenefitPeriod"),
                "Family_Individual": "Family"
            })

        if search("In", item.get("Network"))  and item.get("Level")=="Individual" and search("Maximum", item.get("Type")) and search("All", item.get("Type")):
            EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":item.get("Limit")})
            EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":item.get("Remaining")})
            EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":item.get("Applied")})

            TypeDetail = item.get("Type").split("-",1)

            EligibilityMaximums.append({
                "Type": TypeDetail[0].strip(),
                "Network": "In Network",
                "Amount": item.get("Limit"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Applied"),
                "ServiceCategory": TypeDetail[1].strip(),
                "Period": item.get("Period"),
                "BenefitPeriod": item.get("BenefitPeriod"),
                "Family_Individual": "Individual"
            })

        if search("Out", item.get("Network"))  and item.get("Level")=="Individual" and search("Maximum", item.get("Type")) and search("All", item.get("Type")):

            TypeDetail = item.get("Type").split("-",1)

            EligibilityMaximums.append({
                "Type": TypeDetail[0].strip(),
                "Network": "In Network",
                "Amount": item.get("Limit"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Applied"),
                "ServiceCategory": TypeDetail[1].strip(),
                "Period": item.get("Period"),
                "BenefitPeriod": item.get("BenefitPeriod"),
                "Family_Individual": "Individual"
            })
        if search("In", item.get("Network"))  and item.get("Level")=="Individual" and search("Maximum", item.get("Type")) and search("Orthodontics", item.get("Type")):
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":item.get("Limit")})
            EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":item.get("Remaining")})
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":item.get("Applied")})

            TypeDetail = item.get("Type").split("-",1)

            EligibilityMaximums.append({
                "Type": "Orthodontic Lifetime",
                "Network": "In Network",
                "Amount": item.get("Limit"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Applied"),
                "ServiceCategory": TypeDetail[1].strip(),
                "Period": item.get("Period"),
                "BenefitPeriod": item.get("BenefitPeriod"),
                "Family_Individual": "Individual"
            })


    # Service Treatment History Formation
    print("Processing Service Treatment History:")
    service_treatment_history = {}
    for items in EligibilityServiceTreatmentHistory:
        if service_treatment_history.get(items["ProcedureCode"]):
            history = service_treatment_history[items["ProcedureCode"]]["History"]
            if history.get(items.get("ServiceDate")):
                history[items.get("ServiceDate")] += ","+items.get("Tooth/Quad/Arch")
            else:
                history[items.get("ServiceDate")] = items.get("Tooth/Quad/Arch")
        else:
            service_treatment_history[items["ProcedureCode"]] = {
                "ProcedureCode": items.get("ProcedureCode"),
                "LimitationText": "",
                "History": {
                    items.get("ServiceDate"): items.get("Tooth/Quad/Arch")
                },
                "Tooth": items.get("Tooth/Quad/Arch"),
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": items.get("ProcedureCodeDescription")
            }

    UpdatedEligibilityServiceTreatmentHistory = []
    procedure_history = {}
    for procedure_code, procedure_detail in service_treatment_history.items():
        history_list = []
        for service_date, comma_separated_tooths in procedure_detail["History"].items():
            if comma_separated_tooths:
                history_list.append(service_date+"("+comma_separated_tooths+")")
                continue
            history_list.append(service_date)
        procedure_history[procedure_code] = ", ".join(history_list)

    # Procedure Benefits and Limitations Formation.
    print("Calculating Procedure Benefits and limitations: ")
    procedure_benefits_limitations = get_benefits_and_limitations(massachusetts_procedure_code_description, Scraperdata.get("EligibilityBenefits"))
    print(procedure_benefits_limitations)
    for procedure_code, procedure_details in service_treatment_history.items():
        limitation = ""
        benefit = ""
        if procedure_benefits_limitations.get(procedure_code):
            limitation = procedure_benefits_limitations[procedure_code].get("limitation")
            benefit = procedure_benefits_limitations[procedure_code].get("benefit")
        procedure_details["History"] = procedure_history[procedure_code]
        procedure_details["limitation"] = limitation
        procedure_details["benefit"] = benefit
        UpdatedEligibilityServiceTreatmentHistory.append(procedure_details)

    TreatmentHistorySummary = UpdatedEligibilityServiceTreatmentHistory.copy()

    for procedure_detail in UpdatedEligibilityServiceTreatmentHistory:
        procedure_code_desc = procedure_detail.get("ProcedureCodeDescription")
        deductible_applies = get_deductible_applies_val(procedure_code_desc, EligibilityBenefitsData, EligibilityMaximiums[0])
        procedure_code = procedure_detail.get("ProcedureCode")

        limitation = ""
        benefit = ""
        
        if procedure_code and procedure_benefits_limitations.get(procedure_code):
            limitation = procedure_benefits_limitations[procedure_code].get("limitation")
            benefit = procedure_benefits_limitations[procedure_code].get("benefit")
        
        EligibilityBenefits.append({
            "ProcedureCode": procedure_code,
            "ProcedureCodeDescription": procedure_code_desc,
            "Amount": "",
            "Type": "",
            "DeductibleApplies": deductible_applies,
            "Copay": "",
            "limitation": limitation,
            "benefit": benefit,
        })


    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":UpdatedEligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output

def get_deductible_applies_val(procedure_code_desc, elgi_benefit, elgi_maximum_fist_item):
    diagnostics = elgi_benefit[6].get("data")
    preventives = elgi_benefit[7].get("data")

    procedure_name = procedure_code_desc.split("-")[0].strip()
    if "except Diag,Prev and Ortho" in elgi_maximum_fist_item.get("Type"):
        for diagnostic in diagnostics:
            if procedure_name.strip() in diagnostic[0]:
                return "No"
        for preventive in preventives:
            if procedure_name.strip() in preventive[0]:
                return "No"
        if "periodic oral" in procedure_name.lower():    
            return "No"
        if "fluoride" in procedure_name.lower():    
            return "No"
    return "Yes"

def get_benefits_and_limitations(ui_procedure_code_description, eligibility_benefits):
    procedure_code_benfit_limitation = {}
    for proc_code, ui_proc_desc in ui_procedure_code_description.items():
        for service_block in eligibility_benefits[6:]:
            is_limitation_found, limitation = get_limitation(ui_proc_desc, service_block)
            is_benefit_found, benfit = get_benefits(ui_proc_desc, service_block)
            if is_limitation_found:
                if procedure_code_benfit_limitation.get(proc_code):
                    procedure_code_benfit_limitation[proc_code]["limitation"] = limitation
                else:
                    procedure_code_benfit_limitation[proc_code] = {"limitation":limitation}
            if is_benefit_found:
                if procedure_code_benfit_limitation.get(proc_code):
                    procedure_code_benfit_limitation[proc_code]["benefit"] = benfit
                else:
                    procedure_code_benfit_limitation[proc_code] = {"benefit":benfit}
                break
    return procedure_code_benfit_limitation

def get_limitation(desc, service_list):
    for service_list_item in service_list["data"]:
        if "In and Out of Network" not in service_list_item[0] and desc in service_list_item[0]:
            return True, service_list_item[1]
    return False, ""

def get_benefits(desc, service_list):
    for service_list_item in service_list["data"]:
        if "In and Out of Network" in service_list_item[0] and desc in service_list_item[0]:
            return True, service_list_item[1]
    return False, ""

# data=json.load(open(r"../output_elgi.json", 'r'))
# request=json.load(open(r"../m_mona_input_req.json", 'r'))

# data=json.load(open(r"../output.json", 'r'))
# request=json.load(open(r"../ma_test1.json", 'r'))
# output=main(data, request)
# with open("MasschusettsOutput-wrapperOutput.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
