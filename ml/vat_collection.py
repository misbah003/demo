import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import argparse

# Set random seed for reproducibility
np.random.seed(42)

def generate_large_dataset(num_clients=5000, num_transactions=50000, years_back=5):
    """
    Generate large-scale synthetic VAT data with realistic patterns

    Parameters:
    num_clients: Number of clients to generate
    num_transactions: Number of transactions to generate
    years_back: Number of years of historical data
    """

    print(f"🎯 Generating large dataset: {num_clients} clients, {num_transactions} transactions, {years_back} years back")

    # ---------------------------
    # 1️⃣ Client Profile (Scalable)
    # ---------------------------
    print("📊 Generating client profiles...")

    # Business types with realistic distributions
    business_types = [
        "Retail", "Pharma", "FMCG", "Automotive", "Textile", "Construction",
        "IT Services", "Hospitality", "Electronics", "Consulting", "Manufacturing",
        "Healthcare", "Education", "Real Estate", "Logistics", "Banking"
    ]

    # Generate client IDs
    client_ids = [f"C{1000 + i}" for i in range(1, num_clients + 1)]

    # Business type distribution (weighted towards common types)
    business_weights = [0.15, 0.12, 0.12, 0.08, 0.08, 0.08, 0.08, 0.06, 0.06, 0.06, 0.05, 0.03, 0.03, 0.02, 0.02, 0.02]
    # Normalize to ensure they sum to 1
    business_weights = np.array(business_weights) / np.sum(business_weights)
    client_business_types = np.random.choice(business_types, size=num_clients, p=business_weights)

    # Annual turnover based on business type
    turnover_ranges = {
        "Retail": (1_000_000, 50_000_000),
        "Pharma": (5_000_000, 200_000_000),
        "FMCG": (10_000_000, 500_000_000),
        "Automotive": (20_000_000, 1_000_000_000),
        "Textile": (500_000, 100_000_000),
        "Construction": (5_000_000, 500_000_000),
        "IT Services": (2_000_000, 100_000_000),
        "Hospitality": (1_000_000, 50_000_000),
        "Electronics": (2_000_000, 100_000_000),
        "Consulting": (500_000, 20_000_000),
        "Manufacturing": (10_000_000, 200_000_000),
        "Healthcare": (5_000_000, 100_000_000),
        "Education": (1_000_000, 50_000_000),
        "Real Estate": (5_000_000, 500_000_000),
        "Logistics": (2_000_000, 100_000_000),
        "Banking": (50_000_000, 2_000_000_000)
    }

    turnovers = []
    for bt in client_business_types:
        min_turnover, max_turnover = turnover_ranges[bt]
        turnover = np.random.lognormal(
            mean=np.log(min_turnover + (max_turnover - min_turnover)/2),
            sigma=0.8
        )
        turnover = np.clip(turnover, min_turnover, max_turnover)
        turnovers.append(int(turnover))

    # Registration dates over the past years_back + 2 years
    start_date = datetime.now() - timedelta(days=365 * (years_back + 2))
    registration_dates = [start_date + timedelta(days=random.randint(0, 365 * (years_back + 2))) for _ in range(num_clients)]

    # Risk scores with business type correlation
    risk_base = {
        "Retail": 0.3, "Pharma": 0.2, "FMCG": 0.25, "Automotive": 0.35,
        "Textile": 0.4, "Construction": 0.45, "IT Services": 0.15,
        "Hospitality": 0.3, "Electronics": 0.2, "Consulting": 0.2,
        "Manufacturing": 0.35, "Healthcare": 0.15, "Education": 0.1,
        "Real Estate": 0.4, "Logistics": 0.35, "Banking": 0.1
    }

    risk_scores = []
    compliance_flags = []
    for bt in client_business_types:
        base_risk = risk_base[bt]
        # Add some randomness around the base risk
        risk = np.clip(np.random.normal(base_risk, 0.15), 0.01, 0.99)
        risk_scores.append(round(risk, 2))
        compliance_flags.append("Non-Compliant" if risk > 0.6 else "Compliant")

    client_profile = pd.DataFrame({
        "Client_ID": client_ids,
        "Business_Type": client_business_types,
        "Annual_Turnover": turnovers,
        "Registration_Date": [d.strftime("%Y-%m-%d") for d in registration_dates],
        "Risk_Score": risk_scores,
        "Compliance_Flag": compliance_flags
    })

    # ---------------------------
    # 2️⃣ Transaction Data (Large Scale with Realistic Patterns)
    # ---------------------------
    print("💰 Generating transaction data...")

    # Generate invoice IDs
    invoice_ids = [f"INV{1000 + i}" for i in range(1, num_transactions + 1)]

    # Geographic distribution (weighted by population/economy)
    regions = ["Maharashtra", "Delhi", "Karnataka", "Gujarat", "Tamil Nadu", "Uttar Pradesh", "Rajasthan", "Kerala", "Punjab", "Haryana"]
    region_weights = [0.18, 0.15, 0.12, 0.10, 0.08, 0.08, 0.07, 0.06, 0.05, 0.05]  # Maharashtra and Delhi have highest weight
    # Normalize to ensure they sum to 1
    region_weights = np.array(region_weights) / np.sum(region_weights)

    # Product categories with VAT rate correlations
    category_vat_map = {
        "Essential Food": "5%",
        "Electronics": "18%",
        "Pharmaceuticals": "12%",
        "Food Products": "5%",
        "Textiles": "5%",
        "IT Services": "18%",
        "Construction": "18%",
        "Hospitality": "18%",
        "Automotive": "18%",
        "Chemicals": "18%",
        "Machinery": "18%",
        "Books": "12%",
        "Education Services": "12%",
        "Healthcare": "12%"
    }

    categories = list(category_vat_map.keys())
    category_weights = [0.15, 0.12, 0.10, 0.10, 0.08, 0.08, 0.06, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03]
    # Normalize to ensure they sum to 1
    category_weights = np.array(category_weights) / np.sum(category_weights)

    # Time period for transactions
    start_date = datetime.now() - timedelta(days=365 * years_back)
    end_date = datetime.now()

    # Client transaction frequency based on business size
    client_transaction_counts = {}
    client_turnover_map = dict(zip(client_profile['Client_ID'], client_profile['Annual_Turnover']))

    # Calculate expected transactions per client based on turnover
    for client_id in client_ids:
        turnover = client_turnover_map[client_id]
        # Larger businesses have more transactions (logarithmic relationship)
        expected_transactions = max(1, int(np.log(turnover / 1_000_000) * 50) + np.random.poisson(20))
        client_transaction_counts[client_id] = expected_transactions

    # Normalize to match total desired transactions
    total_expected = sum(client_transaction_counts.values())
    scale_factor = num_transactions / total_expected

    for client_id in client_transaction_counts:
        client_transaction_counts[client_id] = max(1, int(client_transaction_counts[client_id] * scale_factor))

    # Adjust to exactly match num_transactions
    current_total = sum(client_transaction_counts.values())
    if current_total < num_transactions:
        # Add to largest clients
        largest_clients = sorted(client_transaction_counts.keys(),
                               key=lambda x: client_turnover_map[x], reverse=True)
        for client_id in largest_clients[:num_transactions - current_total]:
            client_transaction_counts[client_id] += 1
    elif current_total > num_transactions:
        # Remove from smallest clients
        smallest_clients = sorted(client_transaction_counts.keys(),
                                key=lambda x: client_transaction_counts[x])
        for client_id in smallest_clients[:current_total - num_transactions]:
            client_transaction_counts[client_id] = max(1, client_transaction_counts[client_id] - 1)

    # Generate economic indicators time series
    print("📈 Generating economic indicators...")
    economic_indicators = generate_economic_indicators(start_date, end_date)

    transactions = []
    invoice_counter = 0

    for client_id in client_ids:
        num_client_transactions = client_transaction_counts[client_id]
        client_region = np.random.choice(regions, p=region_weights)
        client_business_type = client_profile[client_profile['Client_ID'] == client_id]['Business_Type'].iloc[0]

        # Business type influences category preferences
        business_category_weights = get_business_category_weights(client_business_type, categories, category_weights)

        for _ in range(num_client_transactions):
            invoice_counter += 1
            if invoice_counter > num_transactions:
                break

            inv_id = invoice_ids[invoice_counter - 1]

            # Generate date with seasonal patterns
            date = generate_seasonal_date(start_date, end_date)

            # Get economic indicators for this date
            month_key = date.strftime("%Y-%m")
            economic_data = economic_indicators.get(month_key, {
                'inflation_rate': 4.5,
                'gdp_growth': 6.5,
                'usd_inr_rate': 83.0,
                'business_confidence': 55.0
            })

            # Transaction amount based on business type and seasonality
            base_amount = get_business_amount_range(client_business_type)
            seasonal_multiplier = get_seasonal_multiplier(date, client_business_type)
            amount = int(np.random.lognormal(np.log(base_amount[0]), 0.8) * seasonal_multiplier)
            amount = np.clip(amount, 1000, 10_000_000)  # Reasonable bounds

            # Category and VAT rate
            category = np.random.choice(categories, p=business_category_weights)
            vat_rate = category_vat_map[category]
            vat_amount = amount * int(vat_rate.strip('%')) / 100

            # Filing status with risk correlation
            client_risk = client_profile[client_profile['Client_ID'] == client_id]['Risk_Score'].iloc[0]
            filing_status = get_filing_status_with_risk(client_risk, date)

            # Refund eligibility based on business logic
            refund_eligible = get_refund_eligibility(amount, vat_rate, filing_status, client_risk)

            transactions.append([inv_id, client_id, date.strftime("%Y-%m-%d"), amount, vat_rate,
                               round(vat_amount, 2), category, filing_status, refund_eligible, client_region,
                               economic_data['inflation_rate'], economic_data['gdp_growth'],
                               economic_data['usd_inr_rate'], economic_data['business_confidence']])

    transaction_data = pd.DataFrame(transactions, columns=[
        "Invoice_ID", "Client_ID", "Invoice_Date", "Amount", "VAT_Rate",
        "VAT_Amount", "Category", "Filing_Status", "Refund_Eligible", "Region",
        "Inflation_Rate", "GDP_Growth", "USD_INR_Rate", "Business_Confidence"
    ])

    print(f"✅ Generated {len(transactions)} transactions")

    return client_profile, transaction_data

