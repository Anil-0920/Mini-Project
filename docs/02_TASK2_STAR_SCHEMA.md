# Task 2: Star Schema Design

## LLM Prompt Used

```
You are a data modeler designing a star schema for online retail analytics.
Given three source tables:
- customers (customer_id, customer_name, email, city, state, country, signup_date)
- products (product_id, product_name, category, price)
- orders (order_id, order_date, customer_id, product_id, quantity, order_status, payment_mode)

Business questions to support:
1. Daily and monthly sales trends
2. Top products and categories by revenue
3. Top customers by spend
4. Order status impact on revenue
5. Average order value (AOV) by region

Design a star schema with:
1. One fact table (fact_sales)
2. Dimension tables (dim_customer, dim_product, dim_date, dim_order_status)
3. Surrogate keys strategy
4. Column descriptions
5. Slowly Changing Dimension (SCD) strategy for dimensions
```

## Star Schema Diagram

```
                    ┌─────────────────────────┐
                    │     DIM_CUSTOMER        │
                    ├─────────────────────────┤
                    │ customer_key (PK)       │
                    │ customer_id (BK)        │
                    │ customer_name           │
                    │ email                   │
                    │ city                    │
                    │ state                   │
                    │ country                 │
                    │ region                  │
                    │ signup_date             │
                    │ is_active               │
                    │ created_date            │
                    │ updated_date            │
                    └────────────┬────────────┘
                                 │
                                 │ FK: customer_key
                                 │
                    ┌────────────▼────────────┐
                    │    FACT_SALES (FK)      │
                    ├─────────────────────────┤
                    │ order_id (PK)           │
                    │ order_date_key (FK)     │
                    │ customer_key (FK)       │
                    │ product_key (FK)        │
                    │ quantity                │
                    │ unit_price              │
                    │ total_amount            │
                    │ order_status            │
                    │ payment_mode            │
                    │ created_date            │
                    └────────────┬─┬──────────┘
                                 │ │
                 ┌───────────────┘ │
                 │                 │
    ┌────────────▼──────────┐  ┌──▼──────────────────┐
    │   DIM_PRODUCT         │  │    DIM_DATE         │
    ├───────────────────────┤  ├─────────────────────┤
    │ product_key (PK)      │  │ date_key (PK)       │
    │ product_id (BK)       │  │ calendar_date       │
    │ product_name          │  │ day_of_week         │
    │ category              │  │ week_of_year        │
    │ price                 │  │ month               │
    │ is_active             │  │ quarter             │
    │ created_date          │  │ year                │
    │ updated_date          │  │ is_holiday          │
    └───────────────────────┘  │ is_weekend          │
                                └─────────────────────┘
```

---

## Data Dictionary

### FACT_SALES (Fact Table)

**Purpose**: Central transaction table containing all order events

| Column | Data Type | Description | Example | Grain |
|--------|-----------|-------------|---------|-------|
| order_id | STRING | Primary key, unique order identifier (immutable) | O001 | Order Level |
| order_date_key | INT | Foreign key to DIM_DATE (YYYYMMDD format) | 20230115 | Order Level |
| customer_key | INT | Foreign key to DIM_CUSTOMER (surrogate key) | 1 | Order Level |
| product_key | INT | Foreign key to DIM_PRODUCT (surrogate key) | 1 | Order Level |
| quantity | INT | Units purchased in the order | 2 | Order Level |
| unit_price | DECIMAL(10,2) | Price of product at time of purchase | 79.99 | Order Level |
| total_amount | DECIMAL(10,2) | Calculated: quantity × unit_price | 159.98 | Order Level |
| order_status | STRING | Status of order: Completed, Cancelled, Returned | Completed | Order Level |
| payment_mode | STRING | Payment method: Credit Card, Debit Card, PayPal | Credit Card | Order Level |
| created_date | DATE | Data warehouse creation timestamp | 2025-01-15 | Metadata |

**Fact Table Characteristics**:
- **Grain**: One row per order
- **Row Count**: ~100 rows (100 orders in sample data)
- **Update Frequency**: Append-only (no updates after creation)
- **Key Metrics**:
  - Revenue = SUM(total_amount) where order_status = 'Completed'
  - Order Count = COUNT(DISTINCT order_id)
  - Average Order Value (AOV) = Revenue / Order Count

---

### DIM_CUSTOMER (Dimension Table)

**Purpose**: Customer profile and demographic information, slowly changing dimension (SCD Type 2)

