
"""centralityhistograms.py

Reads an edge-list Twitter dataset (two integers per line) and generates plots for
multiple centrality measures.

Changes vs b1402_pre:
- Added Katz centrality and Eigenvector centrality.
- For EACH of the two new centralities, generates:
  1) histogram (for parity with existing outputs)
  2) heat map (2D histogram)
  3) radar map (spider chart using binned distribution)

Performance notes:
- The full twitter_combined graph is very large; exact closeness/eigenvector on
  the full graph may be slow. This script uses sampling + optional subgraphing
  to keep runtime reasonable (target: < ~5 minutes on typical machines).

Usage:
  python centralityhistograms.py --input twitter_combined.txt

Outputs are written to the current working directory.
"""

from __future__ import annotations

import argparse
import os
import random
from typing import Dict, Iterable, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def read_graph_edgelist(path: str, directed: bool = True, undirected: bool = True) -> nx.Graph:
    """Read an edge list file with two integers per line."""
    Gd = nx.DiGraph() if directed else nx.Graph()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            s, t = map(int, line.split())
            Gd.add_edge(s, t)

    if undirected:
        return Gd.to_undirected()
    return Gd


def safe_sample_nodes(nodes: List[int], k: int, seed: int) -> List[int]:
    if not nodes:
        return []
    if k >= len(nodes):
        return list(nodes)
    rng = random.Random(seed)
    return rng.sample(nodes, k=k)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_hist(values: Iterable[float], title: str, xlabel: str, out_path: str, bins: int = 30) -> None:
    vals = [v for v in values if v is not None and not np.isnan(v) and np.isfinite(v)]
    if not vals:
        print(f"[skip] No finite values for {title}")
        return
    plt.figure(figsize=(8, 5))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency (log scale)")
    plt.hist(vals, bins=bins, log=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def save_heatmap(values: Iterable[float], title: str, out_path: str, bins: int = 50) -> None:
    """2D heatmap using (value, value) density (visualizes distribution intensity)."""
    vals = np.array([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if vals.size == 0:
        print(f"[skip] No finite values for {title}")
        return

    # Use log-spaced bins when data is heavily skewed.
    vmin = float(np.min(vals))
    vmax = float(np.max(vals))
    if vmin == vmax:
        # Degenerate distribution; fallback to a simple image.
        plt.figure(figsize=(6, 5))
        plt.title(title)
        plt.text(0.5, 0.5, f"All values == {vmin:.4g}", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(out_path, dpi=200)
        plt.close()
        return

    # Avoid negative/zero for log scale; if present, use linear bins.
    if vmin > 0:
        xbins = np.logspace(np.log10(vmin), np.log10(vmax), bins)
    else:
        xbins = np.linspace(vmin, vmax, bins)

    H, xedges, yedges = np.histogram2d(vals, vals, bins=(xbins, xbins))
    plt.figure(figsize=(7, 6))
    plt.title(title)
    plt.imshow(
        np.log1p(H),
        origin="lower",
        aspect="auto",
        cmap="inferno",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
    )
    plt.xlabel("Centrality value")
    plt.ylabel("Centrality value")
    plt.colorbar(label="log(1 + count)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def save_radar(values: Iterable[float], title: str, out_path: str, bins: int = 8) -> None:
    """Radar (spider) chart over binned distribution quantiles."""
    vals = np.array([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if vals.size == 0:
        print(f"[skip] No finite values for {title}")
        return

    # Quantile bin edges to balance skew
    qs = np.linspace(0, 1, bins + 1)
    edges = np.quantile(vals, qs)
    # Make edges strictly increasing to avoid zero-width bins
    edges = np.unique(edges)
    if edges.size < 3:
        # Not enough spread; use a simple bar as fallback
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

    # Radar: close the loop
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


def maybe_subgraph(G: nx.Graph, max_nodes: int, seed: int) -> nx.Graph:
    """Return G if small enough, else induce a subgraph on a random node sample."""
    n = G.number_of_nodes()
    if n <= max_nodes:
        return G
    nodes = list(G.nodes())
    sample = safe_sample_nodes(nodes, k=max_nodes, seed=seed)
    return G.subgraph(sample).copy()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="twitter_combined.txt", help="Edge list input file")
    ap.add_argument("--outdir", default=".", help="Directory to write plots")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--closeness-sample", type=int, default=1000)
    ap.add_argument("--katz-max-nodes", type=int, default=50000, help="Max nodes for Katz/eigenvector computations")
    ap.add_argument(
        "--force",
        action="store_true",
        help="Regenerate plots even if output files already exist",
    )
    args = ap.parse_args()

    ensure_dir(args.outdir)

    print("Reading graph...")
    G = read_graph_edgelist(args.input, directed=True, undirected=True)
    print(f"Graph loaded: |V|={G.number_of_nodes():,}, |E|={G.number_of_edges():,}")

    # Degree centrality histogram (full graph; fast)
    degree_png = os.path.join(args.outdir, "degree_c.png")
    if args.force or not os.path.isfile(degree_png):
        degree_c = nx.degree_centrality(G)
        save_hist(
            degree_c.values(),
            title="Degree Centrality Plot",
            xlabel="Degree Centrality (normalized)",
            out_path=degree_png,
        )
        print("Degree centrality plot made!")
    else:
        print("Degree centrality plot already exists!")

    # Closeness centrality histogram (sampled nodes; keeps time bounded)
    close_png = os.path.join(args.outdir, "closeness_c.png")
    if args.force or not os.path.isfile(close_png):
        nodes = list(G.nodes())
        closeness_sample = safe_sample_nodes(nodes, k=args.closeness_sample, seed=args.seed)
        closeness_c = {node: nx.closeness_centrality(G, node) for node in closeness_sample}
        save_hist(
            closeness_c.values(),
            title=f"Closeness Centrality Plot (sample={len(closeness_sample)})",
            xlabel="Closeness Centrality (normalized)",
            out_path=close_png,
        )
        print("Closeness centrality plot made!")
    else:
        print("Closeness centrality plot already exists!")

    # Betweenness centrality histogram (approx by k samples)
    between_png = os.path.join(args.outdir, "betweenness_c.png")
    if args.force or not os.path.isfile(between_png):
        betweenness_c = nx.betweenness_centrality(G, k=1000, seed=args.seed)
        save_hist(
            betweenness_c.values(),
            title="Betweenness Centrality Plot (k=1000 sample)",
            xlabel="Betweenness Centrality (normalized)",
            out_path=between_png,
        )
        print("Betweenness centrality plot made!")
    else:
        print("Betweenness centrality plot already exists!")

    # Katz + Eigenvector: compute on a bounded subgraph for speed.
    H = maybe_subgraph(G, max_nodes=args.katz_max_nodes, seed=args.seed)
    if H is not G:
        print(f"Using induced subgraph for Katz/Eigenvector: |V|={H.number_of_nodes():,}, |E|={H.number_of_edges():,}")

    # Katz centrality
    katz_hist = os.path.join(args.outdir, "katz_c_hist.png")
    katz_heat = os.path.join(args.outdir, "katz_c_heat.png")
    katz_radar = os.path.join(args.outdir, "katz_c_radar.png")

    if args.force or not (os.path.isfile(katz_hist) and os.path.isfile(katz_heat) and os.path.isfile(katz_radar)):
        print("Computing Katz centrality...")
        # Heuristic alpha: must be < 1/lambda_max; use a conservative small value.
        # networkx can estimate; we keep alpha small for stability.
        katz_c = nx.katz_centrality(H, alpha=0.005, beta=1.0, max_iter=200, tol=1e-06, nstart=None, normalized=True)
        vals = list(katz_c.values())
        save_hist(vals, "Katz Centrality Histogram", "Katz centrality", katz_hist)
        save_heatmap(vals, "Katz Centrality Heat Map", katz_heat)
        save_radar(vals, "Katz Centrality Radar Map", katz_radar)
        print("Katz plots made!")
    else:
        print("Katz plots already exist!")

    # Eigenvector centrality
    eig_hist = os.path.join(args.outdir, "eigenvector_c_hist.png")
    eig_heat = os.path.join(args.outdir, "eigenvector_c_heat.png")
    eig_radar = os.path.join(args.outdir, "eigenvector_c_radar.png")

    if args.force or not (os.path.isfile(eig_hist) and os.path.isfile(eig_heat) and os.path.isfile(eig_radar)):
        print("Computing Eigenvector centrality...")
        # Power iteration; on huge graphs this can be expensive, hence subgraph.
        eig_c = nx.eigenvector_centrality(H, max_iter=200, tol=1e-06)
        vals = list(eig_c.values())
        save_hist(vals, "Eigenvector Centrality Histogram", "Eigenvector centrality", eig_hist)
        save_heatmap(vals, "Eigenvector Centrality Heat Map", eig_heat)
        save_radar(vals, "Eigenvector Centrality Radar Map", eig_radar)
        print("Eigenvector plots made!")
    else:
        print("Eigenvector plots already exist!")

    print("Finished!")


if __name__ == "__main__":
    main()
