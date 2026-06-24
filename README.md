# Community Health Screening & Ration Prioritization Tool

An automated Python tool designed for community health workers to analyze child nutritional data using Mid-Upper Arm Circumference (MUAC) measurements. This code classifies individual malnutrition statuses, flags urgent medical referral cases, and ranks villages based on overall intervention need to optimize emergency ration distribution.

## 📋 Project Overview

In resource-limited settings, timely and accurate triage of nutritional data is critical. This project simulates an end-to-end data pipeline that:
1. **Classifies** individual child screening metrics based on international health standards.
2. **Alerts** clinical teams to immediate, life-threatening cases of Severe Acute Malnutrition (SAM).
3. **Aggregates and Filters** raw field screening data by geographic zones.
4. **Prioritizes Logistics** by ranking villages based on their combined burden of acute malnutrition to guide targeted humanitarian relief.

---

## 🛠️ Methodology & Thresholds

The application categorizes children under 5 years old using standard medical MUAC (Mid-Upper Arm Circumference) millimeter thresholds:

| MUAC Metric (mm) | Classification | Status / Action Required |
| :--- | :--- | :--- |
| `< 115 mm` | **SAM** (Severe Acute Malnutrition) | **Critical** - Immediate Urgent Medical Referral |
| `115 mm – 124 mm` | **MAM** (Moderate Acute Malnutrition) | **Moderate** - Enrolled in Targeted Ration Program |
| `≥ 125 mm` | **Normal** | **Healthy** - Routine Monitoring |

---

## 💻 Architecture & Pipeline Steps

The program processes the field data sequentially through the following pipeline:

* **Step 1: Classification Engine:** An optimized boundary-check function categorizes individual MUAC inputs.
* **Step 2: Operational Triage Loop:** A single-pass loop over raw screening inputs that handles real-time terminal logging, issues instant critical-case alerts, and splits records into specific state-retaining arrays (`sam_cases`, `mam_cases`, `normal_cases`).
* **Step 3: Unique Demographic Discovery:** Dynamically extracts a clean roster of participating villages without hardcoding.
* **Step 4 & 5: Need Aggregation:** Cross-references the triage arrays against individual village data to compile a comprehensive `ranking` matrix.
* **Step 6 & 7: Analytical Reporting:** Sorts the data using stable algorithmic sorting to output a logistics prioritization list alongside cumulative screening statistics.
* **Step 8: Statistical Analysis (Bonus):** Computes descriptive statistics (mean MUAC vectors) across different cohorts to evaluate population-level variances.

---
