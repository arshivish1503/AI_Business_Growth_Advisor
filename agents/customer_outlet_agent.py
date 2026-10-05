import pandas as pd


class CustomerOutletAgent:
    """Customer/Outlet analytics agent for the AI Business Growth Advisor."""

    def __init__(self):
        print("[Customer/Outlet Agent] Loading outlet and sales data...")

        self.sales = pd.read_csv("data/sales_data.csv")
        self.outlets = pd.read_csv("data/outlet_data.csv")

        self.sales.columns = self.sales.columns.str.strip()
        self.outlets.columns = self.outlets.columns.str.strip()

        self.sales["Date"] = pd.to_datetime(
            self.sales["Date"],
            errors="coerce"
        )

        print("[Customer/Outlet Agent] Data loaded successfully.")

    # ==================================================
    # 1. OUTLET TYPE PERFORMANCE
    # ==================================================

    def analyze_outlet_types(self, city=None):

        sales = self.sales.copy()
        outlets = self.outlets.copy()

        if city:
            sales = sales[sales["City"] == city]
            outlets = outlets[outlets["City"] == city]

        merged = sales.merge(
            outlets[
                [
                    "Outlet_ID",
                    "Outlet_Type",
                    "Tier",
                    "Monthly_Footfall",
                    "Active",
                ]
            ],
            on="Outlet_ID",
            how="left",
        )

        result = (
            merged
            .groupby(
                "Outlet_Type",
                dropna=False
            )
            .agg(
                Revenue=("Revenue", "sum"),
                Units_Sold=("Units_Sold", "sum"),
                Average_Footfall=("Monthly_Footfall", "mean"),
                Average_Availability=("Availability_Percent", "mean"),
                Outlet_Count=("Outlet_ID", "nunique"),
            )
            .reset_index()
        )

        total_revenue = result["Revenue"].sum()

        result["Revenue_Contribution_Percent"] = (
            result["Revenue"] / total_revenue * 100
            if total_revenue != 0
            else 0
        )

        return result.sort_values(
            "Revenue",
            ascending=False
        )

    # ==================================================
    # 2. OUTLET TIER PERFORMANCE
    # ==================================================

    def analyze_outlet_tiers(self, city=None):

        sales = self.sales.copy()
        outlets = self.outlets.copy()

        if city:
            sales = sales[sales["City"] == city]
            outlets = outlets[outlets["City"] == city]

        merged = sales.merge(
            outlets[
                [
                    "Outlet_ID",
                    "Outlet_Type",
                    "Tier",
                    "Monthly_Footfall",
                    "Active",
                ]
            ],
            on="Outlet_ID",
            how="left",
        )

        result = (
            merged
            .groupby(
                "Tier",
                dropna=False
            )
            .agg(
                Revenue=("Revenue", "sum"),
                Units_Sold=("Units_Sold", "sum"),
                Average_Footfall=("Monthly_Footfall", "mean"),
                Average_Availability=("Availability_Percent", "mean"),
                Outlet_Count=("Outlet_ID", "nunique"),
            )
            .reset_index()
        )

        total_revenue = result["Revenue"].sum()

        result["Revenue_Contribution_Percent"] = (
            result["Revenue"] / total_revenue * 100
            if total_revenue != 0
            else 0
        )

        return result.sort_values(
            "Revenue",
            ascending=False
        )

    # ==================================================
    # 3. OUTLET-LEVEL PERFORMANCE
    # ==================================================

    def analyze_outlets(
        self,
        city=None,
        top_n=10
    ):

        sales = self.sales.copy()
        outlets = self.outlets.copy()

        if city:
            sales = sales[sales["City"] == city]
            outlets = outlets[outlets["City"] == city]

        merged = sales.merge(
            outlets[
                [
                    "Outlet_ID",
                    "Outlet_Name",
                    "Outlet_Type",
                    "Tier",
                    "Monthly_Footfall",
                    "Active",
                ]
            ],
            on="Outlet_ID",
            how="left",
        )

        result = (
            merged
            .groupby(
                [
                    "Outlet_ID",
                    "Outlet_Name",
                    "Outlet_Type",
                    "Tier",
                ],
                dropna=False
            )
            .agg(
                Revenue=("Revenue", "sum"),
                Units_Sold=("Units_Sold", "sum"),
                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                ),
                Average_Footfall=(
                    "Monthly_Footfall",
                    "mean"
                ),
            )
            .reset_index()
        )

        total_revenue = result["Revenue"].sum()

        result["Revenue_Contribution_Percent"] = (
            result["Revenue"] / total_revenue * 100
            if total_revenue != 0
            else 0
        )

        top_outlets = (
            result
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(top_n)
        )

        bottom_outlets = (
            result
            .sort_values(
                "Revenue",
                ascending=True
            )
            .head(top_n)
        )

        return {
            "Top_Outlets": top_outlets,
            "Bottom_Outlets": bottom_outlets,
        }

    # ==================================================
    # 4. OUTLET Q2 VS Q3
    # ==================================================

    def compare_outlets_q2_q3(
        self,
        city=None,
        year=2026,
        top_n=10
    ):

        sales = self.sales.copy()
        outlets = self.outlets.copy()

        sales = sales[
            sales["Date"].dt.year == year
        ].copy()

        sales["Quarter"] = sales["Date"].dt.quarter

        sales = sales[
            sales["Quarter"].isin([2, 3])
        ]

        if city:
            sales = sales[sales["City"] == city]
            outlets = outlets[outlets["City"] == city]

        merged = sales.merge(
            outlets[
                [
                    "Outlet_ID",
                    "Outlet_Name",
                    "Outlet_Type",
                    "Tier",
                ]
            ],
            on="Outlet_ID",
            how="left",
        )

        result = (
            merged
            .groupby(
                [
                    "Outlet_ID",
                    "Outlet_Name",
                    "Outlet_Type",
                    "Tier",
                    "Quarter",
                ],
                dropna=False
            )
            .agg(
                Revenue=("Revenue", "sum"),
                Units_Sold=("Units_Sold", "sum"),
                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                ),
            )
            .reset_index()
        )

        # --------------------------------------------------
        # Revenue
        # --------------------------------------------------

        revenue = result.pivot_table(
            index=[
                "Outlet_ID",
                "Outlet_Name",
                "Outlet_Type",
                "Tier",
            ],
            columns="Quarter",
            values="Revenue",
            fill_value=0,
        )

        revenue = revenue.rename(
            columns={
                2: "Q2_Revenue",
                3: "Q3_Revenue",
            }
        ).reset_index()

        # --------------------------------------------------
        # Units
        # --------------------------------------------------

        units = result.pivot_table(
            index=[
                "Outlet_ID",
                "Outlet_Name",
                "Outlet_Type",
                "Tier",
            ],
            columns="Quarter",
            values="Units_Sold",
            fill_value=0,
        )

        units = units.rename(
            columns={
                2: "Q2_Units",
                3: "Q3_Units",
            }
        ).reset_index()

        # --------------------------------------------------
        # Availability
        # --------------------------------------------------

        availability = result.pivot_table(
            index=[
                "Outlet_ID",
                "Outlet_Name",
                "Outlet_Type",
                "Tier",
            ],
            columns="Quarter",
            values="Average_Availability",
        )

        availability = availability.rename(
            columns={
                2: "Q2_Availability",
                3: "Q3_Availability",
            }
        ).reset_index()

        # --------------------------------------------------
        # Merge
        # --------------------------------------------------

        final = revenue.merge(
            units,
            on=[
                "Outlet_ID",
                "Outlet_Name",
                "Outlet_Type",
                "Tier",
            ],
            how="outer",
        )

        final = final.merge(
            availability,
            on=[
                "Outlet_ID",
                "Outlet_Name",
                "Outlet_Type",
                "Tier",
            ],
            how="outer",
        )

        numerical_columns = [
            "Q2_Revenue",
            "Q3_Revenue",
            "Q2_Units",
            "Q3_Units",
            "Q2_Availability",
            "Q3_Availability",
        ]

        for column in numerical_columns:
            if column in final.columns:
                final[column] = final[column].fillna(0)

        # --------------------------------------------------
        # Revenue change
        # --------------------------------------------------

        final["Revenue_Change"] = (
            final["Q3_Revenue"]
            - final["Q2_Revenue"]
        )

        final["Revenue_Change_Percent"] = (
            final["Revenue_Change"]
            /
            final["Q2_Revenue"].replace(0, pd.NA)
        ) * 100

        # --------------------------------------------------
        # Units change
        # --------------------------------------------------

        final["Units_Change"] = (
            final["Q3_Units"]
            - final["Q2_Units"]
        )

        final["Units_Change_Percent"] = (
            final["Units_Change"]
            /
            final["Q2_Units"].replace(0, pd.NA)
        ) * 100

        # --------------------------------------------------
        # Availability change
        # --------------------------------------------------

        final["Availability_Change_pp"] = (
            final["Q3_Availability"]
            - final["Q2_Availability"]
        )

        # Largest revenue declines first
        final = final.sort_values(
            "Revenue_Change",
            ascending=True
        )

        return final.head(top_n)

    # ==================================================
    # 5. OUTLET TYPE Q2 VS Q3
    # ==================================================

    def compare_outlet_types_q2_q3(
        self,
        city=None,
        year=2026
    ):

        sales = self.sales.copy()
        outlets = self.outlets.copy()

        sales = sales[
            sales["Date"].dt.year == year
        ].copy()

        sales["Quarter"] = sales["Date"].dt.quarter

        sales = sales[
            sales["Quarter"].isin([2, 3])
        ]

        if city:
            sales = sales[sales["City"] == city]
            outlets = outlets[outlets["City"] == city]

        merged = sales.merge(
            outlets[
                [
                    "Outlet_ID",
                    "Outlet_Type",
                    "Tier",
                ]
            ],
            on="Outlet_ID",
            how="left",
        )

        result = (
            merged
            .groupby(
                [
                    "Outlet_Type",
                    "Quarter",
                ],
                dropna=False
            )
            .agg(
                Revenue=("Revenue", "sum"),
                Units_Sold=("Units_Sold", "sum"),
                Average_Availability=(
                    "Availability_Percent",
                    "mean"
                ),
            )
            .reset_index()
        )

        # --------------------------------------------------
        # Revenue
        # --------------------------------------------------

        revenue = result.pivot_table(
            index="Outlet_Type",
            columns="Quarter",
            values="Revenue",
            fill_value=0,
        )

        revenue = revenue.rename(
            columns={
                2: "Q2_Revenue",
                3: "Q3_Revenue",
            }
        ).reset_index()

        # --------------------------------------------------
        # Units
        # --------------------------------------------------

        units = result.pivot_table(
            index="Outlet_Type",
            columns="Quarter",
            values="Units_Sold",
            fill_value=0,
        )

        units = units.rename(
            columns={
                2: "Q2_Units",
                3: "Q3_Units",
            }
        ).reset_index()

        # --------------------------------------------------
        # Availability
        # --------------------------------------------------

        availability = result.pivot_table(
            index="Outlet_Type",
            columns="Quarter",
            values="Average_Availability",
        )

        availability = availability.rename(
            columns={
                2: "Q2_Availability",
                3: "Q3_Availability",
            }
        ).reset_index()

        # --------------------------------------------------
        # Merge
        # --------------------------------------------------

        final = revenue.merge(
            units,
            on="Outlet_Type",
            how="outer"
        )

        final = final.merge(
            availability,
            on="Outlet_Type",
            how="outer"
        )

        numerical_columns = [
            "Q2_Revenue",
            "Q3_Revenue",
            "Q2_Units",
            "Q3_Units",
            "Q2_Availability",
            "Q3_Availability",
        ]

        for column in numerical_columns:
            if column in final.columns:
                final[column] = final[column].fillna(0)

        # --------------------------------------------------
        # Revenue change
        # --------------------------------------------------

        final["Revenue_Change"] = (
            final["Q3_Revenue"]
            - final["Q2_Revenue"]
        )

        final["Revenue_Change_Percent"] = (
            final["Revenue_Change"]
            /
            final["Q2_Revenue"].replace(0, pd.NA)
        ) * 100

        # --------------------------------------------------
        # Units change
        # --------------------------------------------------

        final["Units_Change_Percent"] = (
            (
                final["Q3_Units"]
                - final["Q2_Units"]
            )
            /
            final["Q2_Units"].replace(0, pd.NA)
        ) * 100

        # --------------------------------------------------
        # Availability change
        # --------------------------------------------------

        final["Availability_Change_pp"] = (
            final["Q3_Availability"]
            - final["Q2_Availability"]
        )

        return final.sort_values(
            "Revenue_Change",
            ascending=True
        )

    # ==================================================
    # 6. DETERMINISTIC EVIDENCE-BASED OUTLET INSIGHT
    # ==================================================

    def generate_insight(
        self,
        outlet_type_analysis,
        tier_analysis,
        q2_q3_analysis,
        outlet_type_q2_q3_analysis=None,
    ):
        """
        Generate reliable business insight using deterministic
        Python calculations rather than asking the LLM to rank
        or interpret numerical tables.
        """

        print(
            "[Customer/Outlet Agent] "
            "Generating deterministic evidence-based outlet insight..."
        )

        if outlet_type_analysis.empty:
            return (
                "No outlet-type data available for the selected scope."
            )

        if tier_analysis.empty:
            return (
                "No outlet-tier data available for the selected scope."
            )

        if q2_q3_analysis.empty:
            return (
                "No Q2-Q3 outlet comparison data available "
                "for the selected scope."
            )

        # --------------------------------------------------
        # 1. BASIC OUTLET TYPE FINDINGS
        # --------------------------------------------------

        highest_revenue_type = outlet_type_analysis.loc[
            outlet_type_analysis["Revenue"].idxmax()
        ]

        highest_units_type = outlet_type_analysis.loc[
            outlet_type_analysis["Units_Sold"].idxmax()
        ]

        highest_contribution_type = outlet_type_analysis.loc[
            outlet_type_analysis[
                "Revenue_Contribution_Percent"
            ].idxmax()
        ]

        # --------------------------------------------------
        # 2. OUTLET TYPE Q2 VS Q3
        # --------------------------------------------------

        priority_types = None
        largest_type_decline = None

        if (
            outlet_type_q2_q3_analysis is not None
            and not outlet_type_q2_q3_analysis.empty
        ):

            priority_types = (
                outlet_type_q2_q3_analysis
                .sort_values(
                    "Revenue_Change_Percent",
                    ascending=True
                )
                .head(3)
            )

            largest_type_decline = (
                outlet_type_q2_q3_analysis.loc[
                    outlet_type_q2_q3_analysis[
                        "Revenue_Change_Percent"
                    ].idxmin()
                ]
            )

        # --------------------------------------------------
        # 3. TIER PERFORMANCE
        # --------------------------------------------------

        tier_ranked = tier_analysis.sort_values(
            "Revenue_Contribution_Percent",
            ascending=False
        )

        # --------------------------------------------------
        # 4. OUTLET-LEVEL INVESTIGATION
        # --------------------------------------------------

        investigation_outlets = (
            q2_q3_analysis
            .sort_values(
                "Revenue_Change_Percent",
                ascending=True
            )
            .head(5)
        )

        # --------------------------------------------------
        # 5. BUILD OUTPUT
        # --------------------------------------------------

        lines = []

        lines.append(
            "## CUSTOMER / OUTLET DIAGNOSIS"
        )

        lines.append(
            f"{highest_contribution_type['Outlet_Type']} "
            f"is the largest revenue-contributing outlet type, "
            f"generating "
            f"₹{highest_contribution_type['Revenue']:,.2f} "
            f"and "
            f"{highest_contribution_type['Revenue_Contribution_Percent']:.2f}% "
            f"of total outlet revenue."
        )

        if largest_type_decline is not None:

            lines.append(
                f"The largest outlet-type revenue decline "
                f"from Q2 to Q3 was recorded by "
                f"{largest_type_decline['Outlet_Type']}, "
                f"with revenue changing by "
                f"{largest_type_decline['Revenue_Change_Percent']:.2f}%."
            )

        # --------------------------------------------------
        # KEY FINDINGS
        # --------------------------------------------------

        lines.append("")
        lines.append(
            "## KEY OUTLET FINDINGS"
        )

        lines.append(
            f"1. {highest_revenue_type['Outlet_Type']} "
            f"generated the highest revenue at "
            f"₹{highest_revenue_type['Revenue']:,.2f}."
        )

        lines.append(
            f"2. {highest_units_type['Outlet_Type']} "
            f"recorded the highest unit volume at "
            f"{highest_units_type['Units_Sold']:,.0f} units."
        )

        if priority_types is not None:

            for i, (_, row) in enumerate(
                priority_types.iterrows(),
                start=3
            ):

                lines.append(
                    f"{i}. {row['Outlet_Type']} recorded a "
                    f"{row['Revenue_Change_Percent']:.2f}% "
                    f"revenue change from Q2 to Q3 and a "
                    f"{row['Units_Change_Percent']:.2f}% "
                    f"change in units."
                )

        # --------------------------------------------------
        # PRIORITY OUTLET TYPES
        # --------------------------------------------------

        lines.append("")
        lines.append(
            "## PRIORITY OUTLET TYPES"
        )

        if priority_types is not None:

            for i, (_, row) in enumerate(
                priority_types.iterrows(),
                start=1
            ):

                lines.append(
                    f"{i}. {row['Outlet_Type']} — "
                    f"Revenue change: "
                    f"{row['Revenue_Change_Percent']:.2f}%, "
                    f"Units change: "
                    f"{row['Units_Change_Percent']:.2f}%."
                )

        else:

            lines.append(
                "No outlet-type Q2-Q3 comparison is available."
            )

        # --------------------------------------------------
        # PRIORITY OUTLET TIERS
        # --------------------------------------------------

        lines.append("")
        lines.append(
            "## PRIORITY OUTLET TIERS"
        )

        for i, (_, row) in enumerate(
            tier_ranked.iterrows(),
            start=1
        ):

            lines.append(
                f"{i}. Tier {row['Tier']} — "
                f"Revenue contribution: "
                f"{row['Revenue_Contribution_Percent']:.2f}% "
                f"(Revenue: ₹{row['Revenue']:,.2f})."
            )

        # --------------------------------------------------
        # OUTLETS REQUIRING INVESTIGATION
        # --------------------------------------------------

        lines.append("")
        lines.append(
            "## OUTLETS REQUIRING INVESTIGATION"
        )

        for i, (_, row) in enumerate(
            investigation_outlets.iterrows(),
            start=1
        ):

            lines.append(
                f"{i}. {row['Outlet_ID']} "
                f"({row['Outlet_Type']}, "
                f"Tier {row['Tier']}) — "
                f"Revenue change: "
                f"{row['Revenue_Change_Percent']:.2f}%, "
                f"Units change: "
                f"{row['Units_Change_Percent']:.2f}%."
            )

        # --------------------------------------------------
        # MANAGEMENT INVESTIGATION AREAS
        # --------------------------------------------------

        lines.append("")
        lines.append(
            "## MANAGEMENT INVESTIGATION AREAS"
        )

        if largest_type_decline is not None:

            lines.append(
                f"1. Investigate the drivers behind the "
                f"{largest_type_decline['Outlet_Type']} "
                f"revenue decline of "
                f"{largest_type_decline['Revenue_Change_Percent']:.2f}%."
            )

        else:

            lines.append(
                "1. Investigate the drivers behind the "
                "observed outlet-type changes."
            )

        lines.append(
            "2. Investigate the specific outlets showing "
            "the largest Q2-to-Q3 revenue and unit declines."
        )

        lines.append(
            "3. Compare outlet-type and tier performance "
            "to identify where management investigation "
            "should be prioritized."
        )

        lines.append(
            "The available evidence identifies performance "
            "changes, but does not establish their underlying "
            "causes. The cause requires further investigation."
        )

        return "\n".join(lines)

    # ==================================================
    # 7. COMPLETE CUSTOMER / OUTLET ANALYSIS BUNDLE
    # ==================================================

    def run_analysis(
        self,
        city="Gurgaon",
        year=2026,
        top_n=10
    ):
        """
        Run all Customer/Outlet analyses and return one
        analysis bundle for the Orchestrator.
        """

        print(
            f"[Customer/Outlet Agent] "
            f"Running complete analysis for {city}, {year}..."
        )

        # --------------------------------------------------
        # Outlet type
        # --------------------------------------------------

        outlet_type_analysis = (
            self.analyze_outlet_types(city)
        )

        # --------------------------------------------------
        # Outlet tier
        # --------------------------------------------------

        outlet_tier_analysis = (
            self.analyze_outlet_tiers(city)
        )

        # --------------------------------------------------
        # Outlet-level performance
        # --------------------------------------------------

        outlet_analysis = (
            self.analyze_outlets(
                city,
                top_n=top_n
            )
        )

        # --------------------------------------------------
        # Outlet Q2 vs Q3
        # --------------------------------------------------

        outlet_q2_q3_analysis = (
            self.compare_outlets_q2_q3(
                city,
                year=year,
                top_n=top_n
            )
        )

        # --------------------------------------------------
        # Outlet type Q2 vs Q3
        # --------------------------------------------------

        outlet_type_q2_q3_analysis = (
            self.compare_outlet_types_q2_q3(
                city,
                year=year
            )
        )

        # --------------------------------------------------
        # Deterministic insight
        # --------------------------------------------------

        insight = self.generate_insight(
            outlet_type_analysis,
            outlet_tier_analysis,
            outlet_q2_q3_analysis,
            outlet_type_q2_q3_analysis,
        )

        return {
            "outlet_type_analysis": outlet_type_analysis,
            "outlet_tier_analysis": outlet_tier_analysis,
            "outlet_analysis": outlet_analysis,
            "outlet_q2_q3_analysis": outlet_q2_q3_analysis,
            "outlet_type_q2_q3_analysis": (
                outlet_type_q2_q3_analysis
            ),
            "insight": insight,
        }


