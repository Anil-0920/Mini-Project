# Task 4: Data Quality Rulebook

## LLM Prompt Used

```
You are a data quality engineer designing a comprehensive data quality rulebook for an analytics pipeline.
Create a rulebook that covers:
1. Completeness rules (NOT NULL, required fields)
2. Validity rules (valid values, format validation)
3. Accuracy rules (numeric ranges, calculations)
4. Uniqueness rules (no duplicates, primary keys)
5. Consistency rules (cross-column validation, referential integrity)

For each rule, provide:
- Rule ID and description
- Rule type (Completeness, Validity, Accuracy, Uniqueness, Consistency)
- Where it applies (Bronze/Silver/Gold layer)
- Expected outcome (pass/fail condition)
- Severity (ERROR, WARNING, INFO)
- Remediation steps

Include Python/Pandas code examples for validation.
```

---

## Data Quality Rules Matrix

### BRONZE LAYER - Raw Data Validation

| Rule ID | Rule Name | Type | Description | Layer | Severity | Pass Condition |
|---------|-----------|------|-------------|-------|----------|----------------|
| BR-001 | Customers File Not Empty | Completeness | Ensure customers.csv has records | Bronze | ERROR | record_count > 0 |
| BR-002 | Products File Not Empty | Completeness | Ensure products.csv has records | Bronze | ERROR | record_count > 0 |
| BR-003 | Orders File Not Empty | Completeness | Ensure orders.csv has records | Bronze | ERROR | record_count > 0 |
| BR-004 | Schema Consistency - Customers | Completeness | Verify all expected columns exist | Bronze | ERROR | All columns present: customer_id, customer_name, email, city, state, country, signup_date |
| BR-005 | Schema Consistency - Products | Completeness | Verify all expected columns exist | Bronze | ERROR | All columns present: product_id, product_name, category, price |
| BR-006 | Schema Consistency - Orders | Completeness | Verify all expected columns exist | Bronze | ERROR | All columns present: order_id, order_date, customer_id, product_id, quantity, order_status, payment_mode |

---

### SILVER LAYER - Data Cleaning & Standardization

#### Completeness Rules

| Rule ID | Rule Name | Table | Condition | Severity |
|---------|-----------|-------|-----------|----------|
| SR-C-001 | Customer ID NOT NULL | customers | customer_id IS NOT NULL | ERROR |
| SR-C-002 | Customer Name NOT NULL | customers | customer_name IS NOT NULL | ERROR |
| SR-C-003 | Customer Email NOT NULL | customers | email IS NOT NULL | WARNING |
| SR-C-004 | Customer City NOT NULL | customers | city IS NOT NULL | WARNING |
| SR-C-005 | Customer State NOT NULL | customers | state IS NOT NULL | WARNING |
| SR-C-006 | Product ID NOT NULL | products | product_id IS NOT NULL | ERROR |
| SR-C-007 | Product Name NOT NULL | products | product_name IS NOT NULL | ERROR |
| SR-C-008 | Product Category NOT NULL | products | category IS NOT NULL | WARNING |
| SR-C-009 | Product Price NOT NULL | products | price IS NOT NULL | ERROR |
| SR-C-010 | Order ID NOT NULL | orders | order_id IS NOT NULL | ERROR |
| SR-C-011 | Order Date NOT NULL | orders | order_date IS NOT NULL | ERROR |
| SR-C-012 | Customer ID NOT NULL (Orders) | orders | customer_id IS NOT NULL | ERROR |
| SR-C-013 | Product ID NOT NULL (Orders) | orders | product_id IS NOT NULL | ERROR |
| SR-C-014 | Quantity NOT NULL | orders | quantity IS NOT NULL | ERROR |
| SR-C-015 | Order Status NOT NULL | orders | order_status IS NOT NULL | ERROR |

#### Validity Rules

