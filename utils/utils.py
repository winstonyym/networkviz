# Map class utility functions
import io
import h5py
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import wkt


def save_to_h5(filepath, gdf_dict, array_dict):

    # Save to HDF5 file
    with h5py.File(filepath, 'w') as f:

        for gdf_key, gdf_data in gdf_dict.items():
            # Save geodataframes as tables (convert to CSV or similar format for storage)
            f.create_dataset(gdf_key, data=gdf_data.to_csv(index=False).encode())

        for array_key, array_data in array_dict.items():
            f.create_dataset(array_key, data=array_data)

def load_from_h5(filepath):
    connections = {}
    objects = {}
    with h5py.File(filepath, 'r') as f:

        for k in f.keys():
            if 'edges' not in k:
                df = pd.read_csv(io.StringIO(f[k][()].decode()), sep=",")
                gdf = gpd.GeoDataFrame(data=df, crs = 'EPSG:4326', geometry=df['geometry'].apply(wkt.loads))
                objects[k] = gdf
            else:
                connections[k] = f[k][:]

    return objects, connections
        
