# {PROJECT_NAME}

{PROJECT_DESCRIPTION}

## リポジトリ構造

```
{PROJECT_NAME}/
├── .claude/   → github.com/{GITHUB_USER}/{PROJECT_NAME}-claude
└── src/       → github.com/{GITHUB_USER}/{PROJECT_NAME}
```

## .claude/ 構造

```
.claude/
├── CLAUDE.md          ← このファイル（目次）
├── settings.json
├── rules/             ← コーディングルール（種別ごとに分割）
│   ├── git.md
│   ├── testing.md
│   └── security.md
├── docs/              ← プロジェクトドキュメント（ドメイン知識）
│   ├── domain/        ← 用語・概念辞書
│   ├── decision/      ← ADR（設計意思決定の記録）
│   ├── architecture/  ← アーキテクチャ・構成図
│   ├── runbook/       ← 運用手順書
│   └── observability/ ← ログ・監視設計
├── agents/            ← サブエージェント定義
├── skills/            ← カスタムスキル
└── commands/          ← カスタムスラッシュコマンド
```

## 技術スタック

{TECH_STACK}

## 開発コマンド（src/ で実行）

```bash
{DEV_COMMANDS}
```

## ルール参照

| 種別 | ファイル |
|------|---------|
| Git | `.claude/rules/git.md` |
| テスト | `.claude/rules/testing.md` |
| セキュリティ | `.claude/rules/security.md` |

## Supabase

- **Project Ref**: `{SUPABASE_PROJECT_REF}`
- **URL**: `https://{SUPABASE_PROJECT_REF}.supabase.co`
