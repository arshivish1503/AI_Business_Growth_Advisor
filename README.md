# 📊 AI Business Growth Advisor

### A Domain-Expert Multi-Agent System for Sales & Marketing Decision Support

An AI-powered business intelligence and decision-support application designed for **FMCG and Retail** businesses. The system combines structured business analytics, specialised AI agents, market intelligence and strategic reasoning to convert raw sales data into actionable management recommendations.

> **Project:** AI Business Growth Advisor  
> **Student:** Arshika Vishwakarma  
> **Roll No.:** 065070  
> **Program:** PGDM-BDA, FORE School of Management  
> **Course:** Agentic AI for Business Automation  
> **Term:** 04 | Academic Year 2026–27

---

## 🚀 Live Application

**Streamlit App:**  
http://localhost:8501/

The application allows users to:

- Analyse FMCG/Retail business performance
- Select a city and year
- Upload new business datasets
- Analyse revenue, units and availability
- Identify underperforming SKUs
- Analyse outlet and customer performance
- Review competitor market signals
- Receive prioritised management recommendations
- Generate a 30-day action plan

---

## 📌 Project Overview

Business managers often have large amounts of sales, product, outlet and market data but still spend significant time manually analysing the information and deciding what requires attention.

The **AI Business Growth Advisor** addresses this problem through a **multi-agent architecture**, where specialised agents perform different business-analysis tasks and collaborate to generate actionable recommendations.

### Core Management Questions

1. Why are sales or revenue changing?
2. Which SKUs are responsible for the change?
3. Which cities, regions, channels or outlets are underperforming?
4. What evidence indicates potential root causes?
5. Which products or outlets should management prioritise?
6. What actions should management take?
7. What should be investigated before taking action?
8. What market or competitor signals should be monitored?

---

## 🧠 Multi-Agent Architecture

```text
                    ┌──────────────────────┐
                    │        USER          │
                    │   Streamlit App      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ORCHESTRATOR       │
                    │       AGENT          │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
   ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
   │  DATA ANALYST   │ │ CUSTOMER/OUTLET │ │ MARKET INTELLIGENCE │
   │      AGENT      │ │      AGENT      │ │        AGENT        │
   └────────┬────────┘ └────────┬────────┘ └──────────┬──────────┘
            │                   │                     │
            └───────────────────┼─────────────────────┘
                                ▼
                    ┌──────────────────────┐
                    │   STRATEGY AGENT     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     REPORT AGENT      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ MANAGEMENT INSIGHTS  │
                    │    & ACTION PLAN     │
                    └──────────────────────┘
```

---

## 🤖 Specialized Agents

### 1. Orchestrator Agent

Coordinates the complete analytical workflow, manages communication between specialised agents, consolidates evidence and sends the combined analysis to the Strategy Agent.

### 2. Data Analyst Agent

Analyses:

- Revenue
- Units sold
- Availability
- City performance
- SKU performance
- Category performance
- Monthly and quarterly trends
- Q2 vs Q3 performance
- Promotion performance
- Competitor-pressure indicators

### 3. Customer / Outlet Agent

Analyses:

- Outlet type performance
- Outlet tier performance
- Individual outlet performance
- Revenue contribution
- Q2 vs Q3 outlet changes
- Priority outlets

### 4. Market Intelligence Agent

Analyses:

- Competitor pricing
- Competitor availability
- Competitor brands
- Category-level competitive signals
- Quarterly competitor movements
- Promotion observations

Market changes are treated as **signals for investigation**, rather than automatically being treated as causal factors.

### 5. Strategy Agent

Converts analytical evidence into management decisions, including:

- Executive diagnosis
- Top 5 actions
- SKU priorities
- Customer/outlet priorities
- Management cautions
- 30-day action plan
- Next management question

The Strategy Agent uses a hybrid approach combining **deterministic Python calculations with local LLM reasoning**.

### 6. Report Agent

Converts the analysis and strategy outputs into a structured management report containing:

- Executive Summary
- Business Performance
- SKU Priorities
- Customer / Outlet Priorities
- Market Intelligence
- Recommended Actions
- 30-Day Action Plan
- Management Focus

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Core implementation |
| Pandas | Data analysis |
| NumPy | Numerical processing |
| scikit-learn | Analytics / ML utilities |
| Ollama | Local LLM runtime |
| Llama 3.2:3b | Local language model |
| Streamlit | Interactive web application |
| Plotly | Visualisation |
| python-dotenv | Configuration |
| CSV | Business data input |

### Why Ollama?

Ollama enables the project to run an LLM locally without requiring a paid OpenAI API.

---

## 📂 Project Structure

```text
AI_Business_Growth_Advisor/
│
├── agents/
│   ├── data_analyst_agent.py
│   ├── customer_outlet_agent.py
│   ├── market_intelligence_agent.py
│   ├── strategy_agent.py
│   ├── report_agent.py
│   └── orchestrator_agent.py
│
├── data/
│   ├── sales_data.csv
│   ├── product_data.csv
│   ├── outlet_data.csv
│   ├── promotion_data.csv
│   └── competitor_data.csv
│
├── docs/
│   └── AI_Business_Growth_Advisor_Project_Report.pdf
│
├── outputs/
├── prompts/
├── tools/
│
├── app.py
├── config.py
├── DATASET_README.json
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 📊 Dataset

The system uses five connected FMCG/Retail datasets:

- **Sales Data** — transaction-level sales performance
- **Product Data** — SKU and product information
- **Outlet Data** — customer and outlet information
- **Promotion Data** — promotional activity
- **Competitor Data** — market and competitor information

The demonstration sales dataset contains **30,000 observations**.

---

## 🔄 How the System Works

```text
Data Selection / Upload
          ↓