| Column | Data Type | Description | Example | Notes |
|--------|-----------|-------------|---------|-------|
| customer_key | INT | Surrogate key (auto-increment) | 1 | Primary Key |
| customer_id | STRING | Business key from source system | C001 | Immutable |
| customer_name | VARCHAR(100) | Full name of customer | John Smith | |
| email | VARCHAR(100) | Customer email address | john.smith@email.com | |
| city | VARCHAR(50) | City of residence | New York | |
| state | VARCHAR(50) | State/Province | NY | |
| country | VARCHAR(50) | Country | USA | |
| region | VARCHAR(50) | Derived region from state | Northeast | Computed field |
| signup_date | DATE | Customer account creation date | 2022-01-15 | |
| is_active | BOOLEAN | Customer status (active/inactive) | true | SCD Type 2 flag |
| created_date | DATE | DW creation timestamp | 2023-01-15 | Metadata |
| updated_date | DATE | DW last update timestamp | 2025-01-15 | Metadata |

**SCD Type 2 Strategy**: Keep historical changes
- When customer address changes, insert new row with new customer_key
- Mark old row: is_active = false, updated_date = today
- Maintains historical accuracy for trend analysis

**Region Mapping**:
- Northeast: NY, PA, MA, CT, etc.
- Southeast: FL, GA, NC, SC, etc.
- Midwest: OH, IL, MI, IN, WI, etc.
- Southwest: TX, AZ, NM, OK, etc.
- West: CA, WA, OR, CO, etc.

---

### DIM_PRODUCT (Dimension Table)

**Purpose**: Product catalog and attributes, slowly changing dimension (SCD Type 1)

| Column | Data Type | Description | Example | Notes |
|--------|-----------|-------------|---------|-------|
| product_key | INT | Surrogate key (auto-increment) | 1 | Primary Key |
| product_id | STRING | Business key from source system | P001 | Immutable |
| product_name | VARCHAR(100) | Product name | Wireless Headphones | |
| category | VARCHAR(50) | Product category | Electronics | |
| price | DECIMAL(10,2) | Current product price | 79.99 | Updated |
| is_active | BOOLEAN | Product availability (active/inactive) | true | |
| created_date | DATE | DW creation timestamp | 2023-01-15 | Metadata |
| updated_date | DATE | DW last update timestamp | 2025-01-15 | Metadata |

**SCD Type 1 Strategy**: Overwrite historical values
- When product price changes, overwrite old price
- Simpler than SCD Type 2, but loses historical price data
- Acceptable for product attributes like category, name
- For historical pricing, use SCD Type 2 (product_price_history table)

**Category Distribution**:
- Electronics: 10 products
- Clothing: 10 products
- Sports: 10 products
- Beauty: 10 products
- Books: 10 products
- Home: 10 products

---

### DIM_DATE (Dimension Table)

**Purpose**: Time dimension for temporal analysis and reporting

| Column | Data Type | Description | Example | Notes |
|--------|-----------|-------------|---------|-------|
| date_key | INT | Surrogate key (YYYYMMDD format) | 20230115 | Primary Key |
| calendar_date | DATE | Actual calendar date | 2023-01-15 | Unique |
| day_of_week | INT | Day number (1=Monday, 7=Sunday) | 7 | |
| day_name | VARCHAR(10) | Day name | Sunday | |
| week_of_year | INT | ISO week number (1-53) | 2 | |
| month | INT | Month number (1-12) | 1 | |
| month_name | VARCHAR(10) | Month name | January | |
| quarter | INT | Quarter (1-4) | 1 | |
| year | INT | Year | 2023 | |
| is_holiday | BOOLEAN | Holiday flag (US holidays) | false | |
| is_weekend | BOOLEAN | Weekend flag (Saturday/Sunday) | true | |
| created_date | DATE | DW creation timestamp | 2023-01-01 | Metadata |

**Pre-populated**: All dates from 2020-01-01 to 2030-12-31 (11 years)
**US Holidays Included**: New Year, MLK Day, Presidents Day, Memorial Day, July 4th, Labor Day, Columbus Day, Veterans Day, Thanksgiving, Christmas

---

## Surrogate Key Strategy

### Why Surrogate Keys?

| Aspect | Business Key | Surrogate Key |
|--------|--------------|---------------|
| **Stability** | Can change (customer ID reuse) | Immutable, never changes |
| **Storage** | VARCHAR(50) = 50 bytes | INT = 4 bytes (92% savings) |
| **Join Performance** | String comparison slow | Integer comparison fast |
| **Dimensionality** | Exposed in analytics | Hidden, technical |
| **Flexibility** | Hard to manage SCD | Easy to implement SCD Type 2 |

