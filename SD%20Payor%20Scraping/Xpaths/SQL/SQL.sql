
IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityPatientVerification')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityPatientVerification'),
'{"flatten":true,"Xpaths":[{"AdditonalInfo":{"Click":null,"fileds":[],"mandatoryfields":["EnrolleeName","DateOfBirth","EnrolleeId","PlanName","PlanNumber","EffectiveDate","EndDate","EligibilityStatus","ProgramType","FamilyMemberName","FamilyMemberEffectiveDate","FamilyMemberId","FamilyMemberEndDate","FamilyMemberDateOfBirth","FamilyMemberEligibilityStatus"]},"xpath":"//*[@summary=''Elligibility and Benefits Summary'']"},{"AdditonalInfo":{"Click":null,"fileds":"Address"},"xpath":"//*[@id=''template1:r1:1:r7:1:r1:0:pgl4'']/tbody"}]}',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityMaximums')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityMaximums'),
'{
            
            "Xpaths": [
                {
                    "AdditonalInfo": {
                        "Click": null,
                        "fileds": []
                    },
                    "xpath": "//*[@id=''template1:r1:1:r7:1:r1:0:r1:0:t3'']"
                }
            ]
   }',
1,4)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityDeductiblesProcCode')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityDeductiblesProcCode'),
'  {
           
            "Xpaths": [
                {
                    "AdditonalInfo": {
                        "Click": null,
                        "fileds": []
                    },
                    "xpath": "//*[@id=''template1:r1:1:r7:1:r1:0:r1:0:table2'']"
                }
            ]
        }',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityLogin')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityLogin'),
'  {         
            "Click": null,
            "Xpaths": [
                {
                    "UsernameXpath": "//*[@id=''username'']",
                    "PasswordXpath": "//*[@id=''password'']",
                    "LoginButtonXpath": "//*[@id=''loginButton'']",
                    "PreSteps": [],
                    "PostSteps": [],
                    "OtpInputXpath": "",
                    "OtpSubmitXpath": "",
                    "OtpXpath": ""
                }
            ]
 }',
1,4)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityServiceTreatmentHistory')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityServiceTreatmentHistory'),
'{
  "Xpaths": [
    {
      "AdditonalInfo": {
        "Click": [
          "//*[text()=''Treatment history'']"
        ],
        "fileds": [
         "ProcedureCode","ProcedureCodeDescription","LimitationText","LimitationAlsoAppliesTo","ServiceDate","ToothCode","ToothDescription","ToothSurface"
        ]
      },
      "xpath": "//*[@id=''template1:r1:1:r7:1:r1:0:r1:1:t3'']"
    }
  ]
} ',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityBenefits')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityBenefits'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Diagnostic'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_4'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Preventive'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_4'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Restorative'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_4'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_5'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Endodontics'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_4'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_5'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Periodontics'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Prosthodontics; Removable'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_4'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_5'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_6'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_7'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_8'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Prosthodontics; Fixed'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Oral & Maxillofacial Surgery'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_4'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_5'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_6'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_7'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Orthodontics'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_4'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_5'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Adjunctive General Services'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_4'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_5'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_6'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_7'']"},{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']","//*[text()=''Search'']","//*[text()=''Eligibility & benefits'']","//*[text()=''Implant Services'']","//*[text()=''Show all +'']"],"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_1'']"},{"AdditonalInfo":{"Click":null,"fileds":["procedureCode","procedureCodeDescription","limitation","PreApproval","DeltaDentalPPOTMDentistContractBenefitLevel","DeltaDentalPPOTMDentistAgelimit","DeltaDentalPremierDentistContractBenefitLevel","DeltaDentalPremierDentistAgelimit","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)ContractBenefitLevel","NonDeltaDentalDentist(Benefitsbasedoncontractallowance)Agelimit"]},"xpath":"//*[@id=''template1:r1:0:r7:0:r1:0:r1:0:t3j_id_2'']"}]} ',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='RcmEobClaimMaster')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='RcmEobClaimMaster'),
'{
    "flatten": true,
    "Xpaths": [
        {
            "AdditonalInfo": {
                "Click": ["//*[text()=''PDF'']"],
                "fileds": [
                    "Enrollee_ClaimId",
                    "EnrolleeId"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:t3x3'']/tbody/tr/td[1]/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "EnrolleeName",
                    "DateOfBirth",
                    "PatientName",
                    "PatientDateOfBirth"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:t3x3'']/tbody/tr/td[2]/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "Relationship",
                    "PlanName",
                    "PlanNumber"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:t3x3'']/tbody/tr/td[3]/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "Billing_Id",
                    "Name"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:t3xa3'']/tbody/tr/td/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "Rendering_Id",
                    "Rendering_Name",
                    "ProviderStatus",
                    "Lic#"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:t3ax3'']/tbody/tr/td/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "Claim_Status"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:tl6'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:tl6_c'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:tl6_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "DirectDepositReference#",
                    "Deposit_Status"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:tl116_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:tlas6_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:tqql6_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:tlt6_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": "Notes"
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:tl2'']/tbody"
        }
    ]
}  ',
1,2)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='ClinicSwitch')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='ClinicSwitch'),
' {
    "Search": {
       
        "Settings": {
            "PreSteps": {
                "Clicks": [
                    "//*[text()=''Switch office'']"
                ],
                "AdditonalInfo": {}
            },
            "SearchButtonXpath": "",
            "SearchFilter": {},
            "PostSteps": {
                "Clicks": [
                    "//*[@id=''template1:pt_lv1::db'']"
                ],
                "AdditonalInfo": {
                    "sleep": 7
                }
            }
        },
        "Queries": [
            {
                "Data": "SearchKey",
                "Xpath": "//*[@placeholder=''Search'']",
                "AdditonalInfo": {}
            }
        ]
    }',
