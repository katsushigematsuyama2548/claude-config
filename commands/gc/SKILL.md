---
name: gc
description: ~/.claude/ とプロジェクト .claude/ の陳腐化ファイルを検出し、削除提案 PR を 1 ファイル 1 PR で GitHub に作成する。PR マージ = 削除承認、クローズ = 保持。
---

# GC (Garbage Collection) Skill

## 概要

60日以上更新されていない skills/rules/docs ファイル、90日以上更新されていない agents ファイルを検出し、GitHub PR を通じて削除を提案する。

```
陳腐化ファイルを検出
  ↓
ユーザーに一覧を確認
  ↓
承認されたファイルそれぞれに 1 PR を作成
（PR マージ → ファイル削除・ブランチ自動削除）
（PR クローズ → 保持）
```

---

## Step 1: 陳腐化ファイルの検出

### グローバル（~/.claude/）

以下のディレクトリを対象にする：

| ディレクトリ | 閾値 |
|-------------|------|
| `~/.claude/skills/` | 60日 |
| `~/.claude/commands/` | 60日 |
| `~/.claude/agents/` | 90日 |

```bash
find ~/.claude/skills ~/.claude/commands ~/.claude/agents -name "*.md" -not -path "*/MEMORY*"
```

各ファイルの最終更新日を確認：

```bash
git -C ~/.claude log -1 --format="%ai" -- {FILE_PATH}
```

git 履歴がないファイルは `stat` で確認：

```bash
stat -f "%Sm" -t "%Y-%m-%d" {FILE_PATH}
```

### プロジェクト（.claude/）

現在のプロジェクトディレクトリ（例: `~/Documents/dev/{PROJECT_NAME}`）がある場合：

| ディレクトリ | 閾値 |
|-------------|------|
| `.claude/skills/` | 60日 |
| `.claude/commands/` | 60日 |
| `.claude/rules/` | 60日 |
| `.claude/docs/` | 60日 |
| `.claude/agents/` | 90日 |

---

## Step 2: 検出結果の表示

陳腐化ファイルを一覧表示する：

```
## 陳腐化ファイル一覧（GC 候補）

### グローバル (~/.claude/)
| ファイル | 最終更新 | 経過日数 | 閾値 |
|---------|---------|---------|------|
| skills/vercel-react-native-skills/SKILL.md | 2025-11-01 | 175日 | 60日 |
| agents/expo-mobile-engineer.md | 2025-10-15 | 192日 | 90日 |

### プロジェクト (.claude/)
（なし）

PR を作成しますか？ (y / n / 個別指定)
```

**0件の場合**: 「陳腐化ファイルは見つかりませんでした。」と伝えて終了する。

---

## Step 3: PR の作成（1 ファイル 1 PR）

ユーザーが承認したファイルそれぞれについて、以下を実行する。

### グローバルファイルの場合

ブランチ名: `gc/{YYYY-MM-DD}/{sanitized-filename}`

```bash
cd ~/.claude
git checkout main
git pull
git checkout -b gc/2026-04-25/skills-vercel-react-native-skills
```

```bash
cd ~/.claude
git rm -r skills/vercel-react-native-skills/
```

```bash
cd ~/.claude
git commit -m "gc: remove stale skills/vercel-react-native-skills (175 days)"
```

```bash
cd ~/.claude
git push -u origin gc/2026-04-25/skills-vercel-react-native-skills
```

```bash
gh pr create \
  --repo katsushigematsuyama2548/claude-config \
  --title "gc: remove stale skills/vercel-react-native-skills" \
  --body "## 削除提案

**ファイル**: \`skills/vercel-react-native-skills/\`
**最終更新**: 2025-11-01（175日前）
**閾値**: 60日

このファイルは60日以上更新されておらず、使用されていない可能性があります。

- **マージ** → ファイルを削除
- **クローズ** → 保持（必要であれば内容を更新してください）" \
  --base main \
  --head gc/2026-04-25/skills-vercel-react-native-skills
```

PR 作成後、main ブランチに戻る：

```bash
cd ~/.claude
git checkout main
```

### プロジェクトファイルの場合

ブランチ名: `claude/gc/{YYYY-MM-DD}/{sanitized-filename}`

手順はグローバルと同様。`gh pr create` 時に `--repo` は不要（プロジェクトの git remote から自動検出）。

---

## Step 4: 完了報告

全 PR を作成したら報告する：

```
## GC 完了

作成した PR：
- https://github.com/katsushigematsuyama2548/claude-config/pull/XX — gc: remove stale skills/vercel-react-native-skills
- https://github.com/katsushigematsuyama2548/claude-config/pull/YY — gc: remove stale agents/expo-mobile-engineer

各 PR をレビューして：
- マージ → ファイル削除（ブランチも自動削除）
- クローズ → 保持

次回 /gc は {今日から60日後} の実行を推奨します。
```

---

## 注意事項

- `CLAUDE.md`、`settings.json`、`README.md`、`.gitignore` は対象外
- `templates/` 配下は対象外
- `commands/` 配下のスキル自身（gc, retro, doc-ship, newproject）は対象外
- PR を作成するだけで、実際のファイル削除はマージ時に行われる
