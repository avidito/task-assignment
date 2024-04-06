import sys

from driver_registration.helper import (
    CSVHelper,
    JSONHelper,
)
from driver_registration.schema import (
    DriverRegistration,
)
from driver_registration.config import Config


def main(filename: str):
    # Init Helper
    config = Config()
    csv_h = CSVHelper(config.SOURCE_DIR, config.TARGET_DIR)
    json_h = JSONHelper(config.SOURCE_DIR, config.TARGET_DIR)
    
    # Get Data
    data = csv_h.get_data(
        source_filename = filename,
        Schema = DriverRegistration,
    )

    # Parse Data
    json_h.export_data(
        data = data,
        target_filename = filename
    )


if __name__ == "__main__":
    _, filename = sys.argv

    main(filename)