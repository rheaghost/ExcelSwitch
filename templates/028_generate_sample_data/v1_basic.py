import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def run(task):

    output_file = task["output"]
    rows = task.get("rows", 100)

    random.seed(42)

    products = ["A", "B", "C", "D"]
    regions = ["Seoul", "Busan", "Daegu", "Incheon"]
    names = [
        "John",
        "Anna",
        "Mike",
        "Jane",
        "Tom",
        "Lisa",
        "David",
        "Susan"
    ]

    start_date = datetime(2026, 1, 1)

    data = []

    for i in range(1, rows + 1):

        price = random.randint(50, 500)
        quantity = random.randint(1, 10)

        data.append({
            "SaleID": f"S{i:04d}",
            "CustomerID": f"C{random.randint(1, 50):03d}",
            "Name": random.choice(names),
            "Product": random.choice(products),
            "Price": price,
            "Quantity": quantity,
            "Region": random.choice(regions),
            "SalesDate": (
                start_date
                + timedelta(days=random.randint(0, 364))
            ).strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(data)

    # Create the output directory if necessary.
    Path(output_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_excel(
        output_file,
        index=False
    )

    print("\nSample data generated.")
    print(f"Rows   : {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Output : {output_file}")

    return {
        "success": True,
        "task_id": "028",
        "output": output_file,
        "rows": len(df),
        "columns": len(df.columns)
    }