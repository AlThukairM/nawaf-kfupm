import re
import streamlit as st
import pandas as pd

# Web-based Private Partner Selection Model with hard-coded criteria
# No external Excel upload required; definitions embedded directly

subcriteria = [
    {
        "main": "Financial",
        "main_weight": 0.34,
        "sub": "Equity/Debt of the company",
        "sub_weight": 0.12,
        "measure": "Equity / Debt ratio",
        "lower": 0.2,
        "upper": 2.0,
        "relationship": "Linear",
    },
    {
        "main": "Financial",
        "main_weight": 0.34,
        "sub": "Working Capital",
        "sub_weight": 0.16,
        "measure": "Working capital / Total assets",
        "lower": 0.1,
        "upper": 0.5,
        "relationship": "Linear",
    },
    {
        "main": "Financial",
        "main_weight": 0.34,
        "sub": "Financial Statement",
        "sub_weight": 0.15,
        "measure": "Audit score (0–100)",
        "lower": 60.0,
        "upper": 95.0,
        "relationship": "Linear",
    },
    {
        "main": "Financial",
        "main_weight": 0.34,
        "sub": "Government Control on Tolls/fees",
        "sub_weight": 0.24,
        "measure": "% revenue subject to government cap",
        "lower": 100.0,
        "upper": 0.0,
        "relationship": "Inverse-linear",
    },
    {
        "main": "Financial",
        "main_weight": 0.34,
        "sub": "Financial Capacity",
        "sub_weight": 0.2,
        "measure": "Available liquidity (SAR million)",
        "lower": 10.0,
        "upper": 200.0,
        "relationship": "Power; (p=0.7)",
    },
    {
        "main": "Financial",
        "main_weight": 0.34,
        "sub": "Expected Revenue Method",
        "sub_weight": 0.13,
        "measure": "Expert judgment Rated from 0 to 5",
        "lower": 0.0,
        "upper": 5.0,
        "relationship": "Linear",
    },
    {
        "main": "Technical",
        "main_weight": 0.18,
        "sub": "Scale of Completed Projects",
        "sub_weight": 0.28,
        "measure": "Total project value completed (SAR billion)",
        "lower": 0.1,
        "upper": 5.0,
        "relationship": "Linear",
    },
    {
        "main": "Technical",
        "main_weight": 0.18,
        "sub": "Resources Capabilities (Manpower, Plant & Equipment)",
        "sub_weight": 0.07,
        "measure": "Subject to expert judgment Rated from 0 to 5",
        "lower": 0.0,
        "upper": 5.0,
        "relationship": "Linear",
    },
    {
        "main": "Technical",
        "main_weight": 0.18,
        "sub": "Current Workload",
        "sub_weight": 0.17,
        "measure": "% utilization of capacity",
        "lower": 0.0,
        "upper": 100.0,
        "relationship": "Inverse-linear",
    },
    {
        "main": "Technical",
        "main_weight": 0.18,
        "sub": "Local Experience",
        "sub_weight": 0.08,
        "measure": "Number of local PPPs delivered",
        "lower": 0.0,
        "upper": 10.0,
        "relationship": "Linear",
    },
    {
        "main": "Technical",
        "main_weight": 0.18,
        "sub": "Capacity of Design",
        "sub_weight": 0.11,
        "measure": "Subject to expert judgment Rated from 0 to 5",
        "lower": 0.0,
        "upper": 5.0,
        "relationship": "Linear",
    },
    {
        "main": "Technical",
        "main_weight": 0.18,
        "sub": "Operation and Maintenance Policy",
        "sub_weight": 0.11,
        "measure": "O&M sustainability score (0–100)",
        "lower": 0.0,
        "upper": 100.0,
        "relationship": "Power (p=0.8)",
    },
    {
        "main": "Technical",
        "main_weight": 0.18,
        "sub": "Construction Program and ability",
        "sub_weight": 0.09,
        "measure": "Schedule adherence (%)",
        "lower": 0.0,
        "upper": 100.0,
        "relationship": "Linear",
    },
    {
        "main": "Technical",
        "main_weight": 0.18,
        "sub": "Construction technologies and methods",
        "sub_weight": 0.09,
        "measure": "Subject to expert judgment Rated from 0 to 5",
        "lower": 0.0,
        "upper": 5.0,
        "relationship": "Linear",
    },
    {
        "main": "Safety & Environment",
        "main_weight": 0.16,
        "sub": "Environmental Management and Policy",
        "sub_weight": 0.35,
        "measure": "EMS maturity level (1–5)",
        "lower": 1.0,
        "upper": 5.0,
        "relationship": "Linear",
    },
    {
        "main": "Safety & Environment",
        "main_weight": 0.16,
        "sub": "Compliance to Laws and Regulations",
        "sub_weight": 0.35,
        "measure": "Compliance incidents per year (count)",
        "lower": 0.0,
        "upper": 10.0,
        "relationship": "Inverse-linear",
    },
    {
        "main": "Safety & Environment",
        "main_weight": 0.16,
        "sub": "Qualification and Experience of Safety Personnel",
        "sub_weight": 0.3,
        "measure": "Avg. yrs of safety staff experience",
        "lower": 0.0,
        "upper": 15.0,
        "relationship": "Power (P=0.9)",
    },
    {
        "main": "Management",
        "main_weight": 0.15,
        "sub": "Relevant experience in similar projects",
        "sub_weight": 0.17,
        "measure": "No. of similar PPPs delivered",
        "lower": 0.0,
        "upper": 8.0,
        "relationship": "Linear",
    },
    {
        "main": "Management",
        "main_weight": 0.15,
        "sub": "Risk appetite and acceptance of Risk transfer",
        "sub_weight": 0.15,
        "measure": "Risk transfer score (0–100)",
        "lower": 0.0,
        "upper": 100.0,
        "relationship": "Power (p=0.8)",
    },
    {
        "main": "Management",
        "main_weight": 0.15,
        "sub": "Contingency Plans",
        "sub_weight": 0.18,
        "measure": "Contingency provision (% of budget)",
        "lower": 5.0,
        "upper": 20.0,
        "relationship": "Linear",
    },
    {
        "main": "Management",
        "main_weight": 0.15,
        "sub": "Responsibilities allocation and proven Leadership capabilities",
        "sub_weight": 0.16,
        "measure": "Leadership index (0–10)",
        "lower": 2.0,
        "upper": 10.0,
        "relationship": "Linear",
    },
    {
        "main": "Management",
        "main_weight": 0.15,
        "sub": "Quality Assurance and Control",
        "sub_weight": 0.1,
        "measure": "QA audit score (0–100)",
        "lower": 70.0,
        "upper": 100.0,
        "relationship": "Linear",
    },
    {
        "main": "Management",
        "main_weight": 0.15,
        "sub": "Contractual relationship among participants",
        "sub_weight": 0.23,
        "measure": "Stakeholder alignment score (0–100)",
        "lower": 40.0,
        "upper": 100.0,
        "relationship": "Power (p=0.7)",
    },
    {
        "main": "Legal",
        "main_weight": 0.17,
        "sub": "Understanding of Legal requirement",
        "sub_weight": 0.25,
        "measure": "Legal compliance score (0–100)",
        "lower": 60.0,
        "upper": 100.0,
        "relationship": "Linear",
    },
    {
        "main": "Legal",
        "main_weight": 0.17,
        "sub": "Compliance to permit requirements",
        "sub_weight": 0.37,
        "measure": "Permit approval rate (%)",
        "lower": 50.0,
        "upper": 100.0,
        "relationship": "Power (p=0.85)",
    },
    {
        "main": "Legal",
        "main_weight": 0.17,
        "sub": "Conflicts/litigation and disputes",
        "sub_weight": 0.38,
        "measure": "Number of active disputes (count)",
        "lower": 10.0,
        "upper": 0.0,
        "relationship": "Inverse-linear",
    },
]


