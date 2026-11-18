# Việt hóa rc_visualizer_app.py của VoltKit và thêm chế độ xả có sẵn; xem NGUON.md.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from voltkit.core.simulator import simulate_rc_dc
from voltkit.core.transient import rc_discharge

st.set_page_config(page_title="Mô phỏng mạch RC", page_icon="⚡", layout="centered")
st.title("⚡ Mô phỏng nạp và xả tụ điện")
st.write("Thay đổi thông số bên trái để xem điện áp trên tụ thay đổi theo thời gian.")
mode = st.sidebar.radio("Chế độ", ["Nạp tụ", "Xả tụ"])
v_source = st.sidebar.slider("Điện áp ban đầu hoặc điện áp nguồn (V)", 1, 20, 5)
r = st.sidebar.slider("Điện trở (Ω)", 100, 10000, 1000)
c = st.sidebar.slider("Điện dung (µF)", 0.1, 1000.0, 100.0)
c_farads = c * 1e-6
t = np.linspace(0, 5 * r * c_farads, 1000)
v = simulate_rc_dc(v_source, r, c_farads, t) if mode == "Nạp tụ" else rc_discharge(v_source, r, c_farads, t)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, v)
ax.set_title("Điện áp trên tụ khi nạp" if mode == "Nạp tụ" else "Điện áp trên tụ khi xả")
ax.set_xlabel("Thời gian (giây)")
ax.set_ylabel("Điện áp trên tụ (V)")
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close(fig)
st.write(f"Hằng số thời gian RC: **{r * c_farads:.4g} giây**.")
st.caption("Mạch lý tưởng; chưa xét sai số linh kiện hoặc đo trên phần cứng.")
data = pd.DataFrame({"Thời gian (giây)": t, "Điện áp trên tụ (V)": v})
st.download_button(
    "Tải bảng số liệu", data.to_csv(index=False).encode("utf-8-sig"), "so_lieu_mach_rc.csv", "text/csv"
)
