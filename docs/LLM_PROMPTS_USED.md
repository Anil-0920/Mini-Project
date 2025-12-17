# LLM Prompts Used in This Project

This document archives all prompts used to generate the five tasks in the GenAI-Driven Analytics Pipeline project.

---

## Task 1: Prompt → Pipeline Design

### Prompt Sent to LLM

```
You are a data architect designing an analytics pipeline for an online retail company.

Business Context:
- An online retail company wants to analyze sales performance and customer behavior
- They need to answer questions about:
  * Daily and monthly sales trends
  * Top products and categories by revenue
  * Top customers by spend
  * Order status (Completed, Cancelled, Returned) impact on revenue
  * Average order value (AOV) by region
- Data sources: customers.csv, products.csv, orders.csv
- Current data: 50 customers, 60 products, 100 orders

Design a medallion architecture analytics pipeline with the following considerations:

1. Define Bronze, Silver, and Gold layers with clear purposes
2. Justify batch processing vs near-real-time, including:
   - Data characteristics that favor batch
   - Business requirements that accept latency
   - Operational benefits
3. Recommend storage format and justify why (e.g., Parquet over CSV)
4. Suggest partitioning strategy and explain rationale
5. Design complete data flow from raw CSV → Bronze → Silver → Gold → BI tools
6. Include data quality checkpoints at each layer
7. Specify technology stack recommendations

Expected Output Format:
- Architecture diagram (ASCII or text-based)
- Detailed justification for each design decision
- Table comparing alternatives (CSV vs Parquet, Batch vs Real-time)
- Partition scheme with directory structure
- Data quality rules by layer
```

### LLM Response Summary

The LLM generated:
- ✓ Medallion architecture diagram (Bronze/Silver/Gold)
- ✓ Batch vs real-time comparison with business justification
- ✓ Parquet format analysis (70-80% compression, query performance)
- ✓ Date-based partitioning strategy with rationale
- ✓ Technology stack recommendations (Pandas, PySpark)
- ✓ Data quality checkpoints at each layer

**Output Document**: [docs/01_TASK1_PIPELINE_DESIGN.md](docs/01_TASK1_PIPELINE_DESIGN.md)

---

## Task 2: Auto-Generated Star Schema

### Prompt Sent to LLM

```
You are a data modeler designing a star schema for online retail analytics.

Given three source tables with the following columns:
- customers: customer_id, customer_name, email, city, state, country, signup_date
- products: product_id, product_name, category, price
- orders: order_id, order_date, customer_id, product_id, quantity, order_status, payment_mode

Business questions to support:
1. Daily and monthly sales trends
2. Top products and categories by revenue
3. Top customers by spend
4. Order status impact on revenue
5. Average order value (AOV) by region

Design a star schema with the following requirements:

1. Create ONE fact table
   - Grain: one row per transaction
   - Measures: quantity, total_amount
   - Attributes: order_status, payment_mode
   
2. Create dimension tables:
   - dim_customer: demographic info, region
   - dim_product: product info, category
   - dim_date: complete date dimension (11 years)
   - Any other dimensions needed

3. Surrogate key strategy:
   - How to generate surrogate keys?
   - Benefits over business keys?
   - Which tables get SK?

4. Slowly Changing Dimension (SCD) strategy:
   - Which dimensions change over time?
   - SCD Type 1 vs Type 2?
   - Why that choice?

5. Deliverables:
   - Text-based star schema diagram showing relationships
   - Complete data dictionary with:
     * Column names, data types, descriptions
     * Nullable/Not Null constraints
     * Key designations (PK, FK, SK, BK)
   - Source-to-target mapping (how source columns map to targets)
   - Data quality rules for star schema
   - Column-level transformations and calculations

Format the data dictionary as a markdown table with:
| Column | Data Type | Description | Example | Notes |

Include detailed explanations for:
- Why this grain?
- Why these dimensions?
- How surrogate keys enable SCD?
- Join paths for common queries
```

### LLM Response Summary

