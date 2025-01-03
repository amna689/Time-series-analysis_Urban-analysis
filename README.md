# Time-series-analysis_Urban-analysis
Lahore Urban Analysis
This project is a Python-based desktop application that analyzes urban expansion and environmental features in Lahore, Pakistan. It uses GIS and remote sensing data to visualize and analyze vegetation, water bodies, and infrastructure changes over selected years.
Features
•	Year Selection: Analyze data for specific years (2018-2019, 2020-2021, 2022-2023).
•	Feature Selection: Visualize vegetation, water bodies, and infrastructure on a map.
•	Dynamic Map: Interactive map with raster overlays, shapefile integration, and dynamic legends.
•	Analysis Results: Display bar graphs of selected feature areas.
Prerequisites
•	Python 3.12 or higher
•	PostgreSQL with PostGIS enabled
•	Required Python packages: 
o	tkinter
o	geopandas
o	psycopg2
o	sqlalchemy
o	rasterio
o	folium
o	matplotlib
o	numpy
Project Structure
LahoreUrbanAnalysis/
|
|-- main.py            # Main application code
|-- database.py        # Database interaction code
|-- requirements.txt   # List of Python dependencies
|-- FLahore_*.tif      # Raster files for different years
|-- lahore_industries/ # Folder containing shapefiles
Getting Started
1. Clone the Repository
git clone <repository_url>
cd LahoreUrbanAnalysis
2. Set Up the Database
1.	Create a PostgreSQL database named urban_analysis.
2.	Enable PostGIS on the database: 
3.	CREATE EXTENSION postgis;
4.	Add a table named lahore_boundary with geometry data. 
5.	CREATE TABLE lahore_boundary (
6.	    id SERIAL PRIMARY KEY,
7.	    geom GEOMETRY(POLYGON, 4326)
8.	);
9.	Load the Lahore boundary shapefile into the database. 
10.	shp2pgsql -s 4326 lahore_boundary.shp lahore_boundary | psql -U postgres -d urban_analysis
3. Install Dependencies
Create a virtual environment and install the required packages:
python -m venv env
source env/bin/activate  # For Linux/macOS
env\Scripts\activate   # For Windows
pip install -r requirements.txt
4. Run the Application
1.	Start the application: 
2.	python main.py
3.	Use the GUI to select years and features, perform analysis, and view results.
Key Files and Their Functions
main.py
•	Contains the UrbanAnalysisApp class for the Tkinter-based GUI.
•	Handles year and feature selection, data analysis, and map visualization.
•	Integrates raster data and shapefiles into an interactive map using Folium.
database.py
•	Provides database interaction functions: 
o	get_lahore_boundary(): Fetch Lahore boundary data as a GeoDataFrame.
o	get_lahore_area(): Calculate the total area of the Lahore boundary.
Raster and Shapefiles
•	FLahore_*.tif: Raster files representing features (vegetation, water bodies, infrastructure) for different years.
•	lahore_industries.shp: Shapefile containing industry locations in Lahore.
 Workflow
1.	Select a year (e.g., 2020-2021).
2.	Choose features to analyze (e.g., Vegetation and Water Bodies).
3.	Click "Perform Analysis" to generate a bar graph and map.
4.	View the map by clicking "View Map."
Troubleshooting
Common Issues
1.	Database Connection Errors:
o	Ensure PostgreSQL is running and the credentials in database.py are correct.
o	Verify the lahore_boundary table contains valid data.
2.	File Not Found Errors:
o	Check that the raster files and shapefiles are in the correct paths.
3.	Missing Dependencies:
o	Install all required Python packages using pip install -r requirements.txt.
Acknowledgments
•	Data sources: Satellite imagery Sentinel-2 and shapefiles.
•	Tools: Python, PostgreSQL, PostGIS, Tkinter, Folium.

Author
Amna Akhtar