# This old code is replaced by the new scalable generation below

def get_business_category_weights(business_type, categories, base_weights):
    """Adjust category weights based on business type"""
    weights = base_weights.copy()

    # Business-specific category preferences
    preferences = {
        "Retail": ["Electronics", "Food Products", "Textiles"],
        "Pharma": ["Pharmaceuticals", "Chemicals"],
        "FMCG": ["Food Products", "Chemicals", "Essential Food"],
        "Automotive": ["Automotive", "Machinery"],
        "Textile": ["Textiles"],
        "Construction": ["Construction", "Machinery"],
        "IT Services": ["IT Services", "Electronics"],
        "Hospitality": ["Hospitality", "Food Products"],
        "Electronics": ["Electronics"],
        "Consulting": ["IT Services", "Education Services"],
        "Manufacturing": ["Machinery", "Chemicals"],
        "Healthcare": ["Healthcare", "Pharmaceuticals"],
        "Education": ["Education Services", "Books"],
        "Real Estate": ["Construction"],
        "Logistics": ["Machinery"],
        "Banking": ["IT Services"]
    }

    if business_type in preferences:
        preferred_categories = preferences[business_type]
        for i, cat in enumerate(categories):
            if cat in preferred_categories:
                weights[i] *= 3  # Boost preferred categories

    # Normalize weights
    total = sum(weights)
    return [w/total for w in weights]

