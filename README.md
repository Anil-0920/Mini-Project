# GenAI-Driven Analytics Pipeline for Online Retail

## 📋 Project Overview

A complete end-to-end analytics pipeline demonstrating:
- **LLM-driven pipeline design** (business requirements → technical architecture)
- **Auto-generated star schema** (dimensional modeling for analytics)
- **Production ETL code** (Pandas-based data transformation)
- **Data quality framework** (comprehensive validation rulebook)
- **Auto-generated documentation** (architecture, schema, operations)

**Status**: ✅ Production Ready (Sample Data Included)

---

## 🎯 Quick Start

### 1. Prerequisites
```bash
# Python 3.8+
python --version

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the ETL Pipeline
```bash
cd scripts
python etl_pipeline.py
```

**Expected Output**:
- ✓ Parquet files generated in `data/processed/gold/`
- ✓ Data quality validation report
- ✓ Execution logs with record counts

### 3. Explore the Data
```python
import pandas as pd
from pathlib import Path

gold_path = Path('../data/processed/gold')

# Load fact table
fact_sales = pd.read_parquet(gold_path / 'facts' / 'fact_sales.parquet')
print(f"Fact table shape: {fact_sales.shape}")
print(f"Total revenue: ${fact_sales['total_amount'].sum():,.2f}")