# ======================================================
# MAIN TEST
# ======================================================

if __name__ == "__main__":

    agent = CustomerOutletAgent()

    city = "Gurgaon"
    year = 2026

    print("\n" + "=" * 60)
    print("CUSTOMER / OUTLET AGENT")
    print("=" * 60)

    # --------------------------------------------------
    # OUTLET TYPE PERFORMANCE
    # --------------------------------------------------

    print(
        "\n===== OUTLET TYPE PERFORMANCE ====="
    )

    outlet_types = (
        agent.analyze_outlet_types(city)
    )

    print(outlet_types)

    # --------------------------------------------------
    # OUTLET TIER PERFORMANCE
    # --------------------------------------------------

    print(
        "\n===== OUTLET TIER PERFORMANCE ====="
    )

    tiers = (
        agent.analyze_outlet_tiers(city)
    )

    print(tiers)

    # --------------------------------------------------
    # TOP / BOTTOM OUTLETS
    # --------------------------------------------------

    print(
        "\n===== TOP / BOTTOM OUTLETS ====="
    )

    outlets = (
        agent.analyze_outlets(
            city,
            top_n=10
        )
    )

    print("\nTop Outlets:")
    print(
        outlets["Top_Outlets"]
    )

    print("\nBottom Outlets:")
    print(
        outlets["Bottom_Outlets"]
    )

    # --------------------------------------------------
    # OUTLET Q2 VS Q3
    # --------------------------------------------------

    print(
        "\n===== OUTLET Q2 VS Q3 ====="
    )

    q2_q3 = (
        agent.compare_outlets_q2_q3(
            city,
            year=year,
            top_n=10
        )
    )

    print(q2_q3)

    # --------------------------------------------------
    # OUTLET TYPE Q2 VS Q3
    # --------------------------------------------------

    print(
        "\n===== OUTLET TYPE Q2 VS Q3 ====="
    )

    outlet_type_q2_q3 = (
        agent.compare_outlet_types_q2_q3(
            city,
            year=year
        )
    )

    print(outlet_type_q2_q3)

    # --------------------------------------------------
    # OUTLET INSIGHT
    # --------------------------------------------------

    print(
        "\n===== OUTLET INSIGHT ====="
    )

    insight = agent.generate_insight(
        outlet_types,
        tiers,
        q2_q3,
        outlet_type_q2_q3
    )

    print(insight)