def get_business_amount_range(business_type):
    """Get typical transaction amount range for business type"""
    ranges = {
        "Retail": (5000, 50000),
        "Pharma": (10000, 100000),
        "FMCG": (20000, 200000),
        "Automotive": (50000, 500000),
        "Textile": (10000, 100000),
        "Construction": (100000, 1000000),
        "IT Services": (25000, 250000),
        "Hospitality": (5000, 50000),
        "Electronics": (10000, 100000),
        "Consulting": (15000, 150000),
        "Manufacturing": (50000, 500000),
        "Healthcare": (5000, 50000),
        "Education": (5000, 30000),
        "Real Estate": (100000, 2000000),
        "Logistics": (20000, 200000),
        "Banking": (10000, 100000)
    }
    return ranges.get(business_type, (5000, 50000))

def generate_seasonal_date(start_date, end_date):
    """Generate date with enhanced seasonal patterns and economic indicators"""
    # Enhanced seasonal patterns with economic cycles
    base_month_weights = [0.08, 0.07, 0.08, 0.09, 0.08, 0.07, 0.09, 0.08, 0.08, 0.09, 0.10, 0.09]

    # Add economic cycle effects (simulate GDP growth patterns)
    economic_cycle = []
    for i, weight in enumerate(base_month_weights):
        month = i + 1
        year_progress = (month - 1) / 11  # 0 to 1 throughout year

        # Economic growth typically peaks in Q4, slows in Q1
        if month in [10, 11, 12]:  # Q4 - peak season
            economic_multiplier = 1.15
        elif month in [1, 2]:  # Q1 - post-holiday slowdown
            economic_multiplier = 0.85
        elif month in [3, 4]:  # Q2 - recovery
            economic_multiplier = 1.05
        else:  # Q3 - stable
            economic_multiplier = 1.0

        # Add festival effects
        if month == 10:  # October - Diwali season
            economic_multiplier *= 1.25
        elif month == 11:  # November - Wedding season
            economic_multiplier *= 1.1
        elif month == 12:  # December - Holiday shopping
            economic_multiplier *= 1.3

        economic_cycle.append(weight * economic_multiplier)

    # Normalize month weights
    month_weights = np.array(economic_cycle) / np.sum(economic_cycle)

    total_days = (end_date - start_date).days
    day_weights = np.array([month_weights[(start_date + timedelta(days=i)).month - 1] for i in range(total_days)])
    day_weights = day_weights / np.sum(day_weights)  # Normalize day weights

    random_day = np.random.choice(range(total_days), p=day_weights)

    return start_date + timedelta(days=int(random_day))

