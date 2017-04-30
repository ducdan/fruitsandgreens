from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, ForeignKey, Integer, String, Text, CHAR, DATE, Float, DECIMAL

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class NCC(db.Model):  # Nhà cung cấp
    ID_NCC = db.Column(db.Integer, autoincrement=True, primary_key=True)
    MANCC = db.Column(db.CHAR(7), nullable=False, unique=True)
    TENNCC = db.Column(db.Text, nullable=False, unique=True)
    DIACHI = db.Column(db.Text)
    NGUOILH = db.Column(db.Text)  # Người liên hệ
    SDT = db.Column(db.String(11))
    Hopdong = db.relationship('HOPDONG', backref='owner_hopdong_ncc', lazy='dynamic')

    def __init__(self, MANCC, TENNCC, DIACHI, NGUOILH, SDT):
        self.MANCC = MANCC
        self.TENNCC = TENNCC
        self.DIACHI = DIACHI
        self.NGUOILH = NGUOILH
        self.SDT = SDT

# ok

class HOPDONG(db.Model):  # Hợp đồng
    ID_HD = Column(Integer, autoincrement=True, primary_key=True)
    MAHD = Column(CHAR(7), nullable=False, unique=True)
    TENHD = Column(Text, nullable=False, unique=True)
    Id_ncc = Column(Integer, ForeignKey('NCC.ID_NCC'))
    phieunhap = db.relationship('PHIEUNHAP', backref='owner_phieunhap_hopdong', lazy='dynamic')

    def __init__(self, MAHD, TENHD, idncc):
        self.MAHD = MAHD
        self.TENHD = TENHD
        self.Id_ncc = idncc

# ok

class LOAISP(db.Model):  # Loại sản phẩm
    ID_LOAISP = Column(Integer, autoincrement=True, primary_key=True)
    MALOAI = Column(String(30), nullable=False, unique=True)
    TENLOAI = Column(Text, nullable=False, unique=True)
    sanphamnhap = db.relationship('SPN', backref='owner_sanphamnhap_loaisp', lazy='dynamic')
    sanphamxuat = db.relationship('SPX', backref='owner_sanphamxuat_loaisp', lazy='dynamic')

    def __init__(self, MALOAI, TENLOAI):
        self.MALOAI = MALOAI
        self.TENLOAI = TENLOAI

# ok

class SPN(db.Model):  # Sản phẩm nhập
    ID_SPN = Column(Integer, autoincrement=True, primary_key=True)
    MASPN = Column(String(30), nullable=False, unique=True)
    TENSPN = Column(Text, nullable=False, unique=True)
    Id_loaisp = Column(Integer, ForeignKey('LOAISP.ID_LOAISP'))
    phieunhap = db.relationship('PHIEUNHAP', backref='owner_phieunhap_spn', lazy='dynamic')
    def __init__(self, MASPN, TENSPN, idlsp):
        self.MASPN = MASPN
        self.TENSPN = TENSPN
        self.Id_loaisp = idlsp

# ok

class SPX(db.Model):  # Sản phẩm xuất
    ID_SPX = Column(Integer, autoincrement=True, primary_key=True)
    MASPX = Column(String(30), nullable=False, unique=True)
    TENSPX = Column(Text, nullable=False, unique=True)
    Id_loaisp = Column(Integer, ForeignKey('LOAISP.ID_LOAISP'))
    phieuxuat = db.relationship('PHIEUXUAT', backref='owner_phieuxuat_spx', lazy='dynamic')

    def __init__(self, MASPX, TENSPX, idlsp):
        self.MASPX = MASPX
        self.TENSPX = TENSPX
        self.Id_loaisp = idlsp

# ok

class LOAIHINHNHAP(db.Model):  # Loại hình nhập
    ID_LHN = Column(Integer, autoincrement=True, primary_key=True)
    MALHN = Column(CHAR(7), nullable=False, unique=True)
    TENLHN = Column(Text, nullable=False, unique=True)
    phieunhap = db.relationship('PHIEUNHAP', backref='owner_phieunhap_loaihinhnhap', lazy='dynamic')

    def __init__(self, MALHN, TENLHN):
        self.MALHN = MALHN
        self.TENLHN = TENLHN

# ok

