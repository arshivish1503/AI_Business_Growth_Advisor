import os

# Ollama is optional.
# The application can run without it on Streamlit Cloud.
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    ollama = None
    OLLAMA_AVAILABLE = False


class StrategyAgent:

    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

    # =========================================================
    # HELPER: Convert DataFrame / list / dictionary to records
    # =========================================================

    def _to_records(self, data):

        if data is None:
            return []

        # Pandas DataFrame
        if hasattr(data, "to_dict"):
            try:
                return data.to_dict(orient="records")
            except Exception:
                pass

        # List
        if isinstance(data, list):
            return data

        # Tuple
        if isinstance(data, tuple):
            return list(data)

        # Single dictionary
        if isinstance(data, dict):
            return [data]

        return []

    # =========================================================
    # OPTIONAL OLLAMA DIAGNOSIS
    # =========================================================

    def _generate_llm_diagnosis(self, prompt, fallback_diagnosis):

        """
        Try Ollama first.

        LOCAL:
            Ollama available -> Llama 3.2:3b generates diagnosis.

        CLOUD:
            Ollama unavailable -> deterministic fallback diagnosis.

        This allows the same application to work both locally
        and on Streamlit Cloud without requiring an external API.
        """

        # -----------------------------------------------------
        # Try Ollama
        # -----------------------------------------------------

        if OLLAMA_AVAILABLE:

            try:

                print(
                    "[Strategy Agent] Attempting Ollama "
                    f"with model {self.model}..."
                )

                response = ollama.chat(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    options={
                        "num_predict": 300,
                        "temperature": 0.1
                    },
                    stream=False
                )

                executive_diagnosis = (
                    response["message"]["content"].strip()
                )

                if executive_diagnosis:

                    print(
                        "[Strategy Agent] Ollama diagnosis "
                        "generated successfully."
                    )

                    return executive_diagnosis

            except Exception as e:

                print(
                    "[Strategy Agent] Ollama unavailable. "
                    f"Using fallback diagnosis. Error: {e}"
                )

        else:

            print(
                "[Strategy Agent] Ollama package unavailable. "
                "Using fallback diagnosis."
            )

        # -----------------------------------------------------
        # Cloud / fallback mode
        # -----------------------------------------------------

        return fallback_diagnosis

    # =========================================================
    # MAIN STRATEGY FUNCTION
    # =========================================================

    def generate_strategy(
        self,
        city_analysis,
        q2_q3_analysis,
        sku_analysis,
        promotion_analysis,
        competitor_analysis,
        customer_outlet_analysis=None
    ):

        print("\n[Strategy Agent] Preparing evidence...")

        # =====================================================
        # 1. OVERALL PERFORMANCE
        # =====================================================

        revenue_change = float(
            q2_q3_analysis.get(
                "Revenue_Change_Percent",
                0
            ) or 0
        )

        units_change = float(
            q2_q3_analysis.get(
                "Units_Change_Percent",
                0
            ) or 0
        )

        availability_change = float(
            q2_q3_analysis.get(
                "Availability_Change_pp",
                0
            ) or 0
        )

        # =====================================================
        # 2. SKU ANALYSIS
        # =====================================================

        sku_list = self._to_records(
            sku_analysis.get(
                "SKUs_With_Largest_Revenue_Decline",
                []
            )
        )

        availability_skus = []
        investigation_skus = []

        for sku in sku_list:

            sku_id = sku.get(
                "SKU_ID",
                "Unknown"
            )

            revenue = float(
                sku.get(
                    "Revenue_Change_Percent",
                    0
                ) or 0
            )

            units = float(
                sku.get(
                    "Units_Change_Percent",
                    0
                ) or 0
            )

            availability = float(
                sku.get(
                    "Availability_Change_pp",
                    0
                ) or 0
            )

            record = {
                "SKU_ID": sku_id,
                "Revenue_Change_Percent": revenue,
                "Units_Change_Percent": units,
                "Availability_Change_pp": availability
            }

            # Strong availability signal
            if (
                revenue <= -40
                and units <= -40
                and availability <= -10
            ):

                availability_skus.append(record)

            # Sales decline without major
            # availability deterioration
            elif (
                revenue <= -40
                and units <= -40
                and availability > -10
            ):

                investigation_skus.append(record)

        # =====================================================
        # 3. PROMOTION ANALYSIS
        # =====================================================

        q3_promotion = promotion_analysis.get(
            "Q3",
            {}
        )

        q3_promoted_revenue = float(
            q3_promotion.get(
                "Promoted_Revenue",
                0
            ) or 0
        )

        q3_promotion_share = float(
            q3_promotion.get(
                "Promotion_Revenue_Share_Percent",
                0
            ) or 0
        )

        # =====================================================
        # 4. COMPETITOR ANALYSIS
        # =====================================================

        competitor_quarters = self._to_records(
            competitor_analysis.get(
                "Quarterly_Summary",
                []
            )
        )

        q2_price = None
        q3_price = None

        q2_comp_availability = None
        q3_comp_availability = None

        for quarter in competitor_quarters:

            quarter_number = quarter.get(
                "Quarter"
            )

            if quarter_number == 2:

                q2_price = quarter.get(
                    "Average_Price"
                )

                q2_comp_availability = quarter.get(
                    "Average_Availability"
                )

            elif quarter_number == 3:

                q3_price = quarter.get(
                    "Average_Price"
                )

                q3_comp_availability = quarter.get(
                    "Average_Availability"
                )

        # =====================================================
        # 5. CUSTOMER / OUTLET ANALYSIS
        # =====================================================

        if customer_outlet_analysis is None:
            customer_outlet_analysis = {}

        # Exact keys returned by CustomerOutletAgent
        outlet_type_analysis = self._to_records(
            customer_outlet_analysis.get(
                "outlet_type_analysis",
                []
            )
        )

        outlet_tier_analysis = self._to_records(
            customer_outlet_analysis.get(
                "outlet_tier_analysis",
                []
            )
        )

        outlet_analysis = self._to_records(
            customer_outlet_analysis.get(
                "outlet_analysis",
                []
            )
        )

        outlet_q2_q3_analysis = self._to_records(
            customer_outlet_analysis.get(
                "outlet_q2_q3_analysis",
                []
            )
        )

        outlet_type_q2_q3_analysis = self._to_records(
            customer_outlet_analysis.get(
                "outlet_type_q2_q3_analysis",
                []
            )
        )

        customer_outlet_insight = (
            customer_outlet_analysis.get(
                "insight",
                ""
            )
        )

        # =====================================================
        # 6. IMPORTANT NORMALIZATION
        # =====================================================

        # The Customer/Outlet Agent may return percentage
        # columns as strings. Convert them safely.

        def get_number(record, key):

            value = record.get(
                key,
                0
            )

            try:
                return float(value)

            except (
                ValueError,
                TypeError
            ):

                return 0.0

        # =====================================================
        # 7. OUTLET TYPE PRIORITIES
        # =====================================================

        top_outlet_types = sorted(
            outlet_type_q2_q3_analysis,
            key=lambda x: get_number(
                x,
                "Revenue_Change_Percent"
            )
        )[:3]

        # =====================================================
        # 8. OUTLET-LEVEL PRIORITIES
        # =====================================================

        top_outlets = sorted(
            outlet_q2_q3_analysis,
            key=lambda x: get_number(
                x,
                "Revenue_Change_Percent"
            )
        )[:5]

        # =====================================================
        # 9. FORMATTING FUNCTIONS
        # =====================================================

        def format_sku(sku):

            return (
                f"{sku.get('SKU_ID', 'Unknown')}: "
                f"Revenue "
                f"{get_number(sku, 'Revenue_Change_Percent'):.2f}%, "
                f"Units "
                f"{get_number(sku, 'Units_Change_Percent'):.2f}%, "
                f"Availability "
                f"{get_number(sku, 'Availability_Change_pp'):.2f} pp"
            )

        def format_outlet_type(outlet):

            return (
                f"{outlet.get('Outlet_Type', 'Unknown')}: "
                f"Revenue "
                f"{get_number(outlet, 'Revenue_Change_Percent'):.2f}%, "
                f"Units "
                f"{get_number(outlet, 'Units_Change_Percent'):.2f}%"
            )

        def format_outlet(outlet):

            return (
                f"{outlet.get('Outlet_ID', 'Unknown')} "
                f"({outlet.get('Outlet_Type', 'Unknown')}, "
                f"Tier {outlet.get('Tier', 'Unknown')}): "
                f"Revenue "
                f"{get_number(outlet, 'Revenue_Change_Percent'):.2f}%, "
                f"Units "
                f"{get_number(outlet, 'Units_Change_Percent'):.2f}%"
            )

        # =====================================================
        # 10. SKU TEXT
        # =====================================================

        availability_lines = []

        for sku in availability_skus:

            availability_lines.append(
                "- " + format_sku(sku)
            )

        if availability_lines:

            availability_section = "\n".join(
                availability_lines
            )

        else:

            availability_section = (
                "- No availability-focused SKUs identified."
            )

        investigation_lines = []

        for sku in investigation_skus:

            investigation_lines.append(
                "- " + format_sku(sku)
            )

        if investigation_lines:

            investigation_section = "\n".join(
                investigation_lines
            )

        else:

            investigation_section = (
                "- No investigation-focused SKUs identified."
            )

        # =====================================================
        # 11. OUTLET TYPE TEXT
        # =====================================================

        outlet_type_lines = []

        for outlet in top_outlet_types:

            outlet_type_lines.append(
                "- " + format_outlet_type(outlet)
            )

        if outlet_type_lines:

            outlet_type_section = "\n".join(
                outlet_type_lines
            )

        else:

            outlet_type_section = (
                "- No outlet-type Q2-Q3 data available."
            )

        # =====================================================
        # 12. OUTLET TEXT
        # =====================================================

        outlet_lines = []

        for outlet in top_outlets:

            outlet_lines.append(
                "- " + format_outlet(outlet)
            )

        if outlet_lines:

            outlet_section = "\n".join(
                outlet_lines
            )

        else:

            outlet_section = (
                "- No outlet-level Q2-Q3 data available."
            )

        # =====================================================
        # 13. DEBUG COUNTS
        # =====================================================

        print(
            "[Strategy Agent] "
            f"Outlet type Q2-Q3 records: "
            f"{len(outlet_type_q2_q3_analysis)}"
        )

        print(
            "[Strategy Agent] "
            f"Outlet Q2-Q3 records: "
            f"{len(outlet_q2_q3_analysis)}"
        )

        print(
            "[Strategy Agent] "
            f"Top outlet types selected: "
            f"{len(top_outlet_types)}"
        )

        print(
            "[Strategy Agent] "
            f"Top outlets selected: "
            f"{len(top_outlets)}"
        )

        # =====================================================
        # 14. EXECUTIVE DIAGNOSIS
        # =====================================================

        executive_evidence = f"""
OVERALL PERFORMANCE

Revenue Q2 to Q3:
{revenue_change:.2f}%

Units Q2 to Q3:
{units_change:.2f}%

Availability Q2 to Q3:
{availability_change:.2f} percentage points


AVAILABILITY-FOCUSED SKUS

{availability_section}


INVESTIGATION-FOCUSED SKUS

{investigation_section}


PRIORITY OUTLET TYPES

{outlet_type_section}


PRIORITY OUTLETS

{outlet_section}


PROMOTION EVIDENCE

Q3 promoted revenue:
₹{q3_promoted_revenue:,.2f}

Q3 promotion revenue share:
{q3_promotion_share:.3f}%


COMPETITOR EVIDENCE

Q2 competitor average price:
{q2_price}

Q3 competitor average price:
{q3_price}

Q2 competitor average availability:
{q2_comp_availability}

Q3 competitor average availability:
{q3_comp_availability}
"""

        prompt = f"""
You are a senior FMCG strategy manager.

Write a concise executive diagnosis using
ONLY the verified evidence below.

{executive_evidence}

Rules:

1. Do not invent numbers.
2. Do not invent outlet names.
3. Do not invent outlet types.
4. Do not invent causes.
5. Do not claim availability caused revenue decline.
6. Do not claim competitor pricing caused our decline.
7. Do not recommend promotions as the primary solution.
8. Use exact numbers from the evidence.
9. Mention specific outlet types and SKUs.
10. Keep the response to 4 sentences.
"""

        print(
            "[Strategy Agent] Generating executive diagnosis..."
        )

        # =====================================================
        # CLOUD-SAFE FALLBACK DIAGNOSIS
        # =====================================================

        fallback_diagnosis = (
            f"Revenue declined {revenue_change:.2f}% from Q2 to Q3, "
            f"while units declined {units_change:.2f}% and overall "
            f"availability changed by {availability_change:.2f} "
            f"percentage points. "
        )

        if availability_skus:

            fallback_diagnosis += (
                "The strongest availability-related SKU signals "
                "are "
                + ", ".join(
                    sku["SKU_ID"]
                    for sku in availability_skus[:3]
                )
                + ". "
            )

        if investigation_skus:

            fallback_diagnosis += (
                "Additional investigation is required for "
                + ", ".join(
                    sku["SKU_ID"]
                    for sku in investigation_skus[:3]
                )
                + ", where sales declined without major "
                "availability deterioration. "
            )

        if top_outlet_types:

            fallback_diagnosis += (
                "At the outlet-type level, the largest observed "
                "decline is in "
                + top_outlet_types[0].get(
                    "Outlet_Type",
                    "the highest-priority outlet type"
                )
                + "."
            )

        # Try Ollama, otherwise use fallback
        executive_diagnosis = self._generate_llm_diagnosis(
            prompt,
            fallback_diagnosis
        )

        # =====================================================
        # 15. DETERMINISTIC ACTIONS
        # =====================================================

        actions = []

        # -----------------------------------------------------
        # ACTION 1 — SKU AVAILABILITY
        # -----------------------------------------------------

        if availability_skus:

            sku = availability_skus[0]

            actions.append({
                "Action":
                    f"Investigate and recover "
                    f"{sku['SKU_ID']} availability",

                "Evidence":
                    format_sku(sku),

                "Why":
                    "The SKU shows a major sales decline "
                    "alongside a major availability deterioration.",

                "Impact":
                    "Potential recovery of availability "
                    "and associated sales performance.",

                "Priority":
                    "P1"
            })

        # -----------------------------------------------------
        # ACTION 2 — OUTLET TYPE
        # -----------------------------------------------------

        if top_outlet_types:

            outlet = top_outlet_types[0]

            outlet_type = outlet.get(
                "Outlet_Type",
                "Unknown"
            )

            actions.append({
                "Action":
                    f"Investigate {outlet_type} performance",

                "Evidence":
                    format_outlet_type(outlet),

                "Why":
                    "It has the largest observed "
                    "outlet-type revenue decline.",

                "Impact":
                    "Identify the factors requiring "
                    "commercial or operational investigation.",

                "Priority":
                    "P1"
            })

        # -----------------------------------------------------
        # ACTION 3 — OUTLET
        # -----------------------------------------------------

        if top_outlets:

            outlet = top_outlets[0]

            actions.append({
                "Action":
                    f"Investigate "
                    f"{outlet.get('Outlet_ID', 'Unknown')} performance",

                "Evidence":
                    format_outlet(outlet),

                "Why":
                    "It has the largest observed "
                    "outlet-level revenue decline.",

                "Impact":
                    "Identify the reason for the "
                    "performance deterioration.",

                "Priority":
                    "P1"
            })

        # -----------------------------------------------------
        # ACTION 4 — SKU INVESTIGATION
        # -----------------------------------------------------

        if investigation_skus:

            sku = investigation_skus[0]

            actions.append({
                "Action":
                    f"Investigate "
                    f"{sku['SKU_ID']} sales decline",

                "Evidence":
                    format_sku(sku),

                "Why":
                    "Revenue and units declined substantially "
                    "without a major availability deterioration.",

                "Impact":
                    "Identify the factors behind the sales decline.",

                "Priority":
                    "P2"
            })

        # -----------------------------------------------------
        # ACTION 5 — COMPETITOR
        # -----------------------------------------------------

        if (
            q2_price is not None
            and q3_price is not None
        ):

            actions.append({
                "Action":
                    "Monitor competitor pricing and availability",

                "Evidence":
                    f"Competitor price Q2: "
                    f"{float(q2_price):.2f}; "
                    f"Q3: "
                    f"{float(q3_price):.2f}",

                "Why":
                    "The change is a potential "
                    "competitive-pressure signal.",

                "Impact":
                    "Improve market understanding before "
                    "making pricing decisions.",

                "Priority":
                    "P3"
            })

        # =====================================================
        # 16. FINAL OUTPUT
        # =====================================================

        strategy = []

        # Executive diagnosis
        strategy.append(
            "## 1. EXECUTIVE DIAGNOSIS\n\n"
            + executive_diagnosis.strip()
        )

        # Top actions
        strategy.append(
            "\n## 2. TOP 5 ACTIONS\n"
        )

        for i, action in enumerate(
            actions[:5],
            start=1
        ):

            strategy.append(
                f"""
### Action {i}: {action['Action']}

**Evidence:** {action['Evidence']}

**Why it matters:** {action['Why']}

**Expected impact:** {action['Impact']}

**Priority:** {action['Priority']}
"""
            )

        # SKU priorities
        strategy.append(
            f"""
## 3. SKU PRIORITIES

### A. Availability Recovery

{availability_section}

### B. Further Investigation

{investigation_section}
"""
        )

        # Customer / outlet priorities
        strategy.append(
            f"""
## 4. CUSTOMER / OUTLET PRIORITIES

### A. Priority Outlet Types

{outlet_type_section}

### B. Priority Outlets

{outlet_section}
"""
        )

        # Warnings
        strategy.append(
            """
## 5. WHAT MANAGEMENT SHOULD NOT DO

1. Do not claim that availability caused the revenue decline.

2. Do not claim that competitor pricing caused the sales decline.

3. Do not increase promotions as the primary response when promotion-linked revenue is negligible.
"""
        )

        # 30-day plan
        strategy.append(
            """
## 6. 30-DAY ACTION PLAN

**Week 1:** Validate the highest-priority SKU and outlet-level declines.

**Week 2:** Investigate the underlying drivers for the priority SKU and outlet types.

**Week 3:** Review competitor signals and evaluate findings from SKU and outlet investigations.

**Week 4:** Implement evidence-supported corrective actions and establish KPI monitoring.
"""
        )

        # Next question
        strategy.append(
            """
## 7. NEXT MANAGEMENT QUESTION

What operational or commercial factors explain the largest SKU and outlet-level declines?
"""
        )

        print(
            "[Strategy Agent] Strategy generated successfully."
        )

        return "\n".join(strategy)