# Mô phỏng mạch RC

Thay đổi điện trở, điện dung hoặc điện áp để xem tụ điện nạp và xả như thế nào. Đường cong cho thấy điện áp trên tụ theo thời gian. Bạn có thể tải bảng số liệu để xem lại.

Code được trích từ phần mô phỏng RC của VoltKit, sau đó Việt hóa và chỉ giữ những phần cần dùng. Công thức của dự án gốc được giữ nguyên.

## Chạy trên máy

Cài Python 3.12. Trên Windows, chạy `CAI_DAT.bat` một lần, rồi mở `CHAY_DEMO.bat`.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Sau khi cài các thư viện, chương trình có thể chạy không cần mạng.

## Quan sát điều gì?

Khi nạp từ 0 V, điện áp trên tụ tăng dần đến gần điện áp nguồn. Khi xả, điện áp giảm dần về gần 0 V.

Tích R × C là hằng số thời gian. Tăng điện trở hoặc điện dung làm quá trình chậm hơn. Biểu đồ luôn vẽ đến năm lần hằng số này, vì vậy bạn cần nhìn cả trục thời gian khi so sánh hai lần chạy.

Đây là mạch lý tưởng. Chưa xét sai số linh kiện hoặc số đo trên phần cứng.

## Đọc code

`app.py` tạo các nút chọn và vẽ đồ thị. `voltkit/core/simulator.py` tính điện áp khi nạp; `voltkit/core/transient.py` tính điện áp khi xả.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Xem [NGUON.md](NGUON.md) để biết tệp gốc và phần đã chỉnh. Giữ giấy phép MIT của Shobhit Bhardwaj.
