import streamlit as st
import pandas as pd
import os
import shutil
from pathlib import Path

from agents.orchestrator_agent import OrchestratorAgent


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Business Growth Advisor",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

BACKUP_DIR = BASE_DIR / "data" / "_demo_backup"

SALES_FILE = DATA_DIR / "sales_data.csv"
PRODUCT_FILE = DATA_DIR / "product_data.csv"
OUTLET_FILE = DATA_DIR / "outlet_data.csv"
PROMOTION_FILE = DATA_DIR / "promotion_data.csv"
COMPETITOR_FILE = DATA_DIR / "competitor_data.csv"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

        .main-title {
            font-size: 38px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 18px;
            color: #666666;
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 25px;
            font-weight: 650;
            margin-top: 25px;
            margin-bottom: 10px;
        }

        .info-box {
            padding: 18px;
            border-radius: 10px;
            background-color: #f5f7fa;
            border: 1px solid #e1e5ea;
        }

        .success-box {
            padding: 15px;
            border-radius: 10px;
            background-color: #eaf7ee;
            border: 1px solid #b7dfc2;
        }

        .warning-box {
            padding: 15px;
            border-radius: 10px;
            background-color: #fff7e6;
            border: 1px solid #f0d48a;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📊 AI BUSINESS GROWTH ADVISOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Domain-Expert Multi-Agent System for Sales & Marketing Decision Support'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# BACKUP DEMO DATASET
# =========================================================

def create_demo_backup():

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    demo_files = [
        SALES_FILE,
        PRODUCT_FILE,
        OUTLET_FILE,
        PROMOTION_FILE,
        COMPETITOR_FILE
    ]

    for file_path in demo_files:

        backup_path = BACKUP_DIR / file_path.name

        if file_path.exists() and not backup_path.exists():

            shutil.copy2(
                file_path,
                backup_path
            )


create_demo_backup()


# =========================================================
# RESTORE DEMO DATASET
# =========================================================

def restore_demo_data():

    if not BACKUP_DIR.exists():
        return

    backup_files = [
        BACKUP_DIR / "sales_data.csv",
        BACKUP_DIR / "product_data.csv",
        BACKUP_DIR / "outlet_data.csv",
        BACKUP_DIR / "promotion_data.csv",
        BACKUP_DIR / "competitor_data.csv"
    ]

    for backup_file in backup_files:

        if backup_file.exists():

            destination = DATA_DIR / backup_file.name

            shutil.copy2(
                backup_file,
                destination
            )


# =========================================================
# SAVE UPLOADED FILE
# =========================================================

def save_uploaded_file(uploaded_file, destination):

    if uploaded_file is None:
        return False

    with open(destination, "wb") as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return True


# =========================================================
# VALIDATE CSV
# =========================================================

def validate_csv(uploaded_file):

    if uploaded_file is None:
        return None, "File not uploaded."

    try:

        df = pd.read_csv(uploaded_file)

        return df, None

    except Exception as e:

        return None, str(e)


# =========================================================
# REQUIRED COLUMN VALIDATION
# =========================================================

def check_required_columns(df, required_columns):

    if df is None:
        return False, required_columns

    actual_columns = set(
        str(column).strip()
        for column in df.columns
    )

    missing = [
        column
        for column in required_columns
        if column not in actual_columns
    ]

    return len(missing) == 0, missing


# =========================================================
# ROBUST KPI EXTRACTION
# =========================================================

def get_kpi(data, possible_names, default=0):

    if not isinstance(data, dict):
        return default

    for name in possible_names:

        if name in data:
            return data[name]

    normalized_data = {}

    for key, value in data.items():

        normalized_key = (
            str(key)
            .lower()
            .replace("_", "")
            .replace(" ", "")
            .replace("-", "")
        )

        normalized_data[normalized_key] = value

    for name in possible_names:

        normalized_name = (
            str(name)
            .lower()
            .replace("_", "")
            .replace(" ", "")
            .replace("-", "")
        )

        if normalized_name in normalized_data:

            return normalized_data[normalized_name]

    return default


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Analysis Settings")


data_source = st.sidebar.radio(
    "Choose Data Source",
    [
        "Demo Dataset",
        "Upload New Dataset"
    ]
)


# =========================================================
# DEMO DATASET MODE
# =========================================================

if data_source == "Demo Dataset":

    city = st.sidebar.selectbox(
        "Select City",
        ["Gurgaon"]
    )

    year = st.sidebar.selectbox(
        "Select Year",
        [2026]
    )

    st.sidebar.markdown("---")

    st.sidebar.info(
        """
        **Demo Mode**

        Uses the prepared FMCG/Retail dataset included with the project.

        **Current Demo**

        📍 Gurgaon  
        📅 2026
        """
    )

    analyze_button = st.sidebar.button(
        "🚀 Analyze Business",
        width="stretch"
    )


# =========================================================
# UPLOAD MODE
# =========================================================

else:

    st.sidebar.markdown(
        "### 📁 Upload Business Data"
    )

    st.sidebar.caption(
        "Upload CSV files using the standard project format."
    )


    sales_upload = st.sidebar.file_uploader(
        "Sales Data *",
        type=["csv"],
        key="sales_upload"
    )


    product_upload = st.sidebar.file_uploader(
        "Product Data *",
        type=["csv"],
        key="product_upload"
    )


    outlet_upload = st.sidebar.file_uploader(
        "Outlet Data *",
        type=["csv"],
        key="outlet_upload"
    )


    promotion_upload = st.sidebar.file_uploader(
        "Promotion Data",
        type=["csv"],
        key="promotion_upload"
    )


    competitor_upload = st.sidebar.file_uploader(
        "Competitor Data",
        type=["csv"],
        key="competitor_upload"
    )


    # -----------------------------------------------------
    # UPLOAD VALIDATION
    # -----------------------------------------------------

    uploaded_sales_df = None
    uploaded_product_df = None
    uploaded_outlet_df = None
    uploaded_promotion_df = None
    uploaded_competitor_df = None

    upload_errors = []


    # SALES

    if sales_upload:

        uploaded_sales_df, error = validate_csv(
            sales_upload
        )

        if error:

            upload_errors.append(
                f"Sales Data: {error}"
            )


    # PRODUCT

    if product_upload:

        uploaded_product_df, error = validate_csv(
            product_upload
        )

        if error:

            upload_errors.append(
                f"Product Data: {error}"
            )


    # OUTLET

    if outlet_upload:

        uploaded_outlet_df, error = validate_csv(
            outlet_upload
        )

        if error:

            upload_errors.append(
                f"Outlet Data: {error}"
            )


    # PROMOTION

    if promotion_upload:

        uploaded_promotion_df, error = validate_csv(
            promotion_upload
        )

        if error:

            upload_errors.append(
                f"Promotion Data: {error}"
            )


    # COMPETITOR

    if competitor_upload:

        uploaded_competitor_df, error = validate_csv(
            competitor_upload
        )

        if error:

            upload_errors.append(
                f"Competitor Data: {error}"
            )


    # -----------------------------------------------------
    # REQUIRED COLUMN CHECKS
    # -----------------------------------------------------

    if uploaded_sales_df is not None:

        required_sales_columns = [
            "Date",
            "Region",
            "City",
            "Outlet_ID",
            "SKU_ID",
            "Units_Sold",
            "Revenue",
            "Selling_Price",
            "Availability_Percent"
        ]

        valid, missing = check_required_columns(
            uploaded_sales_df,
            required_sales_columns
        )

        if not valid:

            upload_errors.append(
                "Sales Data missing: "
                + ", ".join(missing)
            )


    if uploaded_product_df is not None:

        required_product_columns = [
            "SKU_ID",
            "Product_Name",
            "Category",
            "MRP"
        ]

        valid, missing = check_required_columns(
            uploaded_product_df,
            required_product_columns
        )

        if not valid:

            upload_errors.append(
                "Product Data missing: "
                + ", ".join(missing)
            )


    if uploaded_outlet_df is not None:

        required_outlet_columns = [
            "Outlet_ID",
            "Outlet_Name",
            "City",
            "Region",
            "Outlet_Type"
        ]

        valid, missing = check_required_columns(
            uploaded_outlet_df,
            required_outlet_columns
        )

        if not valid:

            upload_errors.append(
                "Outlet Data missing: "
                + ", ".join(missing)
            )


    # -----------------------------------------------------
    # SHOW VALIDATION STATUS
    # -----------------------------------------------------

    if upload_errors:

        st.sidebar.error(
            "⚠️ Data validation issues found."
        )

        for error in upload_errors:

            st.sidebar.write(
                f"• {error}"
            )


    # -----------------------------------------------------
    # DETECT CITIES AND YEARS
    # -----------------------------------------------------

    available_cities = []
    available_years = []


    if uploaded_sales_df is not None:

        if "City" in uploaded_sales_df.columns:

            available_cities = sorted(
                uploaded_sales_df["City"]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )


        if "Date" in uploaded_sales_df.columns:

            dates = pd.to_datetime(
                uploaded_sales_df["Date"],
                errors="coerce"
            )

            available_years = sorted(
                dates.dropna()
                .dt.year
                .unique()
                .tolist()
            )


    # -----------------------------------------------------
    # CITY SELECTOR
    # -----------------------------------------------------

    if available_cities:

        city = st.sidebar.selectbox(
            "Select City",
            available_cities
        )

    else:

        city = None

        st.sidebar.caption(
            "Upload Sales Data to detect cities."
        )


    # -----------------------------------------------------
    # YEAR SELECTOR
    # -----------------------------------------------------

    if available_years:

        year = st.sidebar.selectbox(
            "Select Year",
            available_years
        )

    else:

        year = None

        st.sidebar.caption(
            "Upload Sales Data to detect years."
        )


    st.sidebar.markdown("---")


    # -----------------------------------------------------
    # UPLOAD STATUS
    # -----------------------------------------------------

    uploaded_count = sum(
        file is not None
        for file in [
            sales_upload,
            product_upload,
            outlet_upload,
            promotion_upload,
            competitor_upload
        ]
    )


    st.sidebar.write(
        f"📁 Files uploaded: **{uploaded_count}/5**"
    )


    required_files_ready = (
        sales_upload is not None
        and product_upload is not None
        and outlet_upload is not None
        and not upload_errors
        and city is not None
        and year is not None
    )


    analyze_button = st.sidebar.button(
        "🚀 Analyze Uploaded Data",
        width="stretch",
        disabled=not required_files_ready
    )


# =========================================================
# SYSTEM ARCHITECTURE
# =========================================================

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **System Architecture**

    User → Orchestrator → Specialized Agents → Strategy → Report

    **Specialized Agents**

    • Data Analyst  
    • Customer/Outlet  
    • Market Intelligence  
    • Strategy  
    • Report
    """
)


# =========================================================
# RUN ANALYSIS
# =========================================================

if analyze_button:

    # -----------------------------------------------------
    # DEMO MODE
    # -----------------------------------------------------

    if data_source == "Demo Dataset":

        restore_demo_data()


    # -----------------------------------------------------
    # UPLOAD MODE
    # -----------------------------------------------------

    else:

        with st.spinner(
            "Preparing uploaded business data..."
        ):

            DATA_DIR.mkdir(
                parents=True,
                exist_ok=True
            )


            save_uploaded_file(
                sales_upload,
                SALES_FILE
            )

            save_uploaded_file(
                product_upload,
                PRODUCT_FILE
            )

            save_uploaded_file(
                outlet_upload,
                OUTLET_FILE
            )


            # Optional datasets

            if promotion_upload:

                save_uploaded_file(
                    promotion_upload,
                    PROMOTION_FILE
                )

            else:

                backup_promotion = (
                    BACKUP_DIR / "promotion_data.csv"
                )

                if backup_promotion.exists():

                    shutil.copy2(
                        backup_promotion,
                        PROMOTION_FILE
                    )


            if competitor_upload:

                save_uploaded_file(
                    competitor_upload,
                    COMPETITOR_FILE
                )

            else:

                backup_competitor = (
                    BACKUP_DIR / "competitor_data.csv"
                )

                if backup_competitor.exists():

                    shutil.copy2(
                        backup_competitor,
                        COMPETITOR_FILE
                    )


    # -----------------------------------------------------
    # RUN ORCHESTRATOR
    # -----------------------------------------------------

    with st.spinner(
        "AI Business Growth Advisor is analyzing the business..."
    ):

        try:

            orchestrator = OrchestratorAgent()

            result = orchestrator.run_analysis(
                city=city,
                year=year
            )


            st.session_state["analysis_result"] = result

            st.session_state["analysis_city"] = city

            st.session_state["analysis_year"] = year

            st.session_state["data_source"] = data_source


            st.success(
                "Business analysis completed successfully."
            )


        except Exception as e:

            st.error(
                "An error occurred while running the analysis."
            )

            st.exception(e)


# =========================================================
# DISPLAY RESULTS
# =========================================================

if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]

    analysis_city = st.session_state["analysis_city"]

    analysis_year = st.session_state["analysis_year"]

    data_analysis = result["data_analysis"]

    city_analysis = data_analysis["city_analysis"]

    q2_q3 = data_analysis["q2_q3_analysis"]

    strategy = result["strategy"]

    customer_analysis = result["customer_outlet_analysis"]

    market_analysis = result["market_intelligence"]

    report = result["report"]


    # =====================================================
    # KPI EXTRACTION
    # =====================================================

    revenue = get_kpi(
        city_analysis,
        [
            "total_revenue",
            "Total_Revenue",
            "Total Revenue",
            "Revenue",
            "revenue"
        ]
    )


    units = get_kpi(
        city_analysis,
        [
            "total_units",
            "Total_Units",
            "Total Units",
            "Units_Sold",
            "Units Sold",
            "Units",
            "units"
        ]
    )


    availability = get_kpi(
        city_analysis,
        [
            "average_availability",
            "Average_Availability",
            "Average Availability",
            "avg_availability",
            "Avg Availability",
            "Availability_Percent",
            "Availability"
        ]
    )


    # =====================================================
    # Q2 → Q3
    # =====================================================

    q2_revenue = get_kpi(
        q2_q3,
        [
            "Q2_Revenue",
            "Q2 Revenue",
            "q2_revenue"
        ]
    )


    q3_revenue = get_kpi(
        q2_q3,
        [
            "Q3_Revenue",
            "Q3 Revenue",
            "q3_revenue"
        ]
    )


    revenue_change_pct = get_kpi(
        q2_q3,
        [
            "Revenue_Change_Pct",
            "Revenue Change Pct",
            "Revenue Change %",
            "revenue_change_pct"
        ],
        (
            ((q3_revenue - q2_revenue) / q2_revenue) * 100
            if q2_revenue != 0
            else 0
        )
    )


    q2_units = get_kpi(
        q2_q3,
        [
            "Q2_Units",
            "Q2 Units",
            "Q2_Units_Sold",
            "Q2 Units Sold"
        ]
    )


    q3_units = get_kpi(
        q2_q3,
        [
            "Q3_Units",
            "Q3 Units",
            "Q3_Units_Sold",
            "Q3 Units Sold"
        ]
    )


    units_change_pct = get_kpi(
        q2_q3,
        [
            "Units_Change_Pct",
            "Units Change Pct",
            "Units Change %",
            "units_change_pct"
        ],
        (
            ((q3_units - q2_units) / q2_units) * 100
            if q2_units != 0
            else 0
        )
    )


    availability_change = get_kpi(
        q2_q3,
        [
            "Availability_Change_pp",
            "Availability Change pp",
            "Availability_Change",
            "Availability Change",
            "availability_change_pp"
        ]
    )


    # =====================================================
    # BUSINESS PERFORMANCE
    # =====================================================

    st.markdown(
        f'<div class="section-title">'
        f'📍 {analysis_city} Business Performance'
        f'</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total Revenue",
            f"₹{float(revenue):,.2f}"
        )


    with col2:

        st.metric(
            "Units Sold",
            f"{float(units):,.0f}"
        )


    with col3:

        st.metric(
            "Average Availability",
            f"{float(availability):.2f}%"
        )


    # =====================================================
    # Q2 → Q3 PERFORMANCE
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '📉 Q2 → Q3 Performance'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Q2 Revenue",
            f"₹{float(q2_revenue):,.2f}"
        )


    with col2:

        st.metric(
            "Q3 Revenue",
            f"₹{float(q3_revenue):,.2f}",
            f"{float(revenue_change_pct):.2f}%"
        )


    with col3:

        st.metric(
            "Units Change",
            f"{float(units_change_pct):.2f}%"
        )


    with col4:

        st.metric(
            "Availability Change",
            f"{float(availability_change):.2f} pp"
        )


    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🎯 Executive Diagnosis",
            "📦 SKU & Outlet Priorities",
            "🌐 Market Intelligence",
            "🚀 Recommended Actions",
            "📑 Full Management Report"
        ]
    )


    # =====================================================
    # TAB 1
    # =====================================================

    with tab1:

        st.subheader(
            "Executive Diagnosis"
        )


        if "## 1. EXECUTIVE DIAGNOSIS" in strategy:

            diagnosis = strategy.split(
                "## 1. EXECUTIVE DIAGNOSIS",
                1
            )[1]


            if "## 2. TOP 5 ACTIONS" in diagnosis:

                diagnosis = diagnosis.split(
                    "## 2. TOP 5 ACTIONS",
                    1
                )[0]


            st.markdown(
                diagnosis.strip()
            )

        else:

            st.markdown(strategy)


        st.markdown("---")


        st.subheader(
            "Customer / Outlet Insight"
        )


        customer_insight = customer_analysis.get(
            "insight",
            "Customer and outlet analysis completed."
        )


        st.markdown(
            customer_insight
        )


    # =====================================================
    # TAB 2
    # =====================================================

    with tab2:

        st.subheader(
            "SKU Priorities"
        )


        if "## 3. SKU PRIORITIES" in strategy:

            sku_section = strategy.split(
                "## 3. SKU PRIORITIES",
                1
            )[1]


            if "## 4. CUSTOMER / OUTLET PRIORITIES" in sku_section:

                sku_section = sku_section.split(
                    "## 4. CUSTOMER / OUTLET PRIORITIES",
                    1
                )[0]


            st.markdown(
                sku_section.strip()
            )

        else:

            st.info(
                "SKU priority analysis is available in the full report."
            )


        st.markdown("---")


        st.subheader(
            "Customer / Outlet Priorities"
        )


        if "## 4. CUSTOMER / OUTLET PRIORITIES" in strategy:

            outlet_section = strategy.split(
                "## 4. CUSTOMER / OUTLET PRIORITIES",
                1
            )[1]


            if "## 5. WHAT MANAGEMENT SHOULD NOT DO" in outlet_section:

                outlet_section = outlet_section.split(
                    "## 5. WHAT MANAGEMENT SHOULD NOT DO",
                    1
                )[0]


            st.markdown(
                outlet_section.strip()
            )

        else:

            st.info(
                "Customer/outlet priority analysis is available in the report."
            )


    # =====================================================
    # TAB 3
    # =====================================================

    with tab3:

        st.subheader(
            "Market Intelligence"
        )


        competitor_analysis = market_analysis.get(
            "competitor_analysis"
        )


        if competitor_analysis is not None:

            st.dataframe(
                competitor_analysis,
                width="stretch",
                hide_index=True
            )


        st.markdown("---")


        st.subheader(
            "Market Signals"
        )


        market_signals = market_analysis.get(
            "market_signals",
            []
        )


        if market_signals:

            for signal in market_signals:

                st.markdown(
                    f"• {signal}"
                )

        else:

            st.info(
                "No additional market signals available."
            )


        q2_q3_market = market_analysis.get(
            "q2_q3_analysis"
        )


        if q2_q3_market:

            st.markdown("---")


            st.subheader(
                "Competitor Q2 → Q3 Movement"
            )


            market_col1, market_col2 = st.columns(2)


            with market_col1:

                st.metric(
                    "Competitor Price Change",
                    f"{float(q2_q3_market.get('price_change_pct', 0)):.2f}%"
                )


            with market_col2:

                st.metric(
                    "Competitor Availability Change",
                    f"{float(q2_q3_market.get('availability_change_pp', 0)):.2f} pp"
                )


    # =====================================================
    # TAB 4
    # =====================================================

    with tab4:

        st.subheader(
            "Top 5 Recommended Actions"
        )


        if "## 2. TOP 5 ACTIONS" in strategy:

            actions_section = strategy.split(
                "## 2. TOP 5 ACTIONS",
                1
            )[1]


            if "## 3. SKU PRIORITIES" in actions_section:

                actions_section = actions_section.split(
                    "## 3. SKU PRIORITIES",
                    1
                )[0]


            st.markdown(
                actions_section.strip()
            )

        else:

            st.markdown(
                "Recommendations are available in the management report."
            )


        st.markdown("---")


        st.subheader(
            "30-Day Action Plan"
        )


        if "## 6. 30-DAY ACTION PLAN" in strategy:

            action_plan = strategy.split(
                "## 6. 30-DAY ACTION PLAN",
                1
            )[1]


            if "## 7. NEXT MANAGEMENT QUESTION" in action_plan:

                action_plan = action_plan.split(
                    "## 7. NEXT MANAGEMENT QUESTION",
                    1
                )[0]


            st.markdown(
                action_plan.strip()
            )

        else:

            st.info(
                "30-day action plan is available in the full report."
            )


    # =====================================================
    # TAB 5
    # =====================================================

    with tab5:

        st.subheader(
            f"Management Report — {analysis_city}, {analysis_year}"
        )


        st.markdown(
            report
        )


# =========================================================
# INITIAL SCREEN
# =========================================================

else:

    st.markdown(
        """
        <div class="info-box">

        ### 👋 Welcome to the AI Business Growth Advisor

        This system uses a **multi-agent AI architecture** to analyze
        FMCG/Retail business performance and generate management
        recommendations.

        ### What can you analyze?

        **📊 Demo Dataset**

        Use the prepared Gurgaon 2026 FMCG dataset.

        **📁 Upload New Dataset**

        Upload your own:

        • Sales Data  
        • Product Data  
        • Outlet Data  
        • Promotion Data  
        • Competitor Data  

        The system will automatically detect available **cities and years**
        from the uploaded Sales Data.

        ### Analysis Flow

        **Upload Data → Validate → Select City & Year → Analyze → AI Agents → Recommendations**

        </div>
        """,
        unsafe_allow_html=True
    )