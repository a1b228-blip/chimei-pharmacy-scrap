import os
import zipfile
import json

pkg_dir = "final_flow_package"
workflows_dir = os.path.join(pkg_dir, "Workflows")
other_dir = os.path.join(pkg_dir, "Other")
os.makedirs(workflows_dir, exist_ok=True)
os.makedirs(other_dir, exist_ok=True)

flow_id = "51b922a2-5d2e-4675-a589-8397e657ad1a"
site_url = "https://cmh2400.sharepoint.com/sites/msteams_d944ec"
list_id = "20d0cec4-6b56-45d7-83c0-a7d85c6d00af"

# 1. Workflow JSON
flow_definition = {
  "properties": {
    "connectionReferences": {
      "shared_sharepointonline": {
        "runtimeSource": "embedded",
        "connection": {
          "connectionReferenceLogicalName": "cp_sharedsharepointonline"
        },
        "api": {
          "name": "shared_sharepointonline"
        }
      },
      "shared_office365users": {
        "runtimeSource": "embedded",
        "connection": {
          "connectionReferenceLogicalName": "cp_sharedoffice365users"
        },
        "api": {
          "name": "shared_office365users"
        }
      },
      "shared_teams": {
        "runtimeSource": "embedded",
        "connection": {
          "connectionReferenceLogicalName": "cp_sharedteams"
        },
        "api": {
          "name": "shared_teams"
        }
      }
    },
    "definition": {
      "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
      "contentVersion": "1.0.0.0",
      "parameters": {
        "$connections": {
          "defaultValue": {},
          "type": "Object"
        }
      },
      "triggers": {
        "When_an_item_is_created": {
          "type": "OpenApiConnection",
          "inputs": {
            "host": {
              "connectionName": "shared_sharepointonline",
              "operationId": "GetOnNewItems",
              "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
            },
            "parameters": {
              "dataset": site_url,
              "table": list_id
            },
            "authentication": "@parameters('$connections')['shared_sharepointonline']['connectionId']"
          },
          "recurrence": {
            "frequency": "Minute",
            "interval": 1
          }
        }
      },
      "actions": {
        "Get_manager_(V2)": {
          "runAfter": {},
          "type": "OpenApiConnection",
          "inputs": {
            "host": {
              "connectionName": "shared_office365users",
              "operationId": "ManagerV2",
              "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365users"
            },
            "parameters": {
              "id": "@triggerOutputs()?['body/Author/Email']"
            },
            "authentication": "@parameters('$connections')['shared_office365users']['connectionId']"
          }
        },
        "Post_adaptive_card_and_wait_for_a_response": {
          "runAfter": {
            "Get_manager_(V2)": ["Succeeded"]
          },
          "type": "OpenApiConnectionWebhook",
          "inputs": {
            "host": {
              "connectionName": "shared_teams",
              "operationId": "PostAdaptiveCardAndWaitForResponse",
              "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams"
            },
            "parameters": {
              "poster": "Flow bot",
              "location": "Chat with Flow bot",
              "recipient": "@outputs('Get_manager_(V2)')?['body/mail']",
              "body": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                  {
                    "type": "TextBlock",
                    "text": "🔔 【藥劑科藥品報廢審核通知】",
                    "weight": "Bolder",
                    "size": "Medium",
                    "color": "Attention"
                  },
                  {
                    "type": "FactSet",
                    "facts": [
                      { "title": "申請人：", "value": "@{triggerOutputs()?['body/Author/DisplayName']}" },
                      { "title": "藥品名稱：", "value": "@{triggerOutputs()?['body/OData__x85e5__x54c1__x540d__x7a31_']}" },
                      { "title": "批號：", "value": "@{triggerOutputs()?['body/OData__x6279__x865f_']}" },
                      { "title": "報廢數量：", "value": "@{triggerOutputs()?['body/OData__x5831__x5ee2__x6578__x91cf_']}" },
                      { "title": "報廢原因：", "value": "@{triggerOutputs()?['body/OData__x5831__x5ee2__x539f__x56e0_/Value']}" },
                      { "title": "報廢日期：", "value": "@{triggerOutputs()?['body/OData__x5831__x5ee2__x65e5__x671f_']}" }
                    ]
                  },
                  {
                    "type": "Input.Text",
                    "id": "comment",
                    "placeholder": "請輸入審核意見或退件原因（選填）...",
                    "isMultiline": True
                  }
                ],
                "actions": [
                  {
                    "type": "Action.Submit",
                    "title": "✅ 核准報廢",
                    "data": { "action": "Approve" }
                  },
                  {
                    "type": "Action.Submit",
                    "title": "❌ 退件",
                    "data": { "action": "Reject" }
                  }
                ]
              }
            },
            "authentication": "@parameters('$connections')['shared_teams']['connectionId']"
          }
        },
        "Condition": {
          "runAfter": {
            "Post_adaptive_card_and_wait_for_a_response": ["Succeeded"]
          },
          "type": "If",
          "expression": {
            "equals": [
              "@body('Post_adaptive_card_and_wait_for_a_response')?['data']?['action']",
              "Approve"
            ]
          },
          "actions": {
            "Update_item_Approved": {
              "type": "OpenApiConnection",
              "inputs": {
                "host": {
                  "connectionName": "shared_sharepointonline",
                  "operationId": "PatchItem",
                  "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
                },
                "parameters": {
                  "dataset": site_url,
                  "table": list_id,
                  "id": "@triggerOutputs()?['body/ID']",
                  "item/Title": "@triggerOutputs()?['body/Title']",
                  "item/OData__x5be9__x6838__x72c0__x614b_/Value": "主管已核准",
                  "item/OData__x5099__x8a3b_": "@concat(coalesce(triggerOutputs()?['body/OData__x5099__x8a3b_'], ''), ' [主管審核：核准 - ', coalesce(body('Post_adaptive_card_and_wait_for_a_response')?['data']?['comment'], '無'), ']')"
                },
                "authentication": "@parameters('$connections')['shared_sharepointonline']['connectionId']"
              }
            }
          },
          "else": {
            "actions": {
              "Update_item_Rejected": {
                "type": "OpenApiConnection",
                "inputs": {
                  "host": {
                    "connectionName": "shared_sharepointonline",
                    "operationId": "PatchItem",
                    "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
                  },
                  "parameters": {
                    "dataset": site_url,
                    "table": list_id,
                    "id": "@triggerOutputs()?['body/ID']",
                    "item/Title": "@triggerOutputs()?['body/Title']",
                    "item/OData__x5be9__x6838__x72c0__x614b_/Value": "已退件",
                    "item/OData__x5099__x8a3b_": "@concat(coalesce(triggerOutputs()?['body/OData__x5099__x8a3b_'], ''), ' [主管審核：退件 - ', coalesce(body('Post_adaptive_card_and_wait_for_a_response')?['data']?['comment'], '無'), ']')"
                  },
                  "authentication": "@parameters('$connections')['shared_sharepointonline']['connectionId']"
                }
              }
            }
          }
        }
      }
    },
    "schemaVersion": "1.0.0.0"
  }
}

