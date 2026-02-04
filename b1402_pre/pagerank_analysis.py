"""pagerank_analysis.py

Compute PageRank for a very large edge-list dataset (two integers per line) and
produce plots (histogram + heat map + radar map) plus basic statistics.

Extra:
- Optional sampling of edges to keep runtime bounded.
- Optional interactive lookup of PageRank value for a given node.
- Stores the mapping from original node-id -> internal index so lookup works
  consistently across sampling changes.

Usage examples:
  python pagerank_analysis.py --input twitter_combined.txt
  python pagerank_analysis.py --input twitter_combined.txt --edge-sample 0.2
  python pagerank_analysis.py --input twitter_combined.txt --max-edges 5000000
  python pagerank_analysis.py --input twitter_combined.txt --interactive

Outputs:
  pagerank_hist.png
  pagerank_heat.png
  pagerank_radar.png
  pagerank_stats.txt
  pagerank_values.npz
"""

from __future__ import annotations

import argparse
import os
import random
from typing import Dict, Iterable, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def read_edges_sampled(
    path: str,
    seed: int,
    edge_sample: float | None,
    max_edges: int | None,
) -> List[Tuple[int, int]]:
    """Read edges with optional Bernoulli sampling and/or cap."""
    rng = random.Random(seed)
    edges: List[Tuple[int, int]] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if edge_sample is not None and edge_sample < 1.0:
                if rng.random() > edge_sample:
                    continue

            s, t = map(int, line.split())
            edges.append((s, t))

            if max_edges is not None and len(edges) >= max_edges:
                break

    return edges


def build_digraph(edges: List[Tuple[int, int]]) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


