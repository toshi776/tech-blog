# toshi776技術ブログ

AI/DX技術の最新情報とビジネス活用事例をお届けする技術ブログです。

## 技術スタック

- **Astro**: 静的サイトジェネレーター
- **TypeScript**: 型安全な開発
- **MDX**: Markdownベースのコンテンツ
- **GitHub Actions**: 自動デプロイ
- **FTP**: CoreServerへのデプロイ

## 開発環境

### 必要な環境
- Node.js 20+
- npm

### セットアップ

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev

# ビルド
npm run build

# プレビュー
npm run preview
```

## デプロイ

GitHub Actionsを使用して自動デプロイが設定されています。

### 必要なGitHub Secrets

以下のSecretsを設定してください：

- `FTP_HOST`: FTPサーバーのホスト
- `FTP_USER`: FTPユーザー名
- `FTP_PASS`: FTPパスワード
- `FTP_DIR`: FTPサーバーのデプロイ先ディレクトリ（例: `/public_html/blog/`）

### デプロイの流れ

1. `main`または`master`ブランチにpush
2. GitHub Actionsが自動実行
3. Astroサイトをビルド
4. FTPでCoreServerにデプロイ

## ディレクトリ構造

```
tech-blog/
├── src/
│   ├── content/
│   │   └── posts/        # Markdown記事
│   ├── layouts/
│   │   └── BlogPost.astro # 記事レイアウト
│   └── pages/
│       ├── index.astro    # ブログトップ
│       └── posts/
│           └── [slug].astro # 動的ルート
├── public/
│   └── styles/
│       └── blog.css      # CSSスタイル
├── scripts/              # 自動化スクリプト
├── .github/
│   └── workflows/
│       └── deploy.yml    # GitHub Actions設定
└── queue.yml            # 記事キュー（Day 2で作成）
```

## 記事の追加方法

1. `src/content/posts/` に Markdown ファイルを作成
2. frontmatter に必要な情報を記載
3. コミット・プッシュで自動デプロイ

### 記事のフォーマット

```markdown
---
title: "記事タイトル"
description: "記事の説明"
pubDate: "2025-01-09"
tags: ["AI", "DX", "技術"]
draft: false
---

## 記事内容

記事の内容をここに記載...
```

## 運用フロー

1. **RSS収集**: `scripts/collect_rss.py`
2. **手動選別**: `queue.yml`を編集
3. **記事生成**: `scripts/create_post.py`
4. **自動デプロイ**: GitHub Actions

## サポート

技術的な質問やサポートが必要な場合は、[toshi776.com](https://toshi776.com)までお問い合わせください。