json_file = os.path.join(workflows_dir, f"PharmacyScrapFlow-{flow_id}.json")
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(flow_definition, f, indent=2, ensure_ascii=False)

# 2. Customizations.xml
customizations_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Entities />
  <Roles />
  <Workflows>
    <Workflow WorkflowId="{{{flow_id}}}" Name="藥劑科報廢表單_Teams主管審核流程">
      <JsonFileName>/Workflows/PharmacyScrapFlow-{flow_id}.json</JsonFileName>
      <Type>1</Type>
      <Subprocess>0</Subprocess>
      <Category>5</Category>
      <Mode>0</Mode>
      <Scope>4</Scope>
      <OnDemand>0</OnDemand>
      <TriggerOnCreate>0</TriggerOnCreate>
      <TriggerOnDelete>0</TriggerOnDelete>
      <AsyncAutodelete>0</AsyncAutodelete>
      <SyncWorkflowLogOnFailure>0</SyncWorkflowLogOnFailure>
      <StateCode>1</StateCode>
      <StatusCode>2</StatusCode>
      <RunAs>1</RunAs>
      <IsTransacted>1</IsTransacted>
      <IntroducedVersion>1.0.0.0</IntroducedVersion>
      <IsCustomizable>1</IsCustomizable>
      <BusinessProcessType>0</BusinessProcessType>
      <IsCustomProcessingStepAllowedForOtherPublishers>1</IsCustomProcessingStepAllowedForOtherPublishers>
      <ModernFlowType>0</ModernFlowType>
    </Workflow>
  </Workflows>
  <FieldSecurityProfiles />
  <Templates />
  <EntityMaps />
  <EntityRelationships />
  <OrganizationSettings />
  <optionsets />
  <CustomControls />
  <SolutionPluginAssemblies />
  <EntityDataProviders />
  <Languages>
    <Language>1033</Language>
  </Languages>
