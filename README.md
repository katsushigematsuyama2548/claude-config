# claude-config

Claude Code のグローバル設定を管理するリポジトリ。

## ディレクトリ構成

```
~/.claude/
├── CLAUDE.md                    # グローバル指示（全プロジェクト共通・3行のみ）
├── settings.json                # 権限・MCP・モデル設定
├── .gitignore
│
├── agents/                      # サブエージェント定義（15個）
│   ├── backend-architect.md
│   ├── business-panel-experts.md
│   ├── deep-research-agent.md
│   ├── expo-mobile-engineer.md  ← カスタム
│   ├── frontend-architect.md
│   ├── ios-swift-engineer.md    ← カスタム
│   ├── learning-guide.md
│   ├── python-expert.md
│   ├── quality-engineer.md
│   ├── refactoring-expert.md
│   ├── root-cause-analyst.md
│   ├── security-engineer.md
│   ├── supabase-engineer.md     ← カスタム
│   ├── system-architect.md
│   └── technical-writer.md
│
├── skills/                      # グローバルスキル（5個）
│   ├── app-icon
│   ├── app-store-screenshots
│   ├── find-skills
│   ├── vercel-react-best-practices
│   └── vercel-react-native-skills
│
├── commands/                    # カスタムスラッシュコマンド
│   └── newproject/              # /newproject — 新プロジェクト一括セットアップ
│
└── templates/
    └── project-claude/          # 新プロジェクト用 .claude/ テンプレート
        ├── CLAUDE.md
        ├── settings.json
        ├── skills/
        ├── commands/
        ├── agents/
        └── automatic-code-review/
            └── rules.md
```

## MCP（グローバル登録・5つ）

| サーバー | 用途 |
|---------|------|
| context7 | ライブラリドキュメント検索 |
| github | GitHub 操作 |
| cloudflare | Cloudflare Workers 操作 |
| supabase | Supabase 操作（全プロジェクト共通） |
| xcode | Xcode 操作（iOS プロジェクト） |

## プロジェクト設定との分離

- このリポジトリ → PC 全体のグローバル設定
- 各プロジェクトの `.claude/` → 各プロジェクトの git リポジトリで管理
- 新プロジェクトは `/newproject` コマンドで `templates/project-claude/` をコピーして初期化