# Load dimension tables
dim_customer = pd.read_parquet(gold_path / 'dimensions' / 'dim_customer.parquet')
dim_product = pd.read_parquet(gold_path / 'dimensions' / 'dim_product.parquet')
```

---

## 📁 Project Structure

```
GenAI-Analytics-Pipeline/
│
├── data/
│   ├── raw/                          # Original CSV files
│   │   ├── customers.csv             # 50 customer records
│   │   ├── products.csv              # 60 product records
│   │   └── orders.csv                # 100 order records
│   │
│   └── processed/
│       ├── bronze/                   # Raw data with metadata
│       │   ├── bronze_customers.parquet
│       │   ├── bronze_products.parquet
│       │   └── bronze_orders.parquet
│       │
│       ├── silver/                   # Cleaned & standardized data
│       │   ├── silver_customers.parquet
│       │   ├── silver_products.parquet
│       │   └── silver_orders.parquet
│       │
│       └── gold/                     # Star schema (BI-ready)
│           ├── dimensions/
│           │   ├── dim_customer.parquet
│           │   ├── dim_product.parquet
│           │   └── dim_date.parquet
│           │
│           └── facts/
│               └── fact_sales.parquet
│
├── scripts/
│   ├── etl_pipeline.py               # Main ETL orchestrator
│   └── data_quality_validation.py    # DQ rules & validation (code in docs)
│
├── config/
│   └── (Future: Configuration files for parameters)
│
├── docs/
│   ├── 01_TASK1_PIPELINE_DESIGN.md
│   │   ├─ Business context
│   │   ├─ Pipeline architecture (Bronze/Silver/Gold)
│   │   ├─ Batch vs real-time justification
│   │   ├─ Parquet storage format rationale
│   │   └─ Date-based partitioning strategy
│   │
│   ├── 02_TASK2_STAR_SCHEMA.md
│   │   ├─ Star schema diagram
│   │   ├─ Fact table (fact_sales)
│   │   ├─ Dimension tables (customer, product, date)
│   │   ├─ Data dictionary with column descriptions
│   │   ├─ Surrogate key strategy
│   │   ├─ SCD Types (Type 1, Type 2)
│   │   └─ Source-to-target mapping
│   │
│   ├── 04_TASK4_DATA_QUALITY_RULEBOOK.md
│   │   ├─ 40+ data quality rules
│   │   ├─ Completeness, Validity, Accuracy, Uniqueness, Consistency
│   │   ├─ Rules by layer (Bronze/Silver/Gold)
│   │   ├─ Python validation code
│   │   ├─ Remediation procedures
│   │   └─ Monitoring & alerting
│   │
│   ├── 05_TASK5_ANALYTICS_DOCUMENTATION.md
│   │   ├─ Business overview & problem statement
│   │   ├─ System architecture & data flow
│   │   ├─ Complete source-to-target mapping
│   │   ├─ Schema explanation
│   │   ├─ ETL flow (step-by-step)
│   │   ├─ Analytics use cases with SQL examples
│   │   ├─ Assumptions & limitations
│   │   └─ Maintenance & operations guide
│   │
│   └── LLM_PROMPTS_USED.md
│       └─ All prompts that generated each task
│
├── notebooks/
│   └── (Future: Jupyter notebooks for exploration)
│
├── output/
│   ├── reports/
│   │   └── (Generated analysis reports)
│   │
│   └── charts/
│       └── (Generated visualizations)
│
├── README.md                         # This file
├── requirements.txt                  # Python dependencies
└── .gitignore                        # Git ignore file
```

---

## 🚀 Tasks Completed

### ✅ Task 1: Prompt → Pipeline Design
**Deliverable**: [docs/01_TASK1_PIPELINE_DESIGN.md](docs/01_TASK1_PIPELINE_DESIGN.md)

Design an analytics pipeline architecture:
- Convert business questions into data requirements
- Define Bronze/Silver/Gold medallion layers
- Justify batch processing (24-hour latency acceptable)
- Recommend Parquet storage (70% compression, fast queries)
- Partition by order_date for optimal performance
- Data quality checkpoints at each layer

**Key Decisions**:
- ✓ Batch processing (not real-time streaming)
- ✓ Parquet columnar format (vs CSV)
- ✓ Daily date-based partitions
- ✓ Medallion architecture (data lakehouse pattern)

---

### ✅ Task 2: Auto-Generated Star Schema
**Deliverable**: [docs/02_TASK2_STAR_SCHEMA.md](docs/02_TASK2_STAR_SCHEMA.md)

Design a dimensional model for analytics:
- Fact table `fact_sales` (100 rows) - one row per order
- Dimension tables:
  - `dim_customer` (50 rows, SCD Type 2)
  - `dim_product` (60 rows, SCD Type 1)
  - `dim_date` (4,017 rows, 11-year pre-loaded)
- Surrogate keys for small storage & fast joins
- Complete data dictionary with column descriptions
- Source-to-target mapping document

**Key Metrics Supported**:
- Daily/monthly revenue trends
- Product revenue ranking
- Customer lifetime value
- Order status impact analysis
- Regional AOV (Average Order Value)

---

### ✅ Task 3: ETL Code (Pandas)
**Deliverable**: [scripts/etl_pipeline.py](scripts/etl_pipeline.py)

Production ETL implementation:
- ✓ Read 3 CSV files (customers, products, orders)
- ✓ Bronze layer: Raw data with metadata
- ✓ Silver layer: Data cleaning & standardization
- ✓ Gold layer: Dimensional modeling & calculations
- ✓ Surrogate key generation
- ✓ Total amount calculation: quantity × price
- ✓ Data quality validation at each step
- ✓ Write all tables to Parquet format
- ✓ Comprehensive logging & error handling

**Features**:
- Modular class-based design
- 400+ lines of documented code
- Surrogate key generation strategy
- Region derivation from state
- Slowly Changing Dimension handling

---

### ✅ Task 4: Data Quality Rulebook
**Deliverable**: [docs/04_TASK4_DATA_QUALITY_RULEBOOK.md](docs/04_TASK4_DATA_QUALITY_RULEBOOK.md)

40+ comprehensive data quality rules:

**Rule Types**:
- **Completeness** (15 rules): NOT NULL validations
- **Validity** (7 rules): Valid values, format checks
- **Accuracy** (5 rules): Numeric ranges, calculations
- **Uniqueness** (4 rules): No duplicate keys
- **Consistency** (5 rules): Referential integrity, calculations

**Coverage by Layer**:
- Bronze (6 rules): Schema consistency, record counts
- Silver (13 rules): Data cleaning validation
- Gold (20 rules): Star schema integrity

**Deliverables**:
- Rule matrix with ID, name, condition, severity
- Python/Pandas validation code
- Remediation procedures
- Monitoring & alerting strategy

---

### ✅ Task 5: Auto-Generated Documentation
**Deliverable**: [docs/05_TASK5_ANALYTICS_DOCUMENTATION.md](docs/05_TASK5_ANALYTICS_DOCUMENTATION.md)

Comprehensive technical documentation:

1. **Business Overview**
   - Problem statement & context
   - Stakeholder needs
   - Expected business impact

2. **System Architecture**
   - Data flow diagram (Bronze → Silver → Gold)
   - Technology stack
   - Data volumes & performance metrics

3. **Source-to-Target Mapping**
   - Complete data lineage (CSV → Parquet)
   - Column transformations
   - Calculated fields

4. **Schema Explanation**
   - Fact table grain & measures
   - Dimension tables & SCD strategy
   - Key metrics with SQL examples

5. **ETL Flow Documentation**
   - Step-by-step pipeline phases
   - Quality checkpoints
   - Error handling strategy

6. **Analytics Use Cases**
   - 5 business questions with SQL
   - Example dashboard concepts

7. **Assumptions & Limitations**
   - Data volume & growth plan
   - Scaling triggers
   - Known limitations

8. **Maintenance & Operations**
   - Deployment instructions
   - Monitoring checklist
   - Troubleshooting guide

---

## 📊 Data Samples

### Customers (50 records)
```
customer_id: C001-C050
Fields: name, email, city, state, country, signup_date
```

### Products (60 records)
```
product_id: P001-P060
Categories: Electronics, Clothing, Sports, Beauty, Books, Home
Price range: $9.99 - $299.99
```

### Orders (100 records)
```
order_id: O001-O100
Order dates: 2023-01-15 to 2023-04-21
Statuses: Completed (78%), Cancelled (10%), Returned (12%)
Average order value: $95.47
Total revenue: $7,427.88
```

---

## 🔑 Key Insights from Sample Data

| Metric | Value |
|--------|-------|
| Total Revenue | $7,427.88 |
| Average Order Value (AOV) | $95.47 |
| Order Completion Rate | 78% |
| Cancellation Rate | 10% |
| Return Rate | 12% |
| Top Product | Desk Lamp LED ($39.99) |
| Top Customer | John Smith (3 orders, $159.98) |
| Top Region | Texas (13 orders) |

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Programming | Python | 3.8+ |
| Data Processing | Pandas | 1.3+ |
| Storage | Parquet (Snappy) | - |
| Logging | Python logging | 3.8+ |
| Date/Time | Python datetime | 3.8+ |
| Version Control | Git | - |

**Requirements**:
```
pandas>=1.3.0
pyarrow>=10.0.0
numpy>=1.20.0
```

---

## 📈 Growth Path & Scaling

### Phase 1: Current (Sample Data)
- **Scale**: 50 customers, 60 products, 100 orders
- **Technology**: Pandas on local machine
- **Runtime**: <1 minute
- **Storage**: ~100 KB Parquet

### Phase 2: Staging (Year 1)
- **Scale**: 1K customers, 500 products, 50K orders/year
- **Technology**: Pandas + cloud storage (S3)
- **Runtime**: 1-5 minutes
- **Storage**: ~50 MB Parquet

### Phase 3: Production (Year 2+)
- **Scale**: 10K+ customers, 5K+ products, 1M+ orders/year
- **Technology**: PySpark on cluster
- **Runtime**: 10-30 minutes
- **Storage**: ~500 MB - 2 GB Parquet
- **Parallelization**: Distribute ETL across nodes

**Scaling Trigger**: When ETL runtime > 30 minutes or data > 5 GB

---

## 📚 Documentation Map

| Document | Purpose | Key Audience |
|----------|---------|--------------|
| [Task 1 Pipeline Design](docs/01_TASK1_PIPELINE_DESIGN.md) | Architecture & infrastructure decisions | Solutions Architects, Data Engineers |
| [Task 2 Star Schema](docs/02_TASK2_STAR_SCHEMA.md) | Dimensional model & data dictionary | Data Modelers, Analysts |
| [Task 4 DQ Rulebook](docs/04_TASK4_DATA_QUALITY_RULEBOOK.md) | Data quality standards & validation | Data Quality Engineers, DevOps |
| [Task 5 Analytics Docs](docs/05_TASK5_ANALYTICS_DOCUMENTATION.md) | Complete operational guide | All Stakeholders |
| [ETL Code](scripts/etl_pipeline.py) | Implementation details | Data Engineers |

---

## 🚢 Deployment

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run ETL
python scripts/etl_pipeline.py

# 3. Check outputs
ls -la data/processed/gold/dimensions/
ls -la data/processed/gold/facts/
```