def compute_utility(raw: float, lower: float, upper: float, relationship: str) -> float:
    """
    Compute normalized utility of a raw performance value.
    Supports linear, inverse-linear, and power mappings.
    """
    # Clamp raw between [min_val, max_val]
    min_val, max_val = min(lower, upper), max(lower, upper)
    raw = max(min_val, min(max_val, raw))

    if "Power" in relationship:
        # Extract exponent p
        m = re.search(r"[pP]\s*[=:]?\s*([0-9]*\.?[0-9]+)", relationship)
        p = float(m.group(1)) if m else 1.0
        base = (raw - lower) / (upper - lower)
        utility = base ** p
    elif "Inverse" in relationship:
        utility = (lower - raw) / (lower - upper)
    else:
        utility = (raw - lower) / (upper - lower)

    return max(0.0, min(1.0, utility))


def main():
    st.title("Private Partner Selection Model")
    st.markdown("This application ranks private partner alternatives based on predefined criteria and utility functions.")

    # Sidebar: define alternatives
    st.sidebar.header("Alternatives Setup")
    num_alts = st.sidebar.number_input("Number of Alternatives", min_value=1, max_value=10, value=3, step=1)
    alt_names = []
    for i in range(num_alts):
        name = st.sidebar.text_input(f"Alternative #{i+1} Name", value=f"Partner {i+1}")
        alt_names.append(name)

    # Main form: input performance values
    st.header("Evaluator Inputs")
    inputs = {alt: {} for alt in alt_names}
    for entry in subcriteria:
        sub = entry["sub"]
        measure = entry["measure"]
        lower = entry["lower"]
        upper = entry["upper"]
        rel = entry["relationship"]
        label = f"{sub} ({measure}) | Range: [{lower}, {upper}] | Relationship: {rel}"
        cols = st.columns(len(alt_names))
        for idx, alt in enumerate(alt_names):
            with cols[idx]:
                inputs[alt][sub] = st.number_input(
                    label + f" for {alt}",
                    min_value=min(lower, upper),
                    max_value=max(lower, upper),
                    value=float((lower + upper) / 2),
                    step=(max(lower, upper) - min(lower, upper)) / 100 if upper != lower else 1.0,
                    key=f"{alt}_{sub}")

    # Calculate final scores
    if st.button("Calculate Final Scores"):
        results = []
        for alt in alt_names:
            total_score = 0.0
            for entry in subcriteria:
                raw = inputs[alt][entry["sub"]]
                u = compute_utility(raw, entry["lower"], entry["upper"], entry["relationship"])
                total_score += u * entry["sub_weight"] * entry["main_weight"]
            results.append({"Alternative": alt, "Final Score (%)": total_score * 100})

        # Display results
        results_df = pd.DataFrame(results).sort_values(by="Final Score (%)", ascending=False)
        st.header("Results & Ranking")
        st.table(results_df)

if __name__ == "__main__":
    main()