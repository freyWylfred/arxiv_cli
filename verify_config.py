#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
config.ini の設定値確認スクリプト
"""
import configparser
import os
from datetime import datetime

def verify_config():
    config_file = 'config.ini'
    
    if not os.path.exists(config_file):
        print(f"❌ {config_file} が見つかりません")
        return False
    
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    
    print("="*60)
    print("config.ini 設定値確認")
    print("="*60)
    
    try:
        # 日付範囲
        start_date_str = config.get('DateRange', 'start_date').strip()
        end_date_str = config.get('DateRange', 'end_date').strip()
        
        # 検索設定
        query = config.get('Search', 'query').strip()
        max_results = config.getint('Search', 'max_results')
        
        # ファイル設定
        excel_file = config.get('Files', 'excel_file').strip()
        
        # 日付の妥当性チェック
        start_date = datetime.strptime(start_date_str, "%Y/%m/%d").date()
        end_date = datetime.strptime(end_date_str, "%Y/%m/%d").date()
        
        print(f"\n[DateRange]")
        print(f"  開始日: {start_date_str} → {start_date}")
        print(f"  終了日: {end_date_str} → {end_date}")
        print(f"  処理日数: {(end_date - start_date).days + 1}日")
        
        print(f"\n[Search]")
        print(f"  検索クエリ: {query}")
        print(f"  最大取得件数: {max_results}件")
        
        print(f"\n[Files]")
        print(f"  Excel出力先: {excel_file}")
        
        # 妥当性チェック
        print(f"\n【妥当性チェック】")
        if start_date > end_date:
            print(f"  ❌ エラー: 開始日が終了日より後になっています")
            return False
        else:
            print(f"  ✅ 日付範囲: OK")
        
        if max_results < 1 or max_results > 1000:
            print(f"  ⚠️  警告: 最大取得件数が推奨範囲外です（推奨: 1-1000）")
        else:
            print(f"  ✅ 最大取得件数: OK")
        
        if not excel_file.endswith('.xlsx'):
            print(f"  ⚠️  警告: Excelファイル名の拡張子が .xlsx ではありません")
        else:
            print(f"  ✅ Excelファイル名: OK")
        
        print(f"\n{'='*60}")
        print(f"✅ すべての設定が正しく読み込まれました")
        print(f"{'='*60}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ エラー: {str(e)}")
        return False

if __name__ == "__main__":
    verify_config()
