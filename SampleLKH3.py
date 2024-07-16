import subprocess
import os

def clear_logs():
    if os.path.exists('lkh3_logs'):
        for file in os.listdir('lkh3_logs'):
            os.remove(os.path.join('lkh3_logs', file))
    else:
        os.mkdir('lkh3_logs')

def get_edge_list(distance_matrix):
    edge_list = []
    dimension = len(distance_matrix)
    for i in range(dimension):
        for j in range(dimension):
            if i != j:
                edge_list.append([i + 1, j + 1, distance_matrix[i][j]])  # Nodes are 1-indexed in TSPLIB format
    return edge_list

def tsplib_TSP(filename, distance_matrix):
    dimension = len(distance_matrix)
    with open(f"lkh3_logs/{filename}", 'w') as f:
        f.write("NAME: TSP\n")
        f.write("TYPE: ATSP\n")
        f.write(f"DIMENSION: {dimension}\n")
        f.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
        f.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
        f.write("EDGE_WEIGHT_SECTION\n")
        for row in distance_matrix:
            f.write(" ".join(map(str, row)) + "\n")
        f.write("EOF\n")

def tsplib_STTSP(filename, edge_list, terminals):
    dimension = max(max(edge[0], edge[1]) for edge in edge_list)
    with open(f"lkh3_logs/{filename}", 'w') as f:
        f.write("NAME: STSP_75-1over3\n")
        f.write("TYPE: STTSP\n")
        f.write(f"DIMENSION: {dimension}\n")
        f.write("EDGE_DATA_FORMAT: EDGE_LIST\n")
        f.write("EDGE_DATA_SECTION\n")
        for edge in edge_list:
            f.write(" ".join(map(str, edge)) + "\n")
        f.write("-1\n")
        f.write("REQUIRED_NODES_SECTION\n")
        for terminal in terminals:
            f.write(f"{terminal}\n")
        f.write("-1\n")
        f.write("EOF\n")

def tsplib_TSPTW(filename, distance_matrix, time_windows, depot):
    dimension = len(distance_matrix)
    with open(f"lkh3_logs/{filename}", 'w') as f:
        f.write("NAME : tsp time windows\n")
        f.write("TYPE : TSPTW\n")
        f.write(f"DIMENSION : {dimension}\n")
        f.write("EDGE_WEIGHT_TYPE : EXPLICIT\n")
        f.write("EDGE_WEIGHT_FORMAT : FULL_MATRIX\n")
        f.write("EDGE_WEIGHT_SECTION\n")
        for row in distance_matrix:
            f.write(" ".join(map(str, row)) + "\n")
        f.write("TIME_WINDOW_SECTION\n")
        for node, start, end in time_windows:
            f.write(f"{node} {start} {end}\n")
        f.write("DEPOT_SECTION\n")
        f.write(f"{depot}\n")
        f.write("-1\n")
        f.write("EOF\n")

def par_file(filename, tsp_filename):
    with open(filename, 'w') as f:
        f.write(f"PROBLEM_FILE = lkh3_logs/{tsp_filename}\n")
        f.write("OUTPUT_TOUR_FILE = lkh3_logs/tour.txt\n")

def read_tour(filename):
    with open(f'lkh3_logs/{filename}', 'r') as f:
        lines = f.readlines()
        tour_start = lines.index("TOUR_SECTION\n") + 1
        tour_end = lines.index("-1\n")
        tour = lines[tour_start:tour_end]
        tour = [int(node.strip()) for node in tour]
        return tour

def run_lkh(par_filename):
    lkh_path = "/Users/debojjalbagchi/Documents/LKH3_Solver/LKH-3.0.10/LKH"  # TODO: Replace with the actual path
    subprocess.run([lkh_path, par_filename])

if __name__ == "__main__":
    
    clear_logs()

    pr_type = 'TSP' # 'TSP', 'STTSP', 'TSPTW', 'Clear'
    distance_matrix = [
        [0, 10, 15, 20, 25],
        [5, 0, 9, 10, 15],
        [6, 13, 0, 12, 8],
        [8, 8, 9, 0, 10],
        [15, 5, 6, 9, 0]
    ]

    if pr_type == 'Clear':
        quit()

    if pr_type == "TSP":
        tsp_filename = "tsp_data.atsp"
        tsplib_TSP(tsp_filename, distance_matrix)

    if pr_type == 'STTSP':
        edge_list = get_edge_list(distance_matrix)
        terminals = [1, 3, 4]
        tsp_filename = "steiner_tsp_data.sttsp"
        tsplib_STTSP(tsp_filename, edge_list, terminals)

    if pr_type == 'TSPTW':
        depot = 1
        time_windows = [
            (1, 0, 9600000),
            (2, 430000, 2830000),
            (3, 360000, 2760000),
            (4, 330000, 2730000),
            (5, 330000, 2730000)
        ]
        tsp_filename = "tsptw_data.tsptw"
        tsplib_TSPTW(tsp_filename, distance_matrix, time_windows, depot)

    par_filename = "params.par"
    par_file(par_filename, tsp_filename)
    run_lkh(par_filename)
    tour = read_tour("tour.txt")
    print("Optimal tour:", tour)