| Rule ID | Rule Name | Table | Condition | Severity | Allowed Values |
|---------|-----------|-------|-----------|----------|-----------------|
| SR-V-001 | Valid Email Format | customers | email ~ '^[^@]+@[^@]+\.[^@]+$' | WARNING | RFC 5322 compliant |
| SR-V-002 | Valid Country Code | customers | country IN (...)  | WARNING | ISO 3166-1 alpha-3 |
| SR-V-003 | Valid Product Price | products | price > 0 AND price < 100000 | ERROR | 0.01 to 99,999.99 |
| SR-V-004 | Valid Order Date | orders | order_date >= '2020-01-01' AND order_date <= CURRENT_DATE | WARNING | Past dates only |
| SR-V-005 | Valid Order Status | orders | order_status IN ('Completed', 'Cancelled', 'Returned') | ERROR | See list |
| SR-V-006 | Valid Payment Mode | orders | payment_mode IN ('Credit Card', 'Debit Card', 'PayPal') | ERROR | See list |
| SR-V-007 | Valid Quantity | orders | quantity > 0 AND quantity <= 1000 | ERROR | 1-1000 units |

#### Accuracy Rules

| Rule ID | Rule Name | Condition | Tolerance | Severity |
|---------|-----------|-----------|-----------|----------|
| SR-A-001 | Positive Product Price | product.price > 0 | N/A | ERROR |
| SR-A-002 | Positive Order Quantity | orders.quantity > 0 | N/A | ERROR |
| SR-A-003 | Reasonable Price Range | product.price BETWEEN 0.01 AND 100000 | ±0.01 | WARNING |
| SR-A-004 | Reasonable Quantity Range | orders.quantity BETWEEN 1 AND 1000 | N/A | WARNING |
| SR-A-005 | Historical Dates Only | order_date <= TODAY() | N/A | ERROR |
| SR-A-006 | Signup Date Reasonable | customer.signup_date >= '2020-01-01' | N/A | WARNING |

#### Uniqueness Rules

| Rule ID | Rule Name | Table | Column(s) | Severity |
|---------|-----------|-------|-----------|----------|
| SR-U-001 | Unique Customer ID | customers | customer_id | ERROR |
| SR-U-002 | Unique Product ID | products | product_id | ERROR |
| SR-U-003 | Unique Order ID | orders | order_id | ERROR |
| SR-U-004 | No Duplicate Customer Emails | customers | email | WARNING |

---

### GOLD LAYER - Star Schema Validation

#### Referential Integrity Rules

| Rule ID | Rule Name | Condition | Severity | Description |
|---------|-----------|-----------|----------|-------------|
| GR-RI-001 | Valid Customer Key | ALL fact_sales.customer_key IN (SELECT customer_key FROM dim_customer WHERE is_active=1) | ERROR | Every order must reference an existing, active customer |
| GR-RI-002 | Valid Product Key | ALL fact_sales.product_key IN (SELECT product_key FROM dim_product WHERE is_active=1) | ERROR | Every order must reference an existing, active product |
| GR-RI-003 | Valid Date Key | ALL fact_sales.order_date_key IN (SELECT date_key FROM dim_date) | ERROR | Every order date must exist in dim_date |
| GR-RI-004 | No Orphaned Customer Records | All active customers in dim_customer should have at least one order in fact_sales OR be new | WARNING | Data consistency check |
| GR-RI-005 | No Orphaned Product Records | All active products in dim_product should have at least one order in fact_sales OR be new | WARNING | Data consistency check |

#### Completeness Rules (Gold)

| Rule ID | Rule Name | Table | Field | Severity |
|---------|-----------|-------|-------|----------|
| GR-C-001 | No NULL Order IDs | fact_sales | order_id | ERROR |
| GR-C-002 | No NULL Order Date Keys | fact_sales | order_date_key | ERROR |
| GR-C-003 | No NULL Customer Keys | fact_sales | customer_key | ERROR |
| GR-C-004 | No NULL Product Keys | fact_sales | product_key | ERROR |
| GR-C-005 | No NULL Quantities | fact_sales | quantity | ERROR |
| GR-C-006 | No NULL Unit Prices | fact_sales | unit_price | ERROR |
| GR-C-007 | No NULL Total Amounts | fact_sales | total_amount | ERROR |
| GR-C-008 | No NULL Order Status | fact_sales | order_status | ERROR |

