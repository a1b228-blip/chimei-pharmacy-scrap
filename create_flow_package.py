import os
import zipfile
import json
import uuid

flow_id = "51b922a2-5d2e-4675-a589-8397e657ad1a"
flow_name = "藥劑科報廢表單_Teams主管審核流程"
site_url = "https://cmh2400.sharepoint.com/sites/msteams_d944ec"
list_id = "20d0cec4-6b56-45d7-83c0-a7d85c6d00af"

# 1. definition.json
definition = {
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
}

# 2. manifest.json
manifest = {
  "schema": "1.0",
  "details": {
    "displayName": flow_name,
    "description": "藥劑科報廢表單自動推播至主管 Teams 審核並回寫狀態",
    "creator": "B305W2@chimei.org.tw",
    "sourceEnvironment": "Default-24de0681-c8f7-46e8-8da7-1f5b393d834d"
  },
  "resources": {
    flow_id: {
      "type": "Microsoft.ProcessSimple/flows",
      "suggestedCreationType": "New",
      "relationPreferences": [
        "CreateAsNew"
      ],
      "name": flow_name,
      "details": {
        "displayName": flow_name
      },
      "configurableBy": "User"
    },
    "shared_sharepointonline": {
      "type": "Microsoft.PowerApps/apis/connections",
      "suggestedCreationType": "Existing",
      "displayName": "SharePoint Connection",
      "name": "shared_sharepointonline"
    },
    "shared_office365users": {
      "type": "Microsoft.PowerApps/apis/connections",
      "suggestedCreationType": "Existing",
      "displayName": "Office 365 Users Connection",
      "name": "shared_office365users"
    },
    "shared_teams": {
      "type": "Microsoft.PowerApps/apis/connections",
      "suggestedCreationType": "Existing",
      "displayName": "Microsoft Teams Connection",
      "name": "shared_teams"
    }
  }
}

zip_output = "藥劑科報廢表單_Teams主管審核流程_匯入包.zip"
with zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))
    z.writestr(f"Microsoft.ProcessSimple/flows/{flow_id}/definition.json", json.dumps(definition, indent=2, ensure_ascii=False))

print("Created successfully:", zip_output)
