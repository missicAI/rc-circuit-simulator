import numpy as np
import pytest

from circuitlab.simulation import Circuit, simulate


def test_charging_at_one_time_constant_and_monotonicity():
    circuit = Circuit(1000, 100e-6, 5)
    frame = simulate(circuit, circuit.tau, 101)
    assert frame.voltage_numerical_v.iloc[0] == 0
    assert frame.voltage_numerical_v.iloc[-1] == pytest.approx(5 * (1 - np.exp(-1)), abs=1e-7)
    assert np.all(np.diff(frame.voltage_numerical_v) >= 0)
    assert frame.absolute_error_v.max() < 1e-7


def test_discharge_current_direction_and_energy():
    circuit = Circuit(1000, 100e-6, 0, 5)
    frame = simulate(circuit, circuit.tau, 101)
    assert frame.voltage_numerical_v.iloc[-1] == pytest.approx(5 * np.exp(-1), abs=1e-7)
    assert np.all(frame.current_a < 0)
    assert np.all(np.diff(frame.energy_j) <= 0)


def test_equilibrium_has_zero_current():
    frame = simulate(Circuit(1000, 100e-6, 5, 5))
    np.testing.assert_allclose(frame.voltage_numerical_v, 5)
    np.testing.assert_allclose(frame.current_a, 0)


@pytest.mark.parametrize("r,c,v", [(0, 1e-4, 5), (-1, 1e-4, 5), (1000, 0, 5), (1000, 1e-4, float("nan"))])
def test_invalid_components(r, c, v):
    with pytest.raises(ValueError):
        simulate(Circuit(r, c, v))


def test_units_and_frequency():
    circuit = Circuit(1000, 100 * 1e-6, 5)
    assert circuit.tau == pytest.approx(0.1)
    assert circuit.cutoff_hz == pytest.approx(1.59154943)
