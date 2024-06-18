"""
This script allows the user to set an arbitrary top-N list
where N is the top number of countries in a specified region
who received Chinese loans from 2000 to 2021.

To use:
Set your region, and title.

If you want the name of the country to be inside the graph bar, set
words_in_bar to be True. If the bars are too short to be read properly
then sit it to False.

If you specify a selected_year, it will do just that region for that year. 
If you set the year to None it will do the full range from 2000 to 2021.
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def initialize():
    """Initialize settings and configurations."""
    global df_selected_columns, output_chart_title, selected_region, \
        words_in_bar, top_n, selected_year

    ##### SET SELECTED COLUMNS #####
    df_selected_columns = [
        'Recipient',
        'Recipient ISO-3',
        'Recipient Region',
        'Commitment Year',
        'Amount (Original Currency)',
        'Amount (Nominal USD)',
        'Interest Rate',
        'Default Interest Rate'
    ]

    ##### SET WORKING REGION #####
    # Options: 'africa', 'america', 'asia', 'europe'
    selected_region = "america"

    ##### SET GRAPH TITLE #####
    output_chart_title = 'Chinese Loans in South America in 2021'

    ##### DO YOU WANT THE COUNTRY NAME INSIDE THE GRAPH BAR? #####
    words_in_bar = False

    ##### SET TOP N #####
    top_n = 10

    ##### SET YEAR #####
    # Set year between 2000 and 2020
    # If you want the full range, set year for None
    selected_year = 2021


def load_environment():
    global region_df, top_recipients

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

    # Group by 'Recipient' and sum 'Amount (Nominal USD)'
    recipient_sum_region = region_df.groupby(
        'Recipient')['Amount (Nominal USD)'].sum().reset_index()

    # Do the sort, then filter by top_n selected
    top_recipients = recipient_sum_region.sort_values(
        by='Amount (Nominal USD)', ascending=False).head(top_n)

    # Put them in order
    top_recipients = top_recipients.sort_values(
        by='Amount (Nominal USD)', ascending=True)


def plot_graph():
    """This replaces the '1e09' with an actual value at the bottom"""
    def billions(x, pos):
        'The two args are the value and tick position'
        return '%1.1fB' % (x * 1e-9)

    formatter = FuncFormatter(billions)

    plt.figure(figsize=(12, 8))
    bars = plt.barh(top_recipients['Recipient'],
                    top_recipients['Amount (Nominal USD)'])
    plt.xlabel('Total Amount (Nominal USD)')
    plt.ylabel('Recipient' if not words_in_bar else '')
    plt.title(output_chart_title)

    if words_in_bar:
        # Adding the recipient names inside the bars
        for bar, recipient in zip(bars, top_recipients['Recipient']):
            width = bar.get_width()
            plt.text(width - (width * 0.03), bar.get_y() + bar.get_height()/2,
                     recipient, va='center', ha='right', color='white', fontsize=9)
        # Remove y-axis labels
        plt.yticks([])
    else:
        plt.yticks(top_recipients['Recipient'])

    plt.gca().xaxis.set_major_formatter(formatter)
    plt.show()


if __name__ == "__main__":
    initialize()
    load_environment()
    plot_graph()
