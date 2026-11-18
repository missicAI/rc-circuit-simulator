import matplotlib.pyplot as plt


def plot_result(frame, tau):
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True, layout="constrained")
    axes[0].plot(
        frame.time_s, frame.voltage_numerical_v, color="#2563eb", label="Numerical (solve_ivp)", linewidth=2.5
    )
    axes[0].plot(
        frame.time_s, frame.voltage_analytical_v, "--", color="#f59e0b", label="Analytical", linewidth=1.6
    )
    axes[0].axvline(tau, color="#94a3b8", linestyle=":", label="Time constant RC")
    axes[0].set_ylabel("Capacitor voltage (V)")
    axes[0].legend()
    axes[1].plot(frame.time_s, frame.current_a * 1000, color="#0f766e", linewidth=2)
    axes[1].set_ylabel("Resistor current (mA)")
    axes[1].set_xlabel("Time (s)")
    for axis in axes:
        axis.grid(alpha=0.2)
    fig.suptitle("Ideal series RC circuit — transient response")
    return fig
