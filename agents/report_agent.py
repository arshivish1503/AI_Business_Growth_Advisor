import re


class ReportAgent:

    def __init__(self):
        print("[Report Agent] Initialized successfully.")

    # ---------------------------------------------------------
    # HELPER FUNCTIONS
    # ---------------------------------------------------------

    def _safe_float(self, value, default=None):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _format_currency(self, value):
        try:
            return f"₹{float(value):,.2f}"
        except (TypeError, ValueError):
            return str(value)

    def _format_number(self, value):
        try:
            return f"{int(float(value)):,}"
        except (TypeError, ValueError):
            return str(value)

    # ---------------------------------------------------------
    # EXTRACT SECTION
    # ---------------------------------------------------------

    def _extract_section(self, strategy_text, heading):
        """
        Extract a section from the Strategy Agent output.
        The section's original ## heading is removed because
        the Report Agent creates its own report headings.
        """

        if not isinstance(strategy_text, str):
            return ""

        pattern = (
            rf"##\s*{re.escape(heading)}.*?"
            rf"(?=\n##\s|\Z)"
        )

        match = re.search(
            pattern,
            strategy_text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if not match:
            return ""

        section = match.group(0).strip()

        # Remove the first markdown heading
        section = re.sub(
            r"^##\s*[^\n]+\n?",
            "",
            section,
            count=1
        ).strip()

        return section

    # ---------------------------------------------------------
    # EXECUTIVE SUMMARY
    # ---------------------------------------------------------

    def generate_executive_summary(
        self,
        city_analysis,
        q2_q3_analysis,
        strategy
    ):

        city_analysis = city_analysis or {}
        q2_q3_analysis = q2_q3_analysis or {}

        city = city_analysis.get(
            "city",
            "Selected City"
        )

        revenue_change = self._safe_float(
            q2_q3_analysis.get(
                "Revenue_Change_Percent"
            )
        )

        units_change = self._safe_float(
            q2_q3_analysis.get(
                "Units_Change_Percent"
            )
        )

        availability_change = self._safe_float(
            q2_q3_analysis.get(
                "Availability_Change_pp"
            )
        )

        parts = []

        parts.append(
            f"{city} remains an important market, but the latest "
            f"quarter shows a deterioration in business performance."
        )

        if revenue_change is not None:
            parts.append(
                f"Revenue changed by {revenue_change:.2f}% "
                f"from Q2 to Q3."
            )

        if units_change is not None:
            parts.append(
                f"Units changed by {units_change:.2f}% "
                f"from Q2 to Q3."
            )

        if availability_change is not None:
            parts.append(
                f"Average availability changed by "
                f"{availability_change:.2f} percentage points."
            )

        parts.append(
            "The Strategy Agent identified priority SKUs, "
            "outlet types and individual outlets requiring "
            "management investigation."
        )

        return " ".join(parts)

    # ---------------------------------------------------------
    # BUSINESS PERFORMANCE
    # ---------------------------------------------------------

    def generate_business_performance(
        self,
        city_analysis,
        q2_q3_analysis
    ):

        city_analysis = city_analysis or {}
        q2_q3_analysis = q2_q3_analysis or {}

        report = []

        report.append("### City Performance")

        if city_analysis.get("city") is not None:
            report.append(
                f"- City: {city_analysis['city']}"
            )

        if city_analysis.get("Total_Revenue") is not None:
            report.append(
                f"- Total Revenue: "
                f"{self._format_currency(city_analysis['Total_Revenue'])}"
            )

        if city_analysis.get("Total_Units") is not None:
            report.append(
                f"- Total Units: "
                f"{self._format_number(city_analysis['Total_Units'])}"
            )

        if city_analysis.get("Average_Availability") is not None:
            report.append(
                f"- Average Availability: "
                f"{float(city_analysis['Average_Availability']):.2f}%"
            )

        if city_analysis.get("Revenue_Rank") is not None:
            report.append(
                f"- Revenue Rank: "
                f"#{city_analysis['Revenue_Rank']}"
            )

        report.append("")
        report.append("### Q2 vs Q3")

        if q2_q3_analysis.get("Q2_Revenue") is not None:
            report.append(
                f"- Q2 Revenue: "
                f"{self._format_currency(q2_q3_analysis['Q2_Revenue'])}"
            )

        if q2_q3_analysis.get("Q3_Revenue") is not None:
            report.append(
                f"- Q3 Revenue: "
                f"{self._format_currency(q2_q3_analysis['Q3_Revenue'])}"
            )

        if q2_q3_analysis.get(
            "Revenue_Change_Percent"
        ) is not None:

            report.append(
                f"- Revenue Change: "
                f"{float(q2_q3_analysis['Revenue_Change_Percent']):.2f}%"
            )

        if q2_q3_analysis.get(
            "Units_Change_Percent"
        ) is not None:

            report.append(
                f"- Units Change: "
                f"{float(q2_q3_analysis['Units_Change_Percent']):.2f}%"
            )

        if q2_q3_analysis.get(
            "Availability_Change_pp"
        ) is not None:

            report.append(
                f"- Availability Change: "
                f"{float(q2_q3_analysis['Availability_Change_pp']):.2f} pp"
            )

        return "\n".join(report)

    # ---------------------------------------------------------
    # SKU SECTION
    # ---------------------------------------------------------

    def generate_sku_section(self, strategy):

        if not isinstance(strategy, str):
            return (
                "No SKU priority information available."
            )

        section = self._extract_section(
            strategy,
            "3. SKU PRIORITIES"
        )

        if section:
            return section

        return (
            "No SKU priority information was generated."
        )

    # ---------------------------------------------------------
    # CUSTOMER / OUTLET SECTION
    # ---------------------------------------------------------

    def generate_outlet_section(self, strategy):

        if not isinstance(strategy, str):
            return (
                "No customer/outlet priority information available."
            )

        section = self._extract_section(
            strategy,
            "4. CUSTOMER / OUTLET PRIORITIES"
        )

        if section:
            return section

        return (
            "No customer/outlet priority information was generated."
        )

    # ---------------------------------------------------------
    # MARKET INTELLIGENCE
    # ---------------------------------------------------------

    def generate_market_section(
        self,
        market_intelligence
    ):

        if not isinstance(
            market_intelligence,
            dict
        ):
            return (
                "No market intelligence information available."
            )

        report = []

        city_analysis = market_intelligence.get(
            "city_analysis",
            {}
        )

        q2_q3 = market_intelligence.get(
            "q2_q3_analysis",
            {}
        )

        signals = market_intelligence.get(
            "market_signals",
            []
        )

        report.append(
            "### Competitive Market Snapshot"
        )

        if city_analysis.get(
            "average_competitor_price"
        ) is not None:

            report.append(
                f"- Average Competitor Price: "
                f"₹{float(city_analysis['average_competitor_price']):.2f}"
            )

        if city_analysis.get(
            "average_competitor_availability"
        ) is not None:

            report.append(
                f"- Average Competitor Availability: "
                f"{float(city_analysis['average_competitor_availability']):.2f}%"
            )

        if city_analysis.get(
            "promotion_observations"
        ) is not None:

            report.append(
                f"- Promotion Observations: "
                f"{city_analysis['promotion_observations']}"
            )

        if q2_q3:

            report.append("")
            report.append(
                "### Q2 vs Q3 Competitive Signals"
            )

            if q2_q3.get(
                "Q2_Average_Price"
            ) is not None:

                report.append(
                    f"- Q2 Average Competitor Price: "
                    f"₹{float(q2_q3['Q2_Average_Price']):.2f}"
                )

            if q2_q3.get(
                "Q3_Average_Price"
            ) is not None:

                report.append(
                    f"- Q3 Average Competitor Price: "
                    f"₹{float(q2_q3['Q3_Average_Price']):.2f}"
                )

            if q2_q3.get(
                "Price_Change_Percent"
            ) is not None:

                report.append(
                    f"- Competitor Price Change: "
                    f"{float(q2_q3['Price_Change_Percent']):.2f}%"
                )

            if q2_q3.get(
                "Q2_Average_Availability"
            ) is not None:

                report.append(
                    f"- Q2 Competitor Availability: "
                    f"{float(q2_q3['Q2_Average_Availability']):.2f}%"
                )

            if q2_q3.get(
                "Q3_Average_Availability"
            ) is not None:

                report.append(
                    f"- Q3 Competitor Availability: "
                    f"{float(q2_q3['Q3_Average_Availability']):.2f}%"
                )

            if q2_q3.get(
                "Availability_Change_pp"
            ) is not None:

                report.append(
                    f"- Competitor Availability Change: "
                    f"{float(q2_q3['Availability_Change_pp']):.2f} pp"
                )

        if signals:

            report.append("")
            report.append(
                "### Market Signals"
            )

            for signal in signals:
                report.append(
                    f"- {signal}"
                )

        return "\n".join(report)

    # ---------------------------------------------------------
    # RECOMMENDED ACTIONS
    # ---------------------------------------------------------

    def generate_action_section(self, strategy):

        if not isinstance(strategy, str):
            return (
                "No strategic actions available."
            )

        section = self._extract_section(
            strategy,
            "2. TOP 5 ACTIONS"
        )

        if section:
            return section

        return (
            "No strategic actions were generated."
        )

    # ---------------------------------------------------------
    # 30-DAY ACTION PLAN
    # ---------------------------------------------------------

    def generate_30_day_plan(self, strategy):

        if isinstance(strategy, str):

            section = self._extract_section(
                strategy,
                "6. 30-DAY ACTION PLAN"
            )

            if section:
                return section

        return """
### Week 1
Validate the highest-priority SKU and outlet-level declines.

### Week 2
Investigate the underlying operational and commercial drivers.

### Week 3
Review competitive signals and evaluate findings from SKU and outlet investigations.

### Week 4
Implement evidence-supported corrective actions and establish KPI monitoring.
""".strip()

    # ---------------------------------------------------------
    # MANAGEMENT FOCUS
    # ---------------------------------------------------------

    def generate_management_focus(self, strategy):

        if isinstance(strategy, str):

            section = self._extract_section(
                strategy,
                "7. NEXT MANAGEMENT QUESTION"
            )

            if section:
                return section

        return (
            "Management should prioritize evidence-backed "
            "investigation of the largest SKU and outlet declines "
            "before making major pricing, promotion or distribution decisions."
        )

    # ---------------------------------------------------------
    # COMPLETE REPORT
    # ---------------------------------------------------------

    def generate_report(
        self,
        city_analysis,
        q2_q3_analysis,
        strategy,
        market_intelligence=None
    ):

        print(
            "[Report Agent] Generating management report..."
        )

        report = []

        report.append("=" * 70)
        report.append(
            "AI BUSINESS GROWTH ADVISOR"
        )
        report.append(
            "MANAGEMENT DECISION REPORT"
        )
        report.append("=" * 70)

        # 1. EXECUTIVE SUMMARY
        report.append("")
        report.append(
            "## 1. EXECUTIVE SUMMARY"
        )
        report.append("")

        report.append(
            self.generate_executive_summary(
                city_analysis,
                q2_q3_analysis,
                strategy
            )
        )

        # 2. BUSINESS PERFORMANCE
        report.append("")
        report.append(
            "## 2. BUSINESS PERFORMANCE"
        )
        report.append("")

        report.append(
            self.generate_business_performance(
                city_analysis,
                q2_q3_analysis
            )
        )

        # 3. SKU PRIORITIES
        report.append("")
        report.append(
            "## 3. SKU PRIORITIES"
        )
        report.append("")

        report.append(
            self.generate_sku_section(
                strategy
            )
        )

        # 4. CUSTOMER / OUTLET PRIORITIES
        report.append("")
        report.append(
            "## 4. CUSTOMER / OUTLET PRIORITIES"
        )
        report.append("")

        report.append(
            self.generate_outlet_section(
                strategy
            )
        )

        # 5. MARKET INTELLIGENCE
        report.append("")
        report.append(
            "## 5. MARKET INTELLIGENCE"
        )
        report.append("")

        report.append(
            self.generate_market_section(
                market_intelligence
            )
        )

        # 6. RECOMMENDED ACTIONS
        report.append("")
        report.append(
            "## 6. RECOMMENDED ACTIONS"
        )
        report.append("")

        report.append(
            self.generate_action_section(
                strategy
            )
        )

        # 7. 30-DAY ACTION PLAN
        report.append("")
        report.append(
            "## 7. 30-DAY ACTION PLAN"
        )
        report.append("")

        report.append(
            self.generate_30_day_plan(
                strategy
            )
        )

        # 8. MANAGEMENT FOCUS
        report.append("")
        report.append(
            "## 8. MANAGEMENT FOCUS"
        )
        report.append("")

        report.append(
            self.generate_management_focus(
                strategy
            )
        )

        report.append("")
        report.append("=" * 70)

        return "\n".join(report)


# =========================================================
# STANDALONE TEST
# =========================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("REPORT AGENT STANDALONE TEST")
    print("=" * 70)

    city_analysis = {
        "city": "Gurgaon",
        "Total_Revenue": 1825754.07,
        "Total_Units": 49674,
        "Average_Availability": 90.47,
        "Revenue_Rank": 1
    }

    q2_q3_analysis = {
        "Q2_Revenue": 247844.62,
        "Q3_Revenue": 181130.78,
        "Revenue_Change_Percent": -26.92,
        "Units_Change_Percent": -15.15,
        "Availability_Change_pp": -2.30
    }

    strategy = """
## 1. EXECUTIVE DIAGNOSIS

Gurgaon experienced a decline in revenue, units and availability from Q2 to Q3.

## 2. TOP 5 ACTIONS

### Action 1: Investigate and recover SKU005 availability

**Evidence:** SKU005: Revenue -74.02%, Units -73.94%, Availability -24.33 pp

**Why it matters:** The SKU shows a major sales decline alongside a major availability deterioration.

**Priority:** P1

### Action 2: Investigate Eating & Dining performance

**Evidence:** Eating & Dining: Revenue -47.75%, Units -28.35%

**Why it matters:** It has the largest observed outlet-type revenue decline.

**Priority:** P1

## 3. SKU PRIORITIES

### A. Availability Recovery

- SKU005: Revenue -74.02%, Units -73.94%, Availability -24.33 pp
- SKU004: Revenue -72.86%, Units -72.86%, Availability -18.82 pp

### B. Further Investigation

- SKU012: Revenue -63.91%, Units -63.20%, Availability 2.43 pp

## 4. CUSTOMER / OUTLET PRIORITIES

### A. Priority Outlet Types

- Eating & Dining: Revenue -47.75%, Units -28.35%

### B. Priority Outlets

- OUT0659 (Supermarket, Tier B): Revenue -88.34%, Units -86.41%

## 6. 30-DAY ACTION PLAN

**Week 1:** Validate the highest-priority SKU and outlet-level declines.

**Week 2:** Investigate the underlying drivers.

**Week 3:** Review competitive signals.

**Week 4:** Implement evidence-supported corrective actions.

## 7. NEXT MANAGEMENT QUESTION

What operational or commercial factors explain the largest SKU and outlet-level declines?
"""

    market_intelligence = {
        "city_analysis": {
            "average_competitor_price": 46.12,
            "average_competitor_availability": 88.80,
            "promotion_observations": 50
        },

        "q2_q3_analysis": {
            "Q2_Average_Price": 56.75,
            "Q3_Average_Price": 44.36,
            "Price_Change": -12.39,
            "Price_Change_Percent": -21.83,
            "Q2_Average_Availability": 86.65,
            "Q3_Average_Availability": 92.70,
            "Availability_Change_pp": 6.05
        },

        "market_signals": [
            "Competitor average price declined materially from Q2 to Q3.",
            "Competitor availability improved from Q2 to Q3.",
            "These market signals indicate competitive changes but do not establish that competitor activity caused the company's sales decline."
        ]
    }

    agent = ReportAgent()

    final_report = agent.generate_report(
        city_analysis=city_analysis,
        q2_q3_analysis=q2_q3_analysis,
        strategy=strategy,
        market_intelligence=market_intelligence
    )

    print("\n")
    print(final_report)

    print("\n" + "=" * 70)
    print("REPORT AGENT TEST COMPLETED")
    print("=" * 70)