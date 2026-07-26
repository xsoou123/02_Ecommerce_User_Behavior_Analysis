import pandas as pd
import os

from config import PROJECT_ROOT, create_mysql_engine


# ==================================================
# 1. 项目路径
# ==================================================

DATA_PATH = PROJECT_ROOT / "data" / "raw"


# ==================================================
# 2. MySQL连接
# ==================================================

engine = create_mysql_engine()


print("=" * 70)
print("Olist E-commerce Data Import")
print("=" * 70)



# ==================================================
# 3. CSV文件与MySQL表对应关系
# ==================================================

tables = {

    "olist_customers_dataset.csv":
        "customers",

    "olist_geolocation_dataset.csv":
        "geolocation",

    "olist_order_items_dataset.csv":
        "order_items",

    "olist_order_payments_dataset.csv":
        "payments",

    "olist_order_reviews_dataset.csv":
        "reviews",

    "olist_orders_dataset.csv":
        "orders",

    "olist_products_dataset.csv":
        "products",

    "olist_sellers_dataset.csv":
        "sellers",

    "product_category_name_translation.csv":
        "category_translation"
}



# ==================================================
# 4. 稳定读取CSV函数
# ==================================================

def read_csv_file(file_path):

    """
    Olist数据集编码处理

    优先:
    utf-8

    失败:
    latin1
    """

    try:

        df = pd.read_csv(
            file_path,
            encoding="utf-8"
        )

        print("编码：utf-8")


    except UnicodeDecodeError:


        df = pd.read_csv(
            file_path,
            encoding="latin1"
        )

        print("编码：latin1")


    return df




# ==================================================
# 5. 导入单个CSV
# ==================================================

def import_table(csv_name, table_name):


    print("\n" + "-" * 60)

    print(f"正在处理：{csv_name}")


    file_path = os.path.join(
        DATA_PATH,
        csv_name
    )


    # 检查文件

    if not os.path.exists(file_path):

        print("文件不存在：", file_path)

        return



    # 读取数据

    df = read_csv_file(
        file_path
    )


    print(
        "数据规模：",
        df.shape
    )



    # 导入MySQL

    df.to_sql(

        name=table_name,

        con=engine,

        if_exists="replace",

        index=False,

        chunksize=5000

    )


    print(
        f"✓ {table_name} 导入完成"
    )



    # 数据库验证

    check = pd.read_sql(

        f"""
        SELECT COUNT(*) AS total
        FROM {table_name}
        """,

        engine

    )


    print(
        "数据库数量：",
        check.iloc[0,0]
    )




# ==================================================
# 6. 执行全部导入
# ==================================================

for csv_file, table in tables.items():

    import_table(
        csv_file,
        table
    )



# ==================================================
# 7. 查看最终数据库表
# ==================================================

print("\n")

print("=" * 70)

print("★★★★★ Olist 数据全部导入完成 ★★★★★")

print("=" * 70)



result = pd.read_sql(

    "SHOW TABLES",

    engine

)


print("\n当前数据库表：")

print(result)
