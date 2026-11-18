import json
from dataclasses import asdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from circuitlab.plotting import plot_result
from circuitlab.simulation import Circuit, simulate


def main():
    output = Path(__file__).resolve().parent / "reports"
    output.mkdir(exist_ok=True)
    reports = []
    for name, circuit in [
        ("charging", Circuit(1000, 100e-6, 5, 0)),
        ("discharging", Circuit(1000, 100e-6, 0, 5)),
    ]:
        frame = simulate(circuit)
        frame.to_csv(output / f"{name}.csv", index=False)
        fig = plot_result(frame, circuit.tau)
        fig.savefig(output / f"{name}.png", dpi=160)
        plt.close(fig)
        reports.append(
            {
                "mode": name,
                **asdict(circuit),
                "tau_s": circuit.tau,
                "max_absolute_error_v": float(frame.absolute_error_v.max()),
                "samples": len(frame),
            }
        )
    (output / "validation.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
