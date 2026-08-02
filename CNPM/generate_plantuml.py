# -*- coding: utf-8 -*-
import os
import re

# Source files
CNPM_TXT = r"c:\Users\TiNyX3k\Desktop\CNPM\CNPM.txt"
OUTPUT_DIR = r"c:\Users\TiNyX3k\Desktop\CNPM\UML"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Read CNPM.txt
with open(CNPM_TXT, "r", encoding="utf-8") as f:
    raw_content = f.read()

# Split into 66 questions
matches = re.finditer(r"(Đề số \d+)(.*?)(?=(?:Đề số \d+|$))", raw_content, re.DOTALL)
exams_raw = []
for m in matches:
    title = m.group(1).strip()
    body = m.group(2).strip()
    num_match = re.search(r"\d+", title)
    num = int(num_match.group(0)) if num_match else 0
    exams_raw.append({
        "num": num,
        "title": title,
        "body": body
    })

# Map each index to a domain
def get_domain(num):
    if 1 <= num <= 4:
        return "thuvien"
    elif 5 <= num <= 10:
        return "tinchi"
    elif 11 <= num <= 14:
        return "tour"
    elif 15 <= num <= 21:
        return "nhahang"
    elif 22 <= num <= 25:
        return "kho"
    elif 26 <= num <= 29:
        return "co"
    elif 30 <= num <= 33:
        return "duaxe"
    elif 34 <= num <= 38:
        return "truyen"
    elif 39 <= num <= 44:
        return "calam"
    elif 45 <= num <= 49:
        return "rapphim"
    elif 50 <= num <= 55:
        return "sanbong"
    elif 56 <= num <= 61:
        return "tragop"
    elif 62 <= num <= 66:
        return "trangphuc"
    return "unknown"

