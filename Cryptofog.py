import pandas as pd
from datetime import datetime, timedelta
import argparse
import os

def analyze_inactive_assets(csv_path, days=180):
    if not os.path.isfile(csv_path):
        print(f"Файл {csv_path} не найден.")
        return

    df = pd.read_csv(csv_path)

    if not {'Asset', 'Date', 'Amount'}.issubset(df.columns):
        print("Ожидаемые столбцы: 'Asset', 'Date', 'Amount'")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    cutoff_date = datetime.now() - timedelta(days=days)

    recent_activity = df[df['Date'] > cutoff_date]
    all_assets = set(df['Asset'].unique())
    active_assets = set(recent_activity['Asset'].unique())

    inactive_assets = all_assets - active_assets

    print(f"\n🔎 Активация за последние {days} дней:")
    print(f"  📈 Активные активы: {len(active_assets)}")
    print(f"  💤 Неактивные активы: {len(inactive_assets)}")

    if inactive_assets:
        print("\n💤 Список неактивных активов:")
        for asset in sorted(inactive_assets):
            last_date = df[df['Asset'] == asset]['Date'].max()
            print(f" - {asset}: последнее движение {last_date.date()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Поиск неактивных криптовалют в CSV.")
    parser.add_argument("csv", help="Путь к CSV-файлу с историей транзакций.")
    parser.add_argument("--days", type=int, default=180, help="Период неактивности в днях (по умолчанию 180).")
    args = parser.parse_args()

    analyze_inactive_assets(args.csv, args.days)
