
import duckdb

data_path = "/mnt/c/Users/Sajad/Desktop/DB1C Market June 2026/DB1C.MARKET.202606.16SEP2026.parquet"

query = """
SELECT
    Origin,
    Dest,
    COUNT(*) AS records,
    ROUND(SUM(Passengers), 0) AS sampled_passengers,
    ROUND(MEDIAN(MktAmount - MktTax), 2) AS median_fare
FROM read_parquet(?)
WHERE MktCarrier = 'AA'
  AND OriginCountry = 'US'
  AND DestCountry = 'US'
  AND MktAmount > MktTax
GROUP BY Origin, Dest
ORDER BY sampled_passengers DESC
LIMIT 10
"""

result = duckdb.execute(query, [data_path]).df()
print(result.to_string(index=False))
  