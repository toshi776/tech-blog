#!/bin/bash

# 技術ブログ日次更新スクリプト
# DAY4: 運用自動化スクリプト

echo "=================================="
echo "🤖 技術ブログ日次更新システム"
echo "=================================="
echo "開始時刻: $(date '+%Y-%m-%d %H:%M:%S')"

# 作業ディレクトリの確認
if [ ! -f "queue.yml" ]; then
    echo "❌ queue.yml が見つかりません。正しいディレクトリで実行してください。"
    exit 1
fi

# Python環境の確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 が見つかりません。"
    exit 1
fi

# 1. RSS収集フェーズ
echo ""
echo "📡 Phase 1: RSS収集"
echo "===================="
python3 scripts/collect_rss.py

# エラーハンドリング
if [ $? -ne 0 ]; then
    echo "❌ RSS収集でエラーが発生しました"
    exit 1
fi

# 2. キュー確認フェーズ
echo ""
echo "📋 Phase 2: キュー確認"
echo "===================="
echo "現在のキュー状況:"
python3 scripts/queue_cli.py stats

echo ""
echo "新着記事 (pending):"
python3 scripts/queue_cli.py list pending 5

# 3. 手動選別の案内
echo ""
echo "👀 Phase 3: 手動選別"
echo "===================="
echo "以下の手順で記事を選別してください:"
echo ""
echo "1. 📝 新着記事を確認"
echo "   python3 scripts/queue_cli.py list pending"
echo ""
echo "2. 📄 記事詳細を確認"
echo "   python3 scripts/queue_cli.py detail <記事ID>"
echo ""
echo "3. ✅ 公開したい記事を ready に設定"
echo "   python3 scripts/queue_cli.py status <記事ID> ready"
echo ""
echo "4. 📊 スコアを設定 (1-10)"
echo "   python3 scripts/queue_cli.py score <記事ID> <スコア>"
echo ""
echo "5. 📝 メモを追加"
echo "   python3 scripts/queue_cli.py memo <記事ID> \"日本語でのコメント\""
echo ""

# インタラクティブモードの確認
if [ -t 0 ]; then
    echo "🤔 記事の選別を行いますか？"
    echo "  [Y] はい - 手動で選別する"
    echo "  [N] いいえ - 自動で ready 記事を処理"
    echo "  [Q] 終了 - 今回はスキップ"
    echo ""
    read -p "選択してください [Y/N/Q]: " choice
    
    case $choice in
        [Yy]*)
            echo ""
            echo "📝 記事選別を開始してください。"
            echo "完了したら何かキーを押してください..."
            read -p "Press any key to continue..."
            ;;
        [Qq]*)
            echo "⏹️  処理を終了します"
            exit 0
            ;;
        *)
            echo "✅ 自動処理を継続します"
            ;;
    esac
else
    echo "🔄 非インタラクティブモード: 自動処理を継続"
fi

# 4. 記事生成フェーズ
echo ""
echo "📝 Phase 4: 記事生成"
echo "===================="
echo "ready ステータスの記事を生成中..."

# ready 記事の確認
ready_count=$(python3 scripts/queue_cli.py list ready | grep -c "ready" || echo "0")
echo "📊 ready 記事数: $ready_count"

if [ "$ready_count" -eq 0 ]; then
    echo "📭 ready 記事がありません。処理を終了します。"
    echo ""
    echo "💡 記事を公開するには:"
    echo "   python3 scripts/queue_cli.py status <記事ID> ready"
    echo "   python3 scripts/queue_cli.py score <記事ID> <1-10>"
    echo "   python3 scripts/queue_cli.py memo <記事ID> \"コメント\""
    exit 0
fi

# 記事生成実行
python3 scripts/create_post.py

# エラーハンドリング
if [ $? -ne 0 ]; then
    echo "❌ 記事生成でエラーが発生しました"
    exit 1
fi

# 5. Git操作フェーズ
echo ""
echo "🚀 Phase 5: Git操作"
echo "===================="

# 変更の確認
if [[ `git status --porcelain` ]]; then
    echo "📋 変更されたファイル:"
    git status --short
    
    echo ""
    echo "🔄 Gitコミットを実行中..."
    
    # コミットメッセージの生成
    commit_date=$(date '+%Y-%m-%d')
    published_articles=$(python3 scripts/queue_cli.py list published | grep -c "published" || echo "0")
    
    git add -A
    git commit -m "Update blog: $commit_date

- RSS収集とキュー処理を実行
- 新規記事を自動生成・公開
- 総公開記事数: $published_articles

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    
    if [ $? -eq 0 ]; then
        echo "✅ コミット成功"
        
        # プッシュの確認
        if [ -t 0 ]; then
            echo ""
            read -p "🚀 GitHubにプッシュしますか？ [Y/n]: " push_choice
            case $push_choice in
                [Nn]*)
                    echo "⏸️  プッシュをスキップしました"
                    ;;
                *)
                    echo "🚀 GitHubへプッシュ中..."
                    git push origin main
                    
                    if [ $? -eq 0 ]; then
                        echo "✅ プッシュ完了！GitHub Actionsでデプロイが開始されます"
                        echo "🌐 デプロイ完了後、https://toshi776.com/blog/ で確認できます"
                    else
                        echo "❌ プッシュに失敗しました"
                    fi
                    ;;
            esac
        else
            echo "🚀 GitHubへプッシュ中..."
            git push origin main
            
            if [ $? -eq 0 ]; then
                echo "✅ プッシュ完了！GitHub Actionsでデプロイが開始されます"
            else
                echo "❌ プッシュに失敗しました"
            fi
        fi
    else
        echo "❌ コミットに失敗しました"
    fi
else
    echo "ℹ️  変更がありません"
fi

# 6. 完了レポート
echo ""
echo "🎉 Phase 6: 完了レポート"
echo "========================"
echo "完了時刻: $(date '+%Y-%m-%d %H:%M:%S')"

# 統計情報
echo ""
echo "📊 最終統計:"
python3 scripts/queue_cli.py stats

echo ""
echo "📋 最近の公開記事:"
python3 scripts/queue_cli.py list published 3

echo ""
echo "✅ 日次更新が完了しました！"
echo ""
echo "🔗 確認リンク:"
echo "   ブログ: https://toshi776.com/blog/"
echo "   GitHub: https://github.com/toshi776/tech-blog"
echo ""
echo "💡 次回実行:"
echo "   bash daily_blog_update.sh"
echo ""
echo "=================================="