class PHIEUNHAP(db.Model):  # Phiếu nhập
    ID_PN = Column(Integer, autoincrement=True, primary_key=True)
    MAPN = Column(CHAR(7), nullable=False, unique=True)
    SLNHAP = Column(Float)
    SLNTHUC = Column(Float)
    DVT = Column(String(20))
    CONTAINER_NO = Column(String(20))
    NGAYNHAP = Column(DATE)
    PRICE = Column(DECIMAL)
    TONGTIEN = Column(DECIMAL)
    Id_lhn = Column(Integer, ForeignKey('LOAIHINHNHAP.ID_LHN'))
    Id_hd = Column(Integer, ForeignKey('HOPDONG.ID_HD'))
    Id_nv = Column(Integer, ForeignKey('NHANVIEN.ID_NV'))
    Id_spn = Column(Integer, ForeignKey('SPN.ID_SPN'))
    kho = db.relationship('KHO', backref='owner_kho_phieunhap', lazy='dynamic')

    def __init__(self, MAPN, DVT, SLNHAP, SLNTHUC, CONTAINER_NO, NGAYNHAP, PRICE, TONGTIEN, idlhn, idhd, idnv, idspn):
        self.MAPN = MAPN
        self.SLNHAP = SLNHAP
        self.SLNTHUC = SLNTHUC
        self.DVT = DVT
        self.CONTAINER_NO = CONTAINER_NO
        self.NGAYNHAP = NGAYNHAP
        self.PRICE = PRICE
        self.TONGTIEN = TONGTIEN
        self.Id_lhn = idlhn
        self.Id_hd = idhd
        self.Id_nv = idnv
        self.Id_spn = idspn

# ok

class PHIEUXUAT(db.Model):  # Phiếu xuất
    ID_PX = Column(db.Integer, autoincrement=True, primary_key=True)
    MAPX = Column(CHAR(7), nullable=False, unique=True)
    NGAYDATHANG = Column(DATE)
    NGAYGIAO = Column(DATE)
    PHAN_TRAM_DU_THIEU = Column(Text)
    TRANGTHAI = Column(Text)  # Thùng hoặc KG
    POST_OF_DISCHARGE = Column(Text)
    SLXUAT = Column(Text)
    SLXTHUC = Column(Text)
    DVT = Column(String(20))
    PRICE = Column(DECIMAL)
    TONGTIEN = Column(DECIMAL)
    Id_nv = Column(Integer, ForeignKey('NHANVIEN.ID_NV'))
    Id_kh = Column(Integer, ForeignKey('KHACHHANG.ID_KH'))
    Id_pt = Column(Integer, ForeignKey('PHUONGTIEN.ID_PT'))
    Id_spx = Column(Integer, ForeignKey('SPX.ID_SPX'))
    kho = db.relationship('KHO', backref='owner_kho_phieuxuat', lazy='dynamic')

    def __init__(self, MAPX, NGAYDATHANG, NGAYGIAO, PHANTRAMDUTHIEU, TRANGTHAI,POST_OF_DISCHARGE, SLXUAT, SLXTHUC, DVT,
                 PRICE, TONGTIEN, idnv, idkh, idpt, idspx):
        self.MAPX = MAPX
        self.NGAYDATHANG = NGAYDATHANG
        self.NGAYGIAO = NGAYGIAO
        self.PHAN_TRAM_DU_THIEU = PHANTRAMDUTHIEU
        self.TRANGTHAI = TRANGTHAI
        self.POST_OF_DISCHARGE = POST_OF_DISCHARGE
        self.SLXUAT = SLXUAT
        self.SLXTHUC = SLXTHUC
        self.DVT = DVT
        self.PRICE = PRICE
        self.TONGTIEN = TONGTIEN
        self.Id_nv = idnv
        self.Id_kh = idkh
        self.Id_pt = idpt
        self.Id_spx = idspx

# ok

class KHO(db.Model):  # Kho
    ID_KHO = Column(Integer, autoincrement=True, primary_key=True)
    MAKHO = Column(String(10), nullable=False, unique=True)
    TENKHO = Column(Text, nullable=False, unique=True)
    DIACHI = Column(Text)
    SDT = Column(String(11))
    Id_pn = Column(Integer, ForeignKey('PHIEUNHAP.ID_PN'))
    Id_px = Column(Integer, ForeignKey('PHIEUXUAT.ID_PX'))

    def __init__(self, MAKHO, TENKHO, DIACHI, SDT, idpn, idpx):
        self.MAKHO = MAKHO
        self.TENKHO = TENKHO
        self.DIACHI = DIACHI
        self.SDT = SDT
        self.Id_pn = idpn
        self.Id_px = idpx

# ok

class KHACHHANG(db.Model):  # Khách hàng
    ID_KH = Column(Integer, autoincrement=True, primary_key=True)
    MA_KH = Column(CHAR(7), nullable=False, unique=True)
    TENKH = Column(Text, nullable=False, unique=True)
    DIACHI = Column(Text)
    SDT = Column(String(11))
    NGUOILH = Column(Text)  # Người liên hệ
    phieuxuat = db.relationship('PHIEUXUAT', backref='owner_phieuxuat_khachhang', lazy='dynamic')

    def __init__(self, MA_KH, TENKH, DIACHI, SDT, NGUOILH):
        self.MA_KH = MA_KH
        self.TENKH = TENKH
        self.DIACHI = DIACHI
        self.SDT = SDT
        self.NGUOILH = NGUOILH