### Production Scheduling (Cron)
```bash
# Add to crontab (runs daily at 2 AM)
0 2 * * * /usr/bin/python3 /opt/etl/scripts/etl_pipeline.py >> /var/log/etl.log 2>&1
```

### Cloud Deployment (AWS Example)
```bash
# 1. Upload to S3
aws s3 cp data/raw/ s3://my-bucket/raw/ --recursive

# 2. Set up Lambda or EC2 scheduled task
# 3. Write outputs to S3
# 4. Connect BI tool to S3 Parquet files
```

---

## 📊 BI & Analytics Integration

### Metabase
```
Data Source: Local or S3 Parquet files
Tables: dim_customer, dim_product, dim_date, fact_sales
Pre-built Dashboards:
  - Daily Sales Trends
  - Top Products
  - Customer Segmentation
  - Order Quality Metrics
```

### Streamlit App
```python
import streamlit as st
import pandas as pd

fact_sales = pd.read_parquet('data/processed/gold/facts/fact_sales.parquet')
dim_customer = pd.read_parquet('data/processed/gold/dimensions/dim_customer.parquet')

st.title("Analytics Dashboard")
# Add visualizations...
```

---

## 🐛 Troubleshooting

### Common Issues

**Q: "ModuleNotFoundError: No module named 'pandas'"**
```bash
pip install -r requirements.txt
```

