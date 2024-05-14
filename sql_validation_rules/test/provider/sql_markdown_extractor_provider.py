def create_stats_query_sql():
    return """
System: You are an agent designed to interact with a SQL database.
Human: Please extract only the SQL statements from the following text:

The SQL validation query for the numeric field `cc_tax_percentage` in the table `call_center` has been successfully created and executed. Here is the query:

```sql
WITH Stats AS (
  SELECT AVG(cc_tax_percentage) AS avg_tax, STDDEV(cc_tax_percentage) AS stddev_tax
  FROM "TPCDS_SF10TCL".call_center
)
SELECT c.cc_call_center_sk, c.cc_tax_percentage,
       (c.cc_tax_percentage - s.avg_tax) / s.stddev_tax AS z_score
FROM "TPCDS_SF10TCL".call_center c, Stats s
WHERE ABS((c.cc_tax_percentage - s.avg_tax) / s.stddev_tax) > 2.5
LIMIT 1000
```

This query calculates the z-score for the `cc_tax_percentage` field to identify outliers that are more than 2.5 standard deviations away from the mean. The query was executed without errors.

"""
