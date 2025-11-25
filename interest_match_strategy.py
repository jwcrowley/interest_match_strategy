import matplotlib.pyplot as plt
import numpy as np

# --- 1. Define Loan Parameters ---
principal = 500000  # Loan amount
annual_rate = 0.04  # Annual interest rate
years = 30  # Loan term in years
extra_payment_floor = 1000  # Minimum extra payment for the Hybrid Strategy

# --- 2. Calculate Standard Monthly Payment ---
monthly_rate = annual_rate / 12
num_payments = years * 12

if monthly_rate == 0:
    standard_payment = principal / num_payments
else:
    standard_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

# --- 3. Model the Interest-Matching Strategy ---
balance_match = principal
balances_match = [principal]
interest_payments_match = [0]
total_payment_match_list = [0]
month_match = 0
while balance_match > 0:
    month_match += 1
    interest_payment_match = balance_match * monthly_rate
    principal_payment_standard = standard_payment - interest_payment_match
    additional_payment_match = interest_payment_match
    total_payment_match = standard_payment + additional_payment_match
    total_principal_reduction_match = principal_payment_standard + additional_payment_match
    new_balance_match = balance_match - total_principal_reduction_match
    if new_balance_match < 0: new_balance_match = 0
    
    balances_match.append(new_balance_match)
    interest_payments_match.append(interest_payment_match)
    total_payment_match_list.append(total_payment_match)
    balance_match = new_balance_match

# --- 3b. Model the Hybrid Strategy ---
balance_hybrid = principal
balances_hybrid = [principal]
interest_payments_hybrid = [0]
total_payment_hybrid_list = [0]
month_hybrid = 0
while balance_hybrid > 0:
    month_hybrid += 1
    interest_payment_hybrid = balance_hybrid * monthly_rate
    principal_payment_standard = standard_payment - interest_payment_hybrid
    additional_payment_hybrid = max(interest_payment_hybrid, extra_payment_floor)
    total_payment_hybrid = standard_payment + additional_payment_hybrid
    total_principal_reduction_hybrid = principal_payment_standard + additional_payment_hybrid
    new_balance_hybrid = balance_hybrid - total_principal_reduction_hybrid
    if new_balance_hybrid < 0: new_balance_hybrid = 0

    balances_hybrid.append(new_balance_hybrid)
    interest_payments_hybrid.append(interest_payment_hybrid)
    total_payment_hybrid_list.append(total_payment_hybrid)
    balance_hybrid = new_balance_hybrid

# --- 4. Prepare Data for Plotting ---
# Standard Loan Data
months_standard = np.arange(0, num_payments + 1)
balances_standard = principal * ((1 + monthly_rate)**num_payments - (1 + monthly_rate)**months_standard) / ((1 + monthly_rate)**num_payments - 1)
cumulative_interest_standard = np.array([standard_payment * m - (principal - balances_standard[m]) for m in range(num_payments + 1)])
cumulative_principal_standard = principal - balances_standard
cumulative_paid_standard = months_standard * standard_payment

# Interest-Matching Data
months_match_plot = np.arange(0, month_match + 1)
cumulative_interest_match = np.cumsum(interest_payments_match)
cumulative_principal_match = principal - np.array(balances_match)
cumulative_paid_match = np.cumsum(total_payment_match_list)

# Hybrid Strategy Data
months_hybrid_plot = np.arange(0, month_hybrid + 1)
cumulative_interest_hybrid = np.cumsum(interest_payments_hybrid)
cumulative_principal_hybrid = principal - np.array(balances_hybrid)
cumulative_paid_hybrid = np.cumsum(total_payment_hybrid_list)

# --- 5. Create the Visual Dashboard (ADDITIVE) ---
plt.switch_backend('Agg') 
# Increased height again to accommodate all charts
fig = plt.figure(figsize=(18, 20)) 
fig.suptitle('Mortgage Acceleration Strategy: One-Page Report', fontsize=28, weight='bold')

# Define the new 6-row layout
layout = """
    IIII
    ABCD
    EEEE
    FFFF
    GGGG
    HHHH
"""
ax_dict = fig.subplot_mosaic(layout)

