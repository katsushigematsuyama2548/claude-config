---
name: doc-ship
description: .claude/ への変更をブランチ作成 → PR → マージで反映する。/retro の最後に呼び出す。グローバル（~/.claude/）とプロジェクト（.claude/）の両方に対応。
---

# Doc Ship Skill

## Overview

`/retro` で承認された `.claude/` への変更を GitHub 経由で安全に反映する。

```
変更ファイルを確認
  ↓
対象リポジトリを判定（グローバル / プロジェクト）
  ↓
ブランチ作成
  ↓
コミット
  ↓
PR 作成
  ↓
マージ
```

---

## Step 1: 変更ファイルの確認

変更対象がどちらに属するかを確認する：

| 変更先 | リポジトリ | 作業ディレクトリ |
|--------|-----------|----------------|
| `~/.claude/` 以下 | `claude-config` | `~/.claude/` |
| プロジェクトの `.claude/` 以下 | そのプロジェクトの src リポジトリ | `~/Documents/dev/{name}/src/` |

両方に変更がある場合は、グローバルとプロジェクトで**それぞれ別に**ブランチ・PR を作成する。

---

## Step 2: グローバル変更の ship（~/.claude/ が対象の場合）

```bash
cd ~/.claude
git status
```

ブランチ名は `retro/YYYY-MM-DD` 形式：

```bash
cd ~/.claude
git checkout -b retro/2026-04-25
```

```bash
cd ~/.claude
git add -A
```

```bash
cd ~/.claude
git commit -m "retro: （変更内容の要約）"
```

```bash
cd ~/.claude
git push -u origin retro/2026-04-25
```

PR を作成（変更内容の要約を本文に記載）：

```bash
gh pr create --repo katsushigematsuyama2548/claude-config \
  --title "retro: （変更内容の要約）" \
  --body "## 変更内容\n\n（/retro で承認された提案の一覧）" \
  --base main \
  --head retro/2026-04-25
```

マージ：

```bash
gh pr merge --repo katsushigematsuyama2548/claude-config \
  --squash --delete-branch
```

main に戻る：

```bash
cd ~/.claude
git checkout main
git pull
```

---

## Step 3: プロジェクト変更の ship（.claude/ が対象の場合）

現在のプロジェクト名を確認し、作業ディレクトリに移動する。

ブランチ名は `claude/retro/YYYY-MM-DD` 形式：

```bash
cd ~/Documents/dev/{PROJECT_NAME}/src
git checkout -b claude/retro/2026-04-25
```

```bash
git add .claude/
```

```bash
git commit -m "claude: retro（変更内容の要約）"
```

```bash
git push -u origin claude/retro/2026-04-25
```

```bash
gh pr create \
  --title "claude: retro（変更内容の要約）" \
  --body "## 変更内容\n\n（/retro で承認された提案の一覧）" \
  --base main \
  --head claude/retro/2026-04-25
```

```bash
gh pr merge --squash --delete-branch
```

```bash
git checkout main
git pull
```
