import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from flask import Flask, render_template, request


file_path = "Table.csv"  # Replace with your file's path
data = pd.read_csv(file_path, skiprows=3)

# Preprocess the dataset
data.replace("(NA)", None, inplace=True)
data.iloc[:, 4:] = data.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')


# Load the data (adjust the file path for your local environment)
file_path = "Table.csv"  # Replace with your file's path
cleaned_data = pd.read_csv(file_path, skiprows=3)  # Adjust this line based on your dataset's structure

# Initialize Flask app
app = Flask(__name__)

# Landing Page (Home Page)
@app.route("/")
def landing():
    print("Landing page accessed")
    return render_template("landing.html")

# Dataset Filtering Page
@app.route("/filter")
def index():
    print("Filter page accessed")
    # Retrieve query parameters for filtering
    state = request.args.get("state")
    year = request.args.get("year")

    # Filter the dataset
    filtered_data = cleaned_data
    if state:
        filtered_data = filtered_data[filtered_data["GeoName"].str.contains(state, case=False, na=False)]
    if year:
        year_column = str(year)
        if year_column in filtered_data.columns:
            filtered_data = filtered_data[["GeoFips", "GeoName", "Description", year_column]]

    # If no filters are applied, show all rows and columns
    subset_data = filtered_data

    return render_template(
        "base.html",
        columns=subset_data.columns,
        data=subset_data.values.tolist(),
        state=state,
        year=year,
    )

# Additional Routes

@app.route("/eda", methods=["GET", "POST"])
def eda():
    # Default values
    selected_state = request.form.get("state", "United States")
    selected_metric = request.form.get("metric", "Real GDP (millions of chained 2017 dollars) 1")
    selected_year = request.form.get("year", "2021")

    # Filter data based on user selection
    filtered_data = data[
        (data["GeoName"] == selected_state) & (data["Description"].str.contains(selected_metric, case=False, na=False))
    ]

    # Visualization
    img = None
    if not filtered_data.empty:
        years = [str(year) for year in range(1998, 2024) if str(year) in data.columns]
        values = filtered_data.iloc[0][years].dropna()

        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(values.index, values.values, marker="o")
        plt.title(f"{selected_metric} in {selected_state} Over Time")
        plt.xlabel("Year")
        plt.ylabel(selected_metric)
        plt.xticks(rotation=45)

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        plt.close()

    return render_template(
        "eda.html",
        states=data["GeoName"].dropna().unique(),
        metrics=data["Description"].dropna().unique(),
        years=[str(year) for year in range(1998, 2024)],
        selected_state=selected_state,
        selected_metric=selected_metric,
        selected_year=selected_year,
        plot_url=img,
    )



@app.route("/route1")
def route1():
    print("Route 1 page accessed")
    return render_template("route1.html")

@app.route("/route2")
def route2():
    print("Route 2 page accessed")
    return render_template("route2.html")

@app.route("/route3")
def route3():
    print("Route 3 page accessed")
    return render_template("route3.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