def get_seasonal_multiplier(date, business_type):
    """Get seasonal multiplier for transaction amounts"""
    month = date.month

    # Base seasonal patterns
    seasonal_multipliers = {
        1: 0.9,   # January - post-holiday slowdown
        2: 0.85,  # February - low activity
        3: 1.0,   # March - normal
        4: 1.05,  # April - start of new financial year
        5: 1.0,   # May
        6: 1.0,   # June
        7: 0.95,  # July - monsoon
        8: 0.95,  # August - monsoon
        9: 1.0,   # September
        10: 1.1,  # October - festival season
        11: 1.15, # November - high activity
        12: 1.2   # December - holiday season
    }

    multiplier = seasonal_multipliers[month]

    # Business-specific adjustments
    if business_type == "Hospitality":
        if month in [10, 11, 12]:  # Wedding/festival season
            multiplier *= 1.3
    elif business_type == "Retail":
        if month == 12:  # Christmas shopping
            multiplier *= 1.4
    elif business_type == "Construction":
        if month in [3, 4, 5]:  # Good weather months
            multiplier *= 1.2

    return multiplier

def get_filing_status_with_risk(risk_score, date):
    """Determine filing status based on risk score and date"""
    # High risk clients are more likely to file late or not at all
    if risk_score > 0.8:
        return np.random.choice(["Filed", "Filed Late", "Not Filed"], p=[0.3, 0.4, 0.3])
    elif risk_score > 0.6:
        return np.random.choice(["Filed", "Filed Late", "Not Filed"], p=[0.5, 0.4, 0.1])
    elif risk_score > 0.3:
        return np.random.choice(["Filed", "Filed Late", "Not Filed"], p=[0.7, 0.25, 0.05])
    else:
        return np.random.choice(["Filed", "Filed Late", "Not Filed"], p=[0.85, 0.14, 0.01])

def get_refund_eligibility(amount, vat_rate, filing_status, risk_score):
    """Determine refund eligibility based on business rules"""
    # Basic eligibility criteria
    if filing_status == "Not Filed":
        return "No"

    # Large amounts are more likely to be eligible
    amount_factor = min(amount / 100000, 1.0)  # Cap at 1.0

    # Lower VAT rates have higher eligibility (input VAT vs output VAT logic)
    vat_factor = 1.0 if vat_rate in ["5%", "12%"] else 0.7

    # Low risk clients more likely to get refunds
    risk_factor = 1.0 - risk_score

    # Late filing reduces eligibility
    filing_factor = 0.6 if filing_status == "Filed Late" else 1.0

    probability = amount_factor * vat_factor * risk_factor * filing_factor

    return "Yes" if random.random() < probability else "No"