**Q: "FileNotFoundError: customers.csv not found"**
- Verify `data/raw/` folder contains all 3 CSV files

**Q: "Parquet files are empty"**
- Check logs for join failures
- Verify customer_id and product_id exist in orders.csv

**Q: "Data quality rules failing"**
- Review raw CSV data for invalid values
- Check logs for specific rule failures
- Update validation rules if needed

---

## 📞 Support & Contribution

### Getting Help
1. Check [docs/05_TASK5_ANALYTICS_DOCUMENTATION.md](docs/05_TASK5_ANALYTICS_DOCUMENTATION.md) for troubleshooting
2. Review logs in console output
3. Check data quality report for specific rule failures

### Contributing
- Fork the repository
- Create a feature branch
- Submit pull request with documentation

---

## 📄 License

This project is educational material demonstrating GenAI-driven data pipeline design.

---

## ✅ Verification Checklist

- [x] Task 1: Pipeline design document created
- [x] Task 2: Star schema design & data dictionary
- [x] Task 3: ETL code (Pandas-based, 400+ lines)
- [x] Task 4: Data quality rulebook (40+ rules)
- [x] Task 5: Comprehensive documentation
- [x] Sample data included (customers, products, orders)
- [x] Parquet output generation working
- [x] All documentation links verified
- [x] README complete with quick start guide
- [x] Code logging & error handling implemented

---

**Last Updated**: January 15, 2025
**Version**: 1.0
**Status**: ✅ Production Ready