1,2)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='RcmEobClaimDetail')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='RcmEobClaimDetail'),
'{
    "Xpaths": [
        {
            "AdditonalInfo": {
                "Click":null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r2:1:r1:0:trl1'']"
        }
    ]
} ',
1,2)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EFTPatients')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EFTPatients'),
' {
  "Xpaths": [
    {
      "AdditonalInfo": {
        "Click": null,
        "fileds": "Status"
      },
      "xpath": "//*[@id=''template1:r1:1:r4:0:t1::db'']/table/tbody/tr/td[7]/span/span"
    },
    {
      "AdditonalInfo": {
        "Click": [
          "//*[@id=''template1:r1:1:r4:0:t1:0:ot166'']"
        ],
        "fileds": [
          "",
          "PatientName",
          "EnrolleeId",
          "ClaimNumber",
          "DateOfService",
          "PatientPays",
          "DeltaDentalPays",
          ""
        ],
        "type": "headless"
      },
      "xpath": "//*[@id=''template1:r1:1:r4:1:t1::db'']/table"
    }
  ]
} ',
1,6)

ELSE
print 'not found'




IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='PpEobClaimMaster')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='PpEobClaimMaster'),
'  {
   "MultiplElements":{
      "multiple_elements_xpath":"//*[@class=''x271 xfh'']",
      "action":"Click"
   },
   "Xpaths":[
      {
         "AdditonalInfo":{
            "Click":[
               "//*[text()=''PDF'']"
            ],
            "fileds":[
               "Enrollee_ClaimId",
               "EnrolleeId"
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:t3x3'']/tbody/tr/td[1]/table"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               "EnrolleeName",
               "DateOfBirth",
               "PatientName",
               "PatientDateOfBirth"
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:t3x3'']/tbody/tr/td[2]/table"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               "Relationship",
               "PlanName",
               "PlanNumber"
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:t3x3'']/tbody/tr/td[3]/table"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               "Billing_Id",
               "Name"
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:t3xa3'']/tbody/tr/td/table"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               "Rendering_Id",
               "Rendering_Name",
               "ProviderStatus",
               "Lic#"
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:t3ax3'']/tbody/tr/td/table"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               "Claim_Status"
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:tl6'']"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:tl6_c'']"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:tl6_d'']"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               "DirectDepositReference#",
               "Deposit_Status"
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:tl116_d'']"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:tlas6_d'']"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:tqql6_d'']"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:tlt6_d'']"
      },
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":"Notes"
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:tl2'']/tbody"
      },
      {
         "AdditonalInfo":{
            "Click":[
               "//*[text()=''Claim information'']"
            ],
            "fileds":""
         },
         "xpath":""
      }
   ]
}',
1,6)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='PpEobClaimDetail')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='PpEobClaimDetail'),
' {
   "MultiplElements":{
      "multiple_elements_xpath":"//*[@class=''x271 xfh'']",
      "action":"Click"
   },
   "Xpaths":[
      {
         "AdditonalInfo":{
            "Click":null,
            "fileds":[
               
            ]
         },
         "xpath":"//*[@id=''template1:r1:1:r4:2:r1:0:trl1'']"
      },
      {
         "AdditonalInfo":{
            "Click":[
               "//*[text()=''Claim information'']"
            ],
            "fileds":[
               
            ]
         },
         "xpath":""
      }
   ]
} ',
1,6)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityOtherProvisions')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityOtherProvisions'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[text()=''Eligibility & benefits'']"],"fileds":[]},"xpath":"//*[@title=''Other Provisions'']"}]}',
1,4)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityFamilyMembersWaitingPeriods')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityFamilyMembersWaitingPeriods'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[text()=''Eligibility & benefits'']"],"fileds":[]},"xpath":"//*[@summary=''Benefits and Covered Services'']"}]}',
1,4)