def generate_economic_indicators(start_date, end_date):
    """Generate realistic economic indicators time series"""
    economic_data = {}

    # Generate monthly economic data
    current_date = start_date.replace(day=1)
    while current_date <= end_date:
        month_key = current_date.strftime("%Y-%m")

        # Base values with realistic ranges for Indian economy
        base_inflation = 4.5  # Average Indian inflation
        base_gdp_growth = 6.5  # Average Indian GDP growth
        base_usd_inr = 83.0  # Average USD-INR rate
        base_confidence = 55.0  # Business confidence index

        # Add temporal variations
        year = current_date.year
        month = current_date.month

        # Inflation trends (higher during certain periods)
        inflation_trend = 0
        if year >= 2020:  # Post-COVID inflation surge
            inflation_trend += 2.0
        if month in [10, 11, 12]:  # Festival season inflation
            inflation_trend += 1.5

        # GDP growth cycles
        gdp_trend = 0
        if year in [2019, 2020]:  # COVID impact
            gdp_trend -= 2.0
        elif year >= 2021:  # Recovery
            gdp_trend += 1.0

        # USD-INR volatility (higher during global uncertainty)
        usd_trend = 0
        if year == 2020:  # COVID volatility
            usd_trend += 5.0
        elif year >= 2022:  # Geopolitical tensions
            usd_trend += 3.0

        # Business confidence (affected by economic conditions)
        confidence_trend = 0
        if year == 2020:
            confidence_trend -= 15.0  # COVID impact
        elif year >= 2021:
            confidence_trend += 10.0  # Recovery

        # Add random noise
        inflation_noise = np.random.normal(0, 0.8)
        gdp_noise = np.random.normal(0, 0.5)
        usd_noise = np.random.normal(0, 2.0)
        confidence_noise = np.random.normal(0, 5.0)

        # Calculate final values
        inflation_rate = max(2.0, min(9.0, base_inflation + inflation_trend + inflation_noise))
        gdp_growth = max(3.0, min(9.0, base_gdp_growth + gdp_trend + gdp_noise))
        usd_inr_rate = max(70.0, min(90.0, base_usd_inr + usd_trend + usd_noise))
        business_confidence = max(30.0, min(80.0, base_confidence + confidence_trend + confidence_noise))

        economic_data[month_key] = {
            'inflation_rate': round(inflation_rate, 2),
            'gdp_growth': round(gdp_growth, 2),
            'usd_inr_rate': round(usd_inr_rate, 2),
            'business_confidence': round(business_confidence, 1)
        }

        # Move to next month
        if month == 12:
            current_date = current_date.replace(year=year + 1, month=1)
        else:
            current_date = current_date.replace(month=month + 1)

    return economic_data

