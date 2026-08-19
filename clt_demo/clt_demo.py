"""
Central Limit Theorem demo.

Draws samples from a clearly non-normal population (an exponential
distribution), then repeatedly takes the mean of small samples drawn from
it. As the sample size grows, the distribution of those sample means
approaches a normal distribution, regardless of the shape of the original
population.
"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=42)

# Population: exponential distribution (highly skewed, not normal at all).
POPULATION_SCALE = 1.0
population_mean = POPULATION_SCALE
population_std = POPULATION_SCALE

n_trials = 10_000
sample_sizes = [1, 2, 5, 30]

fig, axes = plt.subplots(1, len(sample_sizes), figsize=(16, 4), sharey=True)

for ax, n in zip(axes, sample_sizes):
    # For each trial, draw n samples from the population and record their mean.
    samples = rng.exponential(scale=POPULATION_SCALE, size=(n_trials, n))
    sample_means = samples.mean(axis=1)

    ax.hist(sample_means, bins=50, density=True, color="steelblue", alpha=0.7)
    ax.set_title(f"n = {n}")
    ax.set_xlabel("sample mean")

    # Overlay the normal distribution the CLT predicts:
    # mean = population mean, std = population std / sqrt(n)
    predicted_std = population_std / np.sqrt(n)
    x = np.linspace(sample_means.min(), sample_means.max(), 200)
    normal_pdf = (
        1
        / (predicted_std * np.sqrt(2 * np.pi))
        * np.exp(-0.5 * ((x - population_mean) / predicted_std) ** 2)
    )
    ax.plot(x, normal_pdf, color="crimson", linewidth=2, label="predicted normal")
    ax.legend(fontsize=8)

axes[0].set_ylabel("density")
fig.suptitle(
    "Central Limit Theorem: distribution of sample means from an exponential population",
    fontsize=13,
)
fig.tight_layout()
fig.savefig("clt_demo.png", dpi=150)
print("Saved plot to clt_demo.png")

for n in sample_sizes:
    samples = rng.exponential(scale=POPULATION_SCALE, size=(n_trials, n))
    sample_means = samples.mean(axis=1)
    print(
        f"n={n:>3}: mean of sample means = {sample_means.mean():.3f}, "
        f"std of sample means = {sample_means.std():.3f} "
        f"(predicted: {population_std / np.sqrt(n):.3f})"
    )
