
import duckdb

data_path = "/mnt/c/Users/Sajad/Desktop/DB1C DB1C Ticket June 2026/DB1C.TICKET.202606.16SEP2026.parquet"

query = """
SELECT
    RpCarrier,
    COUNT(*) AS tickets,
    ROUND(MEDIAN(TotalAmount - TaxAmount), 2) AS median_fare
FROM read_parquet(?)
WHERE TotalAmount > TaxAmount
  AND RpCarrier IS NOT NULL
GROUP BY RpCarrier
ORDER BY tickets DESC
LIMIT 10
"""

result = duckdb.execute(query, [data_path]).df()

print(result.to_string(index=False))
