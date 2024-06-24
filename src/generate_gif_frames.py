"""
This script generates a series of single images (frames) of Chinese loans in a user specified region 
to be used for creating an animated GIF. The script filters the dataset for the 
specified region, groups the data by recipient (country) and year, and saves each 
frame as an image in the specified output directory.

Usage:
- Ensure that the necessary directories exist and adjust the paths as needed.
- Set the input dataset path and output directory in the initialization section.
- Define the columns to be used and the region to filter the data.
- Run the script to generate and save the frames.

Example:
    $ python generate_frames.py
"""

import os
import pandas as pd
import plotly.express as px
import plotly.io as pio


def initialize():
    global input_dataset, output_directory, df_selected_columns, selected_region, \
        output_map_scope, output_map_title
    ##### SET FILE LOCATIONS #####
    input_dataset = "../data/chinese_loan_data.csv"
    output_directory = "../img/europe/gif_frames"

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

    ##### SET WORKING REGIONS #####
    # Options: 'africa', 'america', 'asia', 'europe'
    selected_region = "europe"

    # Select what map you want displayed.
    # Options: 'africa', 'asia', 'europe', 'north america', 'south america', 'usa', 'world'
    output_map_scope = 'europe'
    output_map_title = 'Chinese Loans in Europe from 2000 to 2021'


def load_environment():
    global input_raw_df, input_clean_df, region_df, recipient_sum_yearly
    input_raw_df = pd.read_csv(input_dataset, low_memory=False)
    input_clean_df = input_raw_df[df_selected_columns]

    # Filter based on selected region
    region_df = input_clean_df[input_clean_df['Recipient Region'].str.lower(
    ) == selected_region]

    # Ran into weird looping errors because the year wasn't properly set as an integer
    # It would start in 2000, go through 2021, then loop into 2002 and 2005
    region_df.loc[:, 'Commitment Year'] = region_df['Commitment Year'].astype(
        int)

    # Group by 'Recipient' and 'Commitment Year', then sum 'Amount (Nominal USD)'
    recipient_sum_yearly = region_df.groupby(['Recipient', 'Commitment Year'])[
        'Amount (Nominal USD)'].sum().reset_index()

    # Now that they're integers, we sort to fix the looping error.
    recipient_sum_yearly = recipient_sum_yearly.sort_values(
        by='Commitment Year')


def main():
    # Create the animated choropleth map using Plotly
    fig = px.choropleth(recipient_sum_yearly,
                        locations='Recipient',
                        locationmode='country names',
                        color='Amount (Nominal USD)',
                        hover_name='Recipient',
                        animation_frame='Commitment Year',
                        color_continuous_scale='Algae',
                        scope=output_map_scope,
                        title=output_map_title)

    fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                    showland=True, landcolor="White")

    # Make sure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Save each frame as an image
    # We have to update each year on the bottom slider
    # Or else it'll be stuck at "Commitment Year=2000"
    for frame in fig.frames:
        fig.update(data=frame.data)
        frame_year_index = int(frame.name) - \
            recipient_sum_yearly['Commitment Year'].min()
        fig.layout.sliders[0]['active'] = frame_year_index
        frame_image_path = os.path.join(output_directory, f"{frame.name}.png")
        pio.write_image(fig, frame_image_path)

    print(f"Frames saved in {output_directory}")


if __name__ == "__main__":
    initialize()
    load_environment()
    main()
