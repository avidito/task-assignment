import os
from typing import Optional
from datetime import datetime, timedelta
import pytz

from daily_customer_orders.config import Config
from daily_customer_orders.helper import (
    BQHelper,
)

# Contant
JAKARTA_TZ = pytz.timezone("Asia/Jakarta")
QUERY_DIR = os.path.join(os.path.dirname(__file__), "query")


# Main
def main(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    # Init Helper
    config = Config()
    bq_h = BQHelper(config.PROJECT_ID, QUERY_DIR)

    # Params Resolved
    p_start_date = start_date if (start_date) else (datetime.now(JAKARTA_TZ) - timedelta(days=1)).strftime("%Y-%m-%d")
    p_end_date = end_date if (end_date) else datetime.now(JAKARTA_TZ).strftime("%Y-%m-%d")
    
    # Run Query
    bq_h.run_query("tr_daily_customer_orders.sql", params={
        "dt_filter": f'{config.DATE_COLUMN} BETWEEN "{p_start_date}" AND "{p_end_date}"'
    })

# Runtime
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("daily_customer_orders")
    parser.add_argument("--start-date", default=None, help="Start date of date filter")
    parser.add_argument("--end-date", default=None, help="End date of date filter")
    
    args = parser.parse_args()
    main(args.start_date, args.end_date)