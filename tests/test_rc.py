from pathlib import Path
import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from voltkit.core.simulator import simulate_rc_dc
from voltkit.core.transient import rc_discharge


def test_charging_at_one_time_constant():
    assert simulate_rc_dc(5, 1000, 100e-6, 0.1) == pytest.approx(5 * (1 - np.exp(-1)))
    assert simulate_rc_dc(5, 1000, 100e-6, 0) == 0


def test_discharge_at_one_time_constant():
    assert rc_discharge(5, 1000, 100e-6, 0.1) == pytest.approx(5 * np.exp(-1))
    assert rc_discharge(5, 1000, 100e-6, 0) == 5


def test_both_modes_render_in_vietnamese():
    at = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=15).run()
    assert not at.exception
    at.radio[0].set_value("Xả tụ").run()
    assert not at.exception
    assert "xả" in at.title[0].value
