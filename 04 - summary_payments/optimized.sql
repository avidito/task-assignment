WITH cte_filter AS (
  -- Reusable Row Filter
  SELECT
    "2020-10-01" AS transaction_date,
    "1234" AS gopay_id
),
cte_transaction AS (
  -- Early Row and Column Filter
  SELECT r.gopay_id, r.transaction_id, r.amount FROM ride AS r
  JOIN cte_filter AS fltr
    ON DATE(r.transaction_time) = fltr.transaction_date
    AND r.gopay_id = fltr.gopay_id

  UNION DISTINCT

  SELECT b.gopay_id, b.transaction_id, b.amount FROM bills AS b
  JOIN cte_filter AS fltr
    ON DATE(b.transaction_time) = fltr.transaction_date
    AND b.gopay_id = fltr.gopay_id

  UNION DISTINCT

  SELECT f.gopay_id, f.transaction_id, f.amount FROM food AS f
  JOIN cte_filter AS fltr
    ON DATE(f.transaction_time) = fltr.transaction_date
    AND f.gopay_id = fltr.gopay_id

  UNION DISTINCT

  SELECT p.gopay_id, p.transaction_id, p.amount FROM pulsa AS p
  JOIN cte_filter AS fltr
    ON DATE(p.transaction_time) = fltr.transaction_date
    AND p.gopay_id = fltr.gopay_id
),
cte_payments AS (
  -- Remove 'gopay' table
  SELECT
    trx.gopay_id,
    DATE(trx.creation_time) AS creation_date,
    COUNT(DISTINCT trx.transaction_id) AS transactions,
    SUM(DISTINCT trx.amount) AS amount
  FROM cte_transaction AS trx
  GROUP BY 1, 2
)
SELECT * FROM cte_payments;