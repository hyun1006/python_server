# flask server 구동 코드!!
from flask import Flask, render_template  
from flask import request, redirect, make_response
from aws import detect_labels_local_file as label
from aws import compare_faces
from werkzeug.utils import secure_filename

# html 문서 load!!
# 단, templates 폴더에 있는 html만 바라볼 수 있다.
app = Flask(__name__)

# 서버 주소 / 로 들어오면
# return html 문서
@app.route("/")
def index():
    return render_template("home.html")



@app.route("/compare", methods=["POST"])
def compare():
    try:
        if request.method == "POST":
            f1 = request.files["file1"]
            f2 = request.files["file2"]

            f1_filename = secure_filename(f1.filename)
            f2_filename = secure_filename(f2.filename)

            f1.save("static/" + f1_filename)
            f2.save("static/" + f2_filename)

            r = compare_faces("static/" + f1_filename, "static/" + f2_filename)
            return r
        
    except:
        return "얼굴 비교 실패"



@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]

            filename = secure_filename(f.filename)
            # 외부에서 온 이미지, 파일 등을 마음대로 저장할 수 없음
            
            f.save("static/" + filename)
            r = label("static/" + filename)
            return r
            # 서버에 클라이언트가 보낸 이미지 저장

    except:
        return "감지 실패"



@app.route("/mbti", methods=["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]

            return f"당신의 MBTI는 {mbti}입니다"
    except:
        return "데이터 수신 실패"



@app.route("/login", methods=["GET"])
def login():

    try:
        if request.method == "GET":
            # get -> request.args
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]

            if (login_id == "seokhyun") and (login_pw == "1234"):
                # 로그인 성공 -> 로그인 성공 페이지 이동
                # seokhyun님 환영합니다

                response = make_response(redirect("/login/success"))
                response.set_cookie("user", login_id)
                return response
            else:
                # 로그인 실패 -> / 경로로 다시 이동
                return redirect("/")

            # return f"{login_id}님 환영합니다."
    except:
        return "로그인 실패"



@app.route("/login/success")
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다."



if __name__ == "__main__":
    # 1. host
    # 2. port
    # app.run(host="127.0.0.1")  # localhost
    app.run(host="0.0.0.0")