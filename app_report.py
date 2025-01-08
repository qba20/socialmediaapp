import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shiny import App, render, ui, reactive
import app_values
from pathlib import Path

def load_json_data(file_path):

    #Load JSON campaign data and convert to DataFrame
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Convert to DataFrame
        df = pd.json_normalize(data['data'])

        # Convert date columns if they exist
        if 'date_start' in df.columns:
            df['date_start'] = pd.to_datetime(df['date_start'])
        if 'date_stop' in df.columns:
            df['date_stop'] = pd.to_datetime(df['date_stop'])

        # Calculate additional metrics
        df['ctr'] = df['clicks'] / df['impressions'] * 100  # Click-Through Rate
        df['cpc'] = df['spend'] / df['clicks']  # Cost Per Click

        # Ensure all columns you need are present
        expected_columns = [
            'campaign_name', 'impressions', 'reach', 'clicks', 'frequency',
            'engagement', 'video_plays', 'spend', 'allocated_budget', 'sessions', 'convertion', 'Gender', 'Age', 'Ad_name'
        ]

        for col in expected_columns:
            if col not in df.columns:
                df[col] = None  # If missing, add as None (or NaN)

        return df
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return pd.DataFrame()

def server(input, output, session):
    # @render.text
    # def fbdata():
    #     return app_values.fbapidata

    # Load data when the app starts
    campaign_data = reactive.Value(load_json_data(app_values.JSON_FILE_PATH))


    @render.image
    def qbaLogo():
        currentdir = Path(__file__).parent
        img = {"src": currentdir / 'QBA_Logo.png',"width":'80%'}
        return img
    

    # Output for average metrics
    @output
    @render.text
    def average_metrics():
        df = campaign_data()
        if not df.empty:
            avg_ctr = df['ctr'].mean()
            avg_spend = df['spend'].mean()
            return f"Average CTR: {avg_ctr:.2f}% | Average Spend: ${avg_spend:,.2f}"
        else:
            return "No data available."

    # Campaign Reach and Frequency Plot
    @output
    @render.plot
    def campaign_reach_frequency_plot():
        df = campaign_data()
        if not df.empty:
            plt.figure(figsize=(10, 6))
            ax1 = plt.gca()

            # Plot Reach as bar
            sns.barplot(x='campaign_name', y='reach', data=df, color='lightblue', ax=ax1)

            # Add data labels to Reach bars
            for p in ax1.patches:
                ax1.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                             ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

            # Plot Frequency as line
            ax2 = ax1.twinx()
            sns.lineplot(x='campaign_name', y='frequency', data=df, color='red', marker='o', ax=ax2)

            # Add data labels to Frequency points
            for i, val in enumerate(df['frequency']):
                ax2.text(i, val, f'{val:.2f}', color='red', ha='center', va='bottom', fontsize=10)

            ax1.set_title('Campaign Reach and Frequency', fontsize=14)
            ax1.set_ylabel('Reach', fontsize=12, color='blue')
            ax2.set_ylabel('Frequency', fontsize=12, color='red')
            plt.xticks(rotation=45)
            #plt.tight_layout()
            return plt.gcf()

    # Campaign Impressions and CTR Plot
    @output
    @render.plot
    def campaign_impressions_ctr_plot():
        df = campaign_data()
        if not df.empty:
            plt.figure(figsize=(10, 6))
            ax1 = plt.gca()

            # Plot Impressions as bar
            sns.barplot(x='campaign_name', y='impressions', data=df, color='green', ax=ax1)

            # Add data labels to Impressions bars
            for p in ax1.patches:
                ax1.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                             ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

            # Plot CTR as line
            ax2 = ax1.twinx()
            sns.lineplot(x='campaign_name', y='ctr', data=df, color='orange', marker='o', ax=ax2)

            # Add data labels to CTR points
            for i, val in enumerate(df['ctr']):
                ax2.text(i, val, f'{val:.2f}%', color='orange', ha='center', va='bottom', fontsize=10)

            ax1.set_title('Campaign Impressions and CTR', fontsize=14)
            ax1.set_ylabel('Impressions', fontsize=12, color='green')
            ax2.set_ylabel('CTR (%)', fontsize=12, color='orange')
            plt.xticks(rotation=45)
            #plt.tight_layout()
            return plt.gcf()

    # Campaign Engagement Plot
    @output
    @render.plot
    def campaign_engagement_plot():
        df = campaign_data()
        if not df.empty:
            df_cleaned = df[df['engagement'] > 0].dropna(subset=['engagement'])
        df_sorted = df_cleaned.sort_values(by='campaign_name', ascending=True)  # Sort by campaign_name

        plt.figure(figsize=(10, 6))

        # Plot Engagement as bar
        ax = sns.barplot(x='engagement', y='campaign_name', data=df_sorted, palette='Blues_r', errorbar=None)

        # Add data labels to Engagement bars
        for p in ax.patches:
            ax.annotate(f'{p.get_width():,.0f}', (p.get_width(), p.get_y() + p.get_height() / 2.), 
                         ha='left', va='center', fontsize=10, color='black')

        plt.title('Campaign Engagement', fontsize=14)
        plt.xlabel('Engagement', fontsize=12)
        plt.ylabel('Campaign Name', fontsize=12)
        #plt.tight_layout()

        return plt.gcf()
    
    @output
    @render.plot
    def ad_name_impressions_ctr_plot():
        df = campaign_data()
        if not df.empty:
            plt.figure(figsize=(12, 6))
        
        # Define color map for ad names
        ad_name_colors = {
            'youtube': 'red',
            'facebook': 'skyblue',
            'instagram': 'pink'
        }
        
        # Group by Ad_name and calculate metrics
        grouped = df.groupby('Ad_name').agg({
            'impressions': 'sum',
            'ctr': 'mean'
        }).reset_index()
        
        # Create twin axes
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        
        # Plot Impressions as bars
        bar_width = 0.5
        bars = ax1.bar(grouped['Ad_name'], grouped['impressions'], 
                       color=[ad_name_colors.get(name.lower(), 'gray') for name in grouped['Ad_name']], 
                       alpha=0.7, width=bar_width)
        
        # Add impressions labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:,.0f}', 
                     ha='center', va='bottom', fontsize=10)
        # Plot CTR as line
        line = ax2.plot(grouped['Ad_name'], grouped['ctr'], color='orange', marker='o')      
        # Add CTR labels
        for i, val in enumerate(grouped['ctr']):
            ax2.text(i, val, f'{val:.2f}%', color='orange', ha='center', va='bottom', fontsize=10)

        ax1.set_title('Ad Name Impressions and CTR', fontsize=14)
        ax1.set_xlabel('Ad Name', fontsize=12)
        ax1.set_ylabel('Impressions', fontsize=12, color='blue')
        ax2.set_ylabel('CTR (%)', fontsize=12, color='orange')
        plt.tight_layout()
        return plt.gcf()
    
    @output
    @render.plot
    def ad_name_reach_frequency_plot():
        df = campaign_data()
        if not df.empty:
            plt.figure(figsize=(12, 6))
        
        # Define color map for ad names
        ad_name_colors = {
            'youtube': 'red',
            'facebook': 'skyblue',
            'instagram': 'pink'
        }
        
        # Group by Ad_name and calculate metrics
        grouped = df.groupby('Ad_name').agg({
            'reach': 'sum',
            'frequency': 'mean'
        }).reset_index()
        
        # Create twin axes
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        
        # Plot Reach as bars
        bar_width = 0.5
        bars = ax1.bar(grouped['Ad_name'], grouped['reach'], 
                       color=[ad_name_colors.get(name.lower(), 'gray') for name in grouped['Ad_name']], 
                       alpha=0.7, width=bar_width)
        
        # Add reach labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:,.0f}', 
                     ha='center', va='bottom', fontsize=10)
        
        # Plot Frequency as line
        line = ax2.plot(grouped['Ad_name'], grouped['frequency'], color='green', marker='o')
        
        # Add Frequency labels
        for i, val in enumerate(grouped['frequency']):
            ax2.text(i, val, f'{val:.2f}', color='green', ha='center', va='bottom', fontsize=10)
        
        ax1.set_title('Ad Name Reach and Frequency', fontsize=14)
        ax1.set_xlabel('Ad Name', fontsize=12)
        ax1.set_ylabel('Reach', fontsize=12, color='blue')
        ax2.set_ylabel('Frequency', fontsize=12, color='green')
        
        plt.tight_layout()
        return plt.gcf()

   

    # CTR and Spend by Campaign Pie Charts
    @output
    @render.plot
    def ctr_and_spend_by_campaign_pie_charts():
        df = campaign_data()
        if not df.empty:
            campaign_ctr = df.groupby('campaign_name')['ctr'].sum()
            campaign_spend = df.groupby('campaign_name')['spend'].sum()

            fig, axes = plt.subplots(1, 2, figsize=(15, 8))

            # CTR Pie Chart
            axes[0].pie(campaign_ctr, labels=campaign_ctr.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'),   textprops={'fontsize': 6})
            axes[0].set_title('CTR Distribution by Campaign',fontsize=10)

            # Spend Pie Chart
            axes[1].pie(campaign_spend, labels=campaign_spend.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3'),    textprops={'fontsize': 6})
            axes[1].set_title('Spend Distribution by Campaign',fontsize=10)

            plt.tight_layout(pad=4.0)
            return plt.gcf()

    # Male vs Female Percentage by Ad Name (Pie Chart)
    @output
    @render.plot
    def male_female_percentage_by_ad_name():
        df = campaign_data()
        if not df.empty:
           metrics = ['impressions', 'reach', 'clicks', 'spend']
        
        # Prepare the plot with increased vertical space
        fig, axes = plt.subplots(2, 2, figsize=(15, 15), gridspec_kw={'hspace': 0.4})
        
        # Flatten axes for easier iteration
        axes = axes.flatten()
        
        # Create a pie chart for each metric
        for i, metric in enumerate(metrics):
            # Group by Ad_name and Gender, sum the specific metric
            gender_data = df.groupby('Gender')[metric].sum()
            
            # If data is empty or all zeros, skip
            if gender_data.empty or (gender_data == 0).all():
                axes[i].text(0.5, 0.5, f"No data for {metric}", ha='center', va='center')
                axes[i].axis('off')
                continue
            
            # Plot pie chart
            wedges, texts, autotexts = axes[i].pie(
                gender_data.values, 
                labels=gender_data.index, 
                autopct='%1.1f%%', 
                startangle=90, 
                colors=sns.color_palette('Set2'),    textprops={'fontsize': 8}
            )
            
            # Make the percentage labels more readable
            plt.setp(autotexts, size=10)
            
            # Set title with larger font size
            axes[i].set_title(f'{metric.capitalize()} Distribution by Gender', fontsize=10)
        
        # Add an overall figure title
        
        
        # Adjust layout with more space
        plt.tight_layout(rect=[0, 0.03, 1, 0.95], pad=3.0)
        
        return plt.gcf()
    @output
    @render.plot
    def age_distribution_by_ad_name():
        df = campaign_data()
        if not df.empty:
          metrics = ['impressions', 'reach', 'clicks', 'spend']
    
        # Prepare the plot with more horizontal space
        fig, axes = plt.subplots(2, 2, figsize=(16, 12), gridspec_kw={'wspace': 0.3, 'hspace': 0.4})
    
        # Flatten axes for easier iteration
        axes = axes.flatten()
    
        # Create a pie chart for each metric
        for i, metric in enumerate(metrics):
            # Group by Age, sum the specific metric
            age_data = df.groupby('Age')[metric].sum()
            
            # Filter out very small values (less than 1% of total)
            total = age_data.sum()
            age_data_filtered = age_data[age_data/total >= 0.01]
            
            # If data is empty or all zeros, skip
            if age_data_filtered.empty or (age_data_filtered == 0).all():
                axes[i].text(0.5, 0.5, f"No data for {metric}", ha='center', va='center')
                axes[i].axis('off')
                continue
            
            # Prepare colors and format for spend differently
            if metric == 'spend':
                colors = sns.color_palette('Set3')
                format_func = lambda x: f'${x:,.0f}'
            else:
                colors = sns.color_palette('Set2')
                format_func = lambda x: f'{x:,.0f}'
            
            # Plot pie chart
            wedges, texts, autotexts = axes[i].pie(
                age_data_filtered.values, 
                labels=[f'{age}: {format_func(val)}' for age, val in age_data_filtered.items()], 
                autopct='%1.1f%%', 
                pctdistance=0.85,
                startangle=90, 
                colors=colors
            )
            
            # Make the percentage labels more readable
            plt.setp(autotexts, size=8)
            plt.setp(texts, size=8)
            
            # Set title with metric name
            axes[i].set_title(f'{metric.capitalize()} Distribution by Age Group', fontsize=8)
    
        # Adjust layout 
        plt.tight_layout(pad=3.0)
    
        return plt.gcf()
    
    @output 
    @render.plot
    def clicks_vs_conversion_plot():
        df = campaign_data()
        if not df.empty:
              df_sorted = df.sort_values(by="campaign_name", ascending=True)

        # Melt the DataFrame for stacked bar chart compatibility
        df_melted = df_sorted.melt(
            id_vars=["campaign_name"], 
            value_vars=["clicks", "convertion"], 
            var_name="Metric", 
            value_name="Count"
        )

        # Create a stacked bar chart without black lines
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(
            x="campaign_name", 
            y="Count", 
            hue="Metric", 
            data=df_melted, 
            palette="Set2",
            edgecolor=None,  # Remove black lines
            linewidth=0       # Ensure no border around bars
        )

        # Add data labels
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", label_type="edge", fontsize=9)

        # Customize the chart
        plt.title("Clicks vs Conversion by Campaign", fontsize=14)
        plt.xlabel("Campaign Name", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Metric", loc="upper right")
        plt.tight_layout()

        return plt.gcf()
    @output
    @render.table
    def campaign_summary_table():
        df = campaign_data()
        if not df.empty:
            summary_cols = ['campaign_name', 'impressions', 'reach', 'clicks', 'spend', 'ctr', 'engagement','convertion','allocated_budget']
            df_summary = df[summary_cols].round(2)
            df_summary = df_summary.style.format({'spend': '${:,.2f}', 'ctr': '{:.2f}%'})
            return df_summary
# Define the UI for the Shiny app
# Updated UI for the Shiny app
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.output_image('qbaLogo'),
        ui.input_slider("n", "Slider", min=0, max=100, value=20),
        bg="#f1f1f1", open="open"
    ),

#ui.page_fluid(
    ui.div(
    ui.h1("Government of Kuwait - Social Media Dashboard")),
    ui.output_image('qbaLogo'),

    # ui.panel_title(title="Government of Kuwait - Social Media Dashboard", window_title="Social Media Dashboard"),
    ui.tags.hr(),
    # ui.tags.br(),
    ui.br(),
    ui.tags.h1("Campaign Analysis Dashboard", class_="text-center my-4"),
    ui.row(
        ui.column(6,
            ui.card(
                ui.card_header("Campaign Reach and Frequency"),
                ui.card_body(
                    ui.output_plot("campaign_reach_frequency_plot")
                )
            )
        ),
        ui.column(6,
            ui.card(
                ui.card_header("Campaign Impressions and CTR"),
                ui.card_body(
                    ui.output_plot("campaign_impressions_ctr_plot")
                )
            )
        )
    ),
    ui.row(
        ui.column(6,
            ui.card(
                ui.card_header("Ad Name Impressions and CTR"),
                ui.card_body(
                    ui.output_plot("ad_name_impressions_ctr_plot")
                )
            )
        ),
        ui.column(6,
            ui.card(
                ui.card_header("Ad Name Reach and Frequency"),
                ui.card_body(
                    ui.output_plot("ad_name_reach_frequency_plot")
                )
            )
        )
    ),
    ui.row(
        ui.column(6,
            ui.card(
                ui.card_header("CTR and Spend Distribution"),
                ui.card_body(
                    ui.output_plot("ctr_and_spend_by_campaign_pie_charts")
                )
            )
        ),
        ui.column(6,
            ui.card(
                ui.card_header("Male vs Female Percentage by Different Metrics"),
                ui.card_body(
                    ui.output_plot("male_female_percentage_by_ad_name")
                )
            )
        )
    ),
    ui.row(
        ui.column(6,
            ui.card(
                ui.card_header("Age Distribution by Different Metrics"),
                ui.card_body(
                    ui.output_plot("age_distribution_by_ad_name")
                )
            )
        ),
        ui.column(6,
            ui.card(
                ui.card_header("Clicks vs. Conversion by Campaign"),
                ui.card_body(
                    ui.output_plot("clicks_vs_conversion_plot")
                )
            )
        )
    ),
    ui.row(
        ui.column(12,
            ui.card(
                ui.card_header("Campaign Engagement"),
                ui.card_body(
                    ui.output_plot("campaign_engagement_plot")
                )
            )
        )
    )
)


# Create the Shiny app
app_report = App(app_ui, server)
 
if __name__ == "__main__":
    app_report.run()
