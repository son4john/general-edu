# CLT Demo

A small demonstration of the Central Limit Theorem (CLT).

The script draws samples from a clearly non-normal population (an
exponential distribution), then repeatedly computes the mean of samples of
size `n` drawn from it. As `n` grows, the distribution of those sample
means approaches a normal distribution, regardless of the shape of the
original population — this is the CLT in action.

## Files

- `clt_demo.py` — generates the sample means for `n = 1, 2, 5, 30`, plots
  histograms of each against the normal distribution the CLT predicts
  (mean = population mean, std = population std / sqrt(n)), and prints
  summary statistics for each `n`.
- `clt_demo.png` — the output plot produced by the script.

## Usage

```bash
python clt_demo.py
```

Requires `numpy` and `matplotlib`.
