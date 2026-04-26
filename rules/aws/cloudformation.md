---
paths:
  - "**/src/aws/cloudformation/**"
---

# CloudFormation 規約

## スタック命名規則

`{システム名}-{環境名}-{スタック名}` 形式とする。

```
例: order-prd-lambda
    user-uat-api
```

## 環境管理

dev / uat / prd の3環境を対象とする。
テンプレートファイルは全環境共通とし、環境差異は Parameters で吸収する。

他スタックから ImportValue できる値は ImportValue を使う。
ImportValue できない値（Export されていない VPC エンドポイントIDなど）は Parameter で毎回指定する。

```yaml
Parameters:
  Env:
    Type: String
    AllowedValues: [dev, uat, prd]
  VpcEndpointId:
    Type: String
    Description: "ImportValueできない場合はParameterで環境ごとに指定する"
```

## リソース命名規則

リソース名（論理IDおよび物理リソース名）は `{アカウントエイリアス}-{システム名}-{環境名}-{リソース名}` 形式とする。
アカウントエイリアスは数字のアカウントIDではなく英語名を Parameter で受け取る。

```yaml
Parameters:
  AccountAlias:
    Type: String
  SystemName:
    Type: String
  Env:
    Type: String
    AllowedValues: [dev, uat, prd]

Resources:
  OrderProcessorLambda:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AccountAlias}-${SystemName}-${Env}-order-processor"
```

## 他スタックのリソース参照

VPC・サブネット・セキュリティグループなど他スタックで管理するリソースは `ImportValue` で参照する。ハードコード禁止。
ただし、ImportValue は参照先スタックが Outputs で Export しているものだけ使用できる。Export されていないリソースには使えないので注意する。

```yaml
VpcId: !ImportValue "network-prd-VpcId"
SubnetId: !ImportValue "network-prd-PrivateSubnetId"
```

## 機密情報パラメーター

パスワード・APIキーなど機密情報は `NoEcho: true` を付ける。

```yaml
Parameters:
  DbPassword:
    Type: String
    NoEcho: true
```

## Parameter Store・Lambda 環境変数

Parameter Store のパスや Lambda の環境変数はハードコードせず、CloudFormation の Parameters で指定する。
テンプレートを変えずにパラメーター更新だけで値を変更できるようにするため。

## Lambda

Lambda は原則 VPC 内に配置する（VpcConfig を設定する）。

## スタック分割方針

**システム固有のリソースとシステム固有でないリソースは別スタックにする。**
全ベンダー共通APIなど特定システムに属さないリソースは、システムのスタックとは分離して管理する。
