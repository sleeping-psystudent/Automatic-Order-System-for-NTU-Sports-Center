from flask import Flask, redirect, url_for, render_template,request
import csv
import webbrowser
import sys

app = Flask(__name__)
@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "POST": 
        try :
            file = open('save.csv', 'r', newline='')
            file.close()
        except : 
            with open('save.csv', 'a+', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=',')
                ll = [
                'studentid',
                'password',
                'email',
                'place',
                'Date',
                'Time',
                 'num',
                ] 
                writer.writerow( ll )

        with open('save.csv', 'a+', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=',')
            ll = [
                str( request.form['studentid'] ),
                str( request.form['password'] ),
                str( request.form['email'] ),
                str( request.form['place'] ),
                str( request.form['Date'] ),
                str( request.form['Time'] ),
                str( request.form['num'] ),
                ] 
            writer.writerow( ll )
        
        return "預約成功: "  \
                +  "<br>學號:" +request.form['studentid'] \
                + "<br>EMail:" + request.form['email'] \
               + "<br>password:" + request.form['password'] \
                + "<br>場地：" + request.form['place'] \
                + "<br>日期：" + request.form['Date'] \
                + "<br>時間：" + request.form['Time'] \
                + "<br>場數：" + request.form['num'] \
                
    

    
    return '''
    
<form method="POST" action="">
    
    <div id="Site Name", style = "background-color: 	#336666;height: 70px;position:relative;
                                  margin-top: -10px">
        <font size = "8"><font color = "#D1E9E9">台大新體預約場地</font></font></div>
    <div id = "IDintro" class = "" style = "background-color: 	#D1E9E9;line-height:35px;padding:8px">
        <font color = "#005757">
        ☆ 學號：<input type = "text" name = "studentid" value = ""><br>
        ★ 密碼：<input type = "password" name = "password" value = ""><br>
        </font>
    </div>
    
    <div id = "3W" class = "" style = "background-color: 	#B3D9D9;line-height:35px;padding:8px">
        <font color = "#005757">
        ☆ 欲借場地：<select name="place">
        <option value="3F羽球場">3F羽球場</option>
        <option value="1F羽球場">1F羽球場</option>
        <option value="B1桌球室">B1桌球室</option>
        <option value="B1壁球室">B1壁球室</option>
        <option value="B109教室(桌球)">B109教室(桌球)</option>
    </select><br>
    ★ 日期：<input type = "text" name = "Date" value = ""> (範例：2021/12/03)<br>
    ☆ 時間：<input type = "text" name = "Time" value = ""> (範例：Fri 21:00)<br>
        </font>
    </div>
    
    
    <div id = "" class = "" style = "background-color: 	#D1E9E9;line-height:35px;padding:8px">
        <font color = "#005757">
        ★ Email：<input type = "text" name = "email" value = ""><br>
        ☆ 場數： <input type = "text" name = "num" value = ""><br>
        <input type="submit" value="預約" class="btn btn-primary">  
        </font>
    </div>
 
    <div id="Footer" style = "background-color: 	#336666;height: 60px;position:relative;
　margin-top: -100px;">
    </div>
</form>
   '''

if __name__ == '__main__':
    url = 'http://127.0.0.1:5000/'
    webbrowser.open_new(url)
    app.run()