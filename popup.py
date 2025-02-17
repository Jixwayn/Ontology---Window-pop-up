import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextBrowser
from search_info import OntologySearch

class SearchPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ค้นหาข้อมูลที่เกี่ยวข้อง")
        self.setGeometry(100, 100, 600, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("พิมพ์คำค้นหา เช่น เชียงใหม่, ดอยสุเทพ, สินค้า OTOP...")
        layout.addWidget(self.search_input)

        self.search_button = QPushButton("🔍 ค้นหา", self)
        self.search_button.clicked.connect(self.search)
        self.search_button.setFixedHeight(40)  # เพิ่มขนาดของปุ่ม
        layout.addWidget(self.search_button)

        self.clear_button = QPushButton("🧹 เคลียร์ข้อมูล", self)
        self.clear_button.clicked.connect(self.clear_results)
        self.clear_button.setFixedHeight(40)
        layout.addWidget(self.clear_button)

        self.result_box = QTextBrowser(self)
        layout.addWidget(self.result_box)

        self.setLayout(layout)
        self.ontology = OntologySearch("mytourism.owl")  # โหลด OWL

    def search(self):
        query_text = self.search_input.text()
        try:
            results = self.ontology.search_info(query_text)  # ค้นหาข้อมูล
            if results:
                display_text = ""
                for subject, properties in results.items():
                    display_text += f"\n🌍 **{subject}**\n" + "\n".join(properties) + "\n"
                    
                    # ดึงข้อมูลทั้งหมดของจังหวัดนี้ (ข้อมูลที่ไม่เกี่ยวข้องกับคำค้นหา)
                    full_info = self.ontology.get_full_info(subject)
                    if full_info:
                        display_text += "\nข้อมูลทั้งหมดของจังหวัด:\n"
                        display_text += "\n".join(full_info) + "\n"
                
                self.result_box.setText(display_text)
            else:
                self.result_box.setText("❌ ไม่พบข้อมูลที่เกี่ยวข้อง")
        except Exception as e:
            self.result_box.setText(f"เกิดข้อผิดพลาด: {str(e)}")

    def clear_results(self):
        """ ฟังก์ชันสำหรับล้างช่องค้นหาและผลลัพธ์ """
        self.search_input.clear()
        self.result_box.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchPopup()
    window.show()
    sys.exit(app.exec())
