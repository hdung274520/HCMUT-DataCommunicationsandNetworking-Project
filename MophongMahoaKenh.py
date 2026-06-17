python -m PyInstaller --noconsole --onefile MophongMahoaKenh.pyimport sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, 
                             QTextEdit, QStackedWidget, QSpinBox, QFrame, 
                             QTableWidget, QTableWidgetItem, QAbstractItemView, QDesktopWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class ChannelCodingSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.clean_tx_data = "" 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mô phỏng Mã hóa Kênh')
        
        # Font mặc định cho giao diện chung
        self.setFont(QFont("Arial", 11))
        
        # Thiết lập kích thước động: 75% màn hình, Tỉ lệ 16:10
        screen = QDesktopWidget().availableGeometry()
        w = int(screen.width() * 0.75)
        h = int(w * 10 / 16)
        if h > screen.height() * 0.9: 
            h = int(screen.height() * 0.85)
            w = int(h * 16 / 10)
        self.resize(w, h)
        
        main_layout = QHBoxLayout()

        # ==========================================
        # MODULE 1: PHÍA PHÁT (TRANSMITTER)
        # ==========================================
        mod1_frame = QFrame()
        mod1_frame.setFrameShape(QFrame.StyledPanel)
        mod1_layout = QVBoxLayout(mod1_frame)
        mod1_layout.addWidget(self.create_header("MODULE 1: PHÍA PHÁT", "#4CAF50"))

        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("Thuật toán:"))
        self.algo_combo = QComboBox()
        self.algo_combo.addItems([
            "Parity (Chẵn)", 
            "Parity (Lẻ)", 
            "BCC (Hàng Chẵn - Cột Chẵn)",
            "BCC (Hàng Lẻ - Cột Lẻ)",
            "BCC (Hàng Chẵn - Cột Lẻ)",
            "BCC (Hàng Lẻ - Cột Chẵn)",
            "CRC"
        ])
        
        algo_layout.addWidget(self.algo_combo)
        mod1_layout.addLayout(algo_layout)

        self.input_stack = QStackedWidget()

        # --- Page 0: Dành cho Parity ---
        self.page_parity = QWidget()
        page_p_layout = QVBoxLayout(self.page_parity)
        
        p_len_layout = QHBoxLayout()
        p_len_layout.addWidget(QLabel("Độ dài M(x):"))
        self.spin_p_len = QSpinBox()
        self.spin_p_len.setRange(2, 20)
        self.spin_p_len.setValue(7)
        p_len_layout.addWidget(self.spin_p_len)
        btn_rnd_p = QPushButton("Random M(x)")
        btn_rnd_p.clicked.connect(self.generate_parity_matrix)
        p_len_layout.addWidget(btn_rnd_p)
        page_p_layout.addLayout(p_len_layout)

        page_p_layout.addWidget(QLabel("Dữ liệu gốc M(x) [Click đúp để đảo bit]:"))
        self.table_p_input = self.create_grid()
        self.table_p_input.setMaximumHeight(80) 
        page_p_layout.addWidget(self.table_p_input)
        page_p_layout.addStretch()
        self.input_stack.addWidget(self.page_parity)

        # --- Page 1: Dành cho BCC ---
        self.page_bcc = QWidget()
        page_bcc_layout = QVBoxLayout(self.page_bcc)
        
        bcc_dim_layout = QHBoxLayout()
        bcc_dim_layout.addWidget(QLabel("Số hàng:"))
        self.spin_rows = QSpinBox()
        self.spin_rows.setRange(2, 10)
        self.spin_rows.setValue(4)
        bcc_dim_layout.addWidget(self.spin_rows)
        
        bcc_dim_layout.addWidget(QLabel("Số cột:"))
        self.spin_cols = QSpinBox()
        self.spin_cols.setRange(2, 10)
        self.spin_cols.setValue(5)
        bcc_dim_layout.addWidget(self.spin_cols)
        
        btn_gen_matrix = QPushButton("Tạo Random")
        btn_gen_matrix.clicked.connect(self.generate_bcc_matrix)
        bcc_dim_layout.addWidget(btn_gen_matrix)
        page_bcc_layout.addLayout(bcc_dim_layout)

        page_bcc_layout.addWidget(QLabel("Ma trận dữ liệu [Click đúp để đảo bit]:"))
        self.table_bcc_input = self.create_grid()
        page_bcc_layout.addWidget(self.table_bcc_input)
        self.input_stack.addWidget(self.page_bcc)

        # --- Page 2: Dành cho CRC ---
        self.page_crc = QWidget()
        page_crc_layout = QVBoxLayout(self.page_crc)
        
        crc_len_layout = QHBoxLayout()
        crc_len_layout.addWidget(QLabel("Độ dài M(x):"))
        self.spin_crc_len = QSpinBox()
        self.spin_crc_len.setRange(2, 20)
        self.spin_crc_len.setValue(7)
        crc_len_layout.addWidget(self.spin_crc_len)
        btn_rnd_crc = QPushButton("Random M(x)")
        btn_rnd_crc.clicked.connect(self.generate_crc_matrix)
        crc_len_layout.addWidget(btn_rnd_crc)
        page_crc_layout.addLayout(crc_len_layout)

        page_crc_layout.addWidget(QLabel("Dữ liệu gốc M(x) [Click đúp để đảo bit]:"))
        self.table_crc_input = self.create_grid()
        self.table_crc_input.setMaximumHeight(80)
        page_crc_layout.addWidget(self.table_crc_input)

        box_g = QHBoxLayout()
        box_g.addWidget(QLabel("Đa thức G(x):"))
        self.input_crc_poly = QLineEdit() 
        self.input_crc_poly.setFont(QFont("Courier", 14, QFont.Bold))
        self.input_crc_poly.setPlaceholderText("VD: 1011")
        box_g.addWidget(self.input_crc_poly)
        
        btn_rnd_g = QPushButton("Random 3-bit G(x)")
        btn_rnd_g.clicked.connect(lambda: self.input_crc_poly.setText(f"1{random.randint(0,1)}{random.randint(0,1)}"))
        box_g.addWidget(btn_rnd_g)
        
        page_crc_layout.addLayout(box_g)
        page_crc_layout.addStretch()
        self.input_stack.addWidget(self.page_crc)

        mod1_layout.addWidget(self.input_stack)

        self.btn_encode = QPushButton(">> MÃ HÓA >>")
        self.btn_encode.setMinimumHeight(45)
        self.btn_encode.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_encode.clicked.connect(self.encode_data)
        mod1_layout.addWidget(self.btn_encode)

        main_layout.addWidget(mod1_frame, 1)

        # ==========================================
        # MODULE 2: KÊNH TRUYỀN (CHANNEL)
        # ==========================================
        mod2_frame = QFrame()
        mod2_frame.setFrameShape(QFrame.StyledPanel)
        mod2_layout = QVBoxLayout(mod2_frame)
        mod2_layout.addWidget(self.create_header("MODULE 2: KÊNH TRUYỀN", "#2196F3"))
        
        lbl_tx = QLabel("Dữ liệu truyền đi [Click đúp để lật bit tạo nhiễu]:<br><span style='color: red; font-size: 12px;'>(* Chữ đỏ là các bit Parity/CRC được tự động thêm vào)</span>")
        lbl_tx.setTextFormat(Qt.RichText)
        mod2_layout.addWidget(lbl_tx)
        
        # Dùng chung 1 bảng duy nhất cho tất cả thuật toán
        self.transmitted_table = self.create_grid()
        self.transmitted_table.setStyleSheet("background-color: #e3f2fd;")
        mod2_layout.addWidget(self.transmitted_table)
        
        main_layout.addWidget(mod2_frame, 1)

        # ==========================================
        # MODULE 3: PHÍA THU (RECEIVER)
        # ==========================================
        mod3_frame = QFrame()
        mod3_frame.setFrameShape(QFrame.StyledPanel)
        mod3_layout = QVBoxLayout(mod3_frame)
        mod3_layout.addWidget(self.create_header("MODULE 3: PHÍA THU", "#f44336"))

        self.btn_decode = QPushButton("KIỂM TRA LỖI")
        self.btn_decode.setMinimumHeight(45)
        self.btn_decode.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_decode.clicked.connect(self.decode_data)
        mod3_layout.addWidget(self.btn_decode)

        self.result_label = QLabel("Trạng thái: Đang chờ...")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 5px; margin-bottom: 5px;")
        mod3_layout.addWidget(self.result_label)

        mod3_layout.addWidget(QLabel("Phân tích lỗi:"))
        self.error_vector_display = QTextEdit()
        self.error_vector_display.setReadOnly(True)
        self.error_vector_display.setFont(QFont("Arial", 12))
        self.error_vector_display.setStyleSheet("background-color: #ffebee; color: #b71c1c;")
        mod3_layout.addWidget(self.error_vector_display, 1)

        # Cụm UI hiển thị kết quả (Chỉ dành cho BCC)
        self.lbl_decoded_matrix = QLabel("Ma trận nhận được (Đã qua xử lý & tự sửa):")
        mod3_layout.addWidget(self.lbl_decoded_matrix)
        
        self.decoded_table = self.create_grid()
        self.decoded_table.setStyleSheet("background-color: #f1f8e9;") 
        mod3_layout.addWidget(self.decoded_table, 2) 

        main_layout.addWidget(mod3_frame, 1)

        self.setLayout(main_layout)
        
        # Gán sự kiện cho các tín hiệu (Signals)
        self.algo_combo.currentIndexChanged.connect(self.change_input_module)
        self.spin_p_len.valueChanged.connect(self.generate_parity_matrix)
        self.spin_rows.valueChanged.connect(self.generate_bcc_matrix)
        self.spin_cols.valueChanged.connect(self.generate_bcc_matrix)
        self.spin_crc_len.valueChanged.connect(self.generate_crc_matrix)

        # Khởi tạo mặc định
        self.generate_parity_matrix()
        self.generate_bcc_matrix()
        self.generate_crc_matrix()
        self.change_input_module() # Chạy để ẩn/hiện đúng layout ban đầu

    # --- HÀM TẠO UI LƯỚI ---
    def create_header(self, text, color):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(f"background-color: {color}; color: white; padding: 10px; font-weight: bold; font-size: 14px;")
        return lbl

    def create_grid(self):
        table = QTableWidget()
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setDefaultSectionSize(45)
        table.verticalHeader().setDefaultSectionSize(45)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.cellDoubleClicked.connect(lambda r, c: self.toggle_bit(r, c, table))
        return table

    def toggle_bit(self, row, col, table):
        item = table.item(row, col)
        if item:
            val = item.text().strip()
            new_val = '1' if val == '0' else '0'
            item.setText(new_val)

    def change_input_module(self):
        algo = self.algo_combo.currentText()
        if "Parity" in algo:
            self.input_stack.setCurrentIndex(0)
            self.lbl_decoded_matrix.hide()
            self.decoded_table.hide()
        elif "BCC" in algo:
            self.input_stack.setCurrentIndex(1)
            self.lbl_decoded_matrix.show()
            self.decoded_table.show()
        elif "CRC" in algo:
            self.input_stack.setCurrentIndex(2)
            self.lbl_decoded_matrix.hide()
            self.decoded_table.hide()

    # --- CÁC HÀM SINH RANDOM GRID ---
    def populate_grid_random(self, table, rows, cols):
        table.setRowCount(rows)
        table.setColumnCount(cols)
        for r in range(rows):
            for c in range(cols):
                item = QTableWidgetItem(str(random.randint(0, 1)))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Courier", 16, QFont.Bold)) 
                table.setItem(r, c, item)

    def generate_parity_matrix(self):
        self.populate_grid_random(self.table_p_input, 1, self.spin_p_len.value())

    def generate_bcc_matrix(self):
        self.populate_grid_random(self.table_bcc_input, self.spin_rows.value(), self.spin_cols.value())

    def generate_crc_matrix(self):
        self.populate_grid_random(self.table_crc_input, 1, self.spin_crc_len.value())

    # --- CÁC HÀM TOÁN HỌC ---
    def calc_parity_bit(self, binary_str, rule):
        ones = binary_str.count('1')
        if rule == "Even": return '0' if ones % 2 == 0 else '1'
        else: return '1' if ones % 2 == 0 else '0'

    def xor(self, a, b):
        result = []
        for i in range(1, len(b)):
            if a[i] == b[i]: result.append('0')
            else: result.append('1')
        return ''.join(result)

    def mod2div(self, dividend, divisor):
        pick = len(divisor)
        tmp = dividend[0:pick]
        while pick < len(dividend):
            if tmp[0] == '1': tmp = self.xor(divisor, tmp) + dividend[pick]
            else: tmp = self.xor('0'*pick, tmp) + dividend[pick]
            pick += 1
        if tmp[0] == '1': tmp = self.xor(divisor, tmp)
        else: tmp = self.xor('0'*pick, tmp)
        return tmp

    # --- LOGIC MÃ HÓA ---
    def extract_data_from_grid(self, table):
        rows = table.rowCount()
        cols = table.columnCount()
        lines = []
        for r in range(rows):
            row_str = ""
            for c in range(cols):
                item = table.item(r, c)
                row_str += item.text().strip() if item else "0"
            lines.append(row_str)
        return lines

    def render_to_tx_grid(self, lines, data_len_or_cols, is_bcc=False):
        rows = len(lines)
        cols = len(lines[0])
        self.transmitted_table.setRowCount(rows)
        self.transmitted_table.setColumnCount(cols)
        
        for r in range(rows):
            for c in range(cols):
                char = lines[r][c]
                item = QTableWidgetItem(char)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Courier", 16, QFont.Bold))
                
                if is_bcc:
                    if r == rows - 1 or c == cols - 1:
                        item.setForeground(QColor("#d32f2f"))
                    else:
                        item.setForeground(QColor("#0d47a1"))
                else:
                    if c >= data_len_or_cols: 
                        item.setForeground(QColor("#d32f2f"))
                    else:
                        item.setForeground(QColor("#0d47a1"))
                        
                self.transmitted_table.setItem(r, c, item)

    def encode_data(self):
        algo = self.algo_combo.currentText()
        encoded = ""

        if "Parity" in algo:
            lines = self.extract_data_from_grid(self.table_p_input)
            data = lines[0]
            rule = "Even" if "Chẵn" in algo else "Odd"
            encoded = data + self.calc_parity_bit(data, rule)
            self.clean_tx_data = encoded
            self.render_to_tx_grid([encoded], len(data), is_bcc=False)

        elif "CRC" in algo:
            lines = self.extract_data_from_grid(self.table_crc_input)
            data = lines[0]
            poly = self.input_crc_poly.text().strip()
            
            if not poly or not all(c in '01' for c in poly):
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Đa thức sinh G(x) hợp lệ (chỉ chứa 0 và 1).")
                return
            if poly[0] != '1':
                QMessageBox.warning(self, "Lỗi", "Đa thức sinh G(x) luôn phải bắt đầu bằng bit 1.")
                return
                
            appended_data = data + '0' * (len(poly) - 1)
            remainder = self.mod2div(appended_data, poly)
            encoded = data + remainder
            self.clean_tx_data = encoded
            self.render_to_tx_grid([encoded], len(data), is_bcc=False)

        elif "BCC" in algo:
            lines = self.extract_data_from_grid(self.table_bcc_input)
            rows = len(lines)
            cols = len(lines[0])
            row_rule = "Even" if "Hàng Chẵn" in algo else "Odd"
            col_rule = "Even" if "Cột Chẵn" in algo else "Odd"

            encoded_lines = []
            for line in lines:
                p_bit = self.calc_parity_bit(line, row_rule)
                encoded_lines.append(line + p_bit)
            
            bottom_row = ""
            for c in range(cols + 1):
                col_data = "".join([encoded_lines[r][c] for r in range(rows)])
                bottom_row += self.calc_parity_bit(col_data, col_rule)
            
            encoded_lines.append(bottom_row)
            self.clean_tx_data = "\n".join(encoded_lines)
            self.render_to_tx_grid(encoded_lines, cols, is_bcc=True)

        self.result_label.setText("Trạng thái: Đã chuyển vào Kênh truyền.")
        self.result_label.setStyleSheet("color: black; font-weight: bold; font-size: 16px;")
        self.error_vector_display.clear()
        self.decoded_table.clearContents()

    # --- LOGIC KIỂM TRA LỖI VÀ SỬA LỖI (GIẢI MÃ) ---
    def decode_data(self):
        if self.transmitted_table.rowCount() == 0: return
        algo = self.algo_combo.currentText()
        
        lines_rx = self.extract_data_from_grid(self.transmitted_table)
        received = "\n".join(lines_rx)

        tx_lines = self.clean_tx_data.split('\n')
        rx_lines = received.split('\n')
        
        # 1. --- KIỂM TRA PARITY ---
        if "Parity" in algo:
            received_flat = lines_rx[0]
            rule = "Even" if "Chẵn" in algo else "Odd"
            calc_p = self.calc_parity_bit(received_flat[:-1], rule)
            error_detected = (calc_p != received_flat[-1])
            
            if error_detected: 
                self.result_label.setText("KẾT QUẢ: CÓ LỖI (Không thể tự sửa)")
                self.result_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
                self.error_vector_display.setPlainText("=> Parity xác định có lỗi nhưng không thể định vị bit sai.\n=> Bạn cần yêu cầu trạm phát truyền lại toàn bộ khung tin (ARQ).")
            else:
                self.result_label.setText("KẾT QUẢ: KHÔNG LỖI")
                self.result_label.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")
                self.error_vector_display.setPlainText("=> Không phát hiện sai sót. Dữ liệu toàn vẹn.")

        # 2. --- KIỂM TRA CRC ---
        elif "CRC" in algo:
            received_flat = lines_rx[0]
            poly = self.input_crc_poly.text().strip()
            remainder = self.mod2div(received_flat, poly)
            error_detected = '1' in remainder
            
            wrong_bits = []
            for idx in range(len(received_flat)):
                if received_flat[idx] != self.clean_tx_data[idx]: wrong_bits.append(idx)
            
            if error_detected and wrong_bits:
                self.result_label.setText("KẾT QUẢ: CÓ LỖI (Không thể tự sửa)")
                self.result_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
                self.error_vector_display.setPlainText(f"=> Toán học CRC phát hiện số dư Modulo-2 khác 0.\n=> Bằng cách đối chiếu mô phỏng, lỗi nằm tại các bit (đếm từ 1): {', '.join([str(x+1) for x in wrong_bits])}\n=> CRC chỉ phát hiện, không tự sửa.")
            elif not error_detected and wrong_bits:
                self.result_label.setText("KẾT QUẢ: LỖI LỌT LƯỚI!")
                self.result_label.setStyleSheet("color: #FF5722; font-size: 18px; font-weight: bold;")
                self.error_vector_display.setPlainText(f"!!! CẢNH BÁO !!!\n=> Vector lỗi chia hết cho G(x).\n=> Bị đánh lừa là KHÔNG LỖI dù thực tế sai ở bit: {', '.join([str(x+1) for x in wrong_bits])}")
            else:
                self.result_label.setText("KẾT QUẢ: KHÔNG LỖI")
                self.result_label.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")
                self.error_vector_display.setPlainText("=> Không phát hiện bit sai. Số dư Modulo-2 bằng 0.")

        # 3. --- KIỂM TRA & TỰ SỬA LỖI BCC ---
        elif "BCC" in algo:
            row_rule = "Even" if "Hàng Chẵn" in algo else "Odd"
            col_rule = "Even" if "Cột Chẵn" in algo else "Odd"
            
            grid = [list(line) for line in rx_lines]
            R = len(grid) - 1 
            C = len(grid[0]) - 1 
            
            failing_rows, failing_cols = [], []

            for r in range(R):
                if self.calc_parity_bit("".join(grid[r][:C]), row_rule) != grid[r][C]: failing_rows.append(r)
            for c in range(C + 1):
                col_data = "".join([grid[r][c] for r in range(R)])
                if self.calc_parity_bit(col_data, col_rule) != grid[R][c]: failing_cols.append(c)

            has_error = len(failing_rows) > 0 or len(failing_cols) > 0
            is_corrected = False
            err_pos = []

            if not has_error:
                self.result_label.setText("KẾT QUẢ: KHÔNG LỖI")
                self.result_label.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")
                self.error_vector_display.setPlainText("=> Toán học BCC xác nhận: KHÔNG PHÁT HIỆN LỖI.")
            
            else:
                if len(failing_rows) == 1 and len(failing_cols) == 1:
                    err_row, err_col = failing_rows[0], failing_cols[0]
                    grid[err_row][err_col] = '1' if grid[err_row][err_col] == '0' else '0' 
                    is_corrected = True
                    err_pos = [(err_row, err_col)]
                    self.result_label.setText("KẾT QUẢ: ĐÃ SỬA LỖI (1 bit)")
                    self.result_label.setStyleSheet("color: #FF9800; font-size: 18px; font-weight: bold;")
                    self.error_vector_display.setPlainText(f"=> TỌA ĐỘ TỰ SỬA: Hàng {err_row+1}, Cột {err_col+1}\n=> Ô khôi phục đã được làm sáng ở lưới ma trận bên dưới.")

                elif len(failing_rows) == 0 and len(failing_cols) == 1:
                    err_row, err_col = R, failing_cols[0]
                    grid[err_row][err_col] = '1' if grid[err_row][err_col] == '0' else '0'
                    is_corrected = True
                    err_pos = [(err_row, err_col)]
                    self.result_label.setText("KẾT QUẢ: ĐÃ SỬA LỖI (Parity)")
                    self.result_label.setStyleSheet("color: #FF9800; font-size: 18px; font-weight: bold;")
                    self.error_vector_display.setPlainText(f"=> TỌA ĐỘ TỰ SỬA: Hàng {err_row+1}, Cột {err_col+1}\n=> Ô khôi phục đã được làm sáng ở lưới ma trận bên dưới.")

                else:
                    self.result_label.setText("KẾT QUẢ: LỖI QUÁ NẶNG (Không thể sửa)")
                    self.result_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
                    self.error_vector_display.setPlainText("=> KHÔNG THỂ SỬA LỖI!\n=> BCC phát hiện ≥ 2 bit sai, vượt quá khả năng tự sửa.")
            
            # Khôi phục thành array chuỗi để truyền vào hàm vẽ riêng của BCC
            final_rx_lines = ["".join(row) for row in grid]
            self.render_to_rx_grid_bcc(final_rx_lines, err_pos, has_error, is_corrected)

    def render_to_rx_grid_bcc(self, lines, error_positions, has_error, is_corrected):
        rows = len(lines)
        cols = len(lines[0])
        self.decoded_table.setRowCount(rows)
        self.decoded_table.setColumnCount(cols)
        
        for r in range(rows):
            for c in range(cols):
                char = lines[r][c]
                item = QTableWidgetItem(char)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Courier", 16, QFont.Bold))
                
                if has_error and is_corrected and (r, c) in error_positions:
                    item.setBackground(QColor("#fff59d")) 
                    item.setForeground(QColor("#e65100")) 
                elif has_error and not is_corrected and (r, c) in error_positions:
                    item.setBackground(QColor("#ffcdd2")) 
                    item.setForeground(QColor("black"))
                else:
                    if r == rows - 1 or c == cols - 1: item.setForeground(QColor("#d32f2f"))
                    else: item.setForeground(QColor("#0d47a1"))
                        
                self.decoded_table.setItem(r, c, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChannelCodingSimulator()
    ex.show()
    sys.exit(app.exec_())