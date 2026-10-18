
from pathlib import Path
import duckdb

source = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "DB1C.MARKET.202606.16SEP2026.parquet"
)

output = Path("data/processed/aa_ord_lga_nonstop.parquet")

if not source.is_file():
    raise FileNotFoundError(source)

output.parent.mkdir(parents=True, exist_ok=True)

data = (
    duckdb.read_parquet(str(source))
    .filter("""
        MktCarrier = 'AA'
        AND Origin = 'ORD'
        AND Dest = 'LGA'
        AND Nonstop = 1
        AND MktCoupons = 1
        AND Passengers > 0
        AND MktAmount > MktTax
    """)
    .project("""
        ItinID,
        MktID,
        MktCarrier,
        Origin,
        Dest,
        SchFlMonth,
        PurchaseWindowGroup,
        Passengers,
        ROUND(MktAmount - MktTax, 2) AS fare_ex_tax
    """)
)

data.write_parquet(str(output), overwrite=True, use_tmp_file=True)

result = duckdb.read_parquet(str(output)).aggregate("""
    COUNT(*) AS records,
    ROUND(MEDIAN(fare_ex_tax), 2) AS median_fare
""")

print("DATA PIPELINE OK")
print(result.df().to_string(index=False))
print(f"Saved: {output}")