# --- Inputs & Key Insights Banner (Row I) ---
ax_dict['I'].axis('off')
inputs_text = (
    rf"Loan Inputs: Principal: \${principal:,.0f} | Rate: {annual_rate*100:.1f}% | Term: {years} years | Hybrid Floor: \${extra_payment_floor:,.0f}"
)
ax_dict['I'].text(0.5, 0.7, inputs_text, ha='center', va='center', fontsize=16, weight='bold',
                  bbox=dict(boxstyle='round,pad=0.5', fc='lightsteelblue', alpha=0.8))

hybrid_interest_savings = ((standard_payment * num_payments) - principal) - (cumulative_interest_hybrid[-1])
insight_text = (
    rf"Key Insight: The Hybrid strategy saves \${hybrid_interest_savings:,.0f} in total interest and pays off the loan {years - (month_hybrid/12):.1f} years earlier."
)
ax_dict['I'].text(0.5, 0.2, insight_text, ha='center', va='center', fontsize=14,
                  bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.8))

# --- KPIs (Top Row - 4 Boxes) ---
years_saved_match = years - (month_match / 12)
interest_saved_match = ((standard_payment * num_payments) - principal) - (cumulative_interest_match[-1])
years_saved_hybrid = years - (month_hybrid / 12)
interest_saved_hybrid = ((standard_payment * num_payments) - principal) - (cumulative_interest_hybrid[-1])

ax_dict['A'].text(0.5, 0.5, f'{years_saved_match:.1f}', ha='center', va='center', fontsize=42, weight='bold', color='#2E8B57')
ax_dict['A'].text(0.5, 0.2, 'Years Saved\n(Interest-Match)', ha='center', va='center', fontsize=14, color='grey')
ax_dict['A'].set_xticks([]); ax_dict['A'].set_yticks([])

ax_dict['B'].text(0.5, 0.5, f'${interest_saved_match:,.0f}', ha='center', va='center', fontsize=42, weight='bold', color='#4169E1')
ax_dict['B'].text(0.5, 0.2, 'Interest Saved\n(Interest-Match)', ha='center', va='center', fontsize=14, color='grey')
ax_dict['B'].set_xticks([]); ax_dict['B'].set_yticks([])

ax_dict['C'].text(0.5, 0.5, f'{years_saved_hybrid:.1f}', ha='center', va='center', fontsize=42, weight='bold', color='#2E8B57')
ax_dict['C'].text(0.5, 0.2, 'Years Saved\n(Hybrid)', ha='center', va='center', fontsize=14, color='grey')
ax_dict['C'].set_xticks([]); ax_dict['C'].set_yticks([])

ax_dict['D'].text(0.5, 0.5, f'${interest_saved_hybrid:,.0f}', ha='center', va='center', fontsize=42, weight='bold', color='#4169E1')
ax_dict['D'].text(0.5, 0.2, 'Interest Saved\n(Hybrid)', ha='center', va='center', fontsize=14, color='grey')
ax_dict['D'].set_xticks([]); ax_dict['D'].set_yticks([])

# --- Main Plot: Loan Balance (Row E) ---
ax_dict['E'].plot(months_standard, balances_standard, label='Standard Plan', color='skyblue', linewidth=3)
ax_dict['E'].plot(months_match_plot, balances_match, label='Interest-Match Strategy', color='salmon', linewidth=3)
ax_dict['E'].plot(months_hybrid_plot, balances_hybrid, label=f'Hybrid Strategy (Floor: ${extra_payment_floor:,.0f})', color='mediumseagreen', linewidth=3, linestyle='--')
ax_dict['E'].set_title('Loan Balance Over Time', fontsize=18, weight='bold')
ax_dict['E'].set_ylabel('Loan Balance ($)', fontsize=12)
ax_dict['E'].legend(loc='upper right')
ax_dict['E'].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
ax_dict['E'].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/12)}' if x%12==0 else ''))

# --- Cash Flow Plot (Row F) ---
ax_dict['F'].plot(months_standard, np.full_like(months_standard, standard_payment), label='Standard', color='skyblue', linewidth=3)
ax_dict['F'].plot(months_match_plot, total_payment_match_list, label='Interest-Match', color='salmon', linewidth=3)
ax_dict['F'].plot(months_hybrid_plot, total_payment_hybrid_list, label=f'Hybrid', color='mediumseagreen', linewidth=3, linestyle='--')
ax_dict['F'].set_title('Total Monthly Payment (Cash Flow)', fontsize=18, weight='bold')
ax_dict['F'].set_xlabel('Time (Years)', fontsize=12)
ax_dict['F'].set_ylabel('Payment Amount ($)', fontsize=12)
ax_dict['F'].legend(loc='upper right')
ax_dict['F'].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax_dict['F'].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/12)}' if x%12==0 else ''))

