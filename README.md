# Mortgage Acceleration Strategy Visualizer

A Python script to model and visualize the powerful financial impact of an aggressive mortgage prepayment strategy. This tool generates a detailed visual dashboard and a text summary, allowing you to see exactly how much time and money you can save by matching your interest payment with an additional principal payment each month.

## The "Interest-Matching Strategy" Explained

This strategy is simple but incredibly effective. Each month, you make your standard mortgage payment, **plus** an additional payment that is equal to the interest portion of that month's payment.

**Logic:**
*   A standard payment is `Principal + Interest`.
*   With this strategy, your total payment becomes `(Principal + Interest) + Interest`.
*   This means your entire monthly interest charge is converted into an extra principal payment, dramatically accelerating the amortization of your loan.

## Key Features

*   **Models the Strategy:** Accurately calculates the new loan term and total interest paid.
*   **Visual Dashboard:** Generates a professional, multi-panel PNG image (`mortgage_dashboard.png`) showing:
    *   Key Performance Indicators (Years Saved, Interest Saved).
    *   A comparison of loan balances over time.
    *   A breakdown of cumulative principal vs. interest paid.
*   **Text Summary:** Prints a clear, concise summary of the results to the console.
*   **Remote-Ready:** Configured by default to save a plot file, making it perfect for remote servers without a GUI.
*   **Easily Customizable:** Loan parameters can be changed directly in the script.

## Prerequisites

*   Python 3.6+
*   The required Python libraries are listed in `requirements.txt`.

## Installation & Setup

It's highly recommended to use a virtual environment to manage dependencies.

1.  **Clone or download the project files.**
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```
3.  **Activate the virtual environment:**
    *   On macOS/Linux: `source venv/bin/activate`
    *   On Windows: `.\venv\Scripts\activate`
4.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Step 1: Configure Your Loan

Open the `dashboard_strategy.py` file and edit the loan parameters at the top of the script:

```python
# --- 1. Define Loan Parameters ---
principal = 500000  # Loan amount
annual_rate = 0.04  # Annual interest rate
years = 30          # Loan term in years
