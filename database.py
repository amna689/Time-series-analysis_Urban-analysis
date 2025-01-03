import psycopg2
import geopandas as gpd
from sqlalchemy import create_engine

# Database connection details
host = "localhost"
database = "urban_analysis"
user = "postgres"
password = "Amfoi1257#"

# Function to get Lahore boundary as a GeoDataFrame
def get_lahore_boundary():
    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
        query = "SELECT * FROM lahore_boundary"
        gdf = gpd.read_postgis(query, engine, geom_col='geom')
        return gdf
    except Exception as e:
        raise RuntimeError(f"Error fetching Lahore boundary: {e}")

# Function to calculate the total area of Lahore boundary
def get_lahore_area():
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host
        )
        print("Connection to PostgreSQL successful!")
        
        cur = conn.cursor()
        query = "SELECT SUM(ST_Area(geom)) FROM lahore_boundary;"
        cur.execute(query)
        total_area = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        print(f"The area of Lahore is {total_area} square units.")
        return total_area
    except Exception as e:
        raise RuntimeError(f"Error calculating Lahore area: {e}")

if __name__ == "__main__":
    get_lahore_area()  # Calling the function to calculate the area and display the message
