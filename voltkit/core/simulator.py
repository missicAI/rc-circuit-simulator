# Trích từ VoltKit; đã đổi lời mô tả sang tiếng Việt. Xem NGUON.md.
import numpy as np


def simulate_rc_dc(v_source, r, c, t):
    """Tính điện áp trên tụ khi nạp từ 0 V."""
    tau = r * c
    return v_source * (1 - np.exp(-t / tau))
