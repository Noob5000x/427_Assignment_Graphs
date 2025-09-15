import argparse as ap

def get_args():
    parser = ap.ArgumentParser()

    parser.add_argument("--input")
    parser.add_argument("--create_random_graph", nargs=2, type=float)

    parser.add_argument("--multi_BFS", nargs="+")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--output")

    return parser.parse_args()