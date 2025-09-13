import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "db.sqlite3"
conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

# --- Топ-5 товаров за последний месяц ---
one_month_ago = (datetime.now() - timedelta(days=30)).isoformat()
cur.execute(f"""
SELECT p.name AS product_name,
       rc.name AS top_category,
       SUM(oi.quantity) AS total_sold
FROM order_orderitem oi -- Джанго автоматом подгоняет такие названия 
JOIN order_product p ON p.id = oi.product_id
JOIN order_category c ON p.category_id = c.id
JOIN order_category rc ON rc.id = c.root_category_id
JOIN order_customerorder co ON oi.order_id = co.id
WHERE co.order_date >= '{one_month_ago}'
GROUP BY p.id, p.name, rc.name
ORDER BY total_sold DESC
LIMIT 5;
""")
print("Top 5 products last month:")
for row in cur.fetchall():
    print(row)

# --- Топ клиентов по сумме заказов ---
cur.execute("""
SELECT c.name AS customer_name,
       SUM(oi.quantity * p.price) AS total_amount
FROM order_customer c
LEFT JOIN order_customerorder co ON c.id = co.customer_id
LEFT JOIN order_orderitem oi ON co.id = oi.order_id
LEFT JOIN order_product p ON oi.product_id = p.id
GROUP BY c.id, c.name
ORDER BY total_amount DESC;
""")
print("\nTop customers:")
for row in cur.fetchall():
    print(row)

# --- Количество дочерних категорий 1 уровня ---
cur.execute("""
SELECT COUNT(*)
FROM order_category
WHERE parent_id IN (
    SELECT id
    FROM order_category
    WHERE parent_id IS NULL
);
""")
print("\nFirst-level child categories:", cur.fetchone()[0])

conn.close()