ELSE
print 'not found'





IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityAgeLimitation')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityAgeLimitation'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[text()=''Eligibility & benefits'']","//*[text()=''Click here'']"],"fileds":["FamilyMember","AgeLimit"]},"xpath":"//table[@summary=''Ortho Age informat'']"}]}',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityMaximums')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Ins'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='Eligibilitylimitaiton'),
'{"forCore":false,"Xpaths":[{"AdditonalInfo":{"Click":["//*[text()=''Benefit search'']"],"fileds":[]},"MultiplElements":{"multiple_elements_xpath":[],"type":"SearchLoop","action":"Sendkeys","InputElementsXpath":"//input[@type=''text'']","SearchButtonXpath":"//*[text()=''Search'']","PreSteps":{"Clicks":["//*[text()=''[Limitations Apply]'']"]},"PostSteps":{"Clicks":["//*[text()=''Close'']"]}},"headingXpath":"//*[@id=''template1:r1:1:r7:1:r1:0:r1:1:tablePanelGrp'']/div[7]/table/tbody/tr[3]/td[1]/span","xpath":"//*[@id=''template1:r1:1:r7:1:r1:0:r1:1:t4'']"}]}',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityLogin')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityLogin'),
'{"DataContextId":"1","DataContextName":"EligibilityLogin","Click":null,"Xpaths":[{"UsernameXpath":"//*[@id=''username'']","PasswordXpath":"//*[@id=''password'']","LoginButtonXpath":"/html/body/ui-view/div/div/ui-view/div[2]/div/div[2]/div[1]/form/div[4]/button","OtpInputXpath":"","OtpSubmitXpath":"","PreSteps":[],"PostSteps":[],"OtpXpath":""}]}',
1,4)

ELSE
print 'not found'

IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityPatientVerification')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityPatientVerification'),
'{"Xpaths":[{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''memberInfoSection'']/div[2]"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''eligibilityInfoSection'']/div[2]"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''groupInfoSection'']/div[2]"},{"AdditonalInfo":{"Click":null,"fileds":["Name/Plans","Status"],"type":"headless"},"xpath":"//*[@id=''family-info'']/div/div[2]/table"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''insuranceInfoSection'']/div[2]"}]}',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityServiceTreatmentHistory')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityServiceTreatmentHistory'),
'{"Xpaths":[{"AdditonalInfo":{"Click":null,"fileds":["ProcedureCode","Tooth_Quadrant","Surfaces","Description","DateOfService"]},"xpath":"/html/body/ui-view/ui-view/div/div[4]/div[2]/div/div[4]/div/procedure-history/div/div[2]/div[3]/div/div[2]/div[2]/div"}]}',
1,4)

ELSE
print 'not found'

IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityMaximums')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityMaximums'),
'{"Xpaths":[{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''planInfoSection'']"}]}',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityBenefits')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Dental Network of America'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityBenefits'),
'{"waitTime":0,"MultipleXpaths":[[{"AdditonalInfo":{"Click":["//*[@id=''benefitBlock'']/div[2]/div[5]"],"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[1]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[1]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[1]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[1]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[1]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[1]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[1]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate0'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate0'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator0'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate0'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate0'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate0'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate0'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate0'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate0'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate0'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[2]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[2]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[2]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[2]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[2]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[2]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[2]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate1'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate1'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator1'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate1'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate1'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate1'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate1'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate1'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate1'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate1'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[3]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[3]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[3]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[3]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[3]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[3]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[3]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate2'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate2'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator2'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate2'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate2'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate2'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate2'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate2'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate2'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate2'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[4]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[4]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[4]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[4]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[4]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[4]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[4]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate3'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate3'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator3'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate3'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate3'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate3'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate3'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate3'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate3'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate3'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[5]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[5]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[5]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[5]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[5]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[5]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[5]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate4'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate4'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator4'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate4'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate4'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate4'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate4'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate4'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate4'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate4'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[6]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[6]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[6]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[6]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[6]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[6]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[6]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate5'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate5'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator5'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate5'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate5'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate5'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate5'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate5'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate5'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate5'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[7]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[7]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[7]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[7]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[7]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[7]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[7]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate6'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate6'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator6'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate6'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate6'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate6'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate6'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate6'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate6'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate6'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[8]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[8]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[8]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[8]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[8]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[8]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[8]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate7'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate7'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator7'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate7'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate7'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate7'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate7'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate7'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate7'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate7'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[9]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[9]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[9]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[9]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[9]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[9]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[9]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate8'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate8'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator8'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate8'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate8'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate8'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate8'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate8'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate8'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate8'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[10]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[10]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[10]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[10]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[10]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[10]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[10]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate9'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate9'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator9'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate9'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate9'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate9'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate9'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate9'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate9'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate9'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[11]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[11]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[11]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[11]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[11]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[11]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[11]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate10'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate10'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator10'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate10'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate10'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate10'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate10'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate10'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate10'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate10'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[12]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[12]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[12]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[12]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[12]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[12]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[12]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate11'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate11'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator11'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate11'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate11'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate11'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate11'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate11'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate11'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate11'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[13]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[13]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[13]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[13]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[13]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[13]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[13]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate12'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate12'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator12'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate12'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate12'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate12'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate12'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate12'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate12'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate12'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[14]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[14]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[14]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[14]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[14]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[14]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[14]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate13'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate13'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator13'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate13'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate13'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate13'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate13'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate13'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate13'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate13'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[15]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[15]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[15]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[15]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[15]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[15]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[15]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate14'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate14'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator14'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate14'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate14'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate14'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate14'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate14'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate14'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate14'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[16]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[16]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[16]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[16]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[16]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[16]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[16]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate15'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate15'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator15'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate15'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate15'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate15'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate15'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate15'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate15'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate15'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[17]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[17]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[17]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[17]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[17]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[17]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[17]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate16'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate16'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator16'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate16'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate16'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate16'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate16'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate16'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate16'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate16'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[18]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[18]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[18]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[18]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[18]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[18]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[18]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate17'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate17'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator17'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate17'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate17'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate17'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate17'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate17'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate17'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate17'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[19]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[19]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[19]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[19]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[19]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[19]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[19]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate18'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate18'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator18'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate18'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate18'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate18'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate18'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate18'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate18'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate18'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[20]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[20]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[20]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[20]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[20]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[20]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[20]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate19'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate19'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator19'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate19'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate19'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate19'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate19'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate19'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate19'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate19'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[21]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[21]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[21]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[21]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[21]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[21]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[21]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate20'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate20'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator20'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate20'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate20'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate20'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate20'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate20'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate20'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate20'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[22]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[22]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[22]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[22]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[22]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[22]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[22]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate21'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate21'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator21'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate21'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate21'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate21'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate21'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate21'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate21'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate21'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[23]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[23]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[23]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[23]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[23]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[23]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[23]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate22'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate22'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator22'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate22'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate22'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate22'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate22'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate22'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate22'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate22'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[24]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[24]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[24]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[24]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[24]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[24]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[24]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate23'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate23'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator23'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate23'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate23'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate23'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate23'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate23'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate23'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate23'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}],[{"AdditonalInfo":{"Click":null,"fileds":"Category"},"xpath":"//*[@id=''accorDiv'']/div/div[25]//*[@id=''CategoryName'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[25]//*[@id=''InNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[25]//*[@id=''InNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"Outofnetwork"},"xpath":"//*[@id=''accorDiv'']/div/div[25]//*[@id=''OutNetworkPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"OutNetworkDeductible"},"xpath":"//*[@id=''accorDiv'']/div/div[25]//*[@id=''OutNetworkDeductibleMetPercent'']"},{"AdditonalInfo":{"Click":null,"fileds":"LastDateOfService"},"xpath":"//*[@id=''accorDiv'']/div/div[25]//*[@id=''LastDateOfService'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitationText"},"xpath":"//*[@id=''accorDiv'']/div/div[25]//*[@id=''FrequencyLimitationText'']"},{"AdditonalInfo":{"Click":null,"fileds":"FrequencyLimitations"},"xpath":"//*[@id=''Cate24'']//*[@id=''FrequencyLimitations'']"},{"AdditonalInfo":{"Click":null,"fileds":"WaitingPeriod"},"xpath":"//*[@id=''Cate24'']//*[@id=''Limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":null,"fileds":[]},"xpath":"//*[@id=''accumulator24'']"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimit"},"xpath":"//*[@id=''Cate24'']//*[@id=''Limitations'']/span[2]/dd"},{"AdditonalInfo":{"Click":null,"fileds":"AgeLimitationText"},"xpath":"//*[@id=''Cate24'']//*[@id=''Limitations'']/span[2]/dt"},{"AdditonalInfo":{"Click":null,"fileds":"OtherLimitations"},"xpath":"//*[@id=''Cate24'']//*[text()=''Other Limitations:'']/following::dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''Cate24'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''Cate24'']//*[@id=''OutOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''Cate24'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":null,"fileds":"OutOfInNetworkDeductible"},"xpath":"//*[@id=''Cate24'']//*[@id=''OutOfPocketCosts'']/div/span[2]/dd[2]"}]],"Xpaths":null}',
1,4)