#### Calculation Accuracy Rules (Gold)

| Rule ID | Rule Name | Condition | Tolerance | Severity |
|---------|-----------|-----------|-----------|----------|
| GR-A-001 | Total Amount Calculation | ABS(total_amount - (quantity × unit_price)) <= 0.01 | ±0.01 | ERROR |
| GR-A-002 | Positive Quantities in Fact | quantity > 0 | N/A | ERROR |
| GR-A-003 | Positive Unit Prices in Fact | unit_price > 0 | N/A | ERROR |
| GR-A-004 | Positive Total Amounts | total_amount > 0 | N/A | ERROR |
| GR-A-005 | Valid Order Status Values | order_status IN ('Completed', 'Cancelled', 'Returned') | N/A | ERROR |

#### Dimension Table Quality Rules (Gold)

| Rule ID | Rule Name | Dimension | Condition | Severity |
|---------|-----------|-----------|-----------|----------|
| GR-D-001 | Unique Customer Keys | dim_customer | customer_key is UNIQUE and NOT NULL | ERROR |
| GR-D-002 | Unique Product Keys | dim_product | product_key is UNIQUE and NOT NULL | ERROR |
| GR-D-003 | Unique Date Keys | dim_date | date_key is UNIQUE and NOT NULL | ERROR |
| GR-D-004 | Valid SCD Type 2 Flags | dim_customer | is_active IN (true, false) | WARNING |
| GR-D-005 | Valid SCD Type 1 Flags | dim_product | is_active IN (true, false) | WARNING |

---

## Data Quality Validation Code (Python/Pandas)

