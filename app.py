from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from circuitlab.plotting import plot_result
from circuitlab.simulation import Circuit, simulate

st.set_page_config(page_title="RC Circuit Lab", page_icon="⚡", layout="wide")
st.title("⚡ RC Circuit Lab — Mô phỏng mạch điện")
st.caption("So sánh nghiệm giải tích với nghiệm số của phương trình vi phân")
with st.sidebar:
    mode = st.radio("Chế độ", ["Nạp tụ", "Xả tụ"])
    resistance = st.number_input("Điện trở R (Ω)", 1.0, 1000000.0, 1000.0, 100.0)
    capacitance_uf = st.number_input("Điện dung C (µF)", 0.01, 10000.0, 100.0, 10.0)
    voltage = st.number_input("Điện áp nguồn / điện áp nạp ban đầu (V)", 0.0, 48.0, 5.0, 0.5)
    duration_tau = st.slider("Thời gian mô phỏng (số lần RC)", 1, 10, 5)
circuit = Circuit(
    resistance,
    capacitance_uf * 1e-6,
    voltage if mode == "Nạp tụ" else 0.0,
    0.0 if mode == "Nạp tụ" else voltage,
)
st.image(str(Path(__file__).resolve().parent / "assets/rc_circuit.svg"), width=700)
if mode == "Xả tụ":
    st.caption(
        "Khi xả: đặt Vs = 0 V và tụ đã có điện áp ban đầu. Chiều dòng dương vẫn quy ước từ nguồn qua R sang C."
    )
try:
    frame = simulate(circuit, duration_tau * circuit.tau)
    cols = st.columns(4)
    cols[0].metric("Hằng số thời gian RC", f"{circuit.tau:.6g} s")
    cols[1].metric("Tần số cắt lý tưởng", f"{circuit.cutoff_hz:.4g} Hz")
    cols[2].metric("Điện áp cuối mô phỏng", f"{frame.voltage_numerical_v.iloc[-1]:.4f} V")
    cols[3].metric("Sai số số học lớn nhất", f"{frame.absolute_error_v.max():.2e} V")
    fig = plot_result(frame, circuit.tau)
    st.pyplot(fig)
    image = BytesIO()
    fig.savefig(image, format="png", dpi=160)
    plt.close(fig)
    left, right = st.columns(2)
    left.download_button("Tải bảng CSV", frame.to_csv(index=False), "rc_simulation.csv", "text/csv")
    right.download_button("Tải đồ thị PNG", image.getvalue(), "rc_plot.png", "image/png")
    with st.expander("Công thức và cách đọc đồ thị"):
        st.latex(r"\tau=RC,\quad V_C(t)=V_s+(V_0-V_s)e^{-t/RC}")
        st.latex(r"I(t)=\frac{V_s-V_C(t)}{R},\quad E_C(t)=\frac12CV_C(t)^2")
        st.write("Nạp từ 0 V: sau 1RC, điện áp tụ đạt khoảng 63,2% điện áp nguồn; sau 5RC đạt khoảng 99,3%.")
        st.write(
            "Xả về 0 V: sau 1RC, điện áp còn khoảng 36,8% ban đầu. Dòng âm biểu thị dòng ngược chiều quy ước."
        )
        st.caption(
            "Mô hình lý tưởng, chưa xét điện trở nội của nguồn, điện dung ký sinh và dung sai linh kiện."
        )
    with st.expander("Bảng giá trị"):
        st.dataframe(frame, hide_index=True, width="stretch")
except (ValueError, RuntimeError) as exc:
    st.error(str(exc))