ELSE
print 'not found'




SELECT * FROM EligibilityScrapperXpathMapping

Update EligibilityScrapperXpathMapping
set Xpath = '{      "Search": {          "Settings": {              "PreSteps": {                  "Clicks": [                      "//*[text()=''Switch office'']"                  ],                  "AdditonalInfo": {}              },              "SearchButtonXpath": "",              "SearchFilter": {},              "PostSteps": {                  "Clicks": [                      "//*[@id=''template1:pt_lv1::db'']"                  ],                  "AdditonalInfo": {                      "sleep": 7                  }              }          },          "Queries": [              {                  "Data": "SearchKey",                  "Xpath": "//*[@placeholder=''Search'']",                  "AdditonalInfo": {}              }          ]      }  }'
where datacontextid = 205



select * from EligibilityScrapperXpathMapping
update EligibilityScrapperXpathMapping
set XPath ='{
    "flatten": true,
    "MultiplElements": {
        "multiple_elements_xpath": "//*[@class=''x271 xfh'']",
        "action": "Click"
    },
    "Xpaths": [
        {
            "AdditonalInfo": {
                "Click": [
                    "//*[text()=''PDF'']"
                ],
                "fileds": [
                    "Enrollee_ClaimId",
                    "EnrolleeId"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:t3x3'']/tbody/tr/td[1]/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "EnrolleeName",
                    "DateOfBirth",
                    "PatientName",
                    "PatientDateOfBirth"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:t3x3'']/tbody/tr/td[2]/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "Relationship",
                    "PlanName",
                    "PlanNumber"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:t3x3'']/tbody/tr/td[3]/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "Billing_Id",
                    "Name"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:t3xa3'']/tbody/tr/td/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "Rendering_Id",
                    "Rendering_Name",
                    "ProviderStatus",
                    "Lic#"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:t3ax3'']/tbody/tr/td/table"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "Claim_Status"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:tl6'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:tl6_c'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:tl6_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": [
                    "DirectDepositReference",
                    "Deposit_Status"
                ]
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:tl116_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:tlas6_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:tqql6_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:tlt6_d'']"
        },
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": "Notes"
            },
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:tl2'']/tbody"
        },
        {
            "AdditonalInfo": {
                "Click": [
                    "//*[text()=''Claim information'']"
                ],
                "fileds": ""
            },
            "xpath": ""
        }
    ]
}'

where DataContextId=207




