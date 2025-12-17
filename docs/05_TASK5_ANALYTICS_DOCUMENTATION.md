# Task 5: Auto-Generated Analytics Pipeline Documentation

## LLM Prompt Used

```
You are a technical documentation specialist creating comprehensive documentation for a data analytics pipeline.
Document the following:

1. Business Overview
   - Company context and business questions being answered
   - Stakeholder needs
   - Expected benefits

2. System Architecture
   - Data flow diagram (Bronze → Silver → Gold)
   - Component interactions
   - Technology stack

3. Source-to-Target Mapping
   - How each source column maps to target tables
   - Transformations applied
   - Data lineage

4. Schema Explanation
   - Fact and dimension tables
   - Surrogate keys and slowly changing dimensions
   - Key metrics and calculations

5. ETL Flow Documentation
   - Step-by-step ETL process
   - Validation checkpoints
   - Error handling strategy

6. Data Quality Checks
   - DQ rules applied at each layer
   - Validation framework
   - Remediation procedures

7. Analytics Use Cases
   - Key business questions supported
   - Example queries
   - Dashboard concepts

8. Assumptions & Limitations
   - Data volume assumptions
   - Latency tolerance
   - Growth considerations
   - Known limitations

9. Maintenance & Operations
   - Deployment instructions
   - Monitoring checklist
   - Troubleshooting guide
```

---

## 1. Business Overview

### Problem Statement

An online retail company operates across multiple regions with diverse product categories. Leadership needs data-driven insights to:

1. **Monitor Sales Performance**: What are daily and monthly sales trends?
2. **Optimize Product Mix**: Which products and categories generate highest revenue?
3. **Understand Customer Behavior**: Who are our top customers and how is their spending?
4. **Assess Order Quality**: How does order status (Completed/Cancelled/Returned) impact revenue?
5. **Regional Analysis**: What is average order value by geography?

### Business Context

- **Company**: Online Retail (60 product SKUs, 50 active customers, ~100 orders analyzed)
- **Data Sources**: 3 CSV files (customers, products, orders)
- **Update Frequency**: Daily (batch processing)
- **Primary Users**: BI Analysts, Business Managers, Executive Dashboard Consumers
- **Decision Timeline**: Strategic (weekly/monthly decisions, not real-time alerts)

### Expected Business Impact

| Metric | Impact |
|--------|--------|
| **Revenue Tracking** | Monitor top-selling products and categories, identify seasonal trends |
| **Customer Lifetime Value** | Identify high-value customers, improve retention strategies |
| **Order Quality** | Analyze cancellation/return rates, improve fulfillment |
| **Geographic Performance** | Optimize regional inventory and marketing spend |
| **Dashboard Self-Service** | Enable analysts to query data without SQL engineering support |

---

## 2. System Architecture

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     RAW DATA SOURCES                                │
│   customers.csv (50 rows)  | products.csv (60 rows)               │
│   orders.csv (100 rows)                                             │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BRONZE LAYER                                     │
│              (Raw Data with Metadata)                               │
│   bronze_customers.parquet (50 rows)                                │
│   bronze_products.parquet (60 rows)                                 │
│   bronze_orders.parquet (100 rows)                                  │
│                                                                     │
│   • Minimal transformations                                         │
│   • Add ingestion timestamp & source metadata                       │
│   • Preserve all columns from source                                │
└────────────────────┬────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │ Data Quality Checks     │
        │ - Record counts         │
        │ - Schema validation     │
        └────────────┬────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SILVER LAYER                                     │
│           (Cleaned & Standardized Data)                             │
│   silver_customers.parquet (~50 rows)                               │
│   silver_products.parquet (~60 rows)                                │
│   silver_orders.parquet (~100 rows)                                 │
│                                                                     │
│   • Remove nulls, duplicates                                        │
│   • Standardize column names & data types                           │
│   • Add technical fields (created_date, updated_date)               │
│   • Validate data ranges and formats                                │
└────────────────────┬────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │ Data Quality Checks     │
        │ - Completeness rules    │
        │ - Validity checks       │
        │ - Uniqueness            │
        └────────────┬────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    GOLD LAYER                                       │