# ok

class PHUONGTIEN(db.Model):  # Phương tiện
    ID_PT = Column(Integer, autoincrement=True, primary_key=True)
    MAPT = Column(CHAR(7), nullable=False, unique=True)
    TenPT = Column(Text, nullable=False, unique=True)
    phieuxuat = db.relationship('PHIEUXUAT', backref='owner_phieuxuat_phuongtien', lazy='dynamic')

    def __init__(self, MAPT, TenPT):
        self.MAPT = MAPT
        self.TenPT = TenPT

# ok

class NHANVIEN(db.Model):  # Nhân viên
    ID_NV = Column(Integer, autoincrement=True, primary_key=True)
    MANV = Column(CHAR(7), nullable=False, unique=True)
    TENNV = Column(Text, nullable=False, unique=True)
    phieunhap = db.relationship('PHIEUNHAP', backref='owner_phieunhap_nhanvien', lazy='dynamic')
    phieuxuat = db.relationship('PHIEUXUAT', backref='owner_phieuxuat_nhanvien', lazy='dynamic')

    def __init__(self, MANV, TENNV):
        self.MANV = MANV
        self.TENNV = TENNV

# ok

class XNK(db.Model): #Xuaất nhập khẩu
    ID_XNK = Column(Integer, autoincrement=True, primary_key=True)
    Shipper = Column(Text)
    Cosignee = Column(Text)
    ETA = Column(DATE)
    Port_of_Discharge = Column(Text)
    Invoice = Column(String(10))
    Container_No = Column(Text)
    Goods = Column(Text)
    Carton = Column(Integer)
    Price = Column(DECIMAL)
    Amount_invoice = (DECIMAL)
    payment_from_Fruits_and_Greens = Column(DECIMAL)
    Date_Payment = Column(DATE)
    Credit_note = Column(Text)
    Balance = Column(DECIMAL)
    NOTE = Column(Text)
    Load_N0 = Column(Text)

    def __init__(self,Shipper,Cosignee,ETA,Port_of_Discharge,Invoice,Container_No,Goods,Carton,Price,Amount_invoice,
                 payment_from_Fruits_and_Greens,Date_Payment,Credit_note,Balance,NOTE,Load_N0):
        self.Shipper = Shipper
        self.Cosignee = Cosignee
        self.ETA = ETA
        self.Port_of_Discharge = Port_of_Discharge
        self.Invoice = Invoice
        self.Container_No = Container_No
        self.Goods = Goods
        self.Carton = Carton
        self.Price = Price
        self.Amount_invoice = Amount_invoice
        self.payment_from_Fruits_and_Greens = payment_from_Fruits_and_Greens
        self.Date_Payment = Date_Payment
        self.Credit_note = Credit_note
        self.Balance = Balance
        self.NOTE = NOTE
        self.Load_N0 = Load_N0


def add_NCC(MANCC, TENNCC, DIACHI, NGUOILH, SDT):
    ncc = NCC(MANCC, TENNCC, DIACHI, NGUOILH, SDT)
    db.session.add(ncc)
    db.session.commit()


def add_HD(MAHD, TENHD, idncc):
    hd = HOPDONG(MAHD, TENHD, idncc)
    db.session.add(hd)
    db.session.commit()


def add_LOAISP(MALOAI, TENLOAI):
    lsp = LOAISP(MALOAI, TENLOAI)
    db.session.add(lsp)
    db.session.commit()


def add_SPN(MASPN, TENSPN, idlsp):
    spn = SPN(MASPN, TENSPN, idlsp)
    db.session.add(spn)
    db.session.commit()


def add_SPX(MASPX, TENSPX, idlsp):
    spx = SPX(MASPX, TENSPX, idlsp)
    db.session.add(spx)
    db.session.commit()


def add_LHN(MALHN, TENLHN):
    lhn = LOAIHINHNHAP(MALHN, TENLHN)
    db.session.add(lhn)
    db.session.commit()


def add_PN(MAPN, DVT, SLNHAP, SLNTHUC, CONTAINER_NO, NGAYNHAP, PRICE, TONGTIEN, idlhn, idhd, idnv, idspn):
    pn = PHIEUNHAP(MAPN, DVT, SLNHAP, SLNTHUC, CONTAINER_NO, NGAYNHAP, PRICE, TONGTIEN, idlhn, idhd, idnv, idspn)
    db.session.add(pn)
    db.session.commit()


