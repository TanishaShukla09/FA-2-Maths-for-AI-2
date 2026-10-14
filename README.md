# LogiSight Delivery Performance Dashboard

## Project Overview

LogiSight Delivery Performance Dashboard is an interactive web application developed using Python and Streamlit to analyse last-mile delivery performance. It helps users identify factors affecting delivery times and explore patterns across weather, traffic, vehicle types, delivery agents, areas, and product categories.

This project was developed as part of Formative Assessment 2 (FA-2) for Mathematics for AI-II.

## Live Dashboard

[Click here to access the LogiSight Delivery Performance Dashboard](https://fa-2-maths-for-ai-2.streamlit.app/)

## Objectives

- Analyse last-mile delivery performance using real-world data.
- Clean and prepare data using Python.
- Create meaningful and interactive data visualisations.
- Identify factors that contribute to longer delivery times.
- Compare vehicle and delivery-agent performance.
- Build and deploy an interactive dashboard using Streamlit.

## Technologies Used

- Python
- Streamlit
- pandas
- NumPy
- Plotly Express

## Dashboard Features

### 1. Key Performance Indicators

The dashboard displays four key metrics:

- Total number of orders
- Average delivery time
- Percentage of late deliveries
- Average delivery-agent rating

### 2. Delay Analyzer

A bar chart compares average delivery time under different traffic and weather conditions. This helps identify combinations of external conditions associated with longer deliveries.

### 3. Delivery Time by Order Hour

A line chart displays average delivery time by hour of the day to help identify periods when deliveries take longer.

### 4. Late Deliveries by Traffic

A bar chart compares the percentage of late deliveries across different traffic levels.

### 5. Vehicle Comparison

A bar chart compares average delivery times for different vehicle types to identify which vehicle category has the lowest average delivery time.

### 6. Agent Performance Analysis

A scatter plot compares delivery-agent ratings with delivery times. The points are grouped by agent age to help explore relationships between agent ratings, age groups, and delivery performance.

### 7. Area Heatmap

A heatmap displays average delivery time across different areas and traffic conditions, helping users identify combinations associated with slower deliveries.

### 8. Category Visualizer

A boxplot compares delivery-time distributions across product categories, highlighting differences in delivery performance.

## Interactive Filters

Users can filter the dashboard using the following options:

- Weather
- Traffic
- Vehicle
- Area
- Product category
- Agent rating

The dashboard updates its metrics and charts according to the selected filters. Users can also reset all filters and select from multiple colour themes.

## Data Cleaning and Preparation

The application uses pandas and NumPy to prepare the dataset for analysis.

The data preparation process includes:

- Removing leading and trailing spaces from relevant text fields.
- Converting text representations of missing values into actual missing values.
- Correcting the spelling of the Metropolitan area.
- Standardising vehicle names.
- Removing rows with missing values in required fields.
- Excluding agent ratings above 5.
- Extracting the order hour from the order time.
- Grouping delivery agents into age categories.

A delivery is classified as late when its delivery time exceeds the mean delivery time by more than one standard deviation.

## Project Structure

The project folder contains the following files:

```text
project-folder/
├── .streamlit/
├── app.py
├── Last_mile_Delivery_Data.csv
├── Requirements.txt
├── README.md
└── FA_2_CRS_Y2_Maths_for_AI-II_Formative_Assessment_2.docx
```

### File Descriptions

- `app.py` — contains the Python code and Streamlit dashboard.
- `Last_mile_Delivery_Data.csv` — contains the delivery dataset.
- `Requirements.txt` — lists the Python libraries required by the application.
- `.streamlit/` — contains Streamlit configuration files, if applicable.
- `README.md` — provides project documentation.
- `FA_2_CRS_Y2_Maths_for_AI-II_Formative_Assessment_2.docx` — contains the assignment brief.

## Installation and Setup

### Prerequisites

- Python installed on your computer.
- pip package installer.
- The project files, including the dataset.

### Step 1: Install Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r Requirements.txt
```

### Step 2: Run the Application

Execute the following command:

```bash
streamlit run app.py
```

### Step 3: Open the Dashboard

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Deployment

The application is deployed using Streamlit Community Cloud and hosted through GitHub.

The deployment process involves:

1. Uploading the application code, requirements file, dataset, and README to GitHub.
2. Connecting the GitHub repository to Streamlit Community Cloud.
3. Selecting `app.py` as the main application file.
4. Deploying the application.
5. Testing the live dashboard and its interactive filters.

## Important Notes

- The dataset must be named `Last_mile_Delivery_Data.csv`.
- The dataset must be in the same directory as `app.py`.
- The required Python libraries must be installed before running the application locally.
- Dashboard results depend on the quality and contents of the dataset.
- The late-delivery definition used in this project is statistical and may differ from an organisation's official delivery targets.

## Academic Information

**Course:** Mathematics for AI-II

**Assessment:** Formative Assessment 2 — Dashboarding and Deployment

**Project Title:** Analyzing Last Mile Delivery Data for Performance Insights

## Project Link

Live Dashboard: https://fa-2-maths-for-ai-2.streamlit.app/