│         (Star Schema - BI Ready)                                    │
│                                                                     │
│   DIMENSION TABLES:                                                 │
│   • dim_customer (~50 rows) - Customer profiles                    │
│   • dim_product (~60 rows) - Product catalog                       │
│   • dim_date (4017 rows) - 11-year date dimension                  │
│                                                                     │
│   FACT TABLE:                                                       │
│   • fact_sales (~100 rows) - Order transactions                    │
│     - Surrogate keys linking to dimensions                         │
│     - Calculated metrics (total_amount)                            │
│     - Grain: 1 row per order                                       │
└────────────────────┬────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │ Data Quality Checks     │
        │ - Referential integrity │
        │ - Calculation accuracy  │
        │ - Dimension completeness│
        └────────────┬────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│              BI TOOLS & ANALYTICS                                   │
│   • Metabase / Tableau / Power BI / Streamlit                      │
│   • Ad-hoc SQL queries                                              │
│   • Executive dashboards                                            │
│   • Analytics reports                                               │
└─────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Data Ingestion** | Python 3.x | Read and validate CSV files |
| **Transformation Engine** | Pandas | Clean, join, aggregate data |
| **Storage Format** | Parquet (Snappy compression) | Columnar storage, 70% compression |
| **Orchestration** | Cron / Airflow | Daily ETL scheduling |
| **Languages** | Python, SQL | Data engineering scripts |
| **Version Control** | Git | Code and configuration tracking |
| **BI Platform** | Metabase / Streamlit | Self-service analytics |

### Data Volumes & Performance

| Metric | Current | Projected (Year 2) |
|--------|---------|-------------------|
| **Customers** | 50 | 10,000 |
| **Products** | 60 | 5,000 |
| **Daily Orders** | ~3 | ~500 |
| **Annual Orders** | ~1,200 | 180,000 |
| **Bronze Size** | ~50 KB | ~8 MB |
| **Silver Size** | ~40 KB | ~6 MB |
| **Gold Size** | ~30 KB | ~4 MB |
| **ETL Runtime** | <1 min | ~5-10 min (Pandas) |
| **Growth Trigger for Spark** | 10M+ annual orders | TBD |

---

## 3. Source-to-Target Mapping

### Complete Data Lineage

```
CUSTOMERS.CSV (Source)
├─ customer_id          ──→ DIM_CUSTOMER.customer_id (Business Key)
├─ customer_name        ──→ DIM_CUSTOMER.customer_name
├─ email                ──→ DIM_CUSTOMER.email
├─ city                 ──→ DIM_CUSTOMER.city
├─ state                ──→ DIM_CUSTOMER.state
├─ country              ──→ DIM_CUSTOMER.country
├─ signup_date          ──→ DIM_CUSTOMER.signup_date
├─ [Generated]          ──→ DIM_CUSTOMER.customer_key (Surrogate Key)
├─ [state → region]     ──→ DIM_CUSTOMER.region (Derived)
├─ [TRUE]               ──→ DIM_CUSTOMER.is_active
├─ [TODAY]              ──→ DIM_CUSTOMER.created_date
└─ [TODAY]              ──→ DIM_CUSTOMER.updated_date

PRODUCTS.CSV (Source)
├─ product_id           ──→ DIM_PRODUCT.product_id (Business Key)
├─ product_name         ──→ DIM_PRODUCT.product_name
├─ category             ──→ DIM_PRODUCT.category
├─ price                ──→ DIM_PRODUCT.price
├─ [Generated]          ──→ DIM_PRODUCT.product_key (Surrogate Key)
├─ [TRUE]               ──→ DIM_PRODUCT.is_active
├─ [TODAY]              ──→ DIM_PRODUCT.created_date
└─ [TODAY]              ──→ DIM_PRODUCT.updated_date

ORDERS.CSV (Source)
├─ order_id             ──→ FACT_SALES.order_id (Primary Key)
├─ order_date           ──→ FACT_SALES.order_date_key (YYYYMMDD format)
├─ customer_id          ──→ FACT_SALES.customer_key (via DIM_CUSTOMER join)
├─ product_id           ──→ FACT_SALES.product_key (via DIM_PRODUCT join)
├─ quantity             ──→ FACT_SALES.quantity
├─ [product.price]      ──→ FACT_SALES.unit_price (from PRODUCTS lookup)
├─ [qty × price]        ──→ FACT_SALES.total_amount (CALCULATED)
├─ order_status         ──→ FACT_SALES.order_status
├─ payment_mode         ──→ FACT_SALES.payment_mode
└─ [TODAY]              ──→ FACT_SALES.created_date

DIM_DATE (Generated)
└─ Generate all dates 2020-01-01 to 2030-12-31
   ├─ date_key (YYYYMMDD) ──→ PK for joining
   ├─ calendar_date
   ├─ day_of_week, month, quarter, year
   └─ is_holiday, is_weekend (flags)
```

---

## 4. Schema Explanation

