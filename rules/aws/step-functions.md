---
paths:
  - "**/src/aws/step-functions/**"
---

# Step Functions 規約

## 命名規則

ステートマシン名は `{システム名}-{環境名}` 形式とする。

```
例: order-processing-prd
    user-onboarding-uat
```

## 定義ファイル形式

**JSON** で書く。

## クエリ言語

JSONPath ではなく **JSONata** を使用する。
ステートマシン全体に `"QueryLanguage": "JSONata"` を宣言し、各ステートの入出力変換は JSONata 式で記述する。

```json
{
  "Comment": "注文処理ワークフロー",
  "QueryLanguage": "JSONata",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...",
      "Next": "ProcessPayment"
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...",
      "End": true
    }
  }
}
```