The LLM generated:
- ✓ Star schema ASCII diagram with relationships
- ✓ Fact table (fact_sales) with complete definition
- ✓ Three dimension tables with SCD strategy
- ✓ Detailed data dictionary (40+ columns documented)
- ✓ Surrogate key generation strategy with rationale
- ✓ SCD Type 1 vs Type 2 comparison
- ✓ Complete source-to-target mapping
- ✓ Data quality rules for referential integrity

**Output Document**: [docs/02_TASK2_STAR_SCHEMA.md](docs/02_TASK2_STAR_SCHEMA.md)

---

## Task 3: ETL Logic via Prompts (Pandas Code)

### Prompt Sent to LLM

```
You are a data engineer implementing an ETL pipeline in Python/Pandas.

Requirements:
1. Read three CSV files: customers.csv, products.csv, orders.csv
2. Implement the Bronze layer:
   - Copy CSVs as-is
   - Add ingestion metadata (timestamp, source file)
   - Write to Parquet format

3. Implement the Silver layer:
   - Data quality cleaning:
     * Handle NULL values in required fields
     * Validate data types
     * Remove invalid records (e.g., negative prices)
     * Standardize column names
   - Add technical columns (created_date, updated_date, is_active)
   - Write to Parquet format

4. Implement the Gold layer:
   - Create dim_customer:
     * Generate surrogate keys (ROW_NUMBER)
     * Derive region from state
     * Add is_active flag
   
   - Create dim_product:
     * Generate surrogate keys
     * Keep current product info
   
   - Create dim_date:
     * Generate all dates from 2020-01-01 to 2030-12-31
     * Calculate date_key (YYYYMMDD format)
     * Compute day_of_week, month, quarter, year
     * Flag holidays and weekends
   
   - Create fact_sales:
     * Start with orders
     * Convert order_date to order_date_key
     * Join with dim_customer to get customer_key
     * Join with dim_product to get product_key
     * Calculate total_amount = quantity × price
     * Select final columns
     * Remove rows with NULL foreign keys
     
5. Implement data quality checks:
   - Validate referential integrity (all FKs exist)
   - Check calculation accuracy (±0.01 tolerance)
   - Verify positive values for quantity, price, total_amount
   - Confirm all foreign keys have valid references

6. Code quality requirements:
   - Class-based design with clear methods
   - Comprehensive logging at each step
   - Error handling with meaningful messages
   - Comments explaining complex logic
   - Docstrings for methods
   - Progress indicators (✓ symbols in logs)

7. Output format:
   - Write all tables to Parquet format
   - Organize in directory structure:
     * data/processed/bronze/
     * data/processed/silver/
     * data/processed/gold/dimensions/
     * data/processed/gold/facts/
   
8. Logging output:
   - Row counts at each stage
   - Data quality issue counts
   - File sizes
   - Execution time
   - Success/failure status

Include:
- Complete, runnable code (400+ lines)
- Class definition with methods for each layer
- Error handling and logging
- Comments explaining the logic
- Example usage in __main__ block
```

### LLM Response Summary

The LLM generated:
- ✓ Production-grade ETL code (420+ lines)
- ✓ Class-based design (ETLPipeline class)
- ✓ Bronze layer with metadata
- ✓ Silver layer with data cleaning
- ✓ Gold layer with dimensional modeling
- ✓ Surrogate key generation
- ✓ Referential integrity validation
- ✓ Comprehensive logging with progress indicators
- ✓ Error handling and documentation

**Output Document**: [scripts/etl_pipeline.py](scripts/etl_pipeline.py)

---

## Task 4: Data Quality Rulebook (LLM-Generated)

### Prompt Sent to LLM

