# Task Assignment

## 01 & 02 - Daily Customer Orders

For this implementation, I create Python modules to run Update/Insert query in BigQuery for sample data. I design BQ helper function to create easier BQ interface to run query and parameterized query with Jinja Templating.


**Run Script**
```sh
python -m daily_customer_orders.main [START_DATE] [END_DATE]
```


where:
- START_DATE: start date in format **%Y-%m-%d**
- END_DATE: end date in format **%Y-%m-%d**


By default, the script will process with START_DATE equal to yesterday and END_DATE equal to today.

**Sample Runtime**
```sh
python -m daily_customer_orders.main 2024-01-01 2024-01-02

# Default
python -m daily_customer_orders.main
```

The module can be accessed from [here](./01%20&%2002%20-%20daily_customer_orders/).


## 03 - Driver Registration

For this implementation, I create Python modules to run CSV to JSON parser. I define schema to reflect data model and used as data contract between different format/interface. To achieve this, I used pydantic library. The data extracted and converted to local directory (default: source and target directory in scripts).


**Run Script**
```sh
python -m driver_registration.main [FILENAME]
```

where:
- FILENAME: source CSV file (without extension)


**Sample Runtime**
```sh
python -m driver_registration.main driver_registration
```


The module can be accessed from [here](./03%20-%20driver_registration/).


## 04 - Summary Payments
### Exploration
For this case, I highligthed several issues that I want to solved:

**1. Repetitive query filter defined**


I notice that there are several usage of filter (**transaction_time** and **gopay_id**) defined in several areas. This could lead to hardly maintain query or to many injected query if this query want to be automated/parameterized.


**2. Including unsued query from source filter**


I notice that there is *wildcard* column selected at the first CTE. This could lead to exposing to many information and unmaintainable data model, or even a hardly trace source column of generated data.

**3. Unused table**


I notice that there is **gopay** table included in the query, where all the information already provided in previous CTE. This could lead to uneccessary data scanning.

**4. Late Filter**


I notice that data filtering are happened late of last CTE. This could potentially lead to unused data partition and high computation/scan.


**5. Unlabelled query**

I notice that there are no table alias in column selection. This could lead to unclear information, therefore the query will be hard to track and maintain.

### Solution
The solution that I provided are:
- Create CTE to act as reusable filter, where it can easily be used to filter data
- Filter data early. For row filter, I used previously CTE filter. For column filter, I defined only neccessary filter
- Remove **gopay** table in query to reduce uneccessary data scan
- Giving column label from table alias

The query can be accessed at [here](./04%20-%20summary_payments/optimized.sql).


## 05 - Data Modelling

For this implementation, I focused on creating simple DW model for two cases:
1. Daily Summary, where the goals is to show daily overview of all transaction and total distinct gopay user.
2. Gopay Single View of Customer (Monthly), where the goals is to give summary of each Gopay customer in monthly range.


The ERD can be accessed [here](./05%20-%20data_modelling/data_modelling.png)

![Data Modelling ERD](./05%20-%20data_modelling/data_modelling.png)


## 06 - Data Automation

For this implementation, I create simple data automation flow that focus on ingesting and prepare clean data for report. Below are the implementation diagram:

![Data Automation Flow](./06%20-%20data_automation/data-flow.png)


**Description**:
1. 01.00 AM: Report Data ETL. Data extracted in report format (stuctured as report requirements) from source data.
2. 02.00 AM: Report Metadata ETL. Metadata (e.g., row count, distinct key) extracted from source data.
3. 03.00 AM: Data Validation ETL. Process to validate and make sure data correctly ingested and processed. If there is some inconsistency, it possible to send alert to assigned developer.
4. 07.00 AM: Data Cleansing ETL. Process to cleaning and re-checking data integrity that will be used for reporting.


To implement this solution, several services can be used:
1. Apache Airflow, job orchestrator service. Airflow can be used to schedulle and maintain dependecies between ETL/functions.
2. Dataflow, ETL tools. Dataflow can be used to created ETL modules for all processing. Dataflow ETL modules will be triggered from Airflow.
3. BigQuery, Data Warehouse. BigQuery can be used as data layer for versioning, staging and preparation for data reporting.
4. Google Cloud Storage (GCS), archival storage. GCS can be used as data archival service for log, old data or any reference temporary storage.


To further increase query performance, several things can be implement:
1. Reduce excessive JOIN between tables. Find solution that minimize JOIN operations on table because it can easily create heavy computation processes.
2. Early filter for fact or transactional table. Early filter will reduce scan process when data used at JOIN or any aggregation and calculation function.
3. Run processes on low traffic time. This action will make sure all the resources are focused on ETL processes.
4. Use index on highly used column.
5. Use snapshot summary data on daily report to reduce re-calculation on old data.