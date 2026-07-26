import pandas as pd
import os

from config import PROJECT_ROOT, create_mysql_engine

# ==================================================
# 1. MySQL连接
# ==================================================

engine = create_mysql_engine()


print("=" * 70)
print("Olist E-commerce EDA Analysis")
print("=" * 70)


# ==================================================
# 2. 输出路径
# ==================================================

OUTPUT_PATH = str(PROJECT_ROOT / "report")


os.makedirs(
    OUTPUT_PATH,
    exist_ok=True
)



# ==================================================
# 3. 读取MySQL数据
# ==================================================

print("\n正在读取数据...")


customers = pd.read_sql(
    "SELECT * FROM customers",
    engine
)


orders = pd.read_sql(
    "SELECT * FROM orders",
    engine
)


order_items = pd.read_sql(
    "SELECT * FROM order_items",
    engine
)


payments = pd.read_sql(
    "SELECT * FROM payments",
    engine
)


products = pd.read_sql(
    "SELECT * FROM products",
    engine
)


reviews = pd.read_sql(
    "SELECT * FROM reviews",
    engine
)


print("数据读取完成")



# ==================================================
# 4. 数据规模检查
# ==================================================

print("\n========== 数据规模 ==========")


tables = {

    "customers": customers,

    "orders": orders,

    "order_items": order_items,

    "payments": payments,

    "products": products,

    "reviews": reviews

}


for name, df in tables.items():

    print(
        f"{name}: {df.shape}"
    )



# ==================================================
# 5. 日期处理
# ==================================================

print("\n========== 日期转换 ==========")


orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)


orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"],
    errors="coerce"
)



# ==================================================
# 6. 创建订单宽表
# ==================================================

print("\n创建订单分析表...")


orders_items = order_items.merge(

    orders[

        [
            "order_id",
            "customer_id",
            "order_purchase_timestamp"
        ]

    ],

    on="order_id",

    how="left"

)


print(
    orders_items.head()
)



# ==================================================
# 7. KPI分析
# ==================================================

print("\n========== Business KPI ==========")


total_customers = (
    customers["customer_unique_id"]
    .nunique()
)


total_orders = (
    orders["order_id"]
    .nunique()
)


# GMV = 商品金额 + 运费

total_sales = (

    order_items["price"].sum()

    +

    order_items["freight_value"].sum()

)



avg_order_value = (

    total_sales

    /

    total_orders

)



print(
    f"用户数量: {total_customers:,}"
)


print(
    f"订单数量: {total_orders:,}"
)


print(
    f"GMV: {total_sales:,.2f}"
)


print(
    f"平均订单金额: {avg_order_value:,.2f}"
)



kpi = pd.DataFrame({

    "Metric":[

        "Customers",

        "Orders",

        "GMV",

        "Average Order Value"

    ],

    "Value":[

        total_customers,

        total_orders,

        total_sales,

        avg_order_value

    ]

})


kpi.to_csv(

    OUTPUT_PATH +
    r"\kpi_summary.csv",

    index=False,

    encoding="utf-8-sig"

)



# ==================================================
# 8. 月销售趋势
# ==================================================

print("\n========== Monthly Sales ==========")


orders_items["month"] = (

    orders_items[
        "order_purchase_timestamp"
    ]

    .dt

    .strftime("%Y-%m")

)



monthly_sales = (

    orders_items

    .groupby("month")

    .agg(

        Sales=(

            "price",

            "sum"

        )

    )

    .reset_index()

)



monthly_sales.columns = [

    "Month",

    "Sales"

]


print(
    monthly_sales.head()
)


monthly_sales.to_csv(

    OUTPUT_PATH +
    r"\monthly_sales.csv",

    index=False,

    encoding="utf-8-sig"

)



# ==================================================
# 9. 商品分析
# ==================================================

print("\n========== Product Analysis ==========")


product_analysis = (

    order_items

    .groupby(
        "product_id"
    )

    .agg(

        Sales=(

            "price",

            "sum"

        ),

        Orders=(

            "order_id",

            "count"

        )

    )

    .reset_index()

)



product_analysis = (

    product_analysis

    .sort_values(

        "Sales",

        ascending=False

    )

    .head(20)

)



print(
    product_analysis.head()
)


product_analysis.to_csv(

    OUTPUT_PATH +
    r"\product_analysis.csv",

    index=False,

    encoding="utf-8-sig"

)



# ==================================================
# 10. 支付分析
# ==================================================

print("\n========== Payment Analysis ==========")


payment_analysis = (

    payments

    .groupby(

        "payment_type"

    )

    ["payment_value"]

    .sum()

    .reset_index()

)



payment_analysis.columns = [

    "Payment_Type",

    "Total_Payment"

]


print(
    payment_analysis
)


payment_analysis.to_csv(

    OUTPUT_PATH +
    r"\payment_analysis.csv",

    index=False,

    encoding="utf-8-sig"

)



# ==================================================
# 11. 用户地区分析
# ==================================================

print("\n========== Customer Location ==========")


customer_location = (

    customers

    .groupby(

        "customer_state"

    )

    ["customer_unique_id"]

    .count()

    .reset_index()

)



customer_location.columns = [

    "State",

    "Customer_Count"

]


customer_location = (

    customer_location

    .sort_values(

        "Customer_Count",

        ascending=False

    )

)



customer_location.to_csv(

    OUTPUT_PATH +
    r"\customer_location.csv",

    index=False,

    encoding="utf-8-sig"

)



# ==================================================
# 12. RFM用户价值分析
# ==================================================

print("\n========== RFM Analysis ==========")


rfm_data = orders_items.merge(

    customers[

        [

            "customer_id",

            "customer_unique_id"

        ]

    ],

    on="customer_id",

    how="left"

)



snapshot_date = (

    orders_items[

        "order_purchase_timestamp"

    ]

    .max()

    +

    pd.Timedelta(days=1)

)



rfm = (

    rfm_data

    .groupby(

        "customer_unique_id"

    )

    .agg(

        {

            "order_purchase_timestamp":

            lambda x:

            (

                snapshot_date -

                x.max()

            ).days,


            "order_id":

            "count",


            "price":

            "sum"

        }

    )

    .reset_index()

)



rfm.columns = [

    "Customer_ID",

    "Recency",

    "Frequency",

    "Monetary"

]



# 用户分层

rfm["Segment"] = "Normal Customer"



rfm.loc[

    (

        rfm["Frequency"] >= 5

    )

    &

    (

        rfm["Monetary"]

        >

        rfm["Monetary"].median()

    ),

    "Segment"

] = "VIP Customer"



rfm.loc[

    rfm["Frequency"] == 1,

    "Segment"

] = "New Customer"



print(
    rfm.head()
)



rfm.to_csv(

    OUTPUT_PATH +

    r"\rfm_customer.csv",

    index=False,

    encoding="utf-8-sig"

)



# ==================================================
# 完成
# ==================================================

print("\n")

print("=" * 70)

print("★★★★★ EDA分析完成 ★★★★★")

print("输出文件:")

print(OUTPUT_PATH)

print("=" * 70)