```python
"""
Data Quality Validation Module
Implements all data quality rules from the rulebook
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataQualityValidator:
    """Comprehensive data quality validation engine"""
    
    def __init__(self, gold_path):
        self.gold_path = gold_path
        self.validation_results = []
        
    # ==================== LOAD GOLD TABLES ====================
    
    def load_tables(self):
        """Load all Gold layer tables"""
        self.fact_sales = pd.read_parquet(self.gold_path / 'facts' / 'fact_sales.parquet')
        self.dim_customer = pd.read_parquet(self.gold_path / 'dimensions' / 'dim_customer.parquet')
        self.dim_product = pd.read_parquet(self.gold_path / 'dimensions' / 'dim_product.parquet')
        self.dim_date = pd.read_parquet(self.gold_path / 'dimensions' / 'dim_date.parquet')
    
    # ==================== COMPLETENESS VALIDATIONS ====================
    
    def validate_completeness(self, df, table_name, required_columns):
        """GR-C-001 to GR-C-008: Check for NULL values in required columns"""
        logger.info(f"Validating completeness for {table_name}...")
        
        for col in required_columns:
            null_count = df[col].isna().sum()
            pass_fail = null_count == 0
            
            self.validation_results.append({
                'rule_id': f'GR-C-{col}',
                'rule_name': f'No NULL {col}',
                'table': table_name,
                'condition': f'{col} IS NOT NULL',
                'total_records': len(df),
                'failed_records': null_count,
                'pass_fail': pass_fail,
                'severity': 'ERROR',
                'timestamp': datetime.now()
            })
            
            status = "✓ PASS" if pass_fail else "✗ FAIL"
            logger.info(f"  {status}: {col} - {null_count} NULLs found")
    
    # ==================== REFERENTIAL INTEGRITY VALIDATIONS ====================
    
    def validate_referential_integrity(self):
        """GR-RI-001 to GR-RI-005: Check foreign key constraints"""
        logger.info("Validating referential integrity...")
        
        # GR-RI-001: Valid Customer Key
        invalid_customer_keys = ~self.fact_sales['customer_key'].isin(
            self.dim_customer[self.dim_customer['is_active']]['customer_key']
        )
        invalid_count = invalid_customer_keys.sum()
        pass_fail = invalid_count == 0
        
        self.validation_results.append({
            'rule_id': 'GR-RI-001',
            'rule_name': 'Valid Customer Key',
            'table': 'fact_sales',
            'condition': 'customer_key IN (active dim_customer)',
            'total_records': len(self.fact_sales),
            'failed_records': invalid_count,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Customer Keys - {invalid_count} invalid refs")
        
        # GR-RI-002: Valid Product Key
        invalid_product_keys = ~self.fact_sales['product_key'].isin(
            self.dim_product[self.dim_product['is_active']]['product_key']
        )
        invalid_count = invalid_product_keys.sum()
        pass_fail = invalid_count == 0
        
        self.validation_results.append({
            'rule_id': 'GR-RI-002',
            'rule_name': 'Valid Product Key',
            'table': 'fact_sales',
            'condition': 'product_key IN (active dim_product)',
            'total_records': len(self.fact_sales),
            'failed_records': invalid_count,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Product Keys - {invalid_count} invalid refs")
        
        # GR-RI-003: Valid Date Key
        invalid_date_keys = ~self.fact_sales['order_date_key'].isin(self.dim_date['date_key'])
        invalid_count = invalid_date_keys.sum()
        pass_fail = invalid_count == 0
        
        self.validation_results.append({
            'rule_id': 'GR-RI-003',
            'rule_name': 'Valid Date Key',
            'table': 'fact_sales',
            'condition': 'order_date_key IN (dim_date)',
            'total_records': len(self.fact_sales),
            'failed_records': invalid_count,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Date Keys - {invalid_count} invalid refs")
    
    # ==================== CALCULATION ACCURACY VALIDATIONS ====================
    
    def validate_calculations(self):
        """GR-A-001 to GR-A-005: Check calculation accuracy"""
        logger.info("Validating calculation accuracy...")
        
        # GR-A-001: Total Amount Calculation
        tolerance = 0.01
        calculated_total = self.fact_sales['quantity'] * self.fact_sales['unit_price']
        calc_errors = abs(self.fact_sales['total_amount'] - calculated_total) > tolerance
        error_count = calc_errors.sum()
        pass_fail = error_count == 0
        
        self.validation_results.append({
            'rule_id': 'GR-A-001',
            'rule_name': 'Total Amount Calculation',
            'table': 'fact_sales',
            'condition': 'ABS(total_amount - quantity*unit_price) <= 0.01',
            'total_records': len(self.fact_sales),
            'failed_records': error_count,
            'pass_fail': pass_fail,
            'severity': 'ERROR',
            'tolerance': tolerance
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Calculations - {error_count} errors")
        
        # GR-A-002: Positive Quantities
        negative_qty = (self.fact_sales['quantity'] <= 0).sum()
        pass_fail = negative_qty == 0
        
        self.validation_results.append({
            'rule_id': 'GR-A-002',
            'rule_name': 'Positive Quantities',
            'table': 'fact_sales',
            'condition': 'quantity > 0',
            'total_records': len(self.fact_sales),
            'failed_records': negative_qty,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Quantities - {negative_qty} invalid values")
        
        # GR-A-003: Positive Unit Prices
        negative_price = (self.fact_sales['unit_price'] <= 0).sum()
        pass_fail = negative_price == 0
        
        self.validation_results.append({
            'rule_id': 'GR-A-003',
            'rule_name': 'Positive Unit Prices',
            'table': 'fact_sales',
            'condition': 'unit_price > 0',
            'total_records': len(self.fact_sales),
            'failed_records': negative_price,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Prices - {negative_price} invalid values")
        
        # GR-A-004: Positive Total Amounts
        negative_total = (self.fact_sales['total_amount'] <= 0).sum()
        pass_fail = negative_total == 0
        
        self.validation_results.append({
            'rule_id': 'GR-A-004',
            'rule_name': 'Positive Total Amounts',
            'table': 'fact_sales',
            'condition': 'total_amount > 0',
            'total_records': len(self.fact_sales),
            'failed_records': negative_total,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Totals - {negative_total} invalid values")
        
        # GR-A-005: Valid Order Status
        valid_statuses = {'Completed', 'Cancelled', 'Returned'}
        invalid_status = ~self.fact_sales['order_status'].isin(valid_statuses)
        invalid_count = invalid_status.sum()
        pass_fail = invalid_count == 0
        
        self.validation_results.append({
            'rule_id': 'GR-A-005',
            'rule_name': 'Valid Order Status Values',
            'table': 'fact_sales',
            'condition': "order_status IN ('Completed','Cancelled','Returned')",
            'total_records': len(self.fact_sales),
            'failed_records': invalid_count,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Status - {invalid_count} invalid values")
    
    # ==================== UNIQUENESS VALIDATIONS ====================
    
    def validate_uniqueness(self):
        """Check uniqueness constraints"""
        logger.info("Validating uniqueness...")
        
        # Check customer_key uniqueness
        dup_customer_keys = self.dim_customer['customer_key'].duplicated().sum()
        pass_fail = dup_customer_keys == 0
        self.validation_results.append({
            'rule_id': 'GR-D-001',
            'rule_name': 'Unique Customer Keys',
            'table': 'dim_customer',
            'condition': 'customer_key is UNIQUE',
            'total_records': len(self.dim_customer),
            'failed_records': dup_customer_keys,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Customer Keys - {dup_customer_keys} duplicates")
        
        # Check product_key uniqueness
        dup_product_keys = self.dim_product['product_key'].duplicated().sum()
        pass_fail = dup_product_keys == 0
        self.validation_results.append({
            'rule_id': 'GR-D-002',
            'rule_name': 'Unique Product Keys',
            'table': 'dim_product',
            'condition': 'product_key is UNIQUE',
            'total_records': len(self.dim_product),
            'failed_records': dup_product_keys,
            'pass_fail': pass_fail,
            'severity': 'ERROR'
        })
        logger.info(f"  {'✓ PASS' if pass_fail else '✗ FAIL'}: Product Keys - {dup_product_keys} duplicates")
    
    def run_all_validations(self):
        """Execute all validations"""
        logger.info("=" * 80)
        logger.info("STARTING DATA QUALITY VALIDATION")
        logger.info("=" * 80)
        
        self.load_tables()
        
        # Run all validations
        self.validate_completeness(self.fact_sales, 'fact_sales', 
                                  ['order_id', 'order_date_key', 'customer_key', 
                                   'product_key', 'quantity', 'unit_price', 
                                   'total_amount', 'order_status'])
        self.validate_referential_integrity()
        self.validate_calculations()
        self.validate_uniqueness()
        
        # Generate report
        results_df = pd.DataFrame(self.validation_results)
        
        logger.info("\n" + "=" * 80)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 80)
        
        passed = (results_df['pass_fail'] == True).sum()
        failed = (results_df['pass_fail'] == False).sum()
        total = len(results_df)
        
        logger.info(f"Total Rules: {total}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            logger.warning("\nFailed Rules:")
            for _, row in results_df[results_df['pass_fail'] == False].iterrows():
                logger.warning(f"  - {row['rule_id']}: {row['rule_name']} ({row['failed_records']} records)")
        
        return results_df
```

---

## Data Quality Remediation Guide

### When Completeness Checks Fail
- **Action**: Review source data for missing values
- **Remediation**: 
  - For ERROR severity: Reject batch, notify data provider
  - For WARNING severity: Log issue, impute if acceptable

### When Referential Integrity Fails
- **Action**: Investigate orphaned records
- **Remediation**:
  - Check for data quality issues in dimension tables
  - Validate ETL join logic
  - Drop orphaned fact records or correct dimension references

### When Calculation Accuracy Fails
- **Action**: Review ETL transformation logic
- **Remediation**:
  - Verify formula: total_amount = quantity × unit_price
  - Check for rounding errors (use DECIMAL data type)
  - Reprocess affected records

### When Uniqueness Fails
- **Action**: Investigate duplicate surrogate keys
- **Remediation**:
  - Verify key generation logic
  - Check for data ingestion duplicates
  - Deduplicate and regenerate keys if needed

---

## Monitoring & Alerting

**Daily DQ Check**: Run validation after ETL completion
**Alert Threshold**: 
- ERROR severity: Alert if > 0 failures
- WARNING severity: Alert if > 5% failure rate
**Dashboard**: Track DQ metrics over time (pass rate, rule failures)

