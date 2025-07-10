#!/usr/bin/env python3
"""
キュー管理CLIツール
queue.ymlの内容を確認・更新するためのユーティリティ
"""

import yaml
import sys
from tabulate import tabulate
from datetime import datetime
import os

QUEUE_FILE = 'queue.yml'

def load_queue():
    """キューを読み込み"""
    if not os.path.exists(QUEUE_FILE):
        print(f"❌ {QUEUE_FILE} が見つかりません")
        return []
    
    try:
        with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data if data else []
    except Exception as e:
        print(f"❌ キューの読み込みエラー: {e}")
        return []

def save_queue(queue):
    """キューを保存"""
    try:
        with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(queue, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"❌ キューの保存エラー: {e}")
        return False

def list_queue(status=None, limit=None):
    """キューを一覧表示"""
    queue = load_queue()
    
    if not queue:
        print("📭 キューは空です")
        return
    
    # ステータスフィルタ
    if status:
        queue = [item for item in queue if item.get('status') == status]
        if not queue:
            print(f"📭 ステータス '{status}' のアイテムはありません")
            return
    
    # 制限数
    if limit:
        queue = queue[:limit]
    
    # 表示用データ準備
    table_data = []
    for item in queue:
        # 日付フォーマット
        collected_date = ''
        if item.get('collected_at'):
            try:
                dt = datetime.fromisoformat(item['collected_at'].replace('Z', '+00:00'))
                collected_date = dt.strftime('%m/%d')
            except:
                collected_date = item.get('collected_at', '')[:10]
        
        table_data.append([
            item.get('id', 'N/A'),
            item.get('title', 'No Title')[:50] + ('...' if len(item.get('title', '')) > 50 else ''),
            item.get('source', 'Unknown')[:15],
            item.get('status', 'pending'),
            str(item.get('score', '-')),
            collected_date,
            item.get('memo', '')[:25] + ('...' if len(item.get('memo', '')) > 25 else '')
        ])
    
    headers = ['ID', 'Title', 'Source', 'Status', 'Score', 'Date', 'Memo']
    print(f"\n📋 キュー一覧 (total: {len(load_queue())}, showing: {len(table_data)})")
    print(tabulate(table_data, headers=headers, tablefmt='grid'))

def show_detail(item_id):
    """アイテムの詳細を表示"""
    queue = load_queue()
    
    for item in queue:
        if item.get('id') == item_id:
            print(f"\n📄 詳細情報: {item_id}")
            print(f"タイトル: {item.get('title', 'N/A')}")
            print(f"URL: {item.get('url', 'N/A')}")
            print(f"ソース: {item.get('source', 'N/A')}")
            print(f"ステータス: {item.get('status', 'N/A')}")
            print(f"スコア: {item.get('score', 'N/A')}")
            print(f"収集日: {item.get('collected_at', 'N/A')}")
            print(f"公開日: {item.get('published_date', 'N/A')}")
            print(f"メモ: {item.get('memo', 'N/A')}")
            if item.get('summary'):
                print(f"概要: {item.get('summary', 'N/A')}")
            return
    
    print(f"❌ アイテム '{item_id}' が見つかりません")

def update_status(item_id, new_status):
    """ステータス更新"""
    valid_statuses = ['pending', 'ready', 'published', 'rejected']
    if new_status not in valid_statuses:
        print(f"❌ 無効なステータス: {new_status}")
        print(f"有効なステータス: {', '.join(valid_statuses)}")
        return False
    
    queue = load_queue()
    for item in queue:
        if item.get('id') == item_id:
            old_status = item.get('status', 'pending')
            item['status'] = new_status
            item['updated_at'] = datetime.now().isoformat()
            
            if save_queue(queue):
                print(f"✅ {item_id}: '{old_status}' → '{new_status}'")
                return True
            return False
    
    print(f"❌ アイテム '{item_id}' が見つかりません")
    return False

