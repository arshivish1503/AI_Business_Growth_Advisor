import pandas as pd
from pathlib import Path


class MarketIntelligenceAgent:

    def __init__(self):
        print("[Market Intelligence Agent] Loading competitor data...")

        base_path = Path(__file__).resolve().parent.parent
        competitor_path = base_path / "data" / "competitor_data.csv"

        self.competitor_data = pd.read_csv(competitor_path)

        # Clean column names
        self.competitor_data.columns = (
            self.competitor_data.columns
            .str.strip()
        )

        # Convert date column
        if "Date" in self.competitor_data.columns:
            self.competitor_data["Date"] = pd.to_datetime(
                self.competitor_data["Date"],
                errors="coerce"
            )

        print("[Market Intelligence Agent] Competitor data loaded successfully.")

    # ---------------------------------------------------------
    # 1. CITY-LEVEL COMPETITOR ANALYSIS
    # ---------------------------------------------------------

    def analyze_city(self, city):
        df = self.competitor_data[
            self.competitor_data["City"].astype(str).str.strip().str.lower()
            == city.strip().lower()
        ].copy()

        if df.empty:
            return {
                "city": city,
                "message": "No competitor data available for this city."
            }

        return {
            "city": city,
            "observations": len(df),
            "average_competitor_price": round(
                df["Price"].mean(), 2
            ),
            "average_competitor_availability": round(
                df["Availability_Percent"].mean(), 2
            ),
            "promotion_observations": int(
                df["Promotion"].notna().sum()
            )
        }

    # ---------------------------------------------------------
    # 2. COMPETITOR BRAND ANALYSIS
    # ---------------------------------------------------------

    def analyze_competitors(self, city):
        df = self.competitor_data[
            self.competitor_data["City"].astype(str).str.strip().str.lower()
            == city.strip().lower()
        ].copy()

        if df.empty:
            return pd.DataFrame()

        result = (
            df.groupby("Competitor")
            .agg(
                Average_Price=("Price", "mean"),
                Average_Availability=("Availability_Percent", "mean"),
                Observations=("Price", "count")
            )
            .reset_index()
        )

        result["Average_Price"] = result["Average_Price"].round(2)
        result["Average_Availability"] = (
            result["Average_Availability"].round(2)
        )

        return result.sort_values(
            "Average_Price",
            ascending=True
        )

    # ---------------------------------------------------------
    # 3. CATEGORY COMPETITIVE PRESSURE
    # ---------------------------------------------------------

    def analyze_categories(self, city):
        df = self.competitor_data[
            self.competitor_data["City"].astype(str).str.strip().str.lower()
            == city.strip().lower()
        ].copy()

        if df.empty:
            return pd.DataFrame()

        result = (
            df.groupby("Category")
            .agg(
                Average_Price=("Price", "mean"),
                Average_Availability=("Availability_Percent", "mean"),
                Observations=("Price", "count")
            )
            .reset_index()
        )

        result["Average_Price"] = result["Average_Price"].round(2)
        result["Average_Availability"] = (
            result["Average_Availability"].round(2)
        )

        return result.sort_values(
            "Average_Availability",
            ascending=False
        )

    # ---------------------------------------------------------
    # 4. QUARTERLY COMPETITOR ANALYSIS
    # ---------------------------------------------------------

    def compare_q2_q3(self, city, year=2026):

        df = self.competitor_data[
            self.competitor_data["City"].astype(str).str.strip().str.lower()
            == city.strip().lower()
        ].copy()

        if df.empty:
            return pd.DataFrame()

        df = df[
            df["Date"].dt.year == year
        ].copy()

        df["Quarter"] = df["Date"].dt.quarter

        quarterly = (
            df.groupby("Quarter")
            .agg(
                Average_Price=("Price", "mean"),
                Average_Availability=("Availability_Percent", "mean"),
                Observations=("Price", "count")
            )
            .reset_index()
        )

        q2 = quarterly[quarterly["Quarter"] == 2]
        q3 = quarterly[quarterly["Quarter"] == 3]

        if q2.empty or q3.empty:
            return quarterly

        q2_price = q2.iloc[0]["Average_Price"]
        q3_price = q3.iloc[0]["Average_Price"]

        q2_availability = q2.iloc[0]["Average_Availability"]
        q3_availability = q3.iloc[0]["Average_Availability"]

        result = {
            "Q2_Average_Price": round(q2_price, 2),
            "Q3_Average_Price": round(q3_price, 2),
            "Price_Change": round(q3_price - q2_price, 2),
            "Price_Change_Percent": round(
                ((q3_price - q2_price) / q2_price) * 100,
                2
            ),

            "Q2_Average_Availability": round(
                q2_availability,
                2
            ),
            "Q3_Average_Availability": round(
                q3_availability,
                2
            ),
            "Availability_Change_pp": round(
                q3_availability - q2_availability,
                2
            )
        }

        return result

    # ---------------------------------------------------------
    # 5. MARKET SIGNALS
    # ---------------------------------------------------------

    def generate_market_signals(self, city, year=2026):

        city_analysis = self.analyze_city(city)
        competitor_analysis = self.analyze_competitors(city)
        category_analysis = self.analyze_categories(city)
        q2_q3_analysis = self.compare_q2_q3(city, year)

        signals = []

        # Price signal
        if isinstance(q2_q3_analysis, dict):

            price_change = q2_q3_analysis.get(
                "Price_Change_Percent"
            )

            if price_change is not None:

                if price_change < -5:
                    signals.append(
                        "Competitor average price declined materially "
                        "from Q2 to Q3."
                    )

                elif price_change > 5:
                    signals.append(
                        "Competitor average price increased materially "
                        "from Q2 to Q3."
                    )

                else:
                    signals.append(
                        "Competitor average price remained relatively stable "
                        "from Q2 to Q3."
                    )

            # Availability signal
            availability_change = q2_q3_analysis.get(
                "Availability_Change_pp"
            )

            if availability_change is not None:

                if availability_change > 2:
                    signals.append(
                        "Competitor availability improved from Q2 to Q3."
                    )

                elif availability_change < -2:
                    signals.append(
                        "Competitor availability declined from Q2 to Q3."
                    )

                else:
                    signals.append(
                        "Competitor availability remained relatively stable "
                        "from Q2 to Q3."
                    )

        # Evidence limitation
        signals.append(
            "These market signals indicate competitive changes but do not "
            "establish that competitor activity caused the company's sales decline."
        )

        return signals

    # ---------------------------------------------------------
    # 6. COMPLETE ANALYSIS
    # ---------------------------------------------------------

    def run_analysis(self, city="Gurgaon", year=2026):

        print(
            f"[Market Intelligence Agent] "
            f"Running market analysis for {city}, {year}..."
        )

        city_analysis = self.analyze_city(city)
        competitor_analysis = self.analyze_competitors(city)
        category_analysis = self.analyze_categories(city)
        q2_q3_analysis = self.compare_q2_q3(city, year)
        market_signals = self.generate_market_signals(city, year)

        return {
            "city_analysis": city_analysis,
            "competitor_analysis": competitor_analysis,
            "category_analysis": category_analysis,
            "q2_q3_analysis": q2_q3_analysis,
            "market_signals": market_signals
        }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    agent = MarketIntelligenceAgent()

    result = agent.run_analysis(
        city="Gurgaon",
        year=2026
    )

    print("\n" + "=" * 60)
    print("MARKET INTELLIGENCE ANALYSIS")
    print("=" * 60)

    print("\nCITY ANALYSIS")
    print(result["city_analysis"])

    print("\nCOMPETITOR ANALYSIS")
    print(result["competitor_analysis"].to_string(index=False))

    print("\nCATEGORY ANALYSIS")
    print(result["category_analysis"].to_string(index=False))

    print("\nQ2 VS Q3")
    print(result["q2_q3_analysis"])

    print("\nMARKET SIGNALS")

    for i, signal in enumerate(
        result["market_signals"],
        start=1
    ):
        print(f"{i}. {signal}")