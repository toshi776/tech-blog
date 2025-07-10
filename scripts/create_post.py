#!/usr/bin/env python3
"""
記事生成スクリプト
queue.ymlから「ready」ステータスの記事を読み込み、
ビジネス価値に焦点を当てた記事を生成
"""

import yaml
import os
from datetime import datetime
from pathlib import Path
import re
import sys

QUEUE_FILE = 'queue.yml'
POSTS_DIR = 'tech-blog/src/content/posts'

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

def slugify(text):
    """日本語タイトルをスラッグ化"""
    # 英数字とハイフンのみ残す
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]  # 長すぎる場合は切る

def get_business_value_content(score):
    """スコアに基づいてビジネス価値コンテンツを生成"""
    if score >= 8:
        return {
            'evaluation': '高',
            'priority': '最優先',
            'implementation': 'すぐに検討開始',
            'benefit': '大幅な業務効率化とコスト削減が期待できます',
            'roi': '6ヶ月以内の投資回収が見込める'
        }
    elif score >= 6:
        return {
            'evaluation': '中',
            'priority': '中期検討',
            'implementation': '3-6ヶ月以内に検討',
            'benefit': '業務効率化による一定の効果が期待できます',
            'roi': '12ヶ月以内の投資回収が見込める'
        }
    else:
        return {
            'evaluation': '低',
            'priority': '長期検討',
            'implementation': '将来的な検討項目',
            'benefit': '限定的な効果が期待できます',
            'roi': '投資回収期間は18ヶ月以上'
        }

def generate_tags(title, source, memo):
    """タイトル、ソース、メモから適切なタグを生成"""
    tags = ['AI', 'DX']
    
    # タイトルとメモから追加タグを抽出
    text = (title + " " + memo).lower()
    
    tag_keywords = {
        'automation': '自動化',
        'chatgpt': 'ChatGPT',
        'microsoft': 'Microsoft',
        'python': 'Python',
        'javascript': 'JavaScript',
        'cloud': 'クラウド',
        'saas': 'SaaS',
        'api': 'API',
        'machine-learning': '機械学習',
        'cost-reduction': 'コスト削減',
        'efficiency': '効率化',
        'productivity': '生産性',
        'business': 'ビジネス戦略'
    }
    
    for keyword, tag in tag_keywords.items():
        if keyword in text:
            tags.append(tag)
    
    # ソースベースのタグ
    if 'techcrunch' in source.lower():
        tags.append('海外動向')
    elif 'zenn' in source.lower() or 'qiita' in source.lower():
        tags.append('日本語記事')
    elif 'publickey' in source.lower():
        tags.append('技術解説')
    
    return list(set(tags))  # 重複除去

