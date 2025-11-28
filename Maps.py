import plotly.express as px
import geopandas as gpd
from Provinces import SeatAllocator
from Old.WInnertakesall import seatCalculator

df_seats_2023 = SeatAllocator(1)

# Load Spain provinces GeoJSON into a GeoDataFrame
gdf = gpd.read_file(
    "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain-provinces.geojson",
    crs="epsg:4326",
)

#Making Province names match across data frames
gdf.rename(columns={'name': 'PROVINCIA'}, inplace=True)
gdf["PROVINCIA"] = gdf["PROVINCIA"].replace("Alacant/Alicante", "Alicante / Alacant")
gdf["PROVINCIA"] = gdf["PROVINCIA"].replace("Araba/Álava", "Araba / Álava")
gdf["PROVINCIA"] = gdf["PROVINCIA"].replace("València/Valencia", "Valencia / València")
gdf["PROVINCIA"] = gdf["PROVINCIA"].replace("Bizkaia/Vizcaya", "Bizkaia")
gdf["PROVINCIA"] = gdf["PROVINCIA"].replace("Castelló/Castellón","Castellón / Castelló")
gdf["PROVINCIA"] = gdf["PROVINCIA"].replace("Gipuzkoa/Guipúzcoa","Gipuzkoa")

#Merging data frames
gdf_reset = gdf.reset_index()
seat_df = seatCalculator().reset_index()
mergedgdf = gdf_reset.merge(seat_df, on='PROVINCIA', how='left')
mergedgdf = mergedgdf.merge(df_seats_2023, on="PROVINCIA",how="left")

#Calculation of new variables to plot

#mergedgdf["winner"] = np.where(mergedgdf["PSOE"]>mergedgdf['PP'],mergedgdf["PSOE"],mergedgdf["PP"])
#mergedgdf["ratio"] = mergedgdf["winner"]/mergedgdf["Congress_Seats_2023"]
party_df = mergedgdf.select_dtypes(include=['number'])# selects only numeric columns
party_df = party_df.iloc[:, 2:-1]
mergedgdf['max_seats_party'] = party_df.idxmax(axis=1)
mergedgdf['max_seats'] = party_df.max(axis=1)
#print(mergedgdf['max_seats_party'])
mergedgdf["numcode"]= mergedgdf['max_seats_party'].astype('category').cat.codes




# Plotting
fig = px.choropleth_map(
    mergedgdf,
    geojson=gdf["geometry"].__geo_interface__,
    locations=gdf.index,
    color="numcode",
    hover_name="PROVINCIA",  # province name
    color_continuous_scale="Viridis",
)

# Center map on Spain using bounding box
fig.update_layout(
    map=dict(
        center=dict(lat=40.0, lon=-3.7),
        zoom=4,
        style="carto-positron",  # or any supported style
    ),
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

fig.show()
