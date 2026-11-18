# Nguồn dự án

Trích phần mô phỏng RC từ [VoltKit của Shobhit Bhardwaj](https://github.com/ShobhitBhardwaj763/voltkit), bản `6241117bc39a1aef6e8b6375b63458c040f3fde8`. Giữ giấy phép MIT của tác giả.

Các tệp dùng lại: `voltkit/streamlit_ui/rc_visualizer_app.py`, `voltkit/core/simulator.py` và hàm `rc_discharge` trong `voltkit/core/transient.py`.

Đã Việt hóa giao diện, lấy thời gian vẽ theo RC để đường cong dễ quan sát, thêm lựa chọn xả bằng hàm có sẵn và nút tải số liệu. Chỉ giữ các tệp cần cho mạch RC; công thức tính không thay đổi.
