# test_backend.py
from simulate_bins import generate_bin_data
from route_optimizer import get_optimized_route

df = generate_bin_data()
print(df)

route = get_optimized_route(df)
print("Optimized Route:", " -> ".join(route))
