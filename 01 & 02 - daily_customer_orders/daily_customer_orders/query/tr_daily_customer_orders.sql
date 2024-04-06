MERGE INTO `tmp.daily_customer_orders` AS T
USING (
  /*
    BASE QUERY

    Summary of Daily Customer Orders based on services and payment methods.
  */
  WITH cte_prep_data AS (
    SELECT
      order_date,
      customer_no,
      ARRAY_AGG(DISTINCT order_type ORDER BY order_type) AS services,
      (CASE
        order_payment
          WHEN "CASH&GOPAY" THEN "CASH&GOPAY (ALL)"
          ELSE order_payment
      END) AS order_payment
    FROM (
      SELECT
        DATE(order_time) AS order_date,
        customer_no,
        order_type,
        ARRAY_TO_STRING(ARRAY_AGG(DISTINCT order_payment), "&") AS order_payment
      FROM `tmp.goto_daily_order` AS ord -- DATA FROM SHEET
      WHERE TRUE
        AND order_status = "Completed"
        AND {{ params.dt_filter }}
      GROUP BY 1, 2, 3
    ) AS d
    GROUP BY 1, 2, 4
  ),
  cte_agg_cust AS (
    SELECT
      order_date,
      ARRAY_LENGTH(services) AS no_of_service,
      ARRAY_TO_STRING(services, ", ") AS order_type,
      COUNT(DISTINCT customer_no) AS total_customer_per_order_type,
      order_payment,
    FROM cte_prep_data
    GROUP BY 1, 2, 3, 5
  ),
  cte_summary AS (
    SELECT
      order_date,
      no_of_service,
      SUM(total_customer_per_order_type) AS total_customer,
      ARRAY_AGG(
        STRUCT(order_type, total_customer_per_order_type)
        ORDER BY total_customer_per_order_type
      ) AS detail,
      order_payment
    FROM cte_agg_cust
    GROUP BY 1, 2, 5
  )
  SELECT
    order_date,
    no_of_service,
    total_customer,
    detail,
    order_payment
  FROM cte_summary
  ORDER BY order_date, no_of_service, order_payment
) AS S
  ON T.order_date = S.order_date
  AND T.no_of_service = S.no_of_service
  AND T.order_payment = S.order_payment
-- Update/Insert
WHEN MATCHED THEN
  UPDATE SET
    T.total_customer = S.total_customer,
    T.detail = S.detail
WHEN NOT MATCHED THEN
  INSERT (
    order_date,
    no_of_service,
    total_customer,
    detail,
    order_payment
  )
  VALUES (
    S.order_date,
    S.no_of_service,
    S.total_customer,
    S.detail,
    S.order_payment
  );