def save_hist(values: Iterable[float], title: str, xlabel: str, out_path: str, bins: int = 40) -> None:
    vals = [v for v in values if v is not None and np.isfinite(v)]
    if not vals:
        return
    plt.figure(figsize=(8, 5))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency (log scale)")
    plt.hist(vals, bins=bins, log=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def save_heatmap(values: Iterable[float], title: str, out_path: str, bins: int = 60) -> None:
    vals = np.array([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if vals.size == 0:
        return

    vmin = float(np.min(vals))
    vmax = float(np.max(vals))
    if vmin == vmax:
        plt.figure(figsize=(6, 5))
        plt.title(title)
        plt.text(0.5, 0.5, f"All values == {vmin:.6g}", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(out_path, dpi=200)
        plt.close()
        return

    # PageRank is positive; log bins are safe.
    xbins = np.logspace(np.log10(max(vmin, 1e-18)), np.log10(vmax), bins)
    H, xedges, yedges = np.histogram2d(vals, vals, bins=(xbins, xbins))

    plt.figure(figsize=(7, 6))
    plt.title(title)
    plt.imshow(
        np.log1p(H),
        origin="lower",
        aspect="auto",
        cmap="viridis",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
    )
    plt.xlabel("PageRank")
    plt.ylabel("PageRank")
    plt.colorbar(label="log(1 + count)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def save_radar(values: Iterable[float], title: str, out_path: str, bins: int = 10) -> None:
    vals = np.array([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if vals.size == 0:
        return

    qs = np.linspace(0, 1, bins + 1)
    edges = np.quantile(vals, qs)
    edges = np.unique(edges)
    if edges.size < 3:
        plt.figure(figsize=(7, 4))
        plt.title(title)
        plt.bar(["all"], [vals.size])
        plt.ylabel("count")
        plt.tight_layout()
        plt.savefig(out_path, dpi=200)
        plt.close()
        return

    counts, _ = np.histogram(vals, bins=edges)
    counts = counts.astype(float)
    if counts.sum() > 0:
        counts /= counts.sum()

    labels = [f"q{int(q*100)}-{int(qs[i+1]*100)}" for i, q in enumerate(qs[:-1])][: len(counts)]

    angles = np.linspace(0, 2 * np.pi, len(counts), endpoint=False)
    counts_loop = np.concatenate([counts, counts[:1]])
    angles_loop = np.concatenate([angles, angles[:1]])

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, polar=True)
    ax.set_title(title, va="bottom")
    ax.plot(angles_loop, counts_loop, linewidth=2)
    ax.fill(angles_loop, counts_loop, alpha=0.25)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def write_stats(values: np.ndarray, out_path: str, extra: Dict[str, str]) -> None:
    vals = values[np.isfinite(values)]
    if vals.size == 0:
        return

    lines = []
    lines.append("PageRank basic statistics")
    lines.append(f"count={vals.size}")
    lines.append(f"min={float(np.min(vals)):.12g}")
    lines.append(f"max={float(np.max(vals)):.12g}")
    lines.append(f"mean={float(np.mean(vals)):.12g}")
    lines.append(f"median={float(np.median(vals)):.12g}")
    lines.append(f"std={float(np.std(vals)):.12g}")
    lines.append(f"p90={float(np.quantile(vals, 0.90)):.12g}")
    lines.append(f"p99={float(np.quantile(vals, 0.99)):.12g}")

    for k, v in extra.items():
        lines.append(f"{k}={v}")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="twitter_combined.txt", help="Edge list input file")
    ap.add_argument("--outdir", default=".", help="Directory to write plots")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument(
        "--edge-sample",
        type=float,
        default=None,
        help="Bernoulli sample ratio in (0,1]; e.g. 0.2 keeps ~20%% edges",
    )
    ap.add_argument(
        "--max-edges",
        type=int,
        default=None,
        help="Hard cap on number of edges read (applied after sampling)",
    )
    ap.add_argument("--alpha", type=float, default=0.85, help="PageRank damping factor")
    ap.add_argument("--max-iter", type=int, default=100)
    ap.add_argument("--tol", type=float, default=1e-06)
    ap.add_argument("--interactive", action="store_true", help="Prompt to query PageRank by node id")
    ap.add_argument("--force", action="store_true", help="Regenerate plots even if they exist")
    args = ap.parse_args()

    ensure_dir(args.outdir)

    print("Reading edges...")
    edges = read_edges_sampled(args.input, seed=args.seed, edge_sample=args.edge_sample, max_edges=args.max_edges)
    print(f"Edges loaded: {len(edges):,}")

    print("Building directed graph...")
    G = build_digraph(edges)
    print(f"Graph: |V|={G.number_of_nodes():,}, |E|={G.number_of_edges():,}")

    print("Computing PageRank...")
    pr: Dict[int, float] = nx.pagerank(G, alpha=args.alpha, max_iter=args.max_iter, tol=args.tol)

    # Stable arrays for saving/lookup.
    nodes = np.array(sorted(pr.keys()), dtype=np.int64)
    values = np.array([pr[int(n)] for n in nodes], dtype=np.float64)

    # Save values so lookups can be reproduced later.
    npz_path = os.path.join(args.outdir, "pagerank_values.npz")
    np.savez_compressed(
        npz_path,
        nodes=nodes,
        pagerank=values,
        meta=np.array(
            [
                f"input={args.input}",
                f"seed={args.seed}",
                f"edge_sample={args.edge_sample}",
                f"max_edges={args.max_edges}",
                f"alpha={args.alpha}",
                f"max_iter={args.max_iter}",
                f"tol={args.tol}",
            ],
            dtype=object,
        ),
    )

    stats_path = os.path.join(args.outdir, "pagerank_stats.txt")
    write_stats(
        values,
        stats_path,
        extra={
            "nodes_total": str(G.number_of_nodes()),
            "edges_total": str(G.number_of_edges()),
            "edge_sample": str(args.edge_sample),
            "max_edges": str(args.max_edges),
            "alpha": str(args.alpha),
            "max_iter": str(args.max_iter),
            "tol": str(args.tol),
        },
    )

    hist_path = os.path.join(args.outdir, "pagerank_hist.png")
    heat_path = os.path.join(args.outdir, "pagerank_heat.png")
    radar_path = os.path.join(args.outdir, "pagerank_radar.png")

    if args.force or not os.path.isfile(hist_path):
        save_hist(values, "PageRank Histogram", "PageRank", hist_path)
        print("PageRank histogram made!")
    else:
        print("PageRank histogram already exists!")

    if args.force or not os.path.isfile(heat_path):
        save_heatmap(values, "PageRank Heat Map", heat_path)
        print("PageRank heat map made!")
    else:
        print("PageRank heat map already exists!")

    if args.force or not os.path.isfile(radar_path):
        save_radar(values, "PageRank Radar Map", radar_path)
        print("PageRank radar map made!")
    else:
        print("PageRank radar map already exists!")

    print(f"Wrote: {stats_path}")
    print(f"Wrote: {npz_path}")

    if args.interactive:
        # Build dict for fast lookup
        lookup = {int(n): float(v) for n, v in zip(nodes, values)}
        print("Interactive PageRank lookup. Type a node id (int), or 'q' to quit.")
        while True:
            raw = input("> ").strip()
            if raw.lower() in {"q", "quit", "exit"}:
                break
            try:
                node = int(raw)
            except ValueError:
                print("Please enter an integer node id, or 'q'.")
                continue

            if node in lookup:
                print(f"pagerank[{node}] = {lookup[node]:.12g}")
            else:
                print("Node not present in the current sampled graph.\n"
                      "(If you changed --edge-sample/--max-edges, presence may change.)")

    print("Finished!")


if __name__ == "__main__":
    main()