# --- Cumulative Cost Plot (Row G) ---
ax_dict['G'].plot(months_standard, cumulative_principal_standard, label='Principal (Standard)', color='skyblue', linewidth=2)
ax_dict['G'].plot(months_standard, cumulative_interest_standard, label='Interest (Standard)', color='orange', linewidth=2)
ax_dict['G'].plot(months_match_plot, cumulative_principal_match, label='Principal (Interest-Match)', color='darkred', linewidth=2, linestyle='--')
ax_dict['G'].plot(months_match_plot, cumulative_interest_match, label='Interest (Interest-Match)', color='firebrick', linewidth=2, linestyle='--')
ax_dict['G'].plot(months_hybrid_plot, cumulative_principal_hybrid, label='Principal (Hybrid)', color='darkgreen', linewidth=2, linestyle=':')
ax_dict['G'].plot(months_hybrid_plot, cumulative_interest_hybrid, label='Interest (Hybrid)', color='olivedrab', linewidth=2, linestyle=':')
ax_dict['G'].set_title('Cumulative Principal vs. Interest Paid', fontsize=18, weight='bold')
ax_dict['G'].set_xlabel('Time (Years)', fontsize=12)
ax_dict['G'].set_ylabel('Cumulative Amount Paid ($)', fontsize=12)
ax_dict['G'].legend(loc='upper left', fontsize=10)
ax_dict['G'].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
ax_dict['G'].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/12)}' if x%12==0 else ''))

# --- Detailed Comparison Table (Row H) ---
ax_dict['H'].axis('off')
total_paid_standard = principal + cumulative_interest_standard[-1]
total_paid_match = principal + cumulative_interest_match[-1]
total_paid_hybrid = principal + cumulative_interest_hybrid[-1]

table_data = [
    ['Metric', 'Standard Plan', 'Interest-Match', f'Hybrid (${extra_payment_floor:,.0f} floor)'],
    ['Payoff Time', f'{years} years', f'{month_match/12:.1f} years', f'{month_hybrid/12:.1f} years'],
    ['Total Interest Paid', f'${cumulative_interest_standard[-1]:,.0f}', f'${cumulative_interest_match[-1]:,.0f}', f'${cumulative_interest_hybrid[-1]:,.0f}'],
    ['Total Amount Paid', f'${total_paid_standard:,.0f}', f'${total_paid_match:,.0f}', f'${total_paid_hybrid:,.0f}'],
    ['Years Saved', 'N/A', f'{years - (month_match/12):.1f} years', f'{years - (month_hybrid/12):.1f} years'],
    ['Interest Saved', 'N/A', f'${(cumulative_interest_standard[-1] - cumulative_interest_match[-1]):,.0f}', f'${(cumulative_interest_standard[-1] - cumulative_interest_hybrid[-1]):,.0f}'],
]
table = ax_dict['H'].table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 2)
ax_dict['H'].set_title('Detailed Strategy Comparison', fontsize=18, weight='bold', pad=20)

# --- Save the Figure ---
# Adjusted rect for more space at the bottom
fig.tight_layout(rect=[0, 0.03, 1, 0.96])

output_filename = 'mortgage_one_page_report_all_charts.png'
plt.savefig(output_filename, dpi=300)
print(f"Plot successfully saved to {output_filename}")

# --- 6. Print Final Summary ---
print("\n--- Mortgage Payoff Summary ---")
print(f"Initial Loan Amount: ${principal:,.2f}")
print(f"Annual Interest Rate: {annual_rate*100:.2f}%")
print("-" * 30)
print(f"Standard Plan:")
print(f"  - Payoff Time: {years} years")
print(f"  - Total Interest: ${cumulative_interest_standard[-1]:,.2f}")
print("-" * 30)
print(f"Interest-Matching Strategy:")
print(f"  - Payoff Time: {month_match} months ({month_match/12:.1f} years)")
print(f"  - Total Interest: ${cumulative_interest_match[-1]:,.2f}")
print("-" * 30)
print(f"Hybrid Strategy (Floor: ${extra_payment_floor:,.0f}):")
print(f"  - Payoff Time: {month_hybrid} months ({month_hybrid/12:.1f} years)")
print(f"  - Total Interest: ${cumulative_interest_hybrid[-1]:,.2f}")
print("-" * 30)