### Star Schema Design

**Key Principle**: Dimensional modeling optimizes for fast, intuitive analytics queries.

**Fact Table: fact_sales**
- **Grain**: One row per order transaction
- **Row Count**: 100 rows (sample data)
- **Primary Key**: order_id
- **Foreign Keys**: customer_key, product_key, order_date_key
- **Measures**: quantity, unit_price, total_amount
- **Attributes**: order_status, payment_mode

**Key Metrics Calculated**:
```sql
-- Total Revenue (Completed Orders Only)
SELECT SUM(total_amount) 
FROM fact_sales 
WHERE order_status = 'Completed'

-- Average Order Value (AOV) by Region
SELECT dim_customer.region, AVG(fact_sales.total_amount)
FROM fact_sales
JOIN dim_customer ON fact_sales.customer_key = dim_customer.customer_key
GROUP BY dim_customer.region

-- Product Revenue Ranking
SELECT dim_product.product_name, SUM(fact_sales.total_amount) as revenue
FROM fact_sales
JOIN dim_product ON fact_sales.product_key = dim_product.product_key
WHERE fact_sales.order_status = 'Completed'
GROUP BY dim_product.product_name
ORDER BY revenue DESC
```

### Slowly Changing Dimensions (SCD)

**DIM_CUSTOMER (SCD Type 2 - Track History)**
- When customer address changes: insert new row with new surrogate key
- Old row: is_active = false
- Enables: "What was the revenue from customers in California?" (historical)

**DIM_PRODUCT (SCD Type 1 - Overwrite)**
- When price changes: overwrite old price
- No historical tracking of price changes
- Enables: Current product catalog view

**DIM_DATE (Static)**
- Pre-loaded, immutable
- No changes after initial load

---

## 5. ETL Flow Documentation

### Step-by-Step ETL Process

```
PHASE 1: BRONZE LAYER (Raw Data Ingestion)
├─ Load customers.csv → bronze_customers.parquet
├─ Load products.csv → bronze_products.parquet
├─ Load orders.csv → bronze_orders.parquet
├─ Add _ingestion_timestamp and _source metadata
└─ Quality Check: Record count validation

PHASE 2: SILVER LAYER (Data Cleaning)
├─ silver_customers:
│  ├─ Validate non-null customer_id, customer_name, email
│  ├─ Convert signup_date to DATE type
│  ├─ Add is_active, created_date, updated_date columns
│  └─ Remove records with NULL required fields
├─ silver_products:
│  ├─ Validate non-null product_id, product_name, price
│  ├─ Convert price to DECIMAL, remove negatives
│  ├─ Add is_active, created_date, updated_date columns
│  └─ Remove invalid records
├─ silver_orders:
│  ├─ Validate non-null order_id, customer_id, product_id, quantity, order_status
│  ├─ Convert order_date to DATE type
│  ├─ Validate order_status IN ('Completed', 'Cancelled', 'Returned')
│  ├─ Remove records with quantity ≤ 0
│  └─ Add created_date column
└─ Quality Check: Completeness, validity, uniqueness rules

PHASE 3A: GOLD LAYER - DIM_DATE (Dimension)
├─ Generate date range: 2020-01-01 to 2030-12-31
├─ Calculate date_key (YYYYMMDD format)
├─ Compute day_of_week, month, quarter, year
├─ Flag holidays (US holidays)
├─ Flag weekends
└─ Write to: data/processed/gold/dimensions/dim_date.parquet

PHASE 3B: GOLD LAYER - DIM_CUSTOMER (Dimension)
├─ Copy from silver_customers
├─ Generate customer_key (ROW_NUMBER)
├─ Derive region from state mapping
├─ Write to: data/processed/gold/dimensions/dim_customer.parquet
└─ Quality Check: Unique customer_key, non-null required fields

PHASE 3C: GOLD LAYER - DIM_PRODUCT (Dimension)
├─ Copy from silver_products
├─ Generate product_key (ROW_NUMBER)
├─ Write to: data/processed/gold/dimensions/dim_product.parquet
└─ Quality Check: Unique product_key, non-null required fields

PHASE 3D: GOLD LAYER - FACT_SALES (Fact Table)
├─ Start with silver_orders
├─ Convert order_date to order_date_key (YYYYMMDD)
├─ LEFT JOIN dim_customer on customer_id to get customer_key
├─ LEFT JOIN dim_product on product_id to get product_key
├─ Calculate total_amount = quantity × unit_price
├─ Select final columns: order_id, keys, quantity, unit_price, total_amount, status, payment_mode
├─ Remove rows with NULL foreign keys
├─ Write to: data/processed/gold/facts/fact_sales.parquet
└─ Quality Check: Referential integrity, calculation accuracy, positive values

PHASE 4: DATA QUALITY VALIDATION
├─ Completeness: Check for NULLs in required fields
├─ Referential Integrity: Validate foreign key references
├─ Calculation Accuracy: Verify total_amount = quantity × unit_price
├─ Uniqueness: Check surrogate key duplicates
├─ Validity: Validate order_status values
└─ Report: Pass/Fail status for each rule

PHASE 5: SUCCESS/FAILURE
├─ SUCCESS: Log completion, update metadata
└─ FAILURE: Alert administrator, pause downstream processes
```