select * from EligibilityScrapperXpathMapping
update EligibilityScrapperXpathMapping
set XPath ='{
    "MultiplElements": {
        "multiple_elements_xpath": "//*[@class=''x271 xfh'']",
        "action": "Click"
    },
    "Xpaths": [
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": []
            },
            "headingXpath": "//*[@id=''template1:r1:1:r4:2:r1:0:ot23'']/label",
            "xpath": "//*[@id=''template1:r1:1:r4:2:r1:0:trl1'']"
        },
        {
            "AdditonalInfo": {
                "Click": [
                    "//*[text()=''Claim information'']"
                ],
                "fileds": []
            },
            "xpath": ""
        }
    ]
}'

where DataContextId=208


UPDATE EligibilityScrapperXpathMapping
SET XPath ='{
    "Xpaths": [
        {
            "AdditonalInfo": {
                "Click": null,
                "fileds": "Status"
            },
            "xpath": "//*[@id=''template1:r1:1:r4:0:t1::db'']/table/tbody/tr/td[7]/span/span"
        },
        {
            "AdditonalInfo": {
                "Click": [
                    "//*[@id=''template1:r1:1:r4:0:t1:0:ot166'']"
                ],
                "fileds": [
                    "empty",
                    "PatientName",
                    "EnrolleeId",
                    "ClaimNumber",
                    "DateOfService",
                    "PatientPays",
                    "DeltaDentalPays",
                    "empty"
                ],
                "type": "headless"
            },
            "xpath": "//*[@id=''template1:r1:1:r4:1:t1::db'']/table"
        }
    ]
}'
WHERE DataContextId =206




IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityLogin')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityLogin'),
'{"Click":null,"Xpaths":[{"UsernameXpath":"//input[@name=''userId'']","PasswordXpath":"//input[@name=''password'']","LoginButtonXpath":"//button[text()=''Sign In'']","OtpInputXpath":"","OtpSubmitXpath":"","PreSteps":[],"PostSteps":[],"OtpXpath":""}]}',
1,4)

ELSE
print 'not found'





IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityMaximums')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityMaximums'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[text()=''Member'']","//*[text()=''Maximums and Deductibles'']"],"fileds":["Type","Category","Name","CategoryHistoryAccumator","Individual","Family","AccumPeriodFrom","AccumPeriodFrom"],"type":"headless"},"xpath":"//*[@id=''printmax'']/app-maximums-deductibles/table"}]}',
1,4)

ELSE
print 'not found'


                                                                      
IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityPatientVerification')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityPatientVerification'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[@id=''tab-header'']//*[contains(text(),''PPO Dentist'')]"],"fileds":[]},"headingname":"FamilyMembers","xpath":"//*[@id=''main-home'']/div/app-memberdetails-benefits/div[1]/section[1]/div/div[2]/table"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-memberdetails-benefits/div[1]/section[3]/div[2]/div[1]/div/img"],"fileds":"CobInformation"},"xpath":"//*[@id=''printcob'']/app-coordination-benefits/section"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-memberdetails-benefits/div[1]/section[3]/div[1]/div[1]/div/img"],"fileds":"ClientBenefitInformation"},"xpath":"//*[@id=''printcbi'']/app-claim-benefit-information/section/div"}]}',
1,4)

ELSE
print 'not found'


IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityServiceTreatmentHistory')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityServiceTreatmentHistory'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[@id=''prtRP'']/div[1]"],"fileds":["Procedures","Eligible","ServiceDates"]},"xpath":"//*[@id=''routineprocedures'']/table"}]}',
1,4)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityAgeLimitation')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityAgeLimitation'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-memberdetails-benefits/div[1]/section[2]/div[5]/div[1]","//*[@id=''main-home'']/div/app-memberdetails-benefits/div[1]/section[3]/div[3]/div[1]"],"fileds":"AgeLimitations"},"xpath":"//*[@id=''printagelimit'']/app-eligibility-age-limitations"}]}',
1,4)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityBenefits')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityBenefits'),
'{"MultiplElements":{"Searchlist":null,"action":"Sendkeys","InputElementsXpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[1]/div[1]/form/input","SearchButtonXpath":"//*[text()=''Find'']"},"Xpaths":[{"AdditonalInfo":{"Click":[],"fileds":"procedure"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[2]/div[1]"},{"AdditonalInfo":{"Click":[],"fileds":"procedureCovered"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[2]/div[2]/span"},{"AdditonalInfo":{"Click":[],"fileds":"procedureWaitingPeriod"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[2]/div[3]"},{"AdditonalInfo":{"Click":[],"fileds":"procedureWaitingPeriodMetDate"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[2]/div[4]"},{"AdditonalInfo":{"Click":[],"fileds":"SubProcedureName"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[3]/div[1]"},{"AdditonalInfo":{"Click":[],"fileds":"SubprocedureCovered"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[3]/div[2]/span"},{"AdditonalInfo":{"Click":[],"fileds":"SubprocedureWaitingPeriod"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[3]/div[3]"},{"AdditonalInfo":{"Click":[],"fileds":"SubprocedureWaitingPeriodMetDate"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[3]/div[4]"},{"AdditonalInfo":{"Click":[],"fileds":"procedureCode"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[4]/div[1]"},{"AdditonalInfo":{"Click":[],"fileds":"procedureCodeCovered"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[4]/div[2]"},{"AdditonalInfo":{"Click":[],"fileds":"procedureCodeWaitingPeriod"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[4]/div[3]"},{"AdditonalInfo":{"Click":[],"fileds":"procedureCodeWaitingPeriodMetDate"},"xpath":"//*[@id=''coverages'']/app-exclusions-limitations/div/div[4]/div[4]"}]}',
1,4)

ELSE
print 'not found'



