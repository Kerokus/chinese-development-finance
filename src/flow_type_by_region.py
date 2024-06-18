"""
This script generates a bar chart of the types of payments to 
the countries within a region (e.g., "Loan", "Grant" etc).

If you want the name of the country to be inside the graph bar, set
words_in_bar to be True. If the bars are too short to be read properly
then sit it to False.

If you specify a selected_year, it will do just that region for that year. 
If you set the year to None it will do the full range from 2000 to 2021.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def initialize():
    """Initialize settings and configurations."""
    global df_selected_columns, output_chart_title, selected_region, \
        words_in_bar, selected_year

    ##### SET SELECTED COLUMNS #####
    df_selected_columns = [
        'Recipient',
        'Recipient ISO-3',
        'Recipient Region',
        'Commitment Year',
        'Amount (Original Currency)',
        'Amount (Nominal USD)',
        'Interest Rate',
        'Default Interest Rate',
        'Flow Type Simplified'
    ]

    ##### SET WORKING REGION #####
    # Options: 'africa', 'america', 'asia', 'europe'
    selected_region = "america"

    ##### SET GRAPH TITLE #####
    output_chart_title = 'Payment types for Africa from 2000 to 2021'

    ##### DO YOU WANT THE COUNTRY NAME INSIDE THE GRAPH BAR? #####
    words_in_bar = False

    ##### SET YEAR #####
    # Set year between 2000 and 2025
    # If you want the full range, set year to None
    selected_year = None


def load_environment():
    """Load the dataset and prepare the environment."""
    global region_df, flow_type_summary

    # Load dataset
    input_dataset = "../data/chinese_loan_data.csv"
    input_raw_df = pd.read_csv(input_dataset, low_memory=False)
    input_clean_df = input_raw_df[df_selected_columns]

    # Filter the DataFrame to include only rows where 'Recipient Region' matches the selected region
    region_df = input_clean_df[input_clean_df['Recipient Region'].str.lower(
    ) == selected_region]

    # Ensure 'Commitment Year' is an integer
    region_df['Commitment Year'] = region_df['Commitment Year'].astype(int)

    # Filter by the selected year if specified
    if selected_year is not None:
        region_df = region_df[region_df['Commitment Year'] == selected_year]

    # Group by 'Flow Type Simplified' and sum 'Amount (Nominal USD)'
    flow_type_summary = region_df.groupby('Flow Type Simplified')[
        'Amount (Nominal USD)'].sum().reset_index()

    # Sort the flow type summary by 'Amount (Nominal USD)' for better visualization
    flow_type_summary = flow_type_summary.sort_values(
        by='Amount (Nominal USD)', ascending=True)


def plot_graph():
    """Plot the bar chart."""
    def billions(x, pos):
        'The two args are the value and tick position'
        return '%1.1fB' % (x * 1e-9)

    formatter = FuncFormatter(billions)

    plt.figure(figsize=(12, 8))
    bars = plt.barh(flow_type_summary['Flow Type Simplified'],
                    flow_type_summary['Amount (Nominal USD)'])
    plt.xlabel('Total Amount (Nominal USD)')
    plt.ylabel('Flow Type Simplified' if not words_in_bar else '')
    plt.title(output_chart_title)

    if words_in_bar:
        # Adding the flow type names inside the bars
        for bar, flow_type in zip(bars, flow_type_summary['Flow Type Simplified']):
            width = bar.get_width()
            plt.text(width - (width * 0.03), bar.get_y() + bar.get_height()/2,
                     flow_type, va='center', ha='right', color='white', fontsize=9)
        # Remove y-axis labels
        plt.yticks([])
    else:
        plt.yticks(flow_type_summary['Flow Type Simplified'])

    plt.gca().xaxis.set_major_formatter(formatter)
    plt.show()


if __name__ == "__main__":
    initialize()
    load_environment()
    plot_graph()
