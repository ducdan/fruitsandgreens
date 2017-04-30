from flask import Flask,render_template,request,send_file
from DataModel import KHO
app = Flask(__name__,static_folder='vendors')


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/nhapkho')
def nhapkho():
    return render_template('nhapkho.html')

@app.route('/nhap',methods=['POST'])
def nhap():
    fistname=request.form['firstname']
    lastname = request.form['lastname']
    print(fistname+" "+lastname)
    dic={
        'first':fistname,
        'last':lastname
    }
    return render_template('nhapkho.html',fist=dic)
@app.route('/xemhangton')
def hangton():
    return render_template('XemHangTon.html')





@app.route('/xemkho', methods=['GET', 'POST'])
def show_kho():
    kho = ""
    MaKho = ""
    LoaiSp = ""
    TenSp = ""
    if request.method == 'POST':
        kho = request.form['Kho']
        MaKho = kho[0:4]
        LoaiSp = request.form['LoaiSP']
        TenSp = request.form['TenSP']
    data = []
    if ((kho == "Tất cả") & (LoaiSp == "") & (TenSp == "")):
        data = KHO.query.all()
    elif ((kho == "Tất cả") & (LoaiSp == "")):
        pass
    elif ((kho == "Tất cả") & (TenSp == "")):
        pass
    elif ((kho == "Tất cả")):
        pass
    elif ((LoaiSp == "") & (TenSp == "")):
        data = KHO.query.filter_by(MAKHO=MaKho).all()
    elif ((TenSp == "")):
        pass
    elif ((LoaiSp == "")):
        pass
    else:
        pass

    return render_template("XemHangTon.html", data = data)

@app.route('/report')
def report():
    return send_file('report.pdf',attachment_filename=True)


if __name__ == '__main__':
    app.run(debug=True,port=6767)
