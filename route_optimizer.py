# route_optimizer.py
from geopy.distance import geodesic

def get_optimized_route(df):
    """Returns an optimized route visiting bins > 80% full"""
    # Filter only full bins
    full_bins = df[df['fill_level'] > 80].reset_index(drop=True)

    if full_bins.empty:
        return []

    route = []
    visited = set()

    # Start from the first bin
    current = full_bins.iloc[0]
    route.append(current['bin_id'])
    visited.add(current.name)

    while len(visited) < len(full_bins):
        nearest_idx = None
        nearest_dist = float("inf")

        for idx, row in full_bins.iterrows():
            if idx in visited:
                continue
            dist = geodesic((current['lat'], current['lon']), (row['lat'], row['lon'])).km
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_idx = idx

        if nearest_idx is not None:
            current = full_bins.loc[nearest_idx]
            route.append(current['bin_id'])
            visited.add(nearest_idx)

    return route