### Error Handling Strategy

| Error Type | Detection | Action |
|-----------|-----------|--------|
| **CSV Missing** | File not found | Stop pipeline, alert |
| **Schema Mismatch** | Column count/type mismatch | Stop pipeline, alert |
| **Data Quality** | Validation rules fail | Log warning, continue (non-blocking) |
| **Referential Integrity** | FK validation fails | Remove orphaned records, log |
| **Calculation Error** | Math validation fails | Recalculate, log discrepancy |

---

## 6. Data Quality Checks

### Quality Rules by Layer

**Bronze Layer**:
- ✓ All files present and not empty
- ✓ Column count matches schema definition
- ✓ Record counts logged

**Silver Layer**:
- ✓ Required fields are NOT NULL
- ✓ Data types are correct
- ✓ Value ranges are valid (e.g., price > 0)
- ✓ No duplicate primary keys
- ✓ Date formats standardized

**Gold Layer**:
- ✓ All foreign keys reference existing records
- ✓ Calculations are accurate (±0.01 tolerance)
- ✓ Surrogate keys are unique
- ✓ Order status values valid
- ✓ Fact table grain is consistent

### Validation Framework

```python
# Run validations after each layer
validator = DataQualityValidator(gold_path)
results = validator.run_all_validations()

# Results include:
# - rule_id: Unique rule identifier
# - rule_name: Human-readable rule description
# - pass_fail: Boolean result
# - failed_records: Count of records failing rule
# - severity: ERROR | WARNING | INFO
# - timestamp: When validation ran
```

---

## 7. Analytics Use Cases

### Key Business Questions Supported

#### 1. Sales Trends
```sql
-- Daily Sales Trend
SELECT 
  dd.calendar_date,
  SUM(fs.total_amount) as daily_revenue,
  COUNT(DISTINCT fs.order_id) as order_count
FROM fact_sales fs
JOIN dim_date dd ON fs.order_date_key = dd.date_key
WHERE fs.order_status = 'Completed'
GROUP BY dd.calendar_date
ORDER BY dd.calendar_date DESC
```

#### 2. Top Products by Revenue
```sql
-- Top 10 Products
SELECT 
  dp.product_name,
  dp.category,
  COUNT(DISTINCT fs.order_id) as orders,
  SUM(fs.quantity) as units_sold,
  SUM(fs.total_amount) as total_revenue,
  AVG(fs.total_amount) as avg_order_value
FROM fact_sales fs
JOIN dim_product dp ON fs.product_key = dp.product_key
WHERE fs.order_status = 'Completed'
GROUP BY dp.product_name, dp.category
ORDER BY total_revenue DESC
LIMIT 10
```

#### 3. Top Customers by Spend
```sql
-- Top 20 Customers
SELECT 
  dc.customer_name,
  dc.region,
  COUNT(DISTINCT fs.order_id) as order_count,
  SUM(fs.total_amount) as lifetime_value
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
WHERE fs.order_status = 'Completed'
GROUP BY dc.customer_name, dc.region
ORDER BY lifetime_value DESC
LIMIT 20
```

#### 4. Order Status Impact
```sql
-- Revenue by Order Status
SELECT 
  fs.order_status,
  COUNT(DISTINCT fs.order_id) as order_count,
  SUM(fs.total_amount) as revenue,
  ROUND(SUM(fs.total_amount) / (SELECT SUM(total_amount) FROM fact_sales) * 100, 2) as revenue_pct
FROM fact_sales fs
GROUP BY fs.order_status
ORDER BY revenue DESC
```

#### 5. Average Order Value by Region
```sql
-- AOV by Region
SELECT 
  dc.region,
  COUNT(DISTINCT fs.order_id) as order_count,
  AVG(fs.total_amount) as aov,
  MIN(fs.total_amount) as min_order,
  MAX(fs.total_amount) as max_order
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
WHERE fs.order_status = 'Completed'
GROUP BY dc.region
ORDER BY aov DESC
```

