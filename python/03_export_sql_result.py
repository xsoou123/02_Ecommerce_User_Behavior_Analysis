import pandas as pd
import os

from config import PROJECT_ROOT, create_mysql_engine

engine = create_mysql_engine()



OUTPUT_PATH = str(PROJECT_ROOT / "report" / "sql_result")


os.makedirs(
    OUTPUT_PATH,
    exist_ok=True
)



views = {


"v_kpi_summary":
"01_kpi_summary.csv",


"v_monthly_sales":
"02_monthly_sales.csv",


"v_customer_region":
"03_customer_region.csv",


"v_category_sales":
"04_category_sales.csv",


"v_top_products":
"05_top_products.csv",


"v_payment_analysis":
"06_payment_analysis.csv",


"v_repeat_purchase":
"07_repeat_purchase.csv",


"v_rfm_analysis":
"08_rfm_analysis.csv"

}




for view,file in views.items():


    print(
        "正在导出:",
        view
    )


    df=pd.read_sql(
        f"SELECT * FROM {view}",
        engine
    )


    df.to_csv(

        os.path.join(
            OUTPUT_PATH,
            file
        ),

        index=False,

        encoding="utf-8-sig"

    )


    print(
        "完成:",
        file
    )



print("\n==============================")

print("SQL分析结果全部导出完成")

print(OUTPUT_PATH)

print("==============================")