CSV Validation
          ↓
City & Year Detection
          ↓
Orchestrator Agent
          ↓
Data Analyst
Customer / Outlet
Market Intelligence
          ↓
Evidence Consolidation
          ↓
Strategy Agent
          ↓
Prioritised Recommendations
          ↓
Report Agent
          ↓
Management Dashboard
```

---

## 📁 Upload New Business Data

The application supports two modes.

### Demo Dataset

Uses the prepared FMCG/Retail demonstration dataset.

**City:** Gurgaon  
**Year:** 2026

### Upload New Dataset

Users can upload:

- Sales Data — required
- Product Data — required
- Outlet Data — required
- Promotion Data — optional
- Competitor Data — optional

The application automatically detects available cities and years from the uploaded sales data.

---

## 📈 Demonstration Results

The Gurgaon 2026 demonstration produced:

| KPI | Result |
|---|---:|
| Total Revenue | ₹1,825,754.07 |
| Units Sold | 49,674 |
| Average Availability | 90.47% |
| Revenue Rank | #1 among 14 observed cities |
| Q2 Revenue | ₹247,844.62 |
| Q3 Revenue | ₹181,130.78 |
| Q2 → Q3 Revenue Change | -26.92% |
| Q2 → Q3 Units Change | -15.15% |
| Availability Change | -2.30 pp |

### Key SKU Findings

- **SKU005:** Revenue -74.02%, Units -73.94%, Availability -24.33 pp
- **SKU004:** Revenue -72.86%, Units -72.86%, Availability -18.82 pp
- **SKU001:** Revenue -52.21%, Units -52.36%, Availability -19.94 pp

These SKUs were prioritised for availability recovery and investigation.

---

## 🏪 Customer / Outlet Findings

The system identified:

- **Kirana** as the largest revenue-contributing outlet type.
- **Eating & Dining** as the outlet type with the largest revenue decline.
- Individual outlets with significant Q2-to-Q3 deterioration for management investigation.

The system distinguishes between **observed performance deterioration** and **proven causal drivers** to avoid unsupported business conclusions.

---

## 🌐 Market Intelligence Findings

The Gurgaon demonstration showed:

- Competitor average price declined from Q2 to Q3.
- Competitor availability improved during the same period.

These are presented as **market signals** for management investigation rather than automatically being treated as causes of the company's sales decline.

---

## 🎯 Recommended Management Actions

The demonstration strategy layer prioritises actions such as:

1. Investigate and recover SKU005 availability.
2. Investigate Eating & Dining performance.
3. Investigate priority high-decline outlets.
4. Investigate major SKU declines where availability does not explain the movement.
5. Monitor competitor pricing and availability.

A **30-day action plan** is also generated to support execution.

---

## 🖥️ Streamlit Dashboard

The dashboard contains:

### 🎯 Executive Diagnosis
High-level explanation of the business situation.

### 📦 SKU & Outlet Priorities
Products and outlets requiring management attention.

### 🌐 Market Intelligence
Competitor metrics and market signals.

### 🚀 Recommended Actions
Prioritised actions and 30-day action plan.

### 📑 Full Management Report
Complete management-ready output.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/arshivish1503/AI_Business_Growth_Advisor.git
cd AI_Business_Growth_Advisor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Ollama

Install Ollama and download the required model:

```bash
ollama pull llama3.2:3b
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## 🔐 Environment & Security

The repository excludes local environment files such as `.env`.

Do not upload:

- API keys
- Passwords
- Credentials
- Private business data
- Confidential customer information

---

## 📄 Project Report

The complete academic project report is available in the `docs/` folder.

**[View Project Report](docs/AI_Business_Growth_Advisor_Project_Report.pdf)**

---

## 🔮 Future Scope

- Interactive Plotly dashboards
- Excel upload support
- Automatic schema mapping
- Demand forecasting
- Sales prediction
- Availability-risk prediction
- Price and promotion scenario analysis
- RAG over company documents
- Customer segmentation
- Basket analysis
- Live ERP/CRM integration
- Role-based access
- Automated PDF/Excel reports
- Production-grade multi-user deployment

---

## 🎓 Academic Context

This project was developed as part of:

**Agentic AI for Business Automation**  
PGDM-BDA | Term 04  
FORE School of Management, New Delhi

The project demonstrates the application of:

- Agentic AI
- Multi-agent orchestration
- Business analytics
- Decision-support systems
- Local LLM inference
- FMCG/Retail business intelligence

---

## 👩‍💻 Author

**Arshika Vishwakarma**  
Roll No. 065070  
PGDM-BDA  
FORE School of Management

---

## ⭐ Project Summary

> **AI Business Growth Advisor converts business data into evidence-based management decisions using a domain-expert multi-agent architecture.**

**Data → Analysis → Diagnosis → Market Context → Strategy → Action Plan**