</ImportExportXml>
"""

with open(os.path.join(other_dir, "Customizations.xml"), "w", encoding="utf-8") as f:
    f.write(customizations_xml)

# 3. Solution.xml
solution_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<ImportExportXml version="9.2.26084.147" SolutionPackageVersion="9.2" languagecode="1033" generatedBy="CrmLive" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26084.147" OrganizationSchemaType="Standard" CRMServerServiceabilityVersion="9.2.26084.00147">
  <SolutionManifest>
    <UniqueName>PharmacyScrapApprovalFlow</UniqueName>
    <LocalizedNames>
      <LocalizedName description="藥劑科報廢表單_Teams主管審核方案" languagecode="1033" />
    </LocalizedNames>
    <Descriptions>
      <Description description="藥劑科報廢表單自動推播至主管 Teams 審核並回寫狀態" languagecode="1033" />
    </Descriptions>
    <Version>1.0.0.0</Version>
    <Managed>0</Managed>
    <Publisher>
      <UniqueName>ChimeiPharmacy</UniqueName>
      <LocalizedNames>
        <LocalizedName description="ChimeiPharmacy" languagecode="1033" />
      </LocalizedNames>
      <Descriptions>
        <Description description="ChimeiPharmacy" languagecode="1033" />
      </Descriptions>
      <EMailAddress xsi:nil="true"></EMailAddress>
      <SupportingWebsiteUrl xsi:nil="true"></SupportingWebsiteUrl>
      <CustomizationPrefix>cp</CustomizationPrefix>
      <CustomizationOptionValuePrefix>71723</CustomizationOptionValuePrefix>
      <Addresses>
        <Address>
          <AddressNumber>1</AddressNumber>
          <AddressTypeCode>1</AddressTypeCode>
        </Address>
      </Addresses>
    </Publisher>
    <RootComponents>
      <RootComponent type="29" id="{{{flow_id}}}" behavior="0" />
    </RootComponents>
    <MissingDependencies />
  </SolutionManifest>
</ImportExportXml>
"""

with open(os.path.join(other_dir, "Solution.xml"), "w", encoding="utf-8") as f:
    f.write(solution_xml)

# 4. 直接打包出標準微軟 Solution ZIP（根目錄直接包含 Solution.xml, Customizations.xml 與 [Content_Types].xml）
content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="xml" ContentType="application/octet-stream" />
  <Default Extension="json" ContentType="application/json" />
</Types>
"""

zip_filename = "藥劑科報廢表單_Teams主管審核流程_安裝包.zip"
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.writestr("solution.xml", solution_xml)
    zipf.writestr("customizations.xml", customizations_xml)
    zipf.writestr("[Content_Types].xml", content_types_xml)
    zipf.write(json_file, f"Workflows/PharmacyScrapFlow-{flow_id}.json")

print(f"Solution ZIP successfully created: {zip_filename}")
