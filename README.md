# Mô Phỏng Mã Hóa Kênh - BTL Truyền Số Liệu & Mạng (Nhóm 6 - L01)

Dự án này là ứng dụng giao diện đồ họa (GUI) được phát triển bằng ngôn ngữ Python và thư viện PyQt5, phục vụ cho môn học **Truyền số liệu và mạng** tại HCMUT. Ứng dụng mô phỏng trực quan quá trình mã hóa kênh ở phía phát, truyền qua kênh nhiễu và phát hiện/sửa lỗi ở phía thu.

---

## 🌟 Tính Năng Chính

Ứng dụng hỗ trợ mô phỏng 3 phương pháp mã hóa kênh phổ biến:
1. **Mã hóa Parity (Chẵn/Lẻ):**
   * Cho phép tùy chọn độ dài chuỗi tin ban đầu $M(x)$ từ 2 đến 20 bits.
   * Tự động sinh ngẫu nhiên chuỗi tin hoặc nhập thủ công.
   * Tính toán và thêm bit Parity tương ứng.
2. **Mã hóa BCC (Block Check Character - Parity 2 chiều):**
   * Định cấu hình số hàng và số cột của ma trận dữ liệu từ 2x2 đến 10x10.
   * Hỗ trợ các quy tắc kiểm tra: Hàng Chẵn - Cột Chẵn, Hàng Lẻ - Cột Lẻ, Hàng Chẵn - Cột Lẻ, Hàng Lẻ - Cột Chẵn.
   * Tự động phát hiện và sửa sai **1 bit lỗi** ở bất kỳ tọa độ nào.
3. **Mã hóa CRC (Cyclic Redundancy Check):**
   * Cho phép chọn độ dài chuỗi dữ liệu gốc $M(x)$ và nhập đa thức sinh $G(x)$ bất kỳ (phải bắt đầu bằng bit `1`).
   * Thực hiện phép chia Modulo-2 để tìm phần dư CRC.
   * Phát hiện lỗi truyền và cảnh báo trường hợp đặc biệt "lỗi lọt lưới" (khi vector nhiễu chia hết cho đa thức sinh).

---

## 🎨 Giao Diện Mô Phỏng Trực Quan
* **Đảo bit dễ dàng:** Người dùng có thể double-click trực tiếp vào từng ô trên lưới ma trận ở Kênh truyền (Module 2) để lật bit (từ `0` thành `1` hoặc ngược lại), mô phỏng tác động của nhiễu đường truyền.
* **Đánh dấu màu sắc thông minh:**
  * **Xanh dương:** Các bit dữ liệu gốc.
  * **Đỏ:** Các bit Parity / CRC được thêm vào.
  * **Vàng:** Tọa độ bit lỗi đã được phát hiện và tự động sửa thành công (áp dụng cho BCC).

---

## 🛠️ Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### Yêu cầu hệ thống
* Máy tính đã cài đặt **Python 3.x**.

### Các bước khởi chạy
1. Mở terminal tại thư mục dự án và cài đặt thư viện cần thiết:
   ```bash
   pip install PyQt5
   ```
2. Chạy ứng dụng trực tiếp bằng lệnh Python:
   ```bash
   python MophongMahoaKenh.py
   ```
