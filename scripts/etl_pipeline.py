"""
Task 3: ETL Code - Data Transformation Pipeline
Convert Bronze (Raw CSV) → Silver (Cleaned) → Gold (Star Schema)

LLM Prompt Used:
```
You are a data engineer building an ETL pipeline in Python/Pandas.
Requirements:
1. Read customers.csv, products.csv, orders.csv
2. Apply data quality checks and cleaning
3. Create a star schema with:
   - fact_sales table with surrogate keys
   - dim_customer, dim_product, dim_date dimension tables
4. Calculate total_amount = quantity × price
5. Write all tables to Parquet format in data/processed/gold/

Include:
- Error handling and logging
- Data quality validations
- Surrogate key generation
- Slowly Changing Dimension handling
- Comments and explanations
```
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed'
BRONZE_PATH = PROCESSED_DATA_PATH / 'bronze'
SILVER_PATH = PROCESSED_DATA_PATH / 'silver'
GOLD_PATH = PROCESSED_DATA_PATH / 'gold'

# Create directories if they don't exist
for path in [BRONZE_PATH, SILVER_PATH, GOLD_PATH]:
    path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured directory exists: {path}")


class ETLPipeline:
    """Main ETL Pipeline Orchestrator"""
    
    def __init__(self):
        self.customers_df = None
        self.products_df = None
        self.orders_df = None
        self.dim_customer = None
        self.dim_product = None
        self.dim_date = None
        self.fact_sales = None
        
    def run(self):
        """Execute the complete ETL pipeline"""
        try:
            logger.info("=" * 80)
            logger.info("STARTING ETL PIPELINE")
            logger.info("=" * 80)
            
            # Step 1: Bronze Layer (Raw Data Ingestion)
            self._load_raw_data()
            self._create_bronze_layer()
            
            # Step 2: Silver Layer (Data Cleaning)
            self._create_silver_layer()
            
            # Step 3: Gold Layer (Star Schema)
            self._create_dim_date()
            self._create_dim_customer()
            self._create_dim_product()
            self._create_fact_sales()
            
            # Step 4: Data Quality Validation
            self._validate_referential_integrity()
            
            # Step 5: Write to Parquet
            self._write_gold_tables()
            
            logger.info("=" * 80)
            logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"ETL Pipeline failed with error: {str(e)}", exc_info=True)
            raise
    
    # ==================== BRONZE LAYER ====================
    
    def _load_raw_data(self):
        """Load raw CSV files from source"""
        logger.info("STEP 1: Loading raw data from CSV files")
        
        try:
            self.customers_df = pd.read_csv(RAW_DATA_PATH / 'customers.csv')
            logger.info(f"  ✓ Loaded customers.csv: {len(self.customers_df)} rows, {len(self.customers_df.columns)} columns")
            
            self.products_df = pd.read_csv(RAW_DATA_PATH / 'products.csv')
            logger.info(f"  ✓ Loaded products.csv: {len(self.products_df)} rows, {len(self.products_df.columns)} columns")
            
            self.orders_df = pd.read_csv(RAW_DATA_PATH / 'orders.csv')
            logger.info(f"  ✓ Loaded orders.csv: {len(self.orders_df)} rows, {len(self.orders_df.columns)} columns")
            
        except FileNotFoundError as e:
            logger.error(f"CSV file not found: {e}")
            raise
    
    def _create_bronze_layer(self):
        """Create Bronze layer (raw data copy with metadata)"""
        logger.info("STEP 1B: Creating Bronze Layer tables")
        
        # Add ingestion metadata
        ingestion_time = datetime.now()
        
        bronze_customers = self.customers_df.copy()
        bronze_customers['_ingestion_timestamp'] = ingestion_time
        bronze_customers['_source'] = 'customers.csv'
        
        bronze_products = self.products_df.copy()
        bronze_products['_ingestion_timestamp'] = ingestion_time
        bronze_products['_source'] = 'products.csv'
        
        bronze_orders = self.orders_df.copy()
        bronze_orders['_ingestion_timestamp'] = ingestion_time
        bronze_orders['_source'] = 'orders.csv'
        
        # Write to Parquet
        bronze_customers.to_parquet(BRONZE_PATH / 'bronze_customers.parquet', index=False)
        logger.info(f"  ✓ Saved bronze_customers.parquet")
        
        bronze_products.to_parquet(BRONZE_PATH / 'bronze_products.parquet', index=False)
        logger.info(f"  ✓ Saved bronze_products.parquet")
        
        bronze_orders.to_parquet(BRONZE_PATH / 'bronze_orders.parquet', index=False)
        logger.info(f"  ✓ Saved bronze_orders.parquet")
    
    # ==================== SILVER LAYER ====================
    
    def _create_silver_layer(self):
        """Clean and standardize data for Silver layer"""
        logger.info("STEP 2: Creating Silver Layer (data cleaning & standardization)")
        
        # Clean customers
        silver_customers = self.customers_df.copy()
        silver_customers['signup_date'] = pd.to_datetime(silver_customers['signup_date'])
        silver_customers = silver_customers.dropna(subset=['customer_id', 'customer_name', 'email'])
        silver_customers['created_date'] = datetime.now().date()
        silver_customers['updated_date'] = datetime.now().date()
        silver_customers['is_active'] = True
        
        silver_customers.to_parquet(SILVER_PATH / 'silver_customers.parquet', index=False)
        logger.info(f"  ✓ Silver customers: {len(silver_customers)} rows (removed {len(self.customers_df) - len(silver_customers)} nulls)")
        
        # Clean products
        silver_products = self.products_df.copy()
        silver_products['price'] = pd.to_numeric(silver_products['price'], errors='coerce')
        silver_products = silver_products.dropna(subset=['product_id', 'product_name', 'price'])
        silver_products = silver_products[silver_products['price'] > 0]  # Remove invalid prices
        silver_products['created_date'] = datetime.now().date()
        silver_products['updated_date'] = datetime.now().date()
        silver_products['is_active'] = True
        
        silver_products.to_parquet(SILVER_PATH / 'silver_products.parquet', index=False)
        logger.info(f"  ✓ Silver products: {len(silver_products)} rows (removed invalid prices)")
        
        # Clean orders
        silver_orders = self.orders_df.copy()
        silver_orders['order_date'] = pd.to_datetime(silver_orders['order_date'])
        silver_orders['quantity'] = pd.to_numeric(silver_orders['quantity'], errors='coerce')
        silver_orders = silver_orders.dropna(subset=['order_id', 'customer_id', 'product_id', 'quantity', 'order_status'])
        silver_orders = silver_orders[silver_orders['quantity'] > 0]  # Remove invalid quantities
        silver_orders['created_date'] = datetime.now().date()
        
        silver_orders.to_parquet(SILVER_PATH / 'silver_orders.parquet', index=False)
        logger.info(f"  ✓ Silver orders: {len(silver_orders)} rows (removed invalid quantities)")
        
        # Update instance variables
        self.customers_df = silver_customers
        self.products_df = silver_products
        self.orders_df = silver_orders
    
    # ==================== GOLD LAYER - DIMENSIONS ====================
    
    def _create_dim_date(self):
        """Create dimension table: dim_date"""
        logger.info("STEP 3A: Creating DIM_DATE dimension table")
        
        # Generate date range from 2020-01-01 to 2030-12-31
        date_range = pd.date_range(start='2020-01-01', end='2030-12-31', freq='D')
        
        dim_date = pd.DataFrame({
            'calendar_date': date_range
        })
        
        # Generate date_key (YYYYMMDD format)
        dim_date['date_key'] = dim_date['calendar_date'].dt.strftime('%Y%m%d').astype(int)
        
        # Time dimensions
        dim_date['day_of_week'] = dim_date['calendar_date'].dt.dayofweek + 1  # 1=Monday, 7=Sunday
        dim_date['day_name'] = dim_date['calendar_date'].dt.day_name
        dim_date['week_of_year'] = dim_date['calendar_date'].dt.isocalendar().week
        dim_date['month'] = dim_date['calendar_date'].dt.month
        dim_date['month_name'] = dim_date['calendar_date'].dt.month_name()
        dim_date['quarter'] = dim_date['calendar_date'].dt.quarter
        dim_date['year'] = dim_date['calendar_date'].dt.year
        
        # Flags
        dim_date['is_weekend'] = dim_date['day_of_week'].isin([6, 7])
        
        # US Holiday flags (simplified)
        us_holidays = {
            (1, 1): 'New Year',
            (7, 4): 'Independence Day',
            (11, 25): 'Thanksgiving',
            (12, 25): 'Christmas'
        }
        dim_date['is_holiday'] = dim_date['calendar_date'].apply(
            lambda x: (x.month, x.day) in us_holidays
        )
        
        dim_date['created_date'] = datetime.now().date()
        
        # Reorder columns
        dim_date = dim_date[[
            'date_key', 'calendar_date', 'day_of_week', 'day_name', 
            'week_of_year', 'month', 'month_name', 'quarter', 'year',
            'is_holiday', 'is_weekend', 'created_date'
        ]]
        
        self.dim_date = dim_date
        logger.info(f"  ✓ Created DIM_DATE: {len(dim_date)} rows (2020-2030)")
    
    def _create_dim_customer(self):
        """Create dimension table: dim_customer with surrogate keys"""
        logger.info("STEP 3B: Creating DIM_CUSTOMER dimension table")
        
        # Create surrogate key
        dim_customer = self.customers_df.copy()
        dim_customer['customer_key'] = range(1, len(dim_customer) + 1)
        
        # Derive region from state
        state_to_region = {
            'NY': 'Northeast', 'PA': 'Northeast', 'MA': 'Northeast', 'CT': 'Northeast', 'VT': 'Northeast',
            'FL': 'Southeast', 'GA': 'Southeast', 'NC': 'Southeast', 'SC': 'Southeast', 'VA': 'Southeast',
            'OH': 'Midwest', 'IL': 'Midwest', 'MI': 'Midwest', 'IN': 'Midwest', 'WI': 'Midwest',
            'TX': 'Southwest', 'AZ': 'Southwest', 'NM': 'Southwest', 'OK': 'Southwest',
            'CA': 'West', 'WA': 'West', 'OR': 'West', 'CO': 'West', 'NV': 'West',
            'MO': 'Midwest', 'KY': 'Southeast', 'TN': 'Southeast', 'MD': 'Northeast', 'DC': 'Northeast',
            'LA': 'Southwest'
        }
        dim_customer['region'] = dim_customer['state'].map(state_to_region).fillna('Unknown')
        
        # Metadata
        dim_customer['is_active'] = True
        dim_customer['updated_date'] = datetime.now().date()
        
        # Reorder columns
        dim_customer = dim_customer[[
            'customer_key', 'customer_id', 'customer_name', 'email', 'city', 'state',
            'country', 'region', 'signup_date', 'is_active', 'created_date', 'updated_date'
        ]]
        
        self.dim_customer = dim_customer
        logger.info(f"  ✓ Created DIM_CUSTOMER: {len(dim_customer)} rows with surrogate keys")
    
    def _create_dim_product(self):
        """Create dimension table: dim_product with surrogate keys"""
        logger.info("STEP 3C: Creating DIM_PRODUCT dimension table")
        
        # Create surrogate key
        dim_product = self.products_df.copy()
        dim_product['product_key'] = range(1, len(dim_product) + 1)
        
        # Metadata
        dim_product['is_active'] = True
        dim_product['updated_date'] = datetime.now().date()
        
        # Reorder columns
        dim_product = dim_product[[
            'product_key', 'product_id', 'product_name', 'category', 'price',
            'is_active', 'created_date', 'updated_date'
        ]]
        
        self.dim_product = dim_product
        logger.info(f"  ✓ Created DIM_PRODUCT: {len(dim_product)} rows with surrogate keys")
    
    # ==================== GOLD LAYER - FACT TABLE ====================
    
    def _create_fact_sales(self):
        """Create fact table: fact_sales with all foreign keys and calculations"""
        logger.info("STEP 3D: Creating FACT_SALES fact table")
        
        # Start with orders
        fact_sales = self.orders_df.copy()
        
        # Convert order_date to date_key (YYYYMMDD)
        fact_sales['order_date_key'] = fact_sales['order_date'].dt.strftime('%Y%m%d').astype(int)
        
        # Join with customer dimension to get customer_key
        customer_mapping = self.dim_customer[['customer_id', 'customer_key']].drop_duplicates()
        fact_sales = fact_sales.merge(
            customer_mapping,
            on='customer_id',
            how='left'
        )
        
        # Join with product dimension to get product_key and unit_price
        product_mapping = self.dim_product[['product_id', 'product_key', 'price']].copy()
        product_mapping.rename(columns={'price': 'unit_price'}, inplace=True)
        fact_sales = fact_sales.merge(
            product_mapping,
            on='product_id',
            how='left'
        )
        
        # Calculate total_amount
        fact_sales['total_amount'] = fact_sales['quantity'] * fact_sales['unit_price']
        
        # Add created_date metadata
        fact_sales['created_date'] = datetime.now().date()
        
        # Select and reorder final columns
        fact_sales = fact_sales[[
            'order_id', 'order_date_key', 'customer_key', 'product_key',
            'quantity', 'unit_price', 'total_amount', 'order_status', 'payment_mode',
            'created_date'
        ]]
        
        # Data quality checks
        null_customer_keys = fact_sales['customer_key'].isna().sum()
        null_product_keys = fact_sales['product_key'].isna().sum()
        
        if null_customer_keys > 0:
            logger.warning(f"  ⚠ {null_customer_keys} orders have no matching customer")
            fact_sales = fact_sales.dropna(subset=['customer_key'])
        
        if null_product_keys > 0:
            logger.warning(f"  ⚠ {null_product_keys} orders have no matching product")
            fact_sales = fact_sales.dropna(subset=['product_key'])
        
        self.fact_sales = fact_sales
        logger.info(f"  ✓ Created FACT_SALES: {len(fact_sales)} rows")
        logger.info(f"    - Total Revenue (Completed): ${fact_sales[fact_sales['order_status'] == 'Completed']['total_amount'].sum():,.2f}")
        logger.info(f"    - Cancelled Orders: {(fact_sales['order_status'] == 'Cancelled').sum()}")
        logger.info(f"    - Returned Orders: {(fact_sales['order_status'] == 'Returned').sum()}")
    
    # ==================== DATA QUALITY VALIDATION ====================
    
    def _validate_referential_integrity(self):
        """Validate referential integrity constraints"""
        logger.info("STEP 4: Validating Referential Integrity")
        
        # Check foreign keys
        invalid_customers = self.fact_sales[~self.fact_sales['customer_key'].isin(self.dim_customer['customer_key'])]
        invalid_products = self.fact_sales[~self.fact_sales['product_key'].isin(self.dim_product['product_key'])]
        invalid_dates = self.fact_sales[~self.fact_sales['order_date_key'].isin(self.dim_date['date_key'])]
        
        if len(invalid_customers) > 0:
            logger.warning(f"  ⚠ Found {len(invalid_customers)} fact records with invalid customer_key")
        else:
            logger.info(f"  ✓ All fact sales have valid customer_key references")
        
        if len(invalid_products) > 0:
            logger.warning(f"  ⚠ Found {len(invalid_products)} fact records with invalid product_key")
        else:
            logger.info(f"  ✓ All fact sales have valid product_key references")
        
        if len(invalid_dates) > 0:
            logger.warning(f"  ⚠ Found {len(invalid_dates)} fact records with invalid order_date_key")
        else:
            logger.info(f"  ✓ All fact sales have valid order_date_key references")
        
        # Check calculation accuracy
        tolerance = 0.01
        calc_errors = (abs(self.fact_sales['total_amount'] - (self.fact_sales['quantity'] * self.fact_sales['unit_price'])) > tolerance).sum()
        if calc_errors > 0:
            logger.warning(f"  ⚠ Found {calc_errors} records with calculation errors")
        else:
            logger.info(f"  ✓ All total_amount calculations are correct")
    
    # ==================== WRITE TO PARQUET ====================
    
    def _write_gold_tables(self):
        """Write Gold layer tables to Parquet"""
        logger.info("STEP 5: Writing Gold Layer tables to Parquet")
        
        # Create gold subdirectories
        gold_dims_path = GOLD_PATH / 'dimensions'
        gold_facts_path = GOLD_PATH / 'facts'
        gold_dims_path.mkdir(parents=True, exist_ok=True)
        gold_facts_path.mkdir(parents=True, exist_ok=True)
        
        # Write dimension tables
        self.dim_customer.to_parquet(gold_dims_path / 'dim_customer.parquet', index=False)
        logger.info(f"  ✓ Saved dim_customer.parquet ({len(self.dim_customer)} rows)")
        
        self.dim_product.to_parquet(gold_dims_path / 'dim_product.parquet', index=False)
        logger.info(f"  ✓ Saved dim_product.parquet ({len(self.dim_product)} rows)")
        
        self.dim_date.to_parquet(gold_dims_path / 'dim_date.parquet', index=False)
        logger.info(f"  ✓ Saved dim_date.parquet ({len(self.dim_date)} rows)")
        
        # Write fact table partitioned by order_date_key
        # Note: Pandas doesn't partition by default, but we organize the output
        self.fact_sales.to_parquet(gold_facts_path / 'fact_sales.parquet', index=False)
        logger.info(f"  ✓ Saved fact_sales.parquet ({len(self.fact_sales)} rows)")
        
        logger.info(f"\n✅ All Parquet files written to: {GOLD_PATH}")


if __name__ == '__main__':
    """Execute ETL Pipeline"""
    pipeline = ETLPipeline()
    pipeline.run()

