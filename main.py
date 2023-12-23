import folium
import pandas as pd
from sklearn.cluster import KMeans

# Assuming you have a DataFrame named 'migration_data' with columns 'location-long' and 'location-lat'
# Replace 'your_dataset.csv' with the actual filename or provide the DataFrame directly if using in-memory data.

# Example:
migration_data = pd.read_csv('migration_original.csv').head(1000)

# Create a folium map centered around the first data point
m = folium.Map(location=[migration_data['location-lat'].iloc[0], migration_data['location-long'].iloc[0]], zoom_start=5)

# Add markers for each data point
for index, row in migration_data.iterrows():
    folium.Marker([row['location-lat'], row['location-long']]).add_to(m)

# Add a line for migration path
migration_path = folium.PolyLine(locations=migration_data[['location-lat', 'location-long']].values, color='blue')
migration_path.add_to(m)

# Display the map
m.save('migration_map_with_path.html')

# Use KMeans clustering for better visualization
# You can adjust the number of clusters (n_clusters) based on your dataset
kmeans = KMeans(n_clusters=5, random_state=42)
migration_data['cluster'] = kmeans.fit_predict(migration_data[['location-lat', 'location-long']])

# Create a new folium map for clustered data
clustered_map = folium.Map(location=[migration_data['location-lat'].mean(), migration_data['location-long'].mean()], zoom_start=5)

# Add markers with different colors for each cluster
for index, row in migration_data.iterrows():
    color = 'red' if row['cluster'] == 0 else 'blue' if row['cluster'] == 1 else 'green' if row['cluster'] == 2 else 'purple' if row['cluster'] == 3 else 'orange'
    folium.Marker([row['location-lat'], row['location-long']], icon=folium.Icon(color=color)).add_to(clustered_map)

# Add a line for migration path
migration_path_clustered = folium.PolyLine(locations=migration_data[['location-lat', 'location-long']].values, color='blue')
migration_path_clustered.add_to(clustered_map)

# Display the clustered map
clustered_map.save('clustered_migration_map_with_path.html')
