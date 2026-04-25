---
name: newproject
description: 新しいプロジェクトを標準構造で立ち上げる。GitHub リポジトリ作成・ローカルディレクトリ展開・.claude/ テンプレート適用を一括実行する。
---

# New Project Setup

## Step 1: ヒアリング

以下の情報をまとめてユーザーに確認する：

1. **プロジェクト名**（英語・kebab-case 例: `my-app`）
2. **プロジェクト概要**（日本語 1〜2文）
3. **技術スタック**（複数選択可: React Native / Next.js / Swift / Python / その他）
4. **Supabase を使うか**（Yes / No）
5. **Cloudflare Workers を使うか**（Yes / No）
6. **doc リポジトリも作るか**（Yes / No）
7. **GitHub の visibility**（public / private）

ヒアリング完了後、以下の手順を実行する。

## Step 2: ローカルディレクトリ作成

```bash
mkdir ~/Documents/dev/{PROJECT_NAME}
```

```bash
mkdir ~/Documents/dev/{PROJECT_NAME}/src
```

doc リポジトリを作る場合:
```bash
mkdir ~/Documents/dev/{PROJECT_NAME}/doc
```

## Step 3: .claude/ テンプレートをコピー

```bash
cp -r ~/.claude/templates/project-claude ~/Documents/dev/{PROJECT_NAME}/.claude
```

## Step 4: CLAUDE.md を生成

`~/Documents/dev/{PROJECT_NAME}/.claude/CLAUDE.md` を開き、ヒアリング結果で以下を置換する：
- `{PROJECT_NAME}` → 実際のプロジェクト名
- `{PROJECT_DESCRIPTION}` → 実際の概要
- `{TECH_STACK}` → 選択した技術スタック（箇条書き）
- `{GITHUB_USER}` → `katsushigematsuyama2548`
- `{DEV_COMMANDS}` → 技術スタックに応じた開発コマンド
- Supabase を使わない場合 → Supabase セクションごと削除

## Step 5: GitHub リポジトリ作成

```bash
gh repo create {PROJECT_NAME} --{visibility} --description "{PROJECT_DESCRIPTION}"
```

doc リポジトリを作る場合:
```bash
gh repo create {PROJECT_NAME}-docs --{visibility} --description "{PROJECT_DESCRIPTION} - docs"
```

## Step 6: src/ の git 初期化と初回プッシュ

```bash
cd ~/Documents/dev/{PROJECT_NAME}/src
```

```bash
git init
```

```bash
git branch -M main
```

```bash
git remote add origin https://github.com/katsushigematsuyama2548/{PROJECT_NAME}.git
```

```bash
echo "# {PROJECT_NAME}" > README.md
```

```bash
git add README.md
```

```bash
git commit -m "chore: initial setup"
```

```bash
git push -u origin main
```

## Step 7: doc/ の git 初期化と初回プッシュ（作成する場合）

```bash
cd ~/Documents/dev/{PROJECT_NAME}/doc
```

```bash
git init
```

```bash
git branch -M main
```

```bash
git remote add origin https://github.com/katsushigematsuyama2548/{PROJECT_NAME}-docs.git
```

```bash
echo "# {PROJECT_NAME} docs" > README.md
```

```bash
git add README.md
```

```bash
git commit -m "chore: initial setup"
```

```bash
git push -u origin main
```

## Step 8: 完了報告

セットアップ完了後、以下を報告する：
- 作成したディレクトリパス
- GitHub リポジトリ URL（src / doc）
- 次にやること（Supabase Project Ref の設定、技術スタックのインストール等）
