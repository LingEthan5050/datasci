from flask import Flask, render_template, request
import pandas as pd

# Load the data (adjust the file path for your local environment)
file_path = "Table.csv"  # Replace with your file's path
cleaned_data = pd.read_csv(file_path, skiprows=3)  # Adjust this line based on your dataset's structure

# Initialize Flask app
app = Flask(__name__)

# Define Flask route
@app.route("/")
def index():
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

    # Limit rows to avoid overload
    subset_data = filtered_data.head(50)

    return render_template(
        "base.html",
        columns=subset_data.columns,
        data=subset_data.values.tolist(),
        state=state,
        year=year,
    )

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)





<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Economic Metrics Dashboard</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #ddd;
        }
    </style>
</head>
<body>
    <h1>Economic Metrics Dashboard</h1>

    <form method="get" action="/">
        <label for="state">Filter by State:</label>
        <input type="text" id="state" name="state" placeholder="Enter state name" value="{{ state or '' }}">
        <label for="year">Filter by Year:</label>
        <input type="text" id="year" name="year" placeholder="Enter year (e.g., 2020)" value="{{ year or '' }}">
        <button type="submit">Filter</button>
    </form>

    <table>
        <thead>
            <tr>
                {% for column in columns %}
                    <th>{{ column }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
                <tr>
                    {% for item in row %}
                        <td>{{ item }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>


