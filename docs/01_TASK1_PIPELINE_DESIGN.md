# Task 1: Analytics Pipeline Design

## LLM Prompt Used

```
You are a data architect designing an analytics pipeline for an online retail company.
Business Context:
- An online retail company wants to analyze sales performance and customer behavior
- They need to answer questions about daily/monthly sales trends, top products, top customers, order status impact, and AOV by region
- Data sources: customers.csv, products.csv, orders.csv
- Current data: 50 customers, 60 products, 100 orders

Design a medallion architecture analytics pipeline with the following considerations:
1. Define Bronze, Silver, and Gold layers
2. Justify batch processing vs near-real-time
3. Recommend storage format and why
4. Suggest partitioning strategy
5. Design data flow from raw CSV to BI-ready datasets
```

## Pipeline Design Output

### 1. High-Level Architecture: Bronze → Silver → Gold → BI

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA SOURCES (Raw CSV)                       │
│                customers.csv, products.csv, orders.csv           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           BRONZE LAYER (Raw Data Ingestion)                      │
│   - Copy CSV files as-is with minimal transformations            │
│   - Add ingestion timestamp, source metadata                     │
│   - Preserve all columns, data types from source                 │
│   - Tables: bronze_customers, bronze_products, bronze_orders    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│          SILVER LAYER (Cleaned & Standardized Data)              │
│   - Data quality checks, deduplication, standardization          │
│   - Clean column names, handle nulls, validate data types        │
│   - Add technical fields: created_date, updated_date, is_active  │
│   - Tables: silver_customers, silver_products, silver_orders    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│       GOLD LAYER (Analytics & BI Ready - Star Schema)            │
│   - Dimensional modeling with fact & dimension tables            │
│   - Aggregations, calculated metrics, denormalizations           │
│   - Optimized for reporting and analytics queries                │
│   Fact Table:                                                     │
│   - fact_sales (order_id, order_date_key, customer_key,          │
│                  product_key, quantity, total_amount, status)    │
│   Dimension Tables:                                               │
│   - dim_customer (customer_key, customer_id, name, city, etc)   │
│   - dim_product (product_key, product_id, name, category, price)│
│   - dim_date (date_key, date, day_of_week, month, quarter, year)│
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BI & ANALYTICS TOOLS                           │
│        (Dashboards, Reports, Ad-hoc Queries, ML Models)         │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Batch Processing Justification

**Why Batch Processing?**

1. **Data Characteristics**
   - Orders are recorded at transaction time (hourly/daily level)
   - No real-time trading or high-frequency updates needed
   - Customer & product data changes infrequently
   - Historical analysis is a primary use case

2. **Business Requirements**
   - Daily/monthly trend analysis (daily aggregations sufficient)
   - Strategic decisions, not real-time alerts
   - Can tolerate data latency of 24 hours
   - Cost efficiency is important for SME retailer

3. **Operational Benefits**
   - Simpler infrastructure and maintenance
   - Better resource utilization (scheduled daily jobs)
   - Easier data quality validation and error recovery
   - Lower total cost of ownership
   - Predictable performance and scheduling

4. **Limitations Accepted**
   - Data freshness: Daily (not real-time)
   - Best for: Historical analysis, trend reports, executive dashboards
   - Not suitable for: Real-time inventory alerts, fraud detection

**Processing Schedule**: Daily (e.g., 2 AM UTC) after business day ends

---

### 3. Storage Format: Parquet

**Why Parquet Over CSV or Other Formats?**

| Aspect | CSV | Parquet | Rationale |
|--------|-----|---------|-----------|
| **Compression** | None (10-20% gzip) | 70-80% (snappy) | 🏆 Parquet: Columnar compression |
| **Query Performance** | Full scan required | Column pruning | 🏆 Parquet: Predicate pushdown |
| **Schema Enforcement** | None | Strongly typed | 🏆 Parquet: Data quality |
| **Data Types** | All strings | Native types | 🏆 Parquet: Type safety |
| **Append Operations** | Overwrite only | Schema evolution | 🏆 Parquet: Flexibility |
| **File Size** | Large (~10MB) | Small (~2MB) | 🏆 Parquet: 5x smaller |
| **Ecosystem** | Universal | Spark, Pandas, Arrow | 🏆 Parquet: Modern tools |

**Parquet Benefits:**
- **Storage Efficiency**: Reduces storage cost by 70-80%
- **Query Speed**: 10-100x faster analytical queries
- **Scalability**: Supports petabyte-scale datasets
- **Compatibility**: Native support in Pandas, PySpark, DuckDB
- **Metadata**: Built-in schema and statistics for optimization

---

### 4. Partitioning Strategy

**Partition by: `order_date` (date grain)**

**Rationale:**
1. **Business Alignment**: Most queries filter by date range (daily trends, monthly reports)
2. **Query Performance**: Partition pruning eliminates 90%+ of data scans
3. **Data Volume**: 100 orders ÷ ~3 months ≈ 33 orders/day (manageable partitions)
4. **Retention Policy**: Archive old partitions, delete after 7 years
5. **Consistency**: Order date is immutable, not updated

**Partition Scheme:**
```
data/processed/gold/fact_sales/
├── order_date=2023-01-15/
│   └── fact_sales_20250101_001.parquet
├── order_date=2023-01-16/
│   └── fact_sales_20250101_002.parquet
├── order_date=2023-01-17/
│   └── fact_sales_20250101_003.parquet
└── ...
```

**Alternative Partitions (Not Recommended):**
- `customer_id`: Creates too many small partitions, unbalanced
- `product_id`: Creates sparse partitions with few records
- `year/month`: Good for long-term retention, use for archive

---

### 5. Data Quality Checkpoints

**Bronze Layer**: Preserve all data, document ingestion
- Record count validation (source vs target)
- Schema consistency check

**Silver Layer**: Quality enforcement
- Null checks on key columns
- Duplicate detection
- Data type validation
- Date range validation

**Gold Layer**: Business logic validation
- Referential integrity (customer_key, product_key)
- Calculation accuracy (total_amount = quantity × price)
- Status values IN ('Completed', 'Cancelled', 'Returned')

---

### 6. Technology Stack

| Layer | Tool | Format | Location |
|-------|------|--------|----------|
| **Ingestion** | Python/Pandas | CSV → Parquet | `data/raw/` → `data/processed/bronze/` |
| **Transformation** | PySpark/Pandas | Parquet | `data/processed/silver/` → `data/processed/gold/` |
| **Orchestration** | Airflow/Cron | YAML/Python | `scripts/etl_*.py` |
| **BI/Analytics** | Metabase/Streamlit | Parquet | `data/processed/gold/` |

---

## Assumptions & Constraints

1. **Data Volume**: Current data is small (100 orders), batch jobs run in seconds
2. **Growth Assumption**: If scale to 1M+ daily orders, consider Spark instead of Pandas
3. **Retention**: Keep 7 years of order data, 2 years of customers/products
4. **SLA**: 24-hour data latency acceptable, uptime 99%
5. **Cost**: Minimize compute cost, optimize for storage efficiency

---

## Next Steps

1. ✅ Define star schema (Task 2)
2. ✅ Implement ETL code (Task 3)
3. ✅ Define data quality rules (Task 4)
4. ✅ Auto-generate documentation (Task 5)

