from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class Circuit:
    resistance_ohm: float
    capacitance_f: float
    source_v: float
    initial_v: float = 0.0

    def validate(self):
        values = [self.resistance_ohm, self.capacitance_f, self.source_v, self.initial_v]
        if not all(np.isfinite(v) for v in values):
            raise ValueError("Thông số phải là số hữu hạn.")
        if self.resistance_ohm <= 0 or self.capacitance_f <= 0:
            raise ValueError("Điện trở và điện dung phải lớn hơn 0.")
        if not np.isfinite(self.tau) or self.tau <= 0:
            raise ValueError("Tích R*C nằm ngoài phạm vi tính toán.")

    @property
    def tau(self):
        return self.resistance_ohm * self.capacitance_f

    @property
    def cutoff_hz(self):
        return 1 / (2 * np.pi * self.tau)


def simulate(circuit: Circuit, duration_s: float | None = None, points: int = 1000) -> pd.DataFrame:
    circuit.validate()
    duration_s = 5 * circuit.tau if duration_s is None else duration_s
    if not np.isfinite(duration_s) or duration_s <= 0:
        raise ValueError("Thời gian mô phỏng phải là số dương hữu hạn.")
    if not isinstance(points, int) or not 2 <= points <= 100000:
        raise ValueError("Số điểm cần là số nguyên từ 2 đến 100.000.")
    times = np.linspace(0, duration_s, points)

    def derivative(t, state):
        return [(circuit.source_v - state[0]) / circuit.tau]

    solution = solve_ivp(
        derivative, (0, duration_s), [circuit.initial_v], t_eval=times, rtol=1e-9, atol=1e-11
    )
    if not solution.success:
        raise RuntimeError("Bộ giải phương trình vi phân không hội tụ.")
    numerical = solution.y[0]
    analytical = circuit.source_v + (circuit.initial_v - circuit.source_v) * np.exp(-times / circuit.tau)
    return pd.DataFrame(
        {
            "time_s": times,
            "voltage_numerical_v": numerical,
            "voltage_analytical_v": analytical,
            "current_a": (circuit.source_v - numerical) / circuit.resistance_ohm,
            "energy_j": 0.5 * circuit.capacitance_f * numerical**2,
            "absolute_error_v": np.abs(numerical - analytical),
        }
    )
