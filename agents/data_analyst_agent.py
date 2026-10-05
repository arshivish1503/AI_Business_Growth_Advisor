import pandas as pd
import ollama


class DataAnalystAgent:

    def __init__(self):

        # ==============================
        # LOAD DATASETS
        # ==============================

        self.sales_data = pd.read_csv(
            "data/sales_data.csv"
        )

        self.product_data = pd.read_csv(
            "data/product_data.csv"
        )

        self.promotion_data = pd.read_csv(
            "data/promotion_data.csv"
        )

        self.competitor_data = pd.read_csv(
            "data/competitor_data.csv"
        )

        # ==============================
        # CLEAN COLUMN NAMES
        # ==============================

        self.sales_data.columns = (
            self.sales_data.columns.str.strip()
        )

        self.product_data.columns = (
            self.product_data.columns.str.strip()
        )

        self.promotion_data.columns = (
            self.promotion_data.columns.str.strip()
        )

        self.competitor_data.columns = (
            self.competitor_data.columns.str.strip()
        )

        # ==============================
        # DATE CONVERSION
        # ==============================

        self.sales_data["Date"] = pd.to_datetime(
            self.sales_data["Date"]
        )

        self.product_data["Launch_Date"] = pd.to_datetime(
            self.product_data["Launch_Date"]
        )

        self.promotion_data["Start_Date"] = pd.to_datetime(
            self.promotion_data["Start_Date"]
        )

        self.promotion_data["End_Date"] = pd.to_datetime(
            self.promotion_data["End_Date"]
        )

        self.competitor_data["Date"] = pd.to_datetime(
            self.competitor_data["Date"]
        )


    # =========================================================
    # 1. CITY PERFORMANCE
    # =========================================================

    def analyze_city(self, city):

        city_data = self.sales_data[
            self.sales_data["City"] == city
        ]

        if city_data.empty:
            return {
                "City": city,
                "Status": "No data available"
            }

        total_revenue = city_data["Revenue"].sum()

        total_units = city_data["Units_Sold"].sum()

        average_availability = (
            city_data["Availability_Percent"].mean()
        )

        # City benchmark

        city_revenue = (
            self.sales_data
            .groupby("City")["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        average_city_revenue = city_revenue.mean()

        city_rank = (
            city_revenue.rank(
                ascending=False,
                method="min"
            )[city]
        )

        total_cities = len(city_revenue)

        percentage_vs_average = (
            (
                total_revenue
                - average_city_revenue
            )
            / average_city_revenue
        ) * 100

        return {

            "City": city,

            "Total_Revenue": total_revenue,

            "Total_Units": total_units,

            "Average_Availability": average_availability,

            "Average_City_Revenue":
                average_city_revenue,

            "Revenue_vs_Average_Percent":
                percentage_vs_average,

            "Revenue_Rank":
                int(city_rank),

            "Total_Cities":
                total_cities
        }


    # =========================================================
    # 2. SKU PERFORMANCE
    # =========================================================

    def analyze_skus(self, city, top_n=5):

        city_data = self.sales_data[
            self.sales_data["City"] == city
        ].copy()

        if city_data.empty:
            return {
                "City": city,
                "Status": "No data available"
            }

        sku_summary = (
            city_data
            .groupby("SKU_ID")
            .agg(

                Revenue=("Revenue", "sum"),

                Units_Sold=("Units_Sold", "sum"),

                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                ),

                Average_Selling_Price=(
                    "Selling_Price",
                    "mean"
                )
            )
            .reset_index()
        )

        total_revenue = sku_summary["Revenue"].sum()

        sku_summary[
            "Revenue_Contribution_Percent"
        ] = (
            sku_summary["Revenue"]
            / total_revenue
            * 100
        )

        top_skus = (
            sku_summary
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(top_n)
        )

        bottom_skus = (
            sku_summary
            .sort_values(
                "Revenue",
                ascending=True
            )
            .head(top_n)
        )

        return {

            "City": city,

            "Top_SKUs":
                top_skus.to_dict("records"),

            "Bottom_SKUs":
                bottom_skus.to_dict("records")
        }


    # =========================================================
    # 3. CATEGORY PERFORMANCE
    # =========================================================

    def analyze_categories(self, city):

        city_sales = self.sales_data[
            self.sales_data["City"] == city
        ].copy()

        if city_sales.empty:
            return {
                "City": city,
                "Status": "No data available"
            }

        merged_data = city_sales.merge(
            self.product_data,
            on="SKU_ID",
            how="left",
            indicator=True
        )

        unmatched_records = (
            merged_data["_merge"]
            == "left_only"
        ).sum()

        category_summary = (
            merged_data
            .groupby("Category")
            .agg(

                Revenue=("Revenue", "sum"),

                Units_Sold=(
                    "Units_Sold",
                    "sum"
                ),

                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                ),

                Average_Selling_Price=(
                    "Selling_Price",
                    "mean"
                ),

                Average_Margin_Percent=(
                    "Margin_Percent",
                    "mean"
                )
            )
            .reset_index()
        )

        total_revenue = category_summary[
            "Revenue"
        ].sum()

        category_summary[
            "Revenue_Contribution_Percent"
        ] = (
            category_summary["Revenue"]
            / total_revenue
            * 100
        )

        category_summary = category_summary.sort_values(
            "Revenue",
            ascending=False
        )

        return {

            "City": city,

            "Categories":
                category_summary.to_dict("records"),

            "Unmatched_Product_Records":
                int(unmatched_records)
        }


    # =========================================================
    # 4. MONTHLY TREND
    # =========================================================

    def analyze_monthly_trend(self, city):

        city_data = self.sales_data[
            self.sales_data["City"] == city
        ].copy()

        if city_data.empty:
            return {
                "City": city,
                "Status": "No data available"
            }

        city_data["Month"] = (
            city_data["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly = (
            city_data
            .groupby("Month")
            .agg(

                Revenue=("Revenue", "sum"),

                Units_Sold=(
                    "Units_Sold",
                    "sum"
                ),

                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                )
            )
            .reset_index()
        )

        monthly["MoM_Revenue_Growth_Percent"] = (
            monthly["Revenue"]
            .pct_change()
            * 100
        )

        monthly[
            "MoM_Revenue_Growth_Percent"
        ] = monthly[
            "MoM_Revenue_Growth_Percent"
        ].fillna(0)

        return {

            "City": city,

            "Monthly_Trend":
                monthly.to_dict("records")
        }


    # =========================================================
    # 5. QUARTERLY TREND
    # =========================================================

    def analyze_quarters(self, city):

        city_data = self.sales_data[
            self.sales_data["City"] == city
        ].copy()

        if city_data.empty:
            return {
                "City": city,
                "Status": "No data available"
            }

        city_data["Quarter"] = (
            city_data["Date"]
            .dt.to_period("Q")
            .astype(str)
        )

        quarterly = (
            city_data
            .groupby("Quarter")
            .agg(

                Revenue=("Revenue", "sum"),

                Units_Sold=(
                    "Units_Sold",
                    "sum"
                ),

                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                )
            )
            .reset_index()
        )

        quarterly[
            "Quarter_Revenue_Growth_Percent"
        ] = (
            quarterly["Revenue"]
            .pct_change()
            * 100
        )

        quarterly[
            "Quarter_Revenue_Growth_Percent"
        ] = quarterly[
            "Quarter_Revenue_Growth_Percent"
        ].fillna(0)

        return {

            "City": city,

            "Quarterly_Trend":
                quarterly.to_dict("records")
        }


    # =========================================================
    # 6. Q2 VS Q3 COMPARISON
    # =========================================================

    def compare_q2_q3(
        self,
        city,
        year=2026
    ):

        city_data = self.sales_data[
            self.sales_data["City"] == city
        ].copy()

        city_data = city_data[
            city_data["Date"].dt.year == year
        ]

        q2 = city_data[
            city_data["Date"].dt.quarter == 2
        ]

        q3 = city_data[
            city_data["Date"].dt.quarter == 3
        ]

        q2_revenue = q2["Revenue"].sum()
        q3_revenue = q3["Revenue"].sum()

        q2_units = q2["Units_Sold"].sum()
        q3_units = q3["Units_Sold"].sum()

        q2_availability = (
            q2["Availability_Percent"].mean()
        )

        q3_availability = (
            q3["Availability_Percent"].mean()
        )

        revenue_change = (
            q3_revenue - q2_revenue
        )

        revenue_change_percent = (
            revenue_change
            / q2_revenue
            * 100
            if q2_revenue != 0
            else 0
        )

        units_change_percent = (
            (q3_units - q2_units)
            / q2_units
            * 100
            if q2_units != 0
            else 0
        )

        availability_change_pp = (
            q3_availability
            - q2_availability
        )

        return {

            "City": city,

            "Year": year,

            "Q2_Revenue":
                q2_revenue,

            "Q3_Revenue":
                q3_revenue,

            "Revenue_Change":
                revenue_change,

            "Revenue_Change_Percent":
                revenue_change_percent,

            "Q2_Units":
                q2_units,

            "Q3_Units":
                q3_units,

            "Units_Change_Percent":
                units_change_percent,

            "Q2_Average_Availability":
                q2_availability,

            "Q3_Average_Availability":
                q3_availability,

            "Availability_Change_pp":
                availability_change_pp
        }


    # =========================================================
    # 7. SKU LEVEL Q2 VS Q3
    # =========================================================

    def compare_skus_q2_q3(
        self,
        city,
        year=2026,
        top_n=10
    ):

        city_data = self.sales_data[
            self.sales_data["City"] == city
        ].copy()

        city_data = city_data[
            city_data["Date"].dt.year == year
        ]

        city_data["Quarter"] = (
            city_data["Date"].dt.quarter
        )

        q2 = city_data[
            city_data["Quarter"] == 2
        ]

        q3 = city_data[
            city_data["Quarter"] == 3
        ]

        q2_summary = (
            q2.groupby("SKU_ID")
            .agg(

                Q2_Revenue=("Revenue", "sum"),

                Q2_Units=("Units_Sold", "sum"),

                Q2_Availability=(
                    "Availability_Percent",
                    "mean"
                )
            )
        )

        q3_summary = (
            q3.groupby("SKU_ID")
            .agg(

                Q3_Revenue=("Revenue", "sum"),

                Q3_Units=("Units_Sold", "sum"),

                Q3_Availability=(
                    "Availability_Percent",
                    "mean"
                )
            )
        )

        comparison = q2_summary.join(
            q3_summary,
            how="outer"
        ).fillna(0)

        comparison[
            "Revenue_Change"
        ] = (
            comparison["Q3_Revenue"]
            - comparison["Q2_Revenue"]
        )

        comparison[
            "Revenue_Change_Percent"
        ] = (
            comparison["Revenue_Change"]
            / comparison["Q2_Revenue"]
            * 100
        )

        comparison[
            "Revenue_Change_Percent"
        ] = comparison[
            "Revenue_Change_Percent"
        ].replace(
            [float("inf"), -float("inf")],
            0
        )

        comparison[
            "Units_Change"
        ] = (
            comparison["Q3_Units"]
            - comparison["Q2_Units"]
        )

        comparison[
            "Units_Change_Percent"
        ] = (
            comparison["Units_Change"]
            / comparison["Q2_Units"]
            * 100
        )

        comparison[
            "Units_Change_Percent"
        ] = comparison[
            "Units_Change_Percent"
        ].replace(
            [float("inf"), -float("inf")],
            0
        )

        comparison[
            "Availability_Change_pp"
        ] = (
            comparison["Q3_Availability"]
            - comparison["Q2_Availability"]
        )

        comparison = (
            comparison
            .sort_values(
                "Revenue_Change"
            )
            .head(top_n)
        )

        comparison = comparison.reset_index()

        return {

            "City": city,

            "Year": year,

            "SKUs_With_Largest_Revenue_Decline":
                comparison.to_dict("records")
        }


    # =========================================================
    # 8. PROMOTION ANALYSIS
    # =========================================================

    def analyze_promotions(
        self,
        city,
        year=2026
    ):

        sales = self.sales_data[
            self.sales_data["City"] == city
        ].copy()

        sales = sales[
            sales["Date"].dt.year == year
        ]

        if sales.empty:

            return {

                "City": city,

                "Year": year,

                "Status":
                    "No sales data available"
            }

        # Sales associated with promotion IDs

        promotion_sales = sales[
            sales["Promotion_ID"].notna()
        ].copy()

        total_revenue = sales[
            "Revenue"
        ].sum()

        promoted_revenue = promotion_sales[
            "Revenue"
        ].sum()

        promoted_units = promotion_sales[
            "Units_Sold"
        ].sum()

        promotion_revenue_share = (

            promoted_revenue
            / total_revenue
            * 100

            if total_revenue > 0
            else 0
        )

        # Promotion master data

        promotions = self.promotion_data.copy()

        promotions = promotions[

            (promotions["Start_Date"].dt.year <= year)

            &

            (promotions["End_Date"].dt.year >= year)
        ]

        if not promotions.empty:

            average_discount = (
                promotions[
                    "Discount_Percent"
                ].mean()
            )

            total_budget = (
                promotions[
                    "Campaign_Budget"
                ].sum()
            )

            promotion_count = len(
                promotions
            )

            promotion_types = (

                promotions
                .groupby(
                    "Promotion_Type"
                )
                .agg(

                    Promotion_Count=(
                        "Promotion_ID",
                        "count"
                    ),

                    Average_Discount=(
                        "Discount_Percent",
                        "mean"
                    ),

                    Campaign_Budget=(
                        "Campaign_Budget",
                        "sum"
                    )
                )
                .reset_index()
            )

        else:

            average_discount = 0

            total_budget = 0

            promotion_count = 0

            promotion_types = (
                pd.DataFrame()
            )

        return {

            "City": city,

            "Year": year,

            "Total_Revenue":
                total_revenue,

            "Promoted_Revenue":
                promoted_revenue,

            "Promoted_Units":
                promoted_units,

            "Promotion_Revenue_Share_Percent":
                promotion_revenue_share,

            "Promotion_Count":
                promotion_count,

            "Average_Discount_Percent":
                average_discount,

            "Total_Campaign_Budget":
                total_budget,

            "Promotion_Types":
                promotion_types.to_dict(
                    "records"
                )
        }


    # =========================================================
    # 9. Q2 VS Q3 PROMOTION COMPARISON
    # =========================================================

    def compare_promotions_q2_q3(
        self,
        city,
        year=2026
    ):

        sales = self.sales_data[
            self.sales_data["City"] == city
        ].copy()

        sales = sales[
            sales["Date"].dt.year == year
        ]

        results = {}

        for quarter, quarter_name in [
            (2, "Q2"),
            (3, "Q3")
        ]:

            quarter_sales = sales[
                sales["Date"].dt.quarter
                == quarter
            ]

            total_revenue = (
                quarter_sales[
                    "Revenue"
                ].sum()
            )

            promoted_sales = (
                quarter_sales[
                    quarter_sales[
                        "Promotion_ID"
                    ].notna()
                ]
            )

            promoted_revenue = (
                promoted_sales[
                    "Revenue"
                ].sum()
            )

            promoted_units = (
                promoted_sales[
                    "Units_Sold"
                ].sum()
            )

            promotion_share = (

                promoted_revenue
                / total_revenue
                * 100

                if total_revenue > 0
                else 0
            )

            results[quarter_name] = {

                "Revenue":
                    total_revenue,

                "Promoted_Revenue":
                    promoted_revenue,

                "Promoted_Units":
                    promoted_units,

                "Promotion_Revenue_Share_Percent":
                    promotion_share,

                "Promoted_SKUs":
                    promoted_sales[
                        "SKU_ID"
                    ].nunique()
            }

        revenue_share_change = (

            results["Q3"][
                "Promotion_Revenue_Share_Percent"
            ]

            -

            results["Q2"][
                "Promotion_Revenue_Share_Percent"
            ]
        )

        return {

            "City": city,

            "Year": year,

            "Q2":
                results["Q2"],

            "Q3":
                results["Q3"],

            "Promotion_Revenue_Share_Change_pp":
                revenue_share_change
        }


    # =========================================================
    # 10. COMPETITOR PRESSURE ANALYSIS
    # =========================================================

    def analyze_competitor_pressure(
        self,
        city,
        year=2026
    ):

        competitor = self.competitor_data[
            self.competitor_data["City"] == city
        ].copy()

        competitor = competitor[
            competitor["Date"].dt.year == year
        ]

        if competitor.empty:

            return {

                "City": city,

                "Year": year,

                "Status":
                    "No competitor data available"
            }

        # ------------------------------
        # Competitor level
        # ------------------------------

        competitor_summary = (

            competitor
            .groupby("Competitor")
            .agg(

                Average_Price=(
                    "Price",
                    "mean"
                ),

                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                ),

                Observations=(
                    "Date",
                    "count"
                )
            )
            .reset_index()
        )

        # ------------------------------
        # Category level
        # ------------------------------

        category_summary = (

            competitor
            .groupby("Category")
            .agg(

                Average_Competitor_Price=(
                    "Price",
                    "mean"
                ),

                Average_Competitor_Availability=(
                    "Availability_Percent",
                    "mean"
                ),

                Observations=(
                    "Date",
                    "count"
                )
            )
            .reset_index()
        )

        # ------------------------------
        # Quarterly level
        # ------------------------------

        competitor["Quarter"] = (
            competitor["Date"]
            .dt.quarter
        )

        quarterly_summary = (

            competitor
            .groupby("Quarter")
            .agg(

                Average_Price=(
                    "Price",
                    "mean"
                ),

                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                ),

                Observations=(
                    "Date",
                    "count"
                )
            )
            .reset_index()
        )

        return {

            "City": city,

            "Year": year,

            "Competitor_Summary":
                competitor_summary.to_dict(
                    "records"
                ),

            "Category_Summary":
                category_summary.to_dict(
                    "records"
                ),

            "Quarterly_Summary":
                quarterly_summary.to_dict(
                    "records"
                )
        }


    # =========================================================
    # 11. LLM BUSINESS INSIGHT GENERATION
    # =========================================================

    def generate_insight(
        self,
        analysis
    ):

        prompt = f"""
You are a senior FMCG business analyst.

Analyze the following structured business
analysis and generate a concise,
evidence-based business insight.

IMPORTANT RULES:

1. Use ONLY the evidence provided.
2. Do not invent facts.
3. Do not invent competitors.
4. Do not invent customer behavior.
5. Do not invent pricing or promotion effects.
6. Do not claim causation unless the data
   directly supports causation.
7. Clearly distinguish:
   - Observed facts
   - Business interpretation
   - Hypotheses
8. If the evidence only shows association,
   use words such as:
   "associated with",
   "consistent with",
   "may indicate",
   "suggests".
9. Recommendations must be connected
   to the evidence.
10. Keep the response practical for a
    sales or marketing manager.

Use the following structure:

1. Key Finding
2. Evidence
3. Business Interpretation
4. Potential Concern
5. Recommended Action
6. Confidence

Business Analysis:

{analysis}
"""

        response = ollama.chat(

            model="llama3.2:3b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response[
            "message"
        ][
            "content"
        ]