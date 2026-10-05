from agents.data_analyst_agent import DataAnalystAgent
from agents.customer_outlet_agent import CustomerOutletAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.strategy_agent import StrategyAgent
from agents.report_agent import ReportAgent


class OrchestratorAgent:

    def __init__(self):

        print("[Orchestrator] Initializing agents...")

        # Core analytical agents
        self.data_agent = DataAnalystAgent()
        self.customer_agent = CustomerOutletAgent()
        self.market_agent = MarketIntelligenceAgent()

        # Decision-making and reporting agents
        self.strategy_agent = StrategyAgent()
        self.report_agent = ReportAgent()

        print("[Orchestrator] Agents initialized successfully.")

    # ---------------------------------------------------------
    # COMPLETE BUSINESS ANALYSIS
    # ---------------------------------------------------------

    def run_analysis(
        self,
        city="Gurgaon",
        year=2026
    ):

        print("\n" + "=" * 60)
        print("ORCHESTRATOR AGENT")
        print("=" * 60)

        print(f"\n[Orchestrator] City: {city}")
        print(f"[Orchestrator] Year: {year}")

        # -----------------------------------------------------
        # STEP 1
        # -----------------------------------------------------

        print(
            "\n[Orchestrator] Step 1: "
            "Analyzing city performance..."
        )

        city_analysis = self.data_agent.analyze_city(
            city
        )

        # -----------------------------------------------------
        # STEP 2
        # -----------------------------------------------------

        print(
            "[Orchestrator] Step 2: "
            "Analyzing SKU performance..."
        )

        sku_analysis = self.data_agent.analyze_skus(
            city=city,
            top_n=5
        )

        # -----------------------------------------------------
        # STEP 3
        # -----------------------------------------------------

        print(
            "[Orchestrator] Step 3: "
            "Analyzing category performance..."
        )

        category_analysis = self.data_agent.analyze_categories(
            city
        )

        # -----------------------------------------------------
        # STEP 4
        # -----------------------------------------------------

        print(
            "[Orchestrator] Step 4: "
            "Analyzing quarterly performance..."
        )

        quarterly_analysis = self.data_agent.analyze_quarters(
            city
        )

        # -----------------------------------------------------
        # STEP 5
        # -----------------------------------------------------

        print(
            "[Orchestrator] Step 5: "
            "Comparing Q2 vs Q3..."
        )

        q2_q3_analysis = self.data_agent.compare_q2_q3(
            city=city,
            year=year
        )

        # -----------------------------------------------------
        # STEP 6
        # -----------------------------------------------------

        print(
            "[Orchestrator] Step 6: "
            "Analyzing SKU-level changes..."
        )

        sku_q2_q3_analysis = (
            self.data_agent.compare_skus_q2_q3(
                city=city,
                year=year,
                top_n=10
            )
        )

        # -----------------------------------------------------
        # STEP 7
        # -----------------------------------------------------

        print(
            "[Orchestrator] Step 7: "
            "Analyzing promotions..."
        )

        promotion_analysis = (
            self.data_agent.compare_promotions_q2_q3(
                city=city,
                year=year
            )
        )

        # -----------------------------------------------------
        # STEP 8
        # -----------------------------------------------------

        print(
            "[Orchestrator] Step 8: "
            "Analyzing competitor pressure..."
        )

        competitor_analysis = (
            self.data_agent.analyze_competitor_pressure(
                city=city,
                year=year
            )
        )

        # -----------------------------------------------------
        # STEP 9
        # -----------------------------------------------------

        print(
            "\n[Orchestrator] Step 9: "
            "Analyzing customer/outlet performance..."
        )

        customer_outlet_analysis = (
            self.customer_agent.run_analysis(
                city=city,
                year=year,
                top_n=10
            )
        )

        print(
            "[Orchestrator] "
            "Customer/outlet analysis completed."
        )

        # -----------------------------------------------------
        # STEP 10
        # -----------------------------------------------------

        print(
            "\n[Orchestrator] Step 10: "
            "Analyzing market intelligence..."
        )

        market_intelligence_analysis = (
            self.market_agent.run_analysis(
                city=city,
                year=year
            )
        )

        print(
            "[Orchestrator] "
            "Market intelligence analysis completed."
        )

        # -----------------------------------------------------
        # STEP 11
        # STRATEGY AGENT
        # -----------------------------------------------------

        print(
            "\n[Orchestrator] Step 11: "
            "Sending evidence to Strategy Agent..."
        )

        strategy = self.strategy_agent.generate_strategy(
            city_analysis=city_analysis,
            q2_q3_analysis=q2_q3_analysis,
            sku_analysis=sku_q2_q3_analysis,
            promotion_analysis=promotion_analysis,
            competitor_analysis=competitor_analysis,
            customer_outlet_analysis=customer_outlet_analysis
        )

        print(
            "[Orchestrator] "
            "Strategy generated successfully."
        )

        # -----------------------------------------------------
        # STEP 12
        # REPORT AGENT
        # -----------------------------------------------------

        print(
            "\n[Orchestrator] Step 12: "
            "Generating management report..."
        )

        report = self.report_agent.generate_report(
            city_analysis=city_analysis,
            q2_q3_analysis=q2_q3_analysis,
            strategy=strategy,
            market_intelligence=market_intelligence_analysis
        )

        print(
            "[Orchestrator] "
            "Management report generated successfully."
        )

        # -----------------------------------------------------
        # DISPLAY CUSTOMER / OUTLET INSIGHT
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("CUSTOMER / OUTLET INSIGHT")
        print("=" * 60)

        customer_insight = (
            customer_outlet_analysis.get(
                "insight",
                "No customer/outlet insight available."
            )
        )

        print(customer_insight)

        # -----------------------------------------------------
        # DISPLAY MARKET INTELLIGENCE
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("MARKET INTELLIGENCE")
        print("=" * 60)

        market_signals = (
            market_intelligence_analysis.get(
                "market_signals",
                []
            )
        )

        if market_signals:

            for index, signal in enumerate(
                market_signals,
                start=1
            ):
                print(f"{index}. {signal}")

        else:
            print(
                "No market intelligence signals available."
            )

        # -----------------------------------------------------
        # DISPLAY FINAL STRATEGY
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("FINAL STRATEGY")
        print("=" * 60)

        if isinstance(strategy, str):
            print(strategy)

        else:
            print(
                strategy.get(
                    "final_strategy",
                    strategy
                )
            )

        # -----------------------------------------------------
        # DISPLAY FINAL REPORT
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("FINAL MANAGEMENT REPORT")
        print("=" * 60)

        print(report)

        # -----------------------------------------------------
        # RETURN COMPLETE SYSTEM OUTPUT
        # -----------------------------------------------------

        return {
            "city": city,
            "year": year,

            "data_analysis": {
                "city_analysis": city_analysis,
                "sku_analysis": sku_analysis,
                "category_analysis": category_analysis,
                "quarterly_analysis": quarterly_analysis,
                "q2_q3_analysis": q2_q3_analysis,
                "sku_q2_q3_analysis": sku_q2_q3_analysis,
                "promotion_analysis": promotion_analysis,
                "competitor_analysis": competitor_analysis
            },

            "customer_outlet_analysis":
                customer_outlet_analysis,

            "market_intelligence":
                market_intelligence_analysis,

            "strategy":
                strategy,

            "report":
                report
        }


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    orchestrator = OrchestratorAgent()

    result = orchestrator.run_analysis(
        city="Gurgaon",
        year=2026
    )