# --- 1. Impor Library ---
import networkx as nx
import matplotlib.pyplot as plt 
import heapq
import itertools
import time

# --- 2. Definisi Data Graf ---
# Daftar 10 kota (Vertex)
cities = [
    "Jakarta", "Surabaya", "Bandung", "Medan", "Semarang",
    "Makassar", "Palembang", "Batam", "Balikpapan", "Samarinda"
]

# Daftar 30 jalur & jarak (Edge & Bobot)
edges_with_distance = [
    ("Jakarta", "Bandung", 150), ("Jakarta", "Semarang", 450),
    ("Jakarta", "Surabaya", 780), ("Jakarta", "Palembang", 430),
    ("Jakarta", "Batam", 850), ("Bandung", "Semarang", 350),
    ("Bandung", "Surabaya", 690), ("Surabaya", "Semarang", 350),
    ("Surabaya", "Makassar", 1600), ("Surabaya", "Balikpapan", 1500),
    ("Semarang", "Balikpapan", 1200), ("Semarang", "Palembang", 800),
    ("Palembang", "Batam", 500), ("Palembang", "Medan", 1400),
    ("Batam", "Medan", 900), ("Medan", "Makassar", 2700),
    ("Makassar", "Balikpapan", 900), ("Makassar", "Samarinda", 1000),
    ("Balikpapan", "Samarinda", 115), ("Samarinda", "Medan", 3200),
    ("Bandung", "Batam", 1200), ("Bandung", "Palembang", 900),
    ("Surabaya", "Palembang", 1200), ("Semarang", "Batam", 1300),
    ("Jakarta", "Makassar", 1400), ("Jakarta", "Balikpapan", 1500),
    ("Bandung", "Makassar", 1600), ("Medan", "Balikpapan", 2500),
    ("Batam", "Makassar", 1800), ("Palembang", "Samarinda", 2200)
]

# --- 3. Pembuatan Adjacency List ---
adjacency_list = {city: {} for city in cities}
for city1, city2, distance in edges_with_distance:
    adjacency_list[city1][city2] = distance
    adjacency_list[city2][city1] = distance

# --- 4. Menampilkan Adjacency List  ---
print("--- Adjacency List Peta ---")
for city, neighbors in adjacency_list.items():
    print(f"{city}: {neighbors}")
print("-" * 55)

# --- 5. Implementasi Algoritma Dijkstra ---
def dijkstra_shortest_path(graph, start_node, end_node):
    """Mencari rute terpendek dengan Algoritma Dijkstra."""
    priority_queue = [(0, start_node, [start_node])]
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0

    while priority_queue:
        (current_distance, current_node, current_path) = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node == end_node:
            return current_distance, current_path
        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    new_path = current_path + [neighbor]
                    heapq.heappush(priority_queue, (distance, neighbor, new_path))
    return float('inf'), []

# --- 6. Interaksi Pengguna untuk Dijkstra ---
def run_dijkstra_test():
    """Meminta input & menampilkan hasil Dijkstra."""
    print("\n--- Pencarian Rute Terpendek (Dijkstra) ---")
    print("Daftar Kota:", ", ".join(cities))
    while True:
        start = input("Masukkan Kota Asal: ").strip().title()
        if start in cities: break
        print("Kota Asal tidak ditemukan. Coba lagi.")
    while True:
        end = input("Masukkan Kota Tujuan: ").strip().title()
        if end in cities: break
        print("Kota Tujuan tidak ditemukan. Coba lagi.")
    if start == end:
        print(f"\nKota Asal & Tujuan sama. Jarak: 0 KM, Rute: [{start}]")
        return
    total_cost, route = dijkstra_shortest_path(adjacency_list, start, end)
    if total_cost != float('inf'):
        print(f"\nRute Terpendek: {' -> '.join(route)}")
        print(f"Total Jarak: {total_cost} KM")
    else:
        print(f"\nTidak ada rute dari {start} ke {end}.")

