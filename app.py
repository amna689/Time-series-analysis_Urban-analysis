import os
import tkinter as tk
from tkinter import messagebox
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.plot import show
from folium import plugins, raster_layers
import folium
import matplotlib.pyplot as plt
from database import get_lahore_boundary  # Import the function to fetch the boundary from the database


class UrbanAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lahore Analysis")
        self.root.geometry("600x400")  # Set window size
        self.root.configure(bg="white")  # Set overall background color to white

        # Variables for year selection and feature checkboxes
        self.selected_year = tk.StringVar(value="2018-2019")  # Default to the first radio button
        self.vegetation_var = tk.BooleanVar(value=False)
        self.water_var = tk.BooleanVar(value=False)
        self.infrastructure_var = tk.BooleanVar(value=False)
        self.map_file_path = None

        # Create GUI
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="Lahore Urban Analysis", bg="teal", fg="white", font=("Helvetica", 18, "bold"))
        header.pack(pady=10)

        # Year selection radiobuttons
        years_frame = tk.LabelFrame(self.root, text="Select Year", padx=10, pady=10, bg="#66b2b2", fg="white", font=("Helvetica", 12))
        years_frame.pack(padx=10, pady=5, fill="x")

        for year in ["2018-2019", "2020-2021", "2022-2023"]:
            tk.Radiobutton(
                years_frame,
                text=year,
                variable=self.selected_year,
                value=year,
                bg="#66b2b2",
                fg="white",
                selectcolor="black",
                font=("Helvetica", 12)  # Increased font size
            ).pack(anchor="w")

        # Feature checkboxes with colored backgrounds
        features_frame = tk.LabelFrame(self.root, text="Select Features", padx=10, pady=10, bg="#b2d8d8", fg="black", font=("Helvetica", 12))
        features_frame.pack(padx=10, pady=5, fill="x")

        tk.Checkbutton(features_frame, text="Vegetation", variable=self.vegetation_var, bg="green", fg="white", selectcolor="black", font=("Helvetica", 12)).pack(anchor="w")
        tk.Checkbutton(features_frame, text="Water Bodies", variable=self.water_var, bg="blue", fg="white", selectcolor="black", font=("Helvetica", 12)).pack(anchor="w")
        tk.Checkbutton(features_frame, text="Infrastructure", variable=self.infrastructure_var, bg="red", fg="white", selectcolor="black", font=("Helvetica", 12)).pack(anchor="w")

        # Buttons
        buttons_frame = tk.Frame(self.root, bg="#66b2b2")
        buttons_frame.pack(padx=10, pady=5, fill="x")

        tk.Button(buttons_frame, text="Perform Analysis", command=self.analyze_data, width=20, font=("Helvetica", 12)).pack(pady=5)
        self.view_map_button = tk.Button(buttons_frame, text="View Map", command=self.view_map, state=tk.DISABLED, width=20, font=("Helvetica", 12))
        self.view_map_button.pack(pady=5)

    def analyze_data(self):
        """Perform analysis based on the selected year and features."""
        selected_year = self.selected_year.get()

        # Validate that at least one year and feature is selected
        if not selected_year or not (self.vegetation_var.get() or self.water_var.get() or self.infrastructure_var.get()):
            messagebox.showerror("Error", "Please select at least one year and one feature.")
            return

        # Raster file paths for each year
        raster_files = {
            "2018-2019": "D:/geodatabase lectures/GeodatabaseProject/FLahore_2018_2019.tif",
            "2020-2021": "D:/geodatabase lectures/GeodatabaseProject/FLahore_2020_2021.tif",
            "2022-2023": "D:/geodatabase lectures/GeodatabaseProject/FLahore_2022_2023.tif",
        }

        raster_path = raster_files.get(selected_year)
        if not raster_path or not os.path.exists(raster_path):
            messagebox.showerror("Error", f"Raster file not found: {raster_path}")
            return

        # Paths to the shapefiles
        industries_shapefile = "D:/geodatabase lectures/GeodatabaseProject/lahore_industries/lahore_industries.shp"

        if not os.path.exists(industries_shapefile):
            messagebox.showerror("Error", f"Industries shapefile not found: {industries_shapefile}")
            return

        try:
            # Fetch the Lahore boundary from the database using the database.py function
            lahore_boundary = get_lahore_boundary()  # Using the database function to get the boundary
            if lahore_boundary is None:
                messagebox.showerror("Error", "Failed to fetch Lahore boundary from the database.")
                return

            with rasterio.open(raster_path) as src:
                bands = src.read()
                bounds = [[src.bounds.bottom, src.bounds.left], [src.bounds.top, src.bounds.right]]

                # Create an empty RGB composite
                composite = np.zeros((bands[0].shape[0], bands[0].shape[1], 3), dtype=np.uint8)

                selected_areas = {}

                # Calculate areas and update legend data
                if self.vegetation_var.get():
                    composite[..., 1] = np.where(bands[0] > 0, 255, 0)  # Green for vegetation
                    selected_areas["Vegetation"] = np.sum(bands[0] > 0)
                if self.water_var.get():
                    composite[..., 2] = np.where(bands[1] > 0, 255, 0)  # Blue for water
                    selected_areas["Water Bodies"] = np.sum(bands[1] > 0)
                if self.infrastructure_var.get():
                    composite[..., 0] = np.where(bands[2] > 0, 255, 0)  # Red for infrastructure
                    selected_areas["Infrastructure"] = np.sum(bands[2] > 0)

                # Generate a bar graph only for selected features
                labels, values = zip(*selected_areas.items())
                colors = ["green" if label == "Vegetation" else "blue" if label == "Water Bodies" else "red" for label in labels]
                plt.bar(labels, values, color=colors)
                plt.xlabel("Features")
                plt.ylabel("Area")
                plt.title(f"Area Analysis ({selected_year})")
                plt.tight_layout()

                # Save the bar graph as an image
                bar_graph_path = "bar_graph.png"
                plt.savefig(bar_graph_path)
                plt.close()

                # Create a folium map
                lahore_coordinates = [31.5497, 74.3436]
                m = folium.Map(location=lahore_coordinates, zoom_start=12)

                # Add the raster overlay
                raster_layers.ImageOverlay(image=composite, bounds=bounds, opacity=0.7).add_to(m)

                # Add Lahore boundary (from database)
                folium.GeoJson(
                    lahore_boundary,
                    name="Lahore Boundary",
                    style_function=lambda x: {
                        "color": "yellow",
                        "weight": 3,
                        "fillOpacity": 0
                    }
                ).add_to(m)

                # Add industries shapefile as orange dots
                industries_legend = ""
                if self.infrastructure_var.get():
                    industries = gpd.read_file(industries_shapefile)
                    for _, industry in industries.iterrows():
                        coords = industry.geometry.centroid.coords[0]
                        folium.CircleMarker(
                            location=[coords[1], coords[0]],
                            radius=5,
                            color="orange",
                            fill=True,
                            fill_color="orange",
                            fill_opacity=0.8,
                            popup=industry.get("Name", "Industry")
                        ).add_to(m)
                    industries_legend = '<i style="background: orange; width: 10px; height: 10px; float: left; margin-right: 5px;"></i> Industries<br>'

                # Add a dynamic legend with the bar graph
                legend_html = f'''
                <div style="
                    position: fixed; 
                    bottom: 150px; left: 50px; width: 250px; height: auto; 
                    background-color: white; z-index:9999; font-size:14px;
                    border:2px solid grey; padding: 10px;">
                    <strong>Legend</strong><br>
                    <i style="border: 2px solid yellow; width: 10px; height: 10px; float: left; margin-right: 5px;"></i> Lahore Boundary<br>
                    {industries_legend}
                    {''.join(f'<i style="background: {color}; width: 10px; height: 10px; float: left; margin-right: 5px;"></i> {label}<br>' for label, color in zip(labels, colors))}
                    <img src="{bar_graph_path}" style="width: 200px; margin: 10px;">
                </div>
                '''
                m.get_root().html.add_child(folium.Element(legend_html))

                # Save the map as an HTML file
                self.map_file_path = "lahore_map.html"
                m.save(self.map_file_path)
                self.view_map_button.config(state=tk.NORMAL)

                messagebox.showinfo("Success", f"Analysis complete for {selected_year}. Click 'View Map' to see the results.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def view_map(self):
        """Open the map file in the default web browser."""
        if self.map_file_path and os.path.exists(self.map_file_path):
            os.startfile(self.map_file_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = UrbanAnalysisApp(root)
    root.mainloop()