```
You are a data quality architect designing a comprehensive DQ rulebook for an analytics pipeline.

Create a data quality rulebook that covers all layers (Bronze, Silver, Gold).

For each rule, document:
1. Rule ID (e.g., BR-001, SR-C-001, GR-RI-001)
2. Rule Name (descriptive, human-readable)
3. Rule Type (Completeness, Validity, Accuracy, Uniqueness, Consistency)
4. Table/Layer: Which table does this apply to?
5. Condition: The actual validation rule (SQL/Pandas expression)
6. Severity: ERROR, WARNING, or INFO
7. Expected outcome (pass/fail condition)
8. Remediation steps if rule fails

Rule Type Definitions:
- Completeness: NOT NULL, required fields, all records have values
- Validity: Valid values, correct format, allowed ranges
- Accuracy: Numeric correctness, calculations, expected bounds
- Uniqueness: Primary keys unique, no duplicates
- Consistency: Referential integrity, cross-column consistency, calculations match

Bronze Layer Rules (6 total):
- File existence and non-empty checks
- Schema consistency (expected columns present)
- Record count validation

Silver Layer Rules (15+ total):
- NULL checks for required fields in customers, products, orders
- Data type validation
- Value range checks (e.g., price > 0)
- Duplicate detection

Gold Layer Rules (20+ total):
- Referential integrity (all FKs reference existing records)
- Surrogate key uniqueness
- Calculation accuracy (total_amount = quantity × price)
- Value range checks (positive quantities, prices)
- Order status validity
- Dimension table completeness

Specific Rules to Include:

BRONZE:
- BR-001: Customers file not empty
- BR-002: Products file not empty
- BR-003: Orders file not empty
- BR-004-006: Schema consistency checks

SILVER:
- SR-C-001 to SR-C-015: Completeness (NOT NULL)
- SR-V-001 to SR-V-007: Validity (valid values, formats)
- SR-A-001 to SR-A-006: Accuracy (value ranges)
- SR-U-001 to SR-U-004: Uniqueness

GOLD:
- GR-RI-001 to GR-RI-005: Referential integrity
- GR-C-001 to GR-C-008: Completeness (Gold layer)
- GR-A-001 to GR-A-005: Calculation accuracy
- GR-D-001 to GR-D-005: Dimension table quality

Output Format:
1. Rule matrix table (ID, Name, Type, Condition, Severity)
2. Grouped by layer and rule type
3. Include pass/fail condition for each
4. Provide Python/Pandas code examples for validation
5. Data quality remediation guide
6. Monitoring & alerting strategy

Deliverables:
- Complete rule matrix (40+ rules)
- Sample validation code (DataQualityValidator class)
- Remediation procedures
- Monitoring checklist
```

### LLM Response Summary

The LLM generated:
- ✓ 40+ comprehensive data quality rules
- ✓ Rules organized by layer (Bronze/Silver/Gold)
- ✓ Rules categorized by type (C/V/A/U/Co)
- ✓ Complete rule matrix with all details
- ✓ Python validation code examples
- ✓ Remediation guide
- ✓ Monitoring & alerting strategy

**Output Document**: [docs/04_TASK4_DATA_QUALITY_RULEBOOK.md](docs/04_TASK4_DATA_QUALITY_RULEBOOK.md)

---

## Task 5: Auto-Generated Documentation via LLM

### Prompt Sent to LLM

```
You are a technical documentation specialist creating comprehensive documentation for a data analytics pipeline.

Create a complete technical and operational documentation package that covers:

1. BUSINESS OVERVIEW
   - Problem statement: What business problem does this solve?
   - Company context and data
   - Business questions being answered
   - Expected business impact (with metrics)
   - Stakeholder needs

2. SYSTEM ARCHITECTURE
   - Data flow diagram (ASCII art showing Bronze → Silver → Gold → BI)
   - Component descriptions
   - Technology stack table (with versions)
   - Data volumes & performance metrics (current vs. projected)

3. COMPLETE SOURCE-TO-TARGET MAPPING
   - Show how each source column maps to target tables
   - Include transformations applied
   - Show joins and lookups
   - Data lineage (CSV → Parquet)
   - Include derived fields and calculations

4. SCHEMA EXPLANATION
   - Explain star schema design rationale
   - Define each table (grain, row counts, update frequency)
   - Key metrics and how they're calculated
   - Slowly Changing Dimension strategy (Type 1 vs Type 2)
   - Provide example SQL queries for common business questions
   - Show join paths

5. ETL FLOW DOCUMENTATION
   - Step-by-step ETL process (Phase 1-5)
   - Quality checkpoints at each step
   - Error handling strategy (error types, detection, action)
   - Data transformation logic

6. DATA QUALITY CHECKS
   - DQ rules applied at each layer
   - Validation framework
   - Remediation procedures
   - Reference the comprehensive rulebook

7. ANALYTICS USE CASES
   - 5 key business questions with SQL examples:
     1. Daily/monthly sales trends
     2. Top products by revenue
     3. Top customers by spend
     4. Order status impact
     5. AOV by region
   - Example dashboard concepts
   - KPI definitions

8. ASSUMPTIONS & LIMITATIONS
   - Data volume assumptions (current & growth)
   - Latency tolerance (batch vs real-time)
   - Data quality assumptions
   - Infrastructure assumptions
   - Business context assumptions
   - Scaling triggers & recommendations
   - Known limitations and workarounds
   - Missing data that would improve analysis

9. MAINTENANCE & OPERATIONS
   - Deployment instructions (step-by-step)
   - Daily monitoring checklist
   - Weekly maintenance tasks
   - Monthly reviews
   - Troubleshooting guide (common issues & solutions)
   - Contact & support information

Output Format:
- Markdown document
- Use headers, tables, code blocks, diagrams
- Include examples and concrete scenarios
- Cross-reference other documentation
- Add table of contents
- Version control section

Style:
- Clear, precise technical language
- Assume audience has SQL/data engineering knowledge
- Include concrete examples
- Add context and rationale for decisions
- Visually organize with formatting
```