# Define shared definitions for each domain (Entities, fields, etc.)
DOMAINS_DATA = {
    "thuvien": {
        "entities": [
            ("ThuThu", ["- id: int", "- hoTen: String", "- password: String", "- viTri: String"]),
            ("SinhVien", ["- id: int", "- maDocGia: String", "- hoTen: String", "- ngaySinh: Date", "- dienThoai: String", "- maVach: String"]),
            ("Sach", ["- id: int", "- maSach: int", "- tenSach: String", "- tacGia: String", "- namXB: int", "- gia: double", "- soLuong: int", "- moTa: String"]),
            ("PhieuMuon", ["- id: int", "- maPhieuMuon: String", "- ngayMuon: Date", "- idNguoiTao: int", "- idDocGia: int"]),
            ("ChiTietPhieuMuon", ["- id: int", "- idPhieuMuon: int", "- ngayPhaiTra: Date", "- ngayTra: Date", "- idSach: int", "- tienPhat: double", "- daTra: boolean"])
        ],
        "relationships": [
            "ThuThu \"1\" -- \"0..*\" PhieuMuon",
            "SinhVien \"1\" -- \"0..*\" PhieuMuon",
            "PhieuMuon \"1\" *-- \"0..*\" ChiTietPhieuMuon",
            "ChiTietPhieuMuon \"0..*\" -- \"1\" Sach"
        ],
        "actor": "Thủ thư",
        "home_frm": "TrangChuThuThuFrm",
        "daos": ["SinhVienDAO", "SachDAO", "PhieuMuonDAO", "ChiTietPhieuMuonDAO"]
    },
    "tinchi": {
        "entities": [
            ("GiaoVu", ["- id: int", "- hoTen: String", "- password: String", "- viTri: String"]),
            ("SinhVien", ["- id: int", "- maSinhVien: String", "- hoTen: String", "- ngaySinh: Date", "- lopKey: String", "- queQuan: String", "- diaChi: String"]),
            ("MonHoc", ["- id: int", "- maMon: String", "- tenMon: String", "- soTinChi: int"]),
            ("MonHocYeuCau", ["- id: int", "- monHocId: int", "- monYeuCauId: int"]),
            ("LopHocPhan", ["- id: int", "- maLop: String", "- tenLop: String", "- maxSV: int", "- phongHoc: String", "- khungGio: String", "- maGV: int", "- monHocId: int"]),
            ("DangKyHoc", ["- id: int", "- sinhVienId: int", "- lopHocPhanId: int", "- ngayDangKy: Date"]),
            ("KetQua", ["- id: int", "- sinhVienId: int", "- monHocId: int", "- lopHocPhanId: int", "- diemCC: double", "- diemBT: double", "- diemTH: double", "- diemThi: double", "- diemTongKet: double"])
        ],
        "relationships": [
            "GiaoVu \"1\" -- \"0..*\" LopHocPhan",
            "SinhVien \"1\" -- \"0..*\" DangKyHoc",
            "LopHocPhan \"1\" -- \"0..*\" DangKyHoc",
            "MonHoc \"1\" -- \"0..*\" LopHocPhan",
            "MonHoc \"1\" -- \"0..*\" MonHocYeuCau",
            "SinhVien \"1\" -- \"0..*\" KetQua",
            "MonHoc \"1\" -- \"0..*\" KetQua"
        ],
        "actor": "Giáo vụ",
        "home_frm": "TrangChuGiaoVuFrm",
        "daos": ["SinhVienDAO", "MonHocDAO", "LopHocPhanDAO", "GradeDAO"]
    },
    "tour": {
        "entities": [
            ("NhanVien", ["- id: int", "- hoTen: String", "- password: String", "- chucVu: String"]),
            ("KhachHang", ["- id: int", "- maKhachHang: String", "- hoTen: String", "- soID: String", "- loaiID: String", "- dienThoai: String", "- email: String", "- diaChi: String"]),
            ("Tour", ["- id: int", "- maTour: String", "- tenTour: String", "- noiXuatPhat: String", "- noiDen: String", "- moTa: String"]),
            ("LichTrinhTour", ["- id: int", "- tourId: int", "- ngayXuatPhat: Date", "- soChoTrong: int", "- giaTour: double"]),
            ("HoaDonDatTour", ["- id: int", "- khachHangId: int", "- lichTrinhId: int", "- ngayDat: Date", "- soVe: int", "- tenKhachDaiDien: String", "- tongTien: double", "- trangThai: String"]),
            ("PhieuHuyTour", ["- id: int", "- hoaDonId: int", "- ngayHuy: Date", "- tienHoan: double", "- tienPhat: double"]),
            ("DiaDiemDen", ["- id: int", "- tenDiaDiem: String", "- moTa: String"])
        ],
        "relationships": [
            "NhanVien \"1\" -- \"0..*\" HoaDonDatTour",
            "KhachHang \"1\" -- \"0..*\" HoaDonDatTour",
            "LichTrinhTour \"1\" -- \"0..*\" HoaDonDatTour",
            "Tour \"1\" *-- \"0..*\" LichTrinhTour",
            "HoaDonDatTour \"1\" -- \"0..1\" PhieuHuyTour",
            "Tour \"1\" -- \"0..*\" DiaDiemDen"
        ],
        "actor": "Nhân viên",
        "home_frm": "TrangChuNhanVienFrm",
        "daos": ["KhachHangDAO", "TourDAO", "LichTrinhTourDAO", "BookingDAO"]
    },
    "nhahang": {
        "entities": [
            ("NhanVien", ["- id: int", "- hoTen: String", "- password: String", "- chucVu: String"]),
            ("BanAn", ["- id: int", "- maBan: String", "- tenBan: String", "- maxKhach: int", "- moTa: String", "- daGop: boolean"]),
            ("KhachHang", ["- id: int", "- maKhach: String", "- hoTen: String", "- dienThoai: String", "- email: String", "- diaChi: String"]),
            ("MonAn", ["- id: int", "- maMon: String", "- theLoai: String", "- tenMon: String", "- moTa: String", "- giaHienTai: double"]),
            ("ComboMon", ["- id: int", "- maCombo: String", "- tenCombo: String", "- moTa: String", "- giaCombo: double"]),
            ("ComboChiTiet", ["- id: int", "- comboId: int", "- monAnId: int", "- soLuong: int"]),
            ("PhieuGoiMon", ["- id: int", "- banId: int", "- khachHangId: int", "- ngayGoi: Date", "- trangThai: String"]),
            ("ChiTietGoiMon", ["- id: int", "- phieuGoiId: int", "- monAnId: int", "- comboId: int", "- soLuong: int", "- giaBan: double"]),
            ("HoaDonThanhToan", ["- id: int", "- phieuGoiId: int", "- nhanVienId: int", "- ngayThanhToan: Date", "- maGiamGia: String", "- tienGiam: double", "- tongTienThanhToan: double"]),
            ("PhieuGiamGia", ["- id: int", "- maGiamGia: String", "- moTa: String", "- phanTramGiam: double"])
        ],
        "relationships": [
            "BanAn \"1\" -- \"0..*\" PhieuGoiMon",
            "KhachHang \"1\" -- \"0..*\" PhieuGoiMon",
            "PhieuGoiMon \"1\" *-- \"0..*\" ChiTietGoiMon",
            "ChiTietGoiMon \"0..*\" -- \"0..1\" MonAn",
            "ChiTietGoiMon \"0..*\" -- \"0..1\" ComboMon",
            "ComboMon \"1\" *-- \"0..*\" ComboChiTiet",
            "ComboChiTiet \"0..*\" -- \"1\" MonAn",
            "PhieuGoiMon \"1\" -- \"1\" HoaDonThanhToan",
            "NhanVien \"1\" -- \"0..*\" HoaDonThanhToan",
            "HoaDonThanhToan \"0..*\" -- \"0..1\" PhieuGiamGia"
        ],
        "actor": "Nhân viên phục vụ",
        "home_frm": "TrangChuNhanVienFrm",
        "daos": ["TableDAO", "FoodItemDAO", "OrderDAO", "BillDAO"]
    }
}