# ---------------------------
# Main execution with command line arguments
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate large-scale synthetic VAT data")
    parser.add_argument("--clients", type=int, default=5000, help="Number of clients to generate")
    parser.add_argument("--transactions", type=int, default=50000, help="Number of transactions to generate")
    parser.add_argument("--years", type=int, default=5, help="Number of years of historical data")

    args = parser.parse_args()

    # Generate large dataset
    client_profile, transaction_data = generate_large_dataset(
        num_clients=args.clients,
        num_transactions=args.transactions,
        years_back=args.years
    )

    # ---------------------------
    # 3️⃣ Tax Notices (scalable based on clients)
    # ---------------------------
    print("📄 Generating tax notices...")

    notice_texts = [
        "Your VAT filing for the previous quarter is overdue.",
        "Refund request approved and will be processed soon.",
        "Audit scheduled due to discrepancies in invoices.",
        "Document mismatch found during validation process.",
        "Penalty imposed for late submission of returns.",
        "Compliance check completed successfully.",
        "Quarterly VAT submission reminder.",
        "Annual return filing is due within 30 days.",
        "Input tax credit verification completed.",
        "Business registration renewal reminder."
    ]
    notice_classes = ["Filing Reminder", "Refund Approval", "Audit Notification",
                     "Document Alert", "Penalty Notice", "Compliance Notice",
                     "Registration Alert", "Credit Verification"]

    # Generate notices based on client risk scores
    tax_notices = []
    high_risk_clients = client_profile[client_profile['Risk_Score'] > 0.6]['Client_ID'].tolist()

    # All clients get at least some notices, high-risk get more
    for client_id in client_profile['Client_ID']:
        risk_score = client_profile[client_profile['Client_ID'] == client_id]['Risk_Score'].iloc[0]

        # Number of notices based on risk
        num_notices = np.random.poisson(max(1, risk_score * 5))

        for i in range(num_notices):
            notice_id = f"N{1000 + len(tax_notices) + 1}"
            text = random.choice(notice_texts)
            classification = random.choice(notice_classes)
            tax_notices.append([notice_id, client_id, text, classification])

    tax_notices = pd.DataFrame(tax_notices, columns=["Notice_ID", "Client_ID", "Text", "Classification"])
    print(f"✅ Generated {len(tax_notices)} tax notices")

    # ---------------------------
    # 4️⃣ Monthly Filing Summary (scalable)
    # ---------------------------
    print("📊 Generating monthly filing summaries...")

    # Generate months for the past years_back + current year
    start_date = datetime.now() - timedelta(days=365 * args.years)
    months = pd.date_range(start_date.strftime("%Y-01-01"), datetime.now().strftime("%Y-12-01"), freq="MS").strftime("%Y-%m").tolist()

    summary_records = []

    for client_id in client_profile['Client_ID']:
        client_risk = client_profile[client_profile['Client_ID'] == client_id]['Risk_Score'].iloc[0]

        for month in months:
            # Get actual transaction data for this client and month
            client_transactions = transaction_data[
                (transaction_data['Client_ID'] == client_id) &
                (transaction_data['Invoice_Date'].str.startswith(month))
            ]

            if len(client_transactions) > 0:
                total_sales = client_transactions['Amount'].sum()
                total_vat = client_transactions['VAT_Amount'].sum()

                # Filing status based on risk and actual transaction count
                if len(client_transactions) > 10:  # Active clients
                    filing_prob = max(0.1, 1.0 - client_risk)
                    filed = "Yes" if random.random() < filing_prob else "No"
                else:
                    filed = random.choice(["Yes", "No"])

                refund_claimed = "Yes" if (filed == "Yes" and
                                          client_transactions['Refund_Eligible'].eq('Yes').any()) else "No"

                filing_date = None if filed == "No" else (datetime.strptime(month + "-01", "%Y-%m-%d") +
                                                         timedelta(days=random.randint(20, 40))).strftime("%Y-%m-%d")
            else:
                # No transactions this month
                total_sales = 0
                total_vat = 0
                filed = "No"
                refund_claimed = "No"
                filing_date = None

            summary_records.append([client_id, month, total_sales, total_vat, filing_date, filed, refund_claimed])

    monthly_summary = pd.DataFrame(summary_records, columns=[
        "Client_ID", "Month", "Total_Sales", "Total_VAT", "Filing_Date", "Filed_On_Time", "Refund_Claimed"
    ])

    print(f"✅ Generated {len(monthly_summary)} monthly summaries")

    # ---------------------------
    # 5️⃣ Write to Excel File
    # ---------------------------
    print("💾 Saving to Excel file...")

    with pd.ExcelWriter("../data/AI_Tax_Intelligence_Large.xlsx", engine="openpyxl") as writer:
        transaction_data.to_excel(writer, sheet_name="Transaction_Data", index=False)
        client_profile.to_excel(writer, sheet_name="Client_Profile", index=False)
        tax_notices.to_excel(writer, sheet_name="Tax_Notices", index=False)
        monthly_summary.to_excel(writer, sheet_name="Monthly_Filing_Summary", index=False)

    print(f"✅ Large dataset created successfully: '../data/AI_Tax_Intelligence_Large.xlsx'")
    print(f"   📊 {len(client_profile)} clients")
    print(f"   💰 {len(transaction_data)} transactions")
    print(f"   📄 {len(tax_notices)} tax notices")
    print(f"   📈 {len(monthly_summary)} monthly summaries")
