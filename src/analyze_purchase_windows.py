
import duckdb

data_path = "/mnt/c/Users/Sajad/Desktop/DB1C DB1C Ticket June 2026/DB1C.TICKET.202606.16SEP2026.parquet"

query = """
SELECT
    PurchaseWindowGroup,
    COUNT(*) AS tickets,
    ROUND(AVG(TotalAmount - TaxAmount), 2) AS mean_fare,
    ROUND(MEDIAN(TotalAmount - TaxAmount), 2) AS median_fare
FROM read_parquet(?)
WHERE TotalAmount > TaxAmount
GROUP BY PurchaseWindowGroup
ORDER BY PurchaseWindowGroup
"""

result = duckdb.execute(query, [data_path]).df()

print(result.to_string(index=False))