### LLM Response Summary

The LLM generated:
- ✓ Complete 9-section documentation
- ✓ Business overview with context
- ✓ System architecture diagram
- ✓ Complete source-to-target mapping
- ✓ Schema explanation with SQL examples
- ✓ Detailed ETL flow (5 phases)
- ✓ Analytics use cases (5 business questions)
- ✓ Assumptions & limitations (8 categories)
- ✓ Operational maintenance guide
- ✓ Comprehensive troubleshooting

**Output Document**: [docs/05_TASK5_ANALYTICS_DOCUMENTATION.md](docs/05_TASK5_ANALYTICS_DOCUMENTATION.md)

---

## Summary: LLM Effectiveness

### Strengths Demonstrated
✅ **Quality**: Generated production-grade ETL code with proper error handling  
✅ **Completeness**: All tasks completed with comprehensive documentation  
✅ **Consistency**: Schema design matches ETL implementation matches documentation  
✅ **Scalability**: Included growth scenarios and scaling recommendations  
✅ **Detail**: Generated 40+ data quality rules with validation code  

### Key Success Factors
1. **Clear prompts**: Specific requirements, expected outputs, format specifications
2. **Context**: Detailed business context and data samples
3. **Examples**: Provided table schemas and sample data
4. **Iterative**: Each task built on previous work (Task 1 → Task 2 → Task 3 → Task 4 → Task 5)
5. **Validation**: All generated code runs without modification

### Metrics
- **Total Documentation**: ~8,000 lines (Markdown + Code)
- **ETL Code**: 420+ lines of production code
- **Data Quality Rules**: 40+ comprehensive rules
- **Tasks Completed**: 5/5 (100%)
- **Deliverables**: 6 files + sample data
- **Time to Generate**: <30 minutes with LLM assistance

---

## Recommendations for Future Use

### For Scaling This Project
1. Add PySpark implementation when data > 1M rows/year
2. Implement Slowly Changing Dimension Type 2 properly with effective dating
3. Add change data capture (CDC) for incremental loads
4. Implement data lineage tracking (OpenLineage format)
5. Add Great Expectations for automated data quality validation

### For Extending With GenAI
1. Use LLM to generate dashboard SQL automatically from business questions
2. Auto-generate data dictionary from source CSVs
3. Suggest anomalies in data quality metrics
4. Generate ETL code from YAML schema definitions
5. Create real-time alerting for DQ rule violations

### Prompt Engineering Best Practices Observed
- ✅ Break complex requests into clear sections
- ✅ Provide specific examples and formats
- ✅ State expected output structure explicitly
- ✅ Include rationale and business context
- ✅ Reference previous outputs for consistency
- ✅ Specify code quality standards
- ✅ Ask for explanations alongside code

---

**Document Created**: January 15, 2025  
**All Prompts Used**: 5 major prompts (1 per task)  
**Follow-up Prompts**: None required (all outputs met requirements)