IF EXISTS(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityOtherProvisions')
AND EXISTS(SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit')

INSERT INTO [dbo].[EligibilityScrapperXpathMapping] (EligibilityPayorInfoId,DataContextId,XPath,IsActive,ProductCategoryId) 
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit'),
(SELECT ID FROM PmsSourceDataContext WHERE DataContextName ='EligibilityOtherProvisions'),
'{"Xpaths":[{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-memberdetails-benefits/div[1]/section[2]/div[6]/div[1]"],"fileds":["Category","ExclusionsAndLimitations"],"type":"headless"},"headingname":"ExclusionsAndLimitations","xpath":"//*[@id=''printexcl'']/app-exclusions-limitations-details/table"},{"AdditonalInfo":{"Click":["//*[text()=''Admin'']","//*[text()=''Contact Us'']","//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[2]/div[1]"],"fileds":""},"xpath":""},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofMichiganClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Dental of Michigan'']/table[1]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofMichiganClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Dental of Michigan'']/table[2]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofMichiganClaimMailingAddressCMS"},"xpath":"//*[@id=''Dental of Michigan'']/table[3]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[3]/div[1]"],"fileds":"DeltaDentalofArizonaClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Arizona'']/table[1]/tr[2]/td[2]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofArizonaClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Arizona'']/table[2]/tr[2]/td[2]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofArizonaClaimMailingAddressPatientDirectDiscountPlan"},"xpath":"//*[@id=''Delta Dental of Arizona'']/table[3]/tr[2]/td[2]/p"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[4]/div[1]"],"fileds":"DeltaDentalofArkansasClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Arkansas'']/table[1]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofArkansasClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Arkansas'']/table[2]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofArkansasClaimMailingAddressAllOtherGroups"},"xpath":"//*[@id=''Delta Dental of Arkansas'']/table[3]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofArkansasClaimMailingAddressCMS"},"xpath":"//*[@id=''Delta Dental of Arkansas'']/table[4]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofArkansasClaimMailingAddressMedicaidDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Arkansas'']/table[5]/tr[2]/td[3]"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[5]"],"fileds":"DeltaDentalofKentuckyClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Kentucky'']/table[1]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofKentuckyClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Kentucky'']/table[2]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[6]/div[1]"],"fileds":"DeltaDentalofMinnesotaClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Minnesota'']/table[1]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofMinnesotaClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Minnesota'']/table[2]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[7]/div[1]"],"fileds":"DeltaDentalofNebraskaClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Nebraska'']/table[1]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofNebraskaClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Nebraska'']/table[2]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[8]/div[1]"],"fileds":"DeltaDentalofNewMexicoClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Delta Dental of New Mexico'']/table[1]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofNewMexicoClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Delta Dental of New Mexico'']/table[2]/tr[2]/td[3]"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[9]/div[1]"],"fileds":"DeltaDentalofNorthCarolinaClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Delta Dental of North Carolina'']/table[1]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofNorthCarolinaClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Delta Dental of North Carolina'']/table[2]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[10]/div[1]"],"fileds":"DeltaDentalofSouthDakotaClaimMailingAddressCMS"},"xpath":"//*[@id=''Delta Dental of South Dakota'']/table/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[11]/div[1]"],"fileds":"DeltaDentalofTennesseeClaimMailingAddressGroupDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Tennessee'']/table[1]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofTennesseeClaimMailingAddressIndividualDentalBenefits"},"xpath":"//*[@id=''Delta Dental of Tennessee'']/table[2]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":null,"fileds":"DeltaDentalofTennesseeClaimMailingAddressCMS"},"xpath":"//*[@id=''Delta Dental of Tennessee'']/table[3]/tr[2]/td[3]/p"},{"AdditonalInfo":{"Click":["//*[@id=''main-home'']/div/app-contact-us/html/div/section/div/div[12]/div[1]"],"fileds":"DeltaDentalofWisconsinClaimMailingAddressCMS"},"xpath":"//*[@id=''Delta Dental of Wisconsin'']/table/tr[2]/td[3]/p"}]}',
1,4)

ELSE
print 'not found'





INSERT INTO EligibilityScrapperSearchParams (EligibilityPayorInfoId,JsonSettings,IsActive,ProductCategoryId)
VALUES ((SELECT ID FROM EligibilityPayorInfo WHERE name ='Delta Dental Toolkit'),
'{"Search":{"Settings":{"PreSteps":{"Clicks":["//button[text()=''Change Member'']"],"AdditonalInfo":{"aftersleep":5}},"SearchButtonXpath":"//button[text()=''Search'']","SearchFilter":{"XpathGenerator":{"XPath":"//*[contains(text(),''%s'')]","DataKey":"FirstName","wait":"//*[@id=''patient-name'']","caps":true}},"PostSteps":{"AdditonalInfo":{},"Clicks":[]}},"Queries":[{"Data":"SubscriberId","Xpath":"//input[@id=''memberId'']"},{"Data":"SubscriberFirstName","Xpath":"//input[@id=''first-name'']"},{"Data":"SubscriberLastName","Xpath":"//input[@id=''last-name'']"},{"Data":"SubscriberBirthDate","Xpath":"//input[@id=''dob'']"}]}}',
1, 4)


SELECT * FROM EligibilityScrapperXpathMapping

UPDATE EligibilityScrapperXpathMapping
SET XPath='{"MultiplElements":{"Searchlist":null,"action":"Sendkeys","InputElementsXpath":"//*[@id=''procedureCode'']","SearchButtonXpath":"//button[@type=''submit'']"},"Xpaths":[{"AdditonalInfo":{"Click":[],"fileds":"codeDescription"},"xpath":"//*[@id=''codeDescription'']"},{"AdditonalInfo":{"Click":[],"fileds":"WaitingPeriod"},"xpath":"//*[@id=''limitations'']/span[1]/dd"},{"AdditonalInfo":{"Click":[],"fileds":"AlternateBenefitProcedure"},"xpath":"//*[@id=''limitations'']/span[4]/dd"},{"AdditonalInfo":{"Click":[],"fileds":"InNetworkCoinsurance"},"xpath":"//*[@id=''outOfPocketCosts'']/div/span[1]/dd[1]"},{"AdditonalInfo":{"Click":[],"fileds":"InNetworkDeductible"},"xpath":"//*[@id=''outOfPocketCosts'']/div/span[1]/dd[2]"},{"AdditonalInfo":{"Click":[],"fileds":"OutOfNetworkCoinsurance"},"xpath":"//*[@id=''outOfPocketCosts'']/div/span[2]/dd[1]"},{"AdditonalInfo":{"Click":[],"fileds":"OutOfNetworkDeductible"},"xpath":"//*[@id=''outOfPocketCosts'']/div/span[2]/dd[2]"},{"AdditonalInfo":{"Click":[],"fileds":"Copay"},"xpath":"//*[@id=''outOfPocketCosts'']/span/dd"},{"AdditonalInfo":{"Click":[],"fileds":"Other","waitTime":0},"xpath":"//*[@id=''procCodeSummary'']/div[2]"},{"AdditonalInfo":{"Click":[],"fileds":"procedureCode","waitTime":0},"xpath":"//*[contains(text(),''Procedure Code:'')]"},{"AdditonalInfo":{"Click":["//button[text()=''Close'']"],"fileds":[]},"xpath":""}]}'
WHERE EligibilityPayorInfoId =24 AND DataContextId = 195