### Implementation

**Customer Key Generation**:
```
customer_key = ROW_NUMBER() OVER (ORDER BY customer_id)
Example: C001 → 1, C002 → 2, C050 → 50
```

**Product Key Generation**:
```
product_key = ROW_NUMBER() OVER (ORDER BY product_id)
Example: P001 → 1, P002 → 2, P060 → 60
```

**Date Key Generation**:
```
date_key = CAST(DATE_FORMAT(calendar_date, 'YYYYMMDD') AS INT)
Example: 2023-01-15 → 20230115
```

---

## Data Quality Rules (Star Schema Level)

| Rule | Type | Description | Example |
|------|------|-------------|---------|
| **Referential Integrity** | Validity | All customer_key in fact_sales must exist in dim_customer | fact_sales.customer_key IN (SELECT customer_key FROM dim_customer) |
| **Referential Integrity** | Validity | All product_key in fact_sales must exist in dim_product | fact_sales.product_key IN (SELECT product_key FROM dim_product) |
| **Referential Integrity** | Validity | All order_date_key in fact_sales must exist in dim_date | fact_sales.order_date_key IN (SELECT date_key FROM dim_date) |
| **Completeness** | Completeness | No NULL values in fact_sales key fields | order_id, customer_key, product_key NOT NULL |
| **Calculation Accuracy** | Accuracy | total_amount = quantity × unit_price | Validate with tolerance ±0.01 |
| **Status Validity** | Validity | order_status only IN ('Completed', 'Cancelled', 'Returned') | |
| **Quantity Range** | Accuracy | quantity > 0 and quantity < 1000 | |
| **Price Validity** | Accuracy | unit_price > 0 and unit_price < 10000 | |

---

## ETL Mapping: Source → Target

```
CUSTOMERS.CSV
├─ customer_id       → DIM_CUSTOMER.customer_id (BK)
├─ customer_name     → DIM_CUSTOMER.customer_name
├─ email             → DIM_CUSTOMER.email
├─ city              → DIM_CUSTOMER.city
├─ state             → DIM_CUSTOMER.state
├─ country           → DIM_CUSTOMER.country
├─ signup_date       → DIM_CUSTOMER.signup_date
├─ (GENERATED)       → DIM_CUSTOMER.customer_key (SK)
├─ (GENERATED)       → DIM_CUSTOMER.region (Derived from state)
├─ (GENERATED)       → DIM_CUSTOMER.is_active (TRUE)
├─ (GENERATED)       → DIM_CUSTOMER.created_date (TODAY)
└─ (GENERATED)       → DIM_CUSTOMER.updated_date (TODAY)

PRODUCTS.CSV
├─ product_id        → DIM_PRODUCT.product_id (BK)
├─ product_name      → DIM_PRODUCT.product_name
├─ category          → DIM_PRODUCT.category
├─ price             → DIM_PRODUCT.price
├─ (GENERATED)       → DIM_PRODUCT.product_key (SK)
├─ (GENERATED)       → DIM_PRODUCT.is_active (TRUE)
├─ (GENERATED)       → DIM_PRODUCT.created_date (TODAY)
└─ (GENERATED)       → DIM_PRODUCT.updated_date (TODAY)

ORDERS.CSV + CUSTOMERS.CSV + PRODUCTS.CSV
├─ order_id          → FACT_SALES.order_id (PK)
├─ order_date        → FACT_SALES.order_date_key (CONVERT TO INT YYYYMMDD)
├─ customer_id       → FACT_SALES.customer_key (JOIN → DIM_CUSTOMER)
├─ product_id        → FACT_SALES.product_key (JOIN → DIM_PRODUCT)
├─ quantity          → FACT_SALES.quantity
├─ price             → FACT_SALES.unit_price
├─ quantity*price    → FACT_SALES.total_amount (CALCULATED)
├─ order_status      → FACT_SALES.order_status
├─ payment_mode      → FACT_SALES.payment_mode
└─ (GENERATED)       → FACT_SALES.created_date (TODAY)

DIM_DATE
└─ Generate all dates from 2020-01-01 to 2030-12-31
   ├─ date_key (YYYYMMDD)
   ├─ calendar_date
   ├─ day_of_week, month, quarter, year
   └─ is_holiday, is_weekend flags
```

---

## Schema Change Log

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| 1.0 | 2025-01-15 | Initial schema design | Project kickoff |

---