# --- 7. Implementasi Algoritma TSP (Brute-Force) ---
def calculate_route_distance(graph, route):
    """
    Menghitung total jarak untuk sebuah rute.
    Mengembalikan float('inf') jika ada jalur yang tidak ada.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        city1 = route[i]
        city2 = route[i+1]
        # Menggunakan .get() untuk menangani jalur yang tidak ada.
        distance = graph[city1].get(city2, float('inf'))
        # Jika jalur tidak ada (jarak 'inf'), rute tidak valid.
        if distance == float('inf'):
            return float('inf')
        total_distance += distance
    return total_distance

def tsp_brute_force(graph, start_city):
    """Menemukan rute TSP terpendek menggunakan Brute-Force."""
    other_cities = [city for city in graph if city != start_city]
    min_distance = float('inf')
    best_route = []

    print(f"\nMemulai perhitungan TSP Brute-Force...")
    start_time = time.time()

    # Buat semua permutasi untuk kota_selain_awal
    for permutation in itertools.permutations(other_cities):
        current_route = [start_city] + list(permutation)
        current_distance = calculate_route_distance(graph, current_route)
        # Mempertimbangkan rute yang valid
        if current_distance < min_distance:
            min_distance = current_distance
            best_route = current_route

    end_time = time.time()
    print(f"Perhitungan TSP selesai dalam {end_time - start_time:.2f} detik.")
    return best_route, min_distance

# --- 8. Interaksi Pengguna untuk TSP  ---
def run_tsp_test():
    print("\n--- Pencarian Rute Efisien (TSP Brute-Force) ---")
    print("Mencari rute yang mengunjungi semua 10 kota tepat satu kali.")
    print("Daftar Kota:", ", ".join(cities))

    # Meminta input & validasi Kota Awal untuk TSP
    while True:
        start_city_tsp = input("Masukkan Kota Awal untuk TSP: ").strip().title()
        if start_city_tsp in cities:
            break
        else:
            print("Kota Awal tidak ditemukan. Silakan coba lagi.")

    print(f"\nMencari rute mengunjungi semua kota sekali (mulai dari {start_city_tsp}).")

    # Panggil fungsi TSP dengan kota awal pilihan pengguna
    best_route_tsp, min_distance_tsp = tsp_brute_force(adjacency_list, start_city_tsp)

    # Tampilkan hasilnya
    if best_route_tsp:
        print(f"\nRute TSP Terbaik:")
        print(" -> ".join(best_route_tsp))
        print(f"Total Jarak: {min_distance_tsp} KM")
    else:
        print("\nTidak dapat menemukan rute TSP yang valid.")

# --- 9. Menjalankan Fungsi ---
run_dijkstra_test() # Menjalankan Dijkstra
run_tsp_test()      # Menjalankan TSP

# --- 10. Visualisasi Graf ---
print("\nMembuat visualisasi graf...")
G_viz = nx.Graph()
G_viz.add_nodes_from(cities)
for city1, city2, distance in edges_with_distance:
    G_viz.add_edge(city1, city2, weight=distance)

print(f"Status Graf: {'TERHUBUNG' if nx.is_connected(G_viz) else 'TIDAK TERHUBUNG!'}")
print("-" * 55)

pos = nx.circular_layout(G_viz)
edge_labels = nx.get_edge_attributes(G_viz, 'weight')

plt.figure(figsize=(18, 18))
nx.draw(
    G_viz, pos, with_labels=True, node_color='skyblue',
    node_size=5000, font_size=10, font_weight='bold',
    edge_color='gray', width=1.5
)
nx.draw_networkx_edge_labels(
    G_viz, pos, edge_labels=edge_labels, font_size=8,
    font_color='black', label_pos=0.35,
    bbox=dict(facecolor='white', edgecolor='none', alpha=0.5)
)

plt.title("Visualisasi Graf Peta Kota Indonesia", fontsize=18)
plt.axis('off')
plt.show()

print("\nProgram Selesai.")