---

## 8. Assumptions & Limitations

### Assumptions

1. **Data Volume & Growth**
   - Current: 50 customers, 60 products, 100 orders
   - Projected Year 2: 10K customers, 5K products, 180K orders/year
   - **Scaling Decision**: Switch to PySpark when reaching 1M+ annual orders

2. **Data Latency**
   - Batch processing with 24-hour latency acceptable
   - Daily ETL run at 2 AM UTC (after business day ends)
   - Real-time queries not required

3. **Data Quality**
   - Source data is reasonably clean (no major data corruption)
   - Customers and products are stable (low churn)
   - Orders are immutable once created

4. **Infrastructure**
   - Cloud storage (S3/Azure) for scalability
   - Assume sufficient disk space for Parquet files

5. **Business Context**
   - Online retail with domestic customers (US focus)
   - Quarterly business review cycle
   - Non-regulated industry (PII handling not critical, but good practice)

### Limitations

1. **Historical Price Tracking**
   - DIM_PRODUCT uses SCD Type 1 (overwrites)
   - Cannot analyze "revenue at historical price"
   - Workaround: Create separate dim_product_history table if needed

2. **Customer Attributes**
   - Limited demographic data (no age, gender, segment)
   - Email is only contact point
   - Recommend collecting more customer attributes

3. **Data Completeness**
   - Missing: Product cost, inventory, shipping info
   - Missing: Customer lifetime value, acquisition channel
   - Missing: Competitive pricing data

4. **Analytical Limitations**
   - Cannot perform RFM (Recency/Frequency/Monetary) without more data
   - No churn prediction capability
   - No product recommendation engine possible with current schema

5. **Performance Constraints**
   - Parquet assumes query engines like DuckDB, Pandas, or Spark
   - BI tools must support Parquet natively or via connector
   - Very large fact tables (100M+ rows) may require additional indexing

6. **Geographic Coverage**
   - Currently US-only state mapping
   - Expand region mapping if adding international customers

---

## 9. Maintenance & Operations

### Deployment Instructions

1. **Environment Setup**
   ```bash
   # Clone repository
   git clone <repo-url>
   cd GenAI-Analytics-Pipeline
   
   # Create Python virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Run ETL Pipeline**
   ```bash
   # Execute ETL
   python scripts/etl_pipeline.py
   
   # Expected output:
   # - Parquet files in data/processed/gold/
   # - Log file with execution details
   # - Data quality report
   ```

3. **Schedule Daily Runs**
   ```bash
   # Add to crontab (Linux/Mac)
   0 2 * * * /usr/bin/python3 /path/to/etl_pipeline.py >> /var/log/etl.log 2>&1
   
   # On Windows: Use Task Scheduler
   # Trigger: Daily at 2:00 AM
   # Action: python C:\path\to\etl_pipeline.py
   ```

### Monitoring Checklist

**Daily After ETL Completion**:
- [ ] Check ETL log for errors or warnings
- [ ] Verify all Parquet files created successfully
- [ ] Review data quality report (pass/fail counts)
- [ ] Confirm row counts match expectations
- [ ] Check total file sizes (should be consistent)

**Weekly**:
- [ ] Monitor disk usage for Parquet files
- [ ] Review customer/product growth trends
- [ ] Verify new dimension records are created
- [ ] Check for any data quality degradation

**Monthly**:
- [ ] Review archival/retention policy
- [ ] Analyze ETL runtime trends
- [ ] Check for schema drift (new columns in source)
- [ ] Update documentation if changes made

### Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| **"FileNotFoundError: customers.csv"** | CSV file missing | Verify raw data in `data/raw/` directory |
| **"No module named pandas"** | Missing dependency | Run `pip install -r requirements.txt` |
| **Parquet file empty** | ETL logic error | Check log for join failures, validate SQL |
| **Data quality rules failing** | Data corruption | Review source data, check for new invalid values |
| **Duplicate orders in fact_sales** | Join logic error | Verify customer_id and product_id uniqueness |
| **OutOfMemoryError** | Dataset too large for Pandas | Upgrade to PySpark for distributed processing |

---

## Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-15 | Data Team | Initial documentation |

---

## Contact & Support

- **Data Engineering Lead**: [Contact Info]
- **BI Analyst**: [Contact Info]
- **Documentation**: [Wiki URL]
- **Issues/Bugs**: [GitHub Issues URL]

