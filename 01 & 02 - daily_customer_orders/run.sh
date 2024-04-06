#!/bin/sh

# Format:
#   python -m daily_customer_orders.main [START_DATE] [END_DATE]
# Sample:
#   python -m daily_customer_orders.main 2024-01-01 2024-01-02

python -m daily_customer_orders.main $1 $2