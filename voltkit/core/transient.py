# Giữ hàm xả tụ từ VoltKit; bỏ những phần không dùng. Xem NGUON.md.
import numpy as np


def rc_discharge(V0, R, C, t):
    """Tính điện áp còn lại trên tụ khi xả."""
    tau = R * C
    return V0 * np.exp(-t / tau)
