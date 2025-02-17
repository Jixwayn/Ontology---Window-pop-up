import rdflib
import tkinter as tk
from tkinter import messagebox

class OntologySearch:
    def __init__(self, ontology_file):
        # โหลดไฟล์ RDF/OWL
        self.g = rdflib.Graph()
        self.g.parse(ontology_file, format="xml")  # เปลี่ยนเป็นเส้นทางไฟล์ของคุณ

    def search_info(self, keyword):
        # สร้าง SPARQL query เพื่อค้นหาจังหวัดที่เกี่ยวข้องกับคำค้น
        query = f"""
            PREFIX : <http://www.my_ontology.edu/mytourism#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?subject ?property ?value WHERE {{
                ?subject ?property ?value .
                FILTER (
                    regex(str(?subject), "{keyword}", "i") || 
                    regex(str(?value), "{keyword}", "i") || 
                    regex(str(?property), "{keyword}", "i")
                )
                FILTER (?property IN (:hasFlower, :hasImageOfProvince, :hasLatitudeOfProvince, :hasLongitudeOfProvince, :hasMotto, :hasNameOfProvince, :hasSeal, :hasTraditionalNameOfProvince, :hasTree, :hasURLOfProvince))
            }}
        """
        
        results = self.g.query(query)
        data = {}

        # ประมวลผลผลลัพธ์และจัดเก็บใน dictionary
        for row in results:
            subject = str(row.subject).split("#")[-1]  # เอาชื่อจังหวัดออกจาก URI
            property_name = str(row.property).split("#")[-1]
            value = str(row.value)

            if subject not in data:
                data[subject] = []
            data[subject].append(f"🔹 {property_name}: {value}")

        return data

    def get_full_info(self, subject):
        # สร้าง SPARQL query เพื่อดึงข้อมูลทั้งหมดของจังหวัดที่พบ
        query = f"""
            PREFIX : <http://www.my_ontology.edu/mytourism#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?property ?value WHERE {{
                :{subject} ?property ?value .
                FILTER (?property IN (:hasFlower, :hasImageOfProvince, :hasLatitudeOfProvince, :hasLongitudeOfProvince, :hasMotto, :hasNameOfProvince, :hasSeal, :hasTraditionalNameOfProvince, :hasTree, :hasURLOfProvince))
            }}
        """

        results = self.g.query(query)
        full_data = []
        
        # ประมวลผลข้อมูลทั้งหมดของจังหวัดที่ค้นพบ
        for row in results:
            property_name = str(row.property).split("#")[-1]
            value = str(row.value)
            full_data.append(f"🔹 {property_name}: {value}")

        return full_data

    def show_results(self, data):
        # สร้าง GUI ของ Pop-up เพื่อแสดงผลลัพธ์
        result_text = ""
        for subject, properties in data.items():
            result_text += f"📍 {subject}:\n"
            for property in properties:
                result_text += f"  {property}\n"
            
            # ค้นหาข้อมูลทั้งหมดของจังหวัดนี้
            full_info = self.get_full_info(subject)
            if full_info:
                result_text += "\nข้อมูลทั้งหมดของจังหวัด:\n"
                result_text += "\n".join(full_info) + "\n"
            result_text += "\n"

        # แสดงในหน้าต่าง Pop-up
        if result_text:
            messagebox.showinfo("ผลการค้นหา", result_text)
        else:
            messagebox.showinfo("ผลการค้นหา", "ไม่พบข้อมูลที่เกี่ยวข้อง")

    def search_and_display(self, keyword):
        # ค้นหาข้อมูลและแสดงผล
        data = self.search_info(keyword)
        self.show_results(data)

# สร้างหน้าต่าง GUI
def main():
    ontology_file = "mytourism.owl"  # เปลี่ยนเส้นทางไปยังไฟล์ OWL ของคุณ
    app = OntologySearch(ontology_file)

    # สร้าง GUI สำหรับการค้นหา
    root = tk.Tk()
    root.title("ค้นหาข้อมูลการท่องเที่ยว")

    tk.Label(root, text="ค้นหาคำที่เกี่ยวข้อง:").pack(pady=10)
    search_entry = tk.Entry(root)
    search_entry.pack(pady=10)

    def on_search():
        keyword = search_entry.get()
        if keyword:
            app.search_and_display(keyword)
        else:
            messagebox.showwarning("เตือน", "กรุณากรอกคำค้นหา")

    search_button = tk.Button(root, text="ค้นหา", command=on_search)
    search_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
