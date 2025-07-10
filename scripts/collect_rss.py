#!/usr/bin/env python3
"""
RSS収集スクリプト
AI/DX関連の技術記事を収集してqueue.ymlに保存
"""

import feedparser
import yaml
from datetime import datetime
import os
from dateutil import parser
import sys

# 設定
RSS_FEEDS = [
    'https://techcrunch.com/category/artificial-intelligence/feed/',
    'https://dev.to/feed/tag/ai',
    'https://zenn.dev/topics/ai/feed',
    'https://www.publickey1.jp/atom.xml',  # 日本語ソース
    'https://qiita.com/tags/ai/feed',  # 日本語ソース追加
]

QUEUE_FILE = 'queue.yml'

def load_queue():
    """既存のキューを読み込み"""
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data if data else []
    return []

def save_queue(items):
    """キューを保存"""
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(items, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def normalize_date(date_str):
    """日付文字列を正規化"""
    if not date_str:
        return datetime.now().isoformat()
    try:
        return parser.parse(date_str).isoformat()
    except Exception as e:
        print(f"Date parsing error: {e}")
        return datetime.now().isoformat()

def is_relevant_content(title, summary=""):
    """AI/DX関連のコンテンツかどうかを判定"""
    keywords = [
        'ai', 'artificial intelligence', 'machine learning', 'deep learning',
        'chatgpt', 'gpt', 'llm', 'automation', 'dx', 'digital transformation',
        'openai', 'claude', 'gemini', 'copilot', 'python', 'javascript',
        '人工知能', 'AI', 'DX', 'デジタル変革', '自動化', 'プログラミング',
        'チャットボット', 'ローコード', 'ノーコード'
    ]
    
    text = (title + " " + summary).lower()
    return any(keyword.lower() in text for keyword in keywords)

def collect_feeds():
    """RSS収集メイン処理"""
    queue = load_queue()
    existing_urls = {item.get('url') for item in queue if 'url' in item}
    new_items = []
    
    print(f"📡 RSS収集開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"既存アイテム数: {len(queue)}")
    
    for i, feed_url in enumerate(RSS_FEEDS, 1):
        try:
            print(f"\n[{i}/{len(RSS_FEEDS)}] Fetching: {feed_url}")
            
            # User-Agentを設定してフィードを取得
            feed = feedparser.parse(feed_url)
            
            if hasattr(feed, 'bozo') and feed.bozo:
                print(f"  ⚠️  Warning: Feed parsing issue for {feed_url}")
            
            # フィードタイトル取得
            feed_title = feed.feed.get('title', 'Unknown Source')
            print(f"  📰 Source: {feed_title}")
            
            added_count = 0
            for entry in feed.entries[:5]:  # 各フィードから最新5件
                if entry.link not in existing_urls:
                    # 関連性チェック
                    summary = entry.get('summary', '')
                    if not is_relevant_content(entry.title, summary):
                        continue
                    
                    # 日付取得
                    pub_date = entry.get('published', entry.get('updated', ''))
                    
                    new_item = {
                        'id': datetime.now().strftime('%Y%m%d') + f'-{len(queue) + len(new_items) + 1:03d}',
                        'title': entry.title.strip(),
                        'url': entry.link,
                        'source': feed_title,
                        'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                        'published_date': normalize_date(pub_date),
                        'collected_at': datetime.now().isoformat(),
                        'status': 'pending',
                        'score': None,  # 後で手動評価
                        'memo': ''      # 後で手動追記
                    }
                    new_items.append(new_item)
                    added_count += 1
                    print(f"  ✅ Added: {entry.title[:60]}...")
                    
            print(f"  📊 Added {added_count} new items from this feed")
                    
        except Exception as e:
            print(f"  ❌ Error fetching {feed_url}: {e}")
    
    if new_items:
        queue.extend(new_items)
        save_queue(queue)
        print(f"\n🎉 収集完了！")
        print(f"新規追加: {len(new_items)} 件")
        print(f"総キュー数: {len(queue)} 件")
    else:
        print(f"\n📭 新しいアイテムはありませんでした")
    
    return len(new_items)

def main():
    """メイン処理"""
    try:
        new_count = collect_feeds()
        
        if new_count > 0:
            print(f"\n📋 次のステップ:")
            print(f"1. queue.yml を確認して内容をチェック")
            print(f"2. 公開したい記事の status を 'ready' に変更")
            print(f"3. score (1-10) と memo を追記")
            print(f"4. python3 scripts/create_post.py で記事生成")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  収集を中断しました")
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()