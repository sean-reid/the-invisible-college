#!/usr/bin/env python3
"""
Generate coverage heatmaps from simulation results.
Reads coverage_results.json, produces four PNG heatmaps plus a summary PNG.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

DIST_NAMES = [
    'Normal(0,1)',
    't(3)',
    'Lognormal(0,1)',
    'Exponential(1)',
    'Pareto(2.5)',
    'Beta(0.5,0.5)',
]

SAMPLE_SIZES = [5, 10, 15, 20, 30, 50, 100, 200]
METHOD_NAMES = ['Student-t', 'Basic Bootstrap', 'Percentile Bootstrap', 'BCa Bootstrap']

# Short names for display
DIST_LABELS = [
    'Normal(0,1)',
    't(3)',
    'Lognormal(0,1)',
    'Exponential(1)',
    'Pareto(2.5)',
    'Beta(0.5,0.5)',
]

METHOD_SHORT = ['Student-t', 'Basic Bootstrap', 'Percentile Bootstrap', 'BCa Bootstrap']


def load_results(path='coverage_results.json'):
    with open(path) as fh:
        return json.load(fh)


def extract_grid(results, method):
    """Return 6x8 array of coverage values."""
    grid = np.zeros((len(DIST_NAMES), len(SAMPLE_SIZES)))
    for i, d in enumerate(DIST_NAMES):
        for j, n in enumerate(SAMPLE_SIZES):
            grid[i, j] = results[d][str(n)][method]['coverage']
    return grid


def make_heatmap(ax, grid, title, vmin=0.70, vmax=1.00):
    """Plot a single coverage heatmap on ax."""
    # Custom diverging colormap centered at 0.95 (nominal level)
    # Below 0.90 = deep red, 0.95 = white, above 0.97 = deep blue
    colors_low  = ['#8B0000', '#CC0000', '#FF4444', '#FF9999', '#FFCCCC']
    colors_high = ['#E8E8FF', '#AAAAFF', '#5555FF', '#0000CC', '#000088']
    n_low  = len(colors_low)
    n_high = len(colors_high)

    # Build custom colormap
    # Map [vmin, 0.90] → deep red to light red
    # Map [0.90, 0.95] → light red to white
    # Map [0.95, 0.97] → white to light blue
    # Map [0.97, vmax] → light blue to deep blue
    from matplotlib.colors import LinearSegmentedColormap
    cmap_data = [
        (0.00, '#8B0000'),   # vmin (0.70)
        (0.20, '#CC0000'),   # 0.76
        (0.40, '#FF4444'),   # 0.82
        (0.50, '#FF9999'),   # 0.85
        (0.60, '#FFCCCC'),   # 0.88
        (0.667, '#FFE8E8'),  # 0.90 (failure threshold)
        (0.833, '#FFFFFF'),  # 0.95 (nominal)
        (0.90,  '#CCCCFF'),  # 0.97 (overcoverage threshold)
        (1.00,  '#0000AA'),  # vmax (1.00)
    ]
    cmap = LinearSegmentedColormap.from_list(
        'coverage',
        [(pos, col) for pos, col in cmap_data]
    )

    im = ax.imshow(
        grid,
        aspect='auto',
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        interpolation='nearest',
    )

    # Add contour lines at 0.90, 0.93, 0.95
    X = np.arange(len(SAMPLE_SIZES))
    Y = np.arange(len(DIST_NAMES))
    # Use contourf for crisp boundaries
    levels = [0.90, 0.93, 0.95, 0.97]
    contour_colors = ['#660000', '#AA3300', '#003300', '#000066']
    cs = ax.contour(
        X, Y, grid,
        levels=levels,
        colors=contour_colors,
        linewidths=1.2,
        linestyles=['--', '--', '-', '--'],
    )
    ax.clabel(cs, fmt='%.2f', fontsize=7, inline=True)

    # Add value text
    for i in range(len(DIST_NAMES)):
        for j in range(len(SAMPLE_SIZES)):
            val = grid[i, j]
            color = 'white' if val < 0.85 or val > 0.98 else 'black'
            ax.text(j, i, f'{val:.3f}', ha='center', va='center',
                    fontsize=7, color=color, fontweight='bold')

    ax.set_xticks(range(len(SAMPLE_SIZES)))
    ax.set_xticklabels([f'n={n}' for n in SAMPLE_SIZES], fontsize=9)
    ax.set_yticks(range(len(DIST_NAMES)))
    ax.set_yticklabels(DIST_LABELS, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)

    return im


def main():
    results = load_results()

    os.makedirs('figures', exist_ok=True)

    # --- Individual heatmaps ---
    for method in METHOD_NAMES:
        fig, ax = plt.subplots(figsize=(10, 4.5))
        grid = extract_grid(results, method)
        im = make_heatmap(ax, grid, f'Coverage Probability — {method}')
        plt.colorbar(im, ax=ax, label='Coverage probability', shrink=0.8)
        ax.set_xlabel('Sample size', fontsize=10)
        ax.set_ylabel('Population distribution', fontsize=10)
        plt.tight_layout()
        safe_name = method.lower().replace(' ', '_').replace('-', '_')
        outpath = f'figures/heatmap_{safe_name}.png'
        plt.savefig(outpath, dpi=150, bbox_inches='tight')
        plt.close()
        print(f'Saved {outpath}')

    # --- 2x2 panel of all four methods ---
    fig, axes = plt.subplots(2, 2, figsize=(18, 9))
    fig.suptitle(
        'Realized Coverage Probability (95% CI methods, 10,000 trials per cell)\n'
        'Contours at 0.90, 0.93, 0.95, 0.97',
        fontsize=13, fontweight='bold', y=1.02
    )

    method_ax = [
        ('Student-t',            axes[0, 0]),
        ('Basic Bootstrap',      axes[0, 1]),
        ('Percentile Bootstrap', axes[1, 0]),
        ('BCa Bootstrap',        axes[1, 1]),
    ]

    all_grids = {}
    ims = []
    for method, ax in method_ax:
        grid = extract_grid(results, method)
        all_grids[method] = grid
        im = make_heatmap(ax, grid, method)
        ims.append(im)
        ax.set_xlabel('Sample size', fontsize=9)
        ax.set_ylabel('Distribution', fontsize=9)

    # Shared colorbar
    cbar = fig.colorbar(ims[0], ax=axes, label='Coverage probability', shrink=0.6, aspect=30)

    plt.tight_layout()
    plt.savefig('figures/heatmaps_all.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved figures/heatmaps_all.png')

    # --- Difference map: BCa vs percentile ---
    fig, ax = plt.subplots(figsize=(10, 4.5))
    diff = all_grids['BCa Bootstrap'] - all_grids['Percentile Bootstrap']
    vmax_d = max(abs(diff.min()), abs(diff.max())) + 0.005
    im2 = ax.imshow(
        diff,
        aspect='auto',
        cmap='RdBu',
        vmin=-vmax_d,
        vmax=vmax_d,
        interpolation='nearest',
    )
    plt.colorbar(im2, ax=ax, label='BCa coverage − Percentile coverage', shrink=0.8)
    for i in range(len(DIST_NAMES)):
        for j in range(len(SAMPLE_SIZES)):
            val = diff[i, j]
            color = 'white' if abs(val) > 0.03 else 'black'
            sign = '+' if val > 0 else ''
            ax.text(j, i, f'{sign}{val:.3f}', ha='center', va='center',
                    fontsize=7.5, color=color, fontweight='bold')
    ax.set_xticks(range(len(SAMPLE_SIZES)))
    ax.set_xticklabels([f'n={n}' for n in SAMPLE_SIZES], fontsize=9)
    ax.set_yticks(range(len(DIST_NAMES)))
    ax.set_yticklabels(DIST_LABELS, fontsize=9)
    ax.set_title('BCa Bootstrap coverage minus Percentile Bootstrap coverage\n'
                 'Blue = BCa better, Red = Percentile better', fontsize=11)
    ax.set_xlabel('Sample size', fontsize=10)
    ax.set_ylabel('Distribution', fontsize=10)
    plt.tight_layout()
    plt.savefig('figures/diff_bca_vs_percentile.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved figures/diff_bca_vs_percentile.png')

    # --- Print key stats ---
    print('\n--- BCa minus Percentile coverage ---')
    print(f"{'Distribution':<20s} " + "  ".join(f"n={n:<3d}" for n in SAMPLE_SIZES))
    for i, d in enumerate(DIST_NAMES):
        row = f"{d:<20s} "
        for j, n in enumerate(SAMPLE_SIZES):
            v = diff[i, j]
            sign = '+' if v >= 0 else ''
            row += f" {sign}{v:+.3f}"
        print(row)

    print('\nDone.')


if __name__ == '__main__':
    main()