# Fallback domains generator
def generate_fallback_domain(domain):
    return {
        "entities": [
            ("NhanVien", ["- id: int", "- hoTen: String", "- password: String", "- chucVu: String"]),
            ("KhachHang", ["- id: int", "- maKhach: String", "- hoTen: String", "- dienThoai: String", "- diaChi: String"]),
            ("MatHang", ["- id: int", "- maHang: String", "- tenHang: String", "- giaBan: double", "- soLuong: int"]),
            ("GiaoDich", ["- id: int", "- khachHangId: int", "- nhanVienId: int", "- ngayLap: Date", "- tongTien: double"]),
            ("ChiTietGiaoDich", ["- id: int", "- giaoDichId: int", "- matHangId: int", "- soLuong: int", "- donGia: double"])
        ],
        "relationships": [
            "KhachHang \"1\" -- \"0..*\" GiaoDich",
            "NhanVien \"1\" -- \"0..*\" GiaoDich",
            "GiaoDich \"1\" *-- \"0..*\" ChiTietGiaoDich",
            "ChiTietGiaoDich \"0..*\" -- \"1\" MatHang"
        ],
        "actor": "Nhân viên",
        "home_frm": "TrangChuFrm",
        "daos": ["KhachHangDAO", "MatHangDAO", "GiaoDichDAO", "ChiTietGiaoDichDAO"]
    }