def update_score(item_id, score):
    """スコア更新"""
    try:
        score = int(score)
        if not (1 <= score <= 10):
            print("❌ スコアは1-10の範囲で入力してください")
            return False
    except ValueError:
        print("❌ スコアは数値で入力してください")
        return False
    
    queue = load_queue()
    for item in queue:
        if item.get('id') == item_id:
            old_score = item.get('score', 'N/A')
            item['score'] = score
            item['updated_at'] = datetime.now().isoformat()
            
            if save_queue(queue):
                print(f"✅ {item_id}: score {old_score} → {score}")
                return True
            return False
    
    print(f"❌ アイテム '{item_id}' が見つかりません")
    return False

def update_memo(item_id, memo):
    """メモ更新"""
    queue = load_queue()
    for item in queue:
        if item.get('id') == item_id:
            old_memo = item.get('memo', '')
            item['memo'] = memo
            item['updated_at'] = datetime.now().isoformat()
            
            if save_queue(queue):
                print(f"✅ {item_id}: memo updated")
                if old_memo:
                    print(f"  Old: {old_memo}")
                print(f"  New: {memo}")
                return True
            return False
    
    print(f"❌ アイテム '{item_id}' が見つかりません")
    return False

def stats():
    """統計情報を表示"""
    queue = load_queue()
    
    if not queue:
        print("📭 キューは空です")
        return
    
    # ステータス別集計
    status_counts = {}
    source_counts = {}
    
    for item in queue:
        status = item.get('status', 'pending')
        source = item.get('source', 'Unknown')
        
        status_counts[status] = status_counts.get(status, 0) + 1
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print(f"\n📊 キュー統計")
    print(f"総アイテム数: {len(queue)}")
    print(f"\nステータス別:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    print(f"\nソース別:")
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count}")

def print_help():
    """ヘルプを表示"""
    print("""
📋 キュー管理CLIツール

使用方法:
  python3 scripts/queue_cli.py <command> [options]

コマンド:
  list [status] [limit]    - キューを一覧表示
  detail <id>             - アイテムの詳細を表示
  status <id> <status>    - ステータスを更新
  score <id> <score>      - スコアを更新 (1-10)
  memo <id> <memo>        - メモを更新
  stats                   - 統計情報を表示
  help                    - このヘルプを表示

例:
  python3 scripts/queue_cli.py list
  python3 scripts/queue_cli.py list pending 10
  python3 scripts/queue_cli.py detail 20250710-001
  python3 scripts/queue_cli.py status 20250710-001 ready
  python3 scripts/queue_cli.py score 20250710-001 8
  python3 scripts/queue_cli.py memo 20250710-001 "これは興味深い記事です"
  python3 scripts/queue_cli.py stats
""")

def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    if command == 'list':
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        limit_num = None
        if len(sys.argv) > 3:
            try:
                limit_num = int(sys.argv[3])
            except ValueError:
                print("❌ limit は数値で指定してください")
                return
        list_queue(status_filter, limit_num)
    
    elif command == 'detail':
        if len(sys.argv) < 3:
            print("❌ item_id を指定してください")
            return
        show_detail(sys.argv[2])
    
    elif command == 'status':
        if len(sys.argv) < 4:
            print("❌ item_id と status を指定してください")
            return
        update_status(sys.argv[2], sys.argv[3])
    
    elif command == 'score':
        if len(sys.argv) < 4:
            print("❌ item_id と score を指定してください")
            return
        update_score(sys.argv[2], sys.argv[3])
    
    elif command == 'memo':
        if len(sys.argv) < 4:
            print("❌ item_id と memo を指定してください")
            return
        memo_text = ' '.join(sys.argv[3:])  # 複数の単語を結合
        update_memo(sys.argv[2], memo_text)
    
    elif command == 'stats':
        stats()
    
    elif command == 'help':
        print_help()
    
    else:
        print(f"❌ 未知のコマンド: {command}")
        print_help()

if __name__ == '__main__':
    main()