def add_PX(MAPX, NGAYDATHANG, NGAYGIAO, PHANTRAMDUTHIEU, TRANGTHAI,POST_OF_DISCHARGE, SLXUAT,SLXTHUC, DVT, PRICE,
           TONGTIEN, idnv, idkh, idpt, idspx):
    px = PHIEUXUAT(MAPX, NGAYDATHANG, NGAYGIAO, PHANTRAMDUTHIEU, TRANGTHAI,POST_OF_DISCHARGE,SLXUAT, SLXTHUC, DVT,
                   PRICE, TONGTIEN, idnv, idkh, idpt, idspx)
    db.session.add(px)
    db.session.commit()


def add_KHO(MAKHO, TENKHO, DIACHI, SDT, idpn, idpx):
    kho = KHO(MAKHO, TENKHO, DIACHI, SDT, idpn, idpx)
    db.session.add(kho)
    db.session.commit()


def add_KH(MA_KH, TENKH, DIACHI, SDT, NGUOILH):
    kh = KHACHHANG(MA_KH, TENKH, DIACHI, SDT, NGUOILH)
    db.session.add(kh)
    db.session.commit()


def add_PT(MAPT, TenPT):
    pt = PHUONGTIEN(MAPT, TenPT)
    db.session.add(pt)
    db.session.commit()


def add_NV(MANV, TENNV):
    nv = NHANVIEN(MANV, TENNV)
    db.session.add(nv)
    db.session.commit()

def add_XNK(Shipper,Cosignee,ETA,Port_of_Discharge,Invoice,Container_No,Goods,Carton,Price,Amount_invoice,
            payment_from_Fruits_and_Greens,Date_Payment,Credit_note,Balance,NOTE,Load_N0):
    xnk = XNK(Shipper,Cosignee,ETA,Port_of_Discharge,Invoice,Container_No,Goods,Carton,Price,Amount_invoice,
              payment_from_Fruits_and_Greens,Date_Payment,Credit_note,Balance,NOTE,Load_N0)
    db.session.add(xnk)
    db.session.commit()
def hello_world():
    print(db)
    # db.create_all()
    # add_NCC('NCC001', 'Fresh', '123 DBP, Q.1, TP.HCM', 'An', '0838383838')
    # add_NCC('NCC002', 'Fruits', '456 DBP, Q.1, TP.HCM', 'Anh', '0837373737')
    # add_LOAISP('CA', 'Cam')
    # add_LOAISP('TA', 'Tao')
    # add_LHN('LHN01', 'Nhap tai Cong ty')
    # add_LHN('LHN02', 'Cang')
    # add_KH('KH001', 'QUEEN LAND Q2', 'Q.2-TP.HCM', '0147852369', 'Bao')
    # add_KH('KH002', 'VINMART A12 PHAN VĂN TRỊ', 'Phan Van Tri-TP.HCM', '0123456789', 'Binh')
    # add_PT('XM', 'Xe May')
    # add_PT('XT', 'Xe Tai')
    # add_NV('NV001', 'Long')
    # add_NV('NV002', 'Hung')
    # add_HD('HD001', 'Hop dong dai han', 1)
    # add_HD('HD002', 'Hop dong ngan han',2)
    # add_SPN('CAMYN-40', 'Cam navel My size 40', 1)
    # add_SPN('TAMYDOK20-100', 'Tao Đo My King Size 100 thung 20kg', 2)
    # add_SPX('CAUCN-48', 'Cam navel Uc size 48', 1)
    # add_SPX('TAMYDOK20-113', 'Tao Đo My King Size 113 thung 20kg', 2)
    # add_PN('N0001', 'Thung', '50', '50', 'TCLU 1230412', '2017/04/20', '50', '2500',1,1,1,1)
    # add_PN('N0002', 'Thung', '60', '60', 'TCLU 1230413', '2017/04/21', '60', '3600',2,2,2,2)
    # add_PX('X0001', '2017/04/21', '2017/04/23', '100%', 'Thuc Nhan', 'HCM', '40', '40', 'Thung', '70', '2800',1,1,1,1)
    # add_PX('X0002', '2017/04/22', '2017/04/24', '100%', 'Thuc Nhan', 'HaNoi', '50', '50', 'Thung', '80', '4000',2,2,2,2)
    # add_KHO('K001', 'Kho Thu Duc', 'So 12 duong 6, P.Linh Chieu, Q.Thu Duc', '0838379828',1,1)
    # add_KHO('K002', 'Kho Tran Dinh Xu', '137/31 Tran Dinh Xu, P.Nguyen Cu Trinh, Q.1', '0838385916',2,2)
    add_XNK('DOMEX','F&G','2015/11/25','HCM','477641','TCLU 1230412','Apple Granny Smith 100','855','60','51300',None,None,None,None,None,None)
    add_XNK('Freshmax','F&G','2015/11/25','Hà Nội','51797','176-17889885','Cherry Lapin 28-30mm (5kg/ctn)','168',None,None,None,None,None,None,None,None)
    return 'Hello World!'