# Claude Code 環境設計

作成日: 2026-04-25

## 概要

Claude Code の設定を整理し、GitHub で管理しながら日々成長させていく環境を構築する。

---

## リポジトリ構成

| リポジトリ | パス | 用途 |
|-----------|------|------|
| `claude-config` | `~/.claude/` | Claude グローバル設定（PC 全体） |
| 各プロジェクト | `project/src/` | ソースコード + `.claude/`（プロジェクト固有設定） |
| 各プロジェクト doc | `project/doc/` | ドキュメント |

- `~/.claude/` と各プロジェクトの `.claude/` は**別の git リポジトリ**
- プロジェクトの `.claude/` はそのプロジェクトの git リポジトリに含める（チーム共有可能）

---

## グローバル設定（`~/.claude/`）

### CLAUDE.md（3行のみ）

```markdown
- 必ず日本語で応答する
- `&&`・`;`・`|` を使った複合コマンドは使わず、単体コマンドを個別に実行する
- ユーザーの指示を鵜呑みにせず、より良い方法があれば率直に意見を述べてから実行する
```

### MCP（5つ・すべてグローバル登録）

| サーバー | 種別 | 用途 |
|---------|------|------|
| context7 | npm | ライブラリドキュメント検索 |
| github | npm | GitHub 操作 |
| cloudflare | npm | Cloudflare Workers 操作 |
| supabase | npm | Supabase 操作（project-ref なし = 全プロジェクト対応） |
| xcode | xcrun | Xcode 操作（iOS プロジェクト） |

**注意点:**
- 二重登録（npm版 + リモート版）を解消する → npm版に統一
- プロジェクト固有の Supabase 情報（Project Ref・URL）は各プロジェクトの CLAUDE.md に記載

### Skills（`~/.claude/skills/`）

| スキル | 用途 |
|--------|------|
| app-icon | Expo アプリアイコン生成 |
| app-store-screenshots | App Store / Google Play スクショ生成 |
| find-skills | スキル検索・発見 |
| vercel-react-native-skills | React Native / Expo ベストプラクティス |
| vercel-react-best-practices | React / Next.js 最適化 |

- `startup-financial-modeling` は削除

### Agents（`~/.claude/agents/`）

**削除（4）:**
- socratic-mentor
- devops-architect
- requirements-analyst
- performance-engineer

**残す（12）:**
- backend-architect, business-panel-experts, deep-research-agent
- frontend-architect, learning-guide, python-expert
- quality-engineer, refactoring-expert, root-cause-analyst
- security-engineer, system-architect, technical-writer

**新規追加（3）:**

| エージェント | 役割 |
|------------|------|
| `ios-swift-engineer` | Swift・App Intents・WidgetKit・Screen Time API 専門 |
| `expo-mobile-engineer` | React Native / Expo 専門（frontend-architect より具体的） |
| `supabase-engineer` | Supabase・PostgreSQL・Edge Functions 専門 |

### Plugins（変更なし）

| プラグイン | 内容 |
|-----------|------|
| superpowers | brainstorming・TDD・debugging 等 13 スキル |
| automatic-code-review | コードレビュー |
| ui-ux-pro-max | UI/UX デザイン |
| supabase-agent-skills | Supabase 操作 |

### テンプレート（`~/.claude/templates/project-claude/`）

新プロジェクト作成時に `.claude/` としてコピーされる雛形。

```
templates/project-claude/
├── CLAUDE.md               # 穴埋め形式のプロジェクト設定テンプレート
├── settings.json           # auto-review 等の共通設定
├── skills/                 # プロジェクト固有スキル置き場（初期は空）
├── commands/               # プロジェクト固有コマンド置き場（初期は空）
├── agents/                 # プロジェクト固有エージェント置き場（初期は空）
└── automatic-code-review/
    └── rules.md            # コードレビュールール
```

---

## プロジェクト設定（`.claude/`）

各プロジェクトの git リポジトリに含める。

### CLAUDE.md に書くこと

- プロジェクト概要・技術スタック
- Supabase Project Ref / URL
- リポジトリ構造（doc/ と src/ の分離）
- 開発コマンド
- プロジェクト固有のデザイン・ローカライズルール等

### ディレクトリ構造

```
~/Documents/dev/{name}/
├── .claude/                # プロジェクトルート直下
│   ├── CLAUDE.md
│   ├── settings.json
│   ├── skills/             # プロジェクト固有スキル
│   ├── commands/           # プロジェクト固有コマンド
│   ├── agents/             # プロジェクト固有エージェント
│   └── automatic-code-review/
│       └── rules.md
├── doc/                    # ドキュメントリポジトリ
└── src/                    # ソースコードリポジトリ
```

---

## `/newproject` コマンド

新プロジェクト立ち上げを一発で完了させるカスタムコマンド。

### ヒアリング項目（実行時に対話形式で収集）

| 項目 | 例 |
|------|-----|
| プロジェクト名（英語・kebab-case） | `my-app` |
| プロジェクト概要（日本語） | 「AIを使った〇〇アプリ」 |
| 技術スタック | React Native / Next.js / Swift / Python など |
| Supabase を使うか | Yes → Project Ref を後で記載する旨を CLAUDE.md に明記 |
| Cloudflare Workers を使うか | Yes / No |
| iOS (Swift) を使うか | Yes / No |
| doc リポジトリも作るか | Yes / No |
| GitHub の visibility | public / private |

### 実行内容

1. 上記ヒアリングを対話形式で実施
2. ローカルディレクトリ作成（`~/Documents/dev/{name}/doc/`・`src/`）
3. GitHub リポジトリ作成（src 用・必要なら doc 用）
4. git 初期化（両リポジトリ）
5. `~/.claude/templates/project-claude/` を `~/Documents/dev/{name}/.claude/` にコピー（プロジェクトルート直下）
6. ヒアリング結果をもとに CLAUDE.md を生成
7. 初回コミット・プッシュ

### 配置場所

`~/.claude/commands/newproject/SKILL.md`（グローバルコマンドとして `/newproject` で呼び出し）

---

## 整理作業リスト（初期セットアップ）

- [ ] MCP の二重登録を解消（リモート版を削除、npm版に統一）
- [ ] `~/.claude/` を git 初期化・GitHub リポジトリ作成・プッシュ
- [ ] `startup-financial-modeling` スキルを削除
- [ ] `deploy`（空）スキルを flashguard から削除
- [ ] vercel 系スキルを flashguard → `~/.claude/skills/` に移動
- [ ] エージェント 4 つを削除
- [ ] 新規エージェント 3 つを作成（ios-swift-engineer・expo-mobile-engineer・supabase-engineer）
- [ ] グローバル CLAUDE.md を作成（3行）
- [ ] `templates/project-claude/` を作成
- [ ] `/newproject` コマンドを実装
- [ ] `.gitignore` を設定（settings.json のトークン等を除外）