def create_article(item):
    """queue.ymlから記事Markdownを生成"""
    
    # メタ情報の準備
    title = item['title']
    item_id = item['id']
    memo = item.get('memo', '')
    score = item.get('score', 5)
    source_name = item.get('source', 'External')
    source_url = item.get('url', '#')
    summary = item.get('summary', '')
    
    # ビジネス価値評価
    business_value = get_business_value_content(score)
    
    # タグ生成
    tags = generate_tags(title, source_name, memo)
    
    # 記事テンプレート
    template = f"""---
title: "{title}"
description: "{memo[:150] if memo else '最新のAI/DX技術に関するビジネス価値分析とレポート'}"
pubDate: "{datetime.now().strftime('%Y-%m-%d')}"
tags: {tags}
draft: false
---

## 概要

{memo if memo else 'この技術について詳しく分析します。'}

> **参考記事**: [{source_name}]({source_url})

## ビジネス価値評価

**総合スコア: {score}/10 （{business_value['evaluation']}）**

この技術のビジネス応用における評価ポイント：

### 🎯 導入優先度
- **評価レベル**: {business_value['evaluation']}
- **推奨アクション**: {business_value['implementation']}
- **投資回収期間**: {business_value['roi']}

### 📈 期待される効果

#### 1. 業務効率化
{business_value['benefit']}

#### 2. コスト削減効果
- 人件費の最適化
- 作業時間の短縮
- エラー率の削減

#### 3. 競争優位性
- 先進技術による差別化
- サービス品質の向上
- 顧客満足度の向上

## 実装における検討事項

### 🔧 技術的観点
- **システム連携**: 既存システムとの統合性
- **セキュリティ**: データ保護とアクセス制御
- **拡張性**: 将来的な機能拡張への対応

### 👥 組織的観点
- **人材育成**: 新技術に対応できる人材の確保
- **変更管理**: 業務プロセスの見直しと最適化
- **社内理解**: 経営層・現場双方の理解促進

### 💰 経済的観点
- **初期投資**: システム導入・構築費用
- **運用コスト**: 継続的な維持・管理費用
- **効果測定**: ROI（投資収益率）の定量的評価

## 想定される活用シーン

### 🏢 社内業務の自動化
1. **定型作業の削減**
   - データ入力業務の自動化
   - レポート生成の効率化
   - 承認フローの簡素化

2. **ヒューマンエラーの防止**
   - 自動チェック機能
   - 品質管理の向上
   - 一貫性の確保

### 🤝 顧客サービスの向上
1. **レスポンス時間の短縮**
   - 自動応答システム
   - 迅速な情報提供
   - 24時間対応の実現

2. **パーソナライゼーション**
   - 個別対応の強化
   - 顧客ニーズの把握
   - 満足度向上

### 🚀 新規事業の創出
1. **AIを活用した新サービス**
   - 付加価値の創出
   - 新市場の開拓
   - 収益源の多様化

2. **データ分析による洞察**
   - 意思決定の高度化
   - 予測精度の向上
   - 戦略立案の支援

## 実装アプローチ

### Phase 1: 概念実証（PoC）
**期間**: 1-2ヶ月
**目的**: 技術的実現性の検証
**内容**:
- 小規模での効果検証
- 技術的課題の洗い出し
- 費用対効果の初期評価

### Phase 2: パイロット導入
**期間**: 3-6ヶ月
**目的**: 実運用での効果測定
**内容**:
- 限定部署での実運用
- パフォーマンス測定
- 改善点の特定

### Phase 3: 本格展開
**期間**: 6ヶ月以降
**目的**: 全社的な展開
**内容**:
- 全社展開の実施
- 継続的な改善
- ROI の定量的評価

## 地方企業への適用可能性

### 🌟 地方企業の強み
- **小回りの利く意思決定**: 迅速な導入判断が可能
- **密な人間関係**: 変更管理がスムーズ
- **特化した専門性**: ニッチな分野での差別化

### 📊 導入における優位性
- **競合他社との差別化**: 先進技術による優位性確保
- **人材不足の解決**: 自動化による人手不足の補完
- **地域貢献**: 地方におけるDX推進のリーダー的存在

## まとめ

{title}は、{business_value['evaluation']}いビジネス価値を持つ技術として評価されます。
{business_value['implementation']}を推奨し、段階的な導入アプローチで{business_value['roi']}が期待できます。

地方企業においても、適切な計画と実行により、大きな競争優位性を獲得できる可能性があります。

---

## 🚀 この技術の導入をお考えですか？

**toshi776では、最新AI/DX技術の導入をトータルサポートいたします。**

<div style="background: #f8fafc; padding: 24px; border-radius: 8px; margin: 24px 0;">
  <h3 style="color: #1e293b; margin-bottom: 16px;">💡 無料相談サービス</h3>
  <p style="margin-bottom: 16px;">この技術の導入について、お気軽にご相談ください。</p>
  <div style="text-align: center;">
    <a href="/" style="background: #3b82f6; color: white; padding: 16px 32px; border-radius: 8px; text-decoration: none; display: inline-block;">
      📞 無料相談を申し込む
    </a>
  </div>
</div>

### 🎯 関連サービス

| サービス | 価格 | 概要 |
|----------|------|------|
| **技術調査・PoC支援** | ¥300,000〜 | 技術の実現可能性調査と概念実証 |
| **導入コンサルティング** | ¥500,000〜 | 導入計画策定から実装まで |
| **運用サポート** | ¥50,000/月〜 | 継続的な運用・改善支援 |

詳細は[サービス一覧](/)をご覧ください。

---

<div style="background: #fef3f2; padding: 16px; border-radius: 6px; margin: 24px 0;">
  <strong>📢 最新情報をお届け</strong><br>
  AI/DX技術の最新情報を定期的に配信しています。<br>
  <a href="/blog/">📝 技術ブログ一覧</a> | 
  <a href="/">🏠 会社サイト</a>
</div>
"""
    
    # ファイル作成
    filename = f"{POSTS_DIR}/{item_id}.md"
    Path(POSTS_DIR).mkdir(parents=True, exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✅ Created: {filename}")
    return filename

def main():
    """メイン処理"""
    try:
        # キュー読み込み
        queue = load_queue()
        
        if not queue:
            print("📭 キューが空です")
            return
        
        created_count = 0
        
        # statusが'ready'のものを記事化
        for item in queue:
            if item.get('status') == 'ready':
                try:
                    print(f"\n📝 記事生成中: {item['title'][:50]}...")
                    create_article(item)
                    item['status'] = 'published'
                    item['published_at'] = datetime.now().isoformat()
                    created_count += 1
                except Exception as e:
                    print(f"❌ Error creating article for {item['id']}: {e}")
        
        # キュー更新
        if created_count > 0:
            save_queue(queue)
            print(f"\n🎉 記事生成完了！")
            print(f"作成された記事: {created_count} 件")
            print(f"\n📋 次のステップ:")
            print(f"1. tech-blog/src/content/posts/ で記事を確認")
            print(f"2. git add & commit でコミット")
            print(f"3. git push でデプロイ開始")
        else:
            print("\n📭 生成対象の記事がありません")
            print("ヒント: python3 scripts/queue_cli.py status <id> ready")
    
    except KeyboardInterrupt:
        print("\n⏹️  記事生成を中断しました")
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()