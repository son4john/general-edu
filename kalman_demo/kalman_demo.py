"""
Kalman Filter Educational Demo
================================
Scenario: A car drives in a straight line. We have a noisy GPS sensor
measuring only position. The Kalman filter fuses our motion model with
the noisy measurements to produce a smoother, more accurate estimate.

State vector:  x = [position, velocity]  (2D)
Measurement:   z = [position]            (1D, GPS only)

Kalman Filter Cycle (two steps per time step):
  1. PREDICT — project state forward using motion model
  2. UPDATE  — correct prediction with new measurement
"""

import numpy as np
import matplotlib.pyplot as plt

# ── Simulation parameters ──────────────────────────────────────────────────────
np.random.seed(42)
dt = 0.1          # time step (seconds)
n_steps = 100     # number of time steps
true_velocity = 5.0  # m/s (constant)

# Noise magnitudes
process_noise_std = 0.1    # how much the true motion deviates from our model
measurement_noise_std = 3.0  # GPS noise (meters)

# ── Ground truth & noisy measurements ─────────────────────────────────────────
true_positions = np.array([true_velocity * dt * k for k in range(n_steps)])
measurements   = true_positions + np.random.normal(0, measurement_noise_std, n_steps)

# ── Kalman Filter matrices ─────────────────────────────────────────────────────

# State transition matrix F: x_k = F * x_{k-1}
# "position advances by velocity*dt; velocity stays the same"
F = np.array([[1, dt],
              [0,  1]])

# Measurement matrix H: z_k = H * x_k
# "we can only see position, not velocity"
H = np.array([[1, 0]])

# Process noise covariance Q (how much we trust our motion model)
Q = np.array([[dt**4/4, dt**3/2],
              [dt**3/2, dt**2  ]]) * process_noise_std**2

# Measurement noise covariance R (how noisy is the GPS)
R = np.array([[measurement_noise_std**2]])

# ── Initial state ──────────────────────────────────────────────────────────────
x = np.array([[0.0],   # initial position estimate
              [0.0]])  # initial velocity estimate

P = np.eye(2) * 500   # initial uncertainty (large = "I don't know yet")

# ── Run the filter ─────────────────────────────────────────────────────────────
estimates   = []
uncertainties = []

for z_scalar in measurements:
    z = np.array([[z_scalar]])  # measurement as column vector

    # ── PREDICT step ──────────────────────────────────────────────────────────
    x = F @ x                   # project state forward
    P = F @ P @ F.T + Q         # grow uncertainty (things change between steps)

    # ── UPDATE step ───────────────────────────────────────────────────────────
    S = H @ P @ H.T + R         # innovation covariance (predicted measurement uncertainty)
    K = P @ H.T @ np.linalg.inv(S)  # Kalman gain: how much to trust the measurement
    y = z - H @ x              # innovation: how far off was our prediction?
    x = x + K @ y              # blend prediction and measurement
    P = (np.eye(2) - K @ H) @ P  # reduce uncertainty now that we have a measurement

    estimates.append(x[0, 0])   # save position estimate
    uncertainties.append(np.sqrt(P[0, 0]))  # save 1-sigma position uncertainty

estimates    = np.array(estimates)
uncertainties = np.array(uncertainties)
time         = np.arange(n_steps) * dt

# ── Plot ───────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(12, 9))
fig.suptitle("Kalman Filter Demo: 1D Position Tracking", fontsize=14, fontweight="bold")

# --- Top plot: position ---
ax = axes[0]
ax.plot(time, true_positions, "g-",  linewidth=2,   label="True position")
ax.scatter(time, measurements,  color="red", s=12, alpha=0.5, label="Noisy GPS measurements")
ax.plot(time, estimates,        "b-",  linewidth=2,   label="Kalman estimate")
ax.fill_between(time,
                estimates - 2 * uncertainties,
                estimates + 2 * uncertainties,
                alpha=0.2, color="blue", label="±2σ uncertainty")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Position (m)")
ax.set_title("Position: Truth vs Measurements vs Kalman Estimate")
ax.legend()
ax.grid(True, alpha=0.3)

# Annotate key concepts
ax.annotate("Large uncertainty\nat start", xy=(0.5, estimates[5]),
            xytext=(3, estimates[5] - 8),
            arrowprops=dict(arrowstyle="->", color="black"), fontsize=9)
ax.annotate("Filter converges\nas data accumulates", xy=(3, estimates[30]),
            xytext=(4.5, estimates[30] - 6),
            arrowprops=dict(arrowstyle="->", color="black"), fontsize=9)

# --- Bottom plot: uncertainty over time ---
ax2 = axes[1]
ax2.plot(time, uncertainties, "b-", linewidth=2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Position uncertainty σ (m)")
ax2.set_title("Kalman Filter Uncertainty Over Time\n"
              "(drops fast at first, then plateaus — more data stops helping when process noise is the bottleneck)")
ax2.grid(True, alpha=0.3)
ax2.axhline(measurement_noise_std / np.sqrt(n_steps), color="gray",
            linestyle="--", label="Theoretical floor")
ax2.legend()

plt.tight_layout()
plt.savefig("/Users/johnsonpowers/Documents/kalman_demo.png", dpi=150, bbox_inches="tight")
plt.show()

# ── Print summary ──────────────────────────────────────────────────────────────
raw_error    = np.abs(measurements  - true_positions).mean()
filter_error = np.abs(estimates     - true_positions).mean()
print(f"\n{'='*45}")
print(f"  GPS measurement error (mean absolute): {raw_error:.2f} m")
print(f"  Kalman filter error   (mean absolute): {filter_error:.2f} m")
print(f"  Improvement: {raw_error / filter_error:.1f}x")
print(f"{'='*45}")
print("\nKey matrices (final step):")
print(f"  State estimate x = [pos={x[0,0]:.2f} m, vel={x[1,0]:.2f} m/s]")
print(f"  True final pos  = {true_positions[-1]:.2f} m")
print(f"  True velocity   = {true_velocity:.2f} m/s")