# Process and write PlantUML code for all 66 exams
for idx, exam in enumerate(exams_raw):
    num = exam["num"]
    title = exam["title"]
    body = exam["body"]
    
    domain = get_domain(num)
    domain_data = DOMAINS_DATA.get(domain, generate_fallback_domain(domain))
    
    actor = domain_data.get("actor", "Nhân viên")
    home_frm = domain_data.get("home_frm", "TrangChuFrm")
    
    # Identify module name from text
    mod_match = re.search(r"(?:Anh/chị hãy thực hiện modul|Modul)\s+[\"']?([^\"'\n]+)[\"']?", body, re.IGNORECASE)
    mod_name = mod_match.group(1).strip() if mod_match else "Quản lý nghiệp vụ"
    mod_name = re.sub(r"\s+với\s+các\s+bước.*", "", mod_name, flags=re.IGNORECASE)
    mod_name = re.sub(r"\s+được\s+mô\s+tả.*", "", mod_name, flags=re.IGNORECASE)
    mod_name = re.sub(r"\s+với\s+mô\s+tả.*", "", mod_name, flags=re.IGNORECASE)
    
    boundary_class_base = mod_name.replace(' ', '').replace('“','').replace('”','')
    
    # MVC Boundaries
    if domain == "thuvien":
        view_classes = ["TrangChuThuThuFrm", "TimKiemDocGiaFrm", "ChoMuonSachFrm", "PhieuMuonFrm"]
    elif domain == "tinchi":
        view_classes = ["TrangChuSVFrm", "DangKyHocFrm", "LichHocLopHPFrm", "PhieuDangKyFrm"]
    else:
        view_classes = ["TrangChuFrm", f"{boundary_class_base}Frm", f"XacNhan{boundary_class_base}Frm"]
        
    daos_classes = domain_data.get("daos", ["KhachHangDAO", "MatHangDAO", "GiaoDichDAO"])

    # 1. PLANTUML ENTITY DIAGRAM
    puml_entity = "@startuml Sơ_đồ_lớp_thực_thể\n"
    for name, fields in domain_data["entities"]:
        puml_entity += f"class {name} {{\n"
        for field in fields:
            puml_entity += f"  {field}\n"
        puml_entity += "}\n"
    for rel in domain_data["relationships"]:
        puml_entity += f"{rel}\n"
    puml_entity += "@enduml\n"

    # 2. PLANTUML MVC DIAGRAM
    puml_mvc = "@startuml Sơ_đồ_lớp_MVC\n"
    # base DAO class
    puml_mvc += "class DAO {\n  ~ con: Connection\n  + DAO()\n}\n"
    # Views
    for view in view_classes:
        puml_mvc += f"class {view} {{\n  + actionPerformed(e: ActionEvent): void\n}}\n"
    # DAOs
    for dao in daos_classes:
        puml_mvc += f"class {dao} {{\n  + layDuLieu(): Object\n  + luuDuLieu(): boolean\n}}\n"
        puml_mvc += f"DAO <|-- {dao}\n"
    # Entities references (simplified list)
    for name, _ in domain_data["entities"]:
        puml_mvc += f"class {name} {{\n  - id: int\n}}\n"

    # Connections between View -> DAO and View -> View
    for i in range(len(view_classes) - 1):
        puml_mvc += f"{view_classes[i]} ..> {view_classes[i+1]}\n"
    
    # Associate first DAO with second screen, second DAO with third screen
    if len(daos_classes) >= 1 and len(view_classes) >= 2:
        puml_mvc += f"{view_classes[1]} --> {daos_classes[0]}\n"
    if len(daos_classes) >= 2 and len(view_classes) >= 3:
        puml_mvc += f"{view_classes[2]} --> {daos_classes[1]}\n"
        
    puml_mvc += "@enduml\n"

    # 3. PLANTUML SEQUENCE DIAGRAM
    puml_seq = "@startuml Sơ_đồ_tuần_tự\n"
    puml_seq += f"actor \"{actor}\" as User\n"
    for view in view_classes:
        puml_seq += f"boundary {view}\n"
    for dao in daos_classes[:2]:
        puml_seq += f"control {dao}\n"
    puml_seq += "database CSDL\n"
    
    # Message flows
    puml_seq += f"User -> {view_classes[0]} : Chọn chức năng \"{mod_name}\"\n"
    puml_seq += f"activate {view_classes[0]}\n"
    puml_seq += f"{view_classes[0]} -> {view_classes[1]} : new {view_classes[1]}()\n"
    puml_seq += f"activate {view_classes[1]}\n"
    puml_seq += f"{view_classes[1]} --> User : hiển thị biểu mẫu nhập dữ liệu\n"
    puml_seq += f"deactivate {view_classes[0]}\n"
    
    puml_seq += f"User -> {view_classes[1]} : Nhập khóa tra cứu và click tìm kiếm\n"
    if len(daos_classes) >= 1:
        puml_seq += f"{view_classes[1]} -> {daos_classes[0]} : timKiemTheoMa(ma)\n"
        puml_seq += f"activate {daos_classes[0]}\n"
        puml_seq += f"{daos_classes[0]} -> CSDL : SELECT chi tiết đối tượng\n"
        puml_seq += f"activate CSDL\n"
        puml_seq += f"CSDL --> {daos_classes[0]} : Trả kết quả về\n"
        puml_seq += f"deactivate CSDL\n"
        puml_seq += f"{daos_classes[0]} --> {view_classes[1]} : Trả về đối tượng Entity\n"
        puml_seq += f"deactivate {daos_classes[0]}\n"
        
    if len(view_classes) >= 3:
        puml_seq += f"{view_classes[1]} -> {view_classes[2]} : new {view_classes[2]}(Entity)\n"
        puml_seq += f"activate {view_classes[2]}\n"
        puml_seq += f"{view_classes[2]} --> User : hiển thị chi tiết màn hình nghiệp vụ chính\n"
        puml_seq += f"deactivate {view_classes[1]}\n"
        
        puml_seq += f"User -> {view_classes[2]} : Bấm nút Xác nhận lưu giao dịch\n"
        if len(daos_classes) >= 2:
            puml_seq += f"{view_classes[2]} -> {daos_classes[1]} : themGiaoDich(data)\n"
            puml_seq += f"activate {daos_classes[1]}\n"
            puml_seq += f"{daos_classes[1]} -> CSDL : INSERT/UPDATE dữ liệu mới\n"
            puml_seq += f"activate CSDL\n"
            puml_seq += f"CSDL --> {daos_classes[1]} : Lưu thành công\n"
            puml_seq += f"deactivate CSDL\n"
            puml_seq += f"{daos_classes[1]} --> {view_classes[2]} : Trả về Success = true\n"
            puml_seq += f"deactivate {daos_classes[1]}\n"
            
        if len(view_classes) >= 4:
            puml_seq += f"{view_classes[2]} -> {view_classes[3]} : new {view_classes[3]}()\n"
            puml_seq += f"activate {view_classes[3]}\n"
            puml_seq += f"{view_classes[3]} --> User : hiển thị hóa đơn kết quả và in phiếu\n"
            puml_seq += f"deactivate {view_classes[3]}\n"
            
        puml_seq += f"{view_classes[2]} --> User : Thông báo thành công\n"
        puml_seq += f"deactivate {view_classes[2]}\n"
        
    puml_seq += "@enduml\n"

    # Combine all 3 diagrams into a single .puml file
    combined_puml = f"' Đề số {num:02d} - UML Code\n\n" + puml_entity + "\n" + puml_mvc + "\n" + puml_seq

    # Write file
    filename = f"UML_D{num}.puml"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f_out:
        f_out.write(combined_puml)

print("Successfully generated all 66 flat files in target folder.")
