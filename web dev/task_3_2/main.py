from crypt import methods
from encodings import search_function
from hashlib import new
from operator import methodcaller
import re
from sqlite3 import connect
import pickle
from urllib import response
from wsgiref.simple_server import make_server
from flask import Flask, jsonify, make_response, redirect, render_template, request
import database
import email_bot
import random

app = Flask(__name__)


@app.route('/bruh')
def bruh():
    return render_template('feed.html', username="sanjiv")


@app.errorhandler(404)
def error_404(e):
    return render_template('error404.html', error = "404")


@app.errorhandler(500)
def error_500(e):
    return render_template('error404.html', error = "500")

@app.route('/admin')
def admin():
    return '''
    <html>
    <head>
    <title>admin page | Slambook</title>
    </head>
    <body>
    <a href="./admin/passwords">passwords database</a>
    <br><br>
    <a href="./admin/users">user database</a>
    <br><br>
    <a href="./admin/posts">all posts</a>
    <br><br>
    <a href="./admin/follow">all profile following and followers list</a>
    </body>
    </html>
    '''

@app.route('/admin/passwords')
def admin_pass():
    return make_response(jsonify(database.get_login_info()), 200)

@app.route('/admin/users')
def admin_users():
    return make_response(jsonify(database.get_all_user_info()), 200)

@app.route('/admin/posts')
def admin_posts():
    return make_response(jsonify(database.get_all_posts()), 200)

@app.route('/admin/follow')
def admin_follow():
    return make_response(jsonify(database.get_follow()), 200)



@app.route('/', methods = ["GET", "POST"])
def function():
    if request.method == "GET":
        if request.cookies.get('login_status') == 'True':
            username = request.cookies.get('login_username')
            rollno = request.cookies.get('login_rollno')
            f = open("./data/posts.bin", "rb")
            all_posts = list(pickle.load(f))    #[["by", "message", ["tags"...], "timestamp"]...]
            f.close()
            f = open("./data/user_data/{}.bin".format(rollno), "rb")
            following, followers = list(pickle.load(f))
            f.close()
            posts = []
            if len(following) == 0:
                posts = [[["search and follow your friends to see their posts"], ["slambook"]]]
            else:
                for i in all_posts:
                    for j in following:
                        if i[1] not in [bruh[0] for bruh in posts] and (i[0] == username or j in i[1] or rollno in i[1]):
                            #posts.append([i[1], i[0]])
                            posts.append([database.change_rollno_to_username(i[1]), database.change_rollno_to_username(i[0])])
            for bruh in range(12-len(posts)):
                posts.append(["", ""])
            return render_template('feed.html', username = username, posts0 = posts[0][0], posts1 = posts[1][0], posts2 = posts[2][0], posts3 = posts[3][0], posts4 = posts[4][0], posts5 = posts[5][0], posts6 = posts[6][0], posts7 = posts[7][0], posts8 = posts[8][0], posts9 = posts[9][0], posts10 = posts[10][0], postby0 = posts[0][1], postby1 = posts[1][1], postby2 = posts[2][1], postby3 = posts[3][1], postby4 = posts[4][1], postby5 = posts[5][1], postby6 = posts[6][1], postby7 = posts[7][1], postby8 = posts[8][1], postby9 = posts[9][1], postby10 = posts[10][1])
            # return render_template('feed.html', username = username, posts0 = "sanjiv", postby0 = "sanjiv", posts1 = "", postby1 = "")
        else:
            return redirect('./login')
    if request.method == "POST":
        search_content = str(request.form.get("search_bar"))
        new_post_content = str(request.form.get("new_post_bar"))
        print(search_content)
        print(new_post_content)
        if search_content != "None":
            f = open("./data/search.bin", "wb")
            pickle.dump(search_content, f)
            f.close()
            res = make_response(redirect('/search_result'))
            res.set_cookie("branch", "None")
            res.set_cookie("section", "None")
            res.set_cookie("hostel", "None")
            return res
        if new_post_content != "None":
            print("making a new post")
            database.push_new_post(new_post_content, str(request.cookies.get('login_username')))
            return redirect("/")
        return redirect("/")

@app.route("/search_result", methods = ["GET", "POST"])
def search_result():
    if request.method == "GET":
        f = open("./data/search.bin", "rb")
        search_content = str(pickle.load(f)).split()
        f.close()
        f = open("./data/user_info.bin", "rb")
        user_info = dict(pickle.load(f))
        f.close()
        branch = request.cookies.get("branch")
        section = request.cookies.get("section")
        hostel = request.cookies.get("hostel")
        search_result = []
        for i in user_info.values():
            name = i['name'].split(" ")
            username = i['username'].split(" ")
            for search_content_element in search_content:
                for name_element in name:
                    if search_content_element == name_element:
                        search_result.append(i)
            for search_content_element in search_content:
                for name_element in username:
                    if search_content_element == name_element:
                        search_result.append(i)
        final = []
        if branch != 'None':
            for i in search_result:
                if i['branch'] == branch:
                    final.append(i)
        if section != 'None':
            for i in search_result:
                if i['section'] == section:
                    final.append(i)
        if hostel != 'None':
            for i in search_result:
                if i['hostel'] == hostel:
                    final.append(i)
        if branch == 'None' and section == 'None' and hostel == 'None':
            final = list(search_result)
        print(final)
        for i in range(31 - len(final)):
            final.append({"name" : "", "gender" : "", "programme" : "", "branch" : "", "section" : "", "username" : "", "hostel" : "", "rollno": ""})
        return render_template('search_result.html', username = str(request.cookies.get('login_username')), rollno0 = final[0]['rollno'], user0 = final[0]['username'], dept0 = final[0]['branch'] + ' ' + final[0]['section'], rollno1 = final[1]['rollno'], user1 = final[1]['username'], dept1 = final[1]['branch'] + ' ' + final[1]['section'], rollno2 = final[2]['rollno'], user2 = final[2]['username'], dept2 = final[2]['branch'] + ' ' + final[2]['section'], rollno3 = final[3]['rollno'], user3 = final[3]['username'], dept3 = final[3]['branch'] + ' ' + final[3]['section'], rollno4 = final[4]['rollno'], user4 = final[4]['username'], dept4 = final[4]['branch'] + ' ' + final[4]['section'], rollno5 = final[5]['rollno'], user5 = final[5]['username'], dept5 = final[5]['branch'] + ' ' + final[5]['section'], rollno6 = final[6]['rollno'], user6 = final[6]['username'], dept6 = final[6]['branch'] + ' ' + final[6]['section'], rollno7 = final[7]['rollno'], user7 = final[7]['username'], dept7 = final[7]['branch'] + ' ' + final[7]['section'], rollno8 = final[8]['rollno'], user8 = final[8]['username'], dept8 = final[8]['branch'] + ' ' + final[8]['section'], rollno9 = final[9]['rollno'], user9 = final[9]['username'], dept9 = final[9]['branch'] + ' ' + final[9]['section'], rollno10 = final[10]['rollno'], user10 = final[10]['username'], dept10 = final[10]['branch'] + ' ' + final[10]['section'], rollno11 = final[11]['rollno'], user11 = final[11]['username'], dept11 = final[11]['branch'] + ' ' + final[11]['section'], rollno12 = final[12]['rollno'], user12 = final[12]['username'], dept12 = final[12]['branch'] + ' ' + final[12]['section'], rollno13 = final[13]['rollno'], user13 = final[13]['username'], dept13 = final[13]['branch'] + ' ' + final[13]['section'], rollno14 = final[14]['rollno'], user14 = final[14]['username'], dept14 = final[14]['branch'] + ' ' + final[14]['section'], rollno15 = final[15]['rollno'], user15 = final[15]['username'], dept15 = final[15]['branch'] + ' ' + final[15]['section'], rollno16 = final[16]['rollno'], user16 = final[16]['username'], dept16 = final[16]['branch'] + ' ' + final[16]['section'], rollno17 = final[17]['rollno'], user17 = final[17]['username'], dept17 = final[17]['branch'] + ' ' + final[17]['section'], rollno18 = final[18]['rollno'], user18 = final[18]['username'], dept18 = final[18]['branch'] + ' ' + final[18]['section'], rollno19 = final[19]['rollno'], user19 = final[19]['username'], dept19 = final[19]['branch'] + ' ' + final[19]['section'], rollno20 = final[20]['rollno'], user20 = final[20]['username'], dept20 = final[20]['branch'] + ' ' + final[20]['section'], rollno21 = final[21]['rollno'], user21 = final[21]['username'], dept21 = final[21]['branch'] + ' ' + final[21]['section'], rollno22 = final[22]['rollno'], user22 = final[22]['username'], dept22 = final[22]['branch'] + ' ' + final[22]['section'], rollno23 = final[23]['rollno'], user23 = final[23]['username'], dept23 = final[23]['branch'] + ' ' + final[23]['section'], rollno24 = final[24]['rollno'], user24 = final[24]['username'], dept24 = final[24]['branch'] + ' ' + final[24]['section'], rollno25 = final[25]['rollno'], user25 = final[25]['username'], dept25 = final[25]['branch'] + ' ' + final[25]['section'], rollno26 = final[26]['rollno'], user26 = final[26]['username'], dept26 = final[26]['branch'] + ' ' + final[26]['section'], rollno27 = final[27]['rollno'], user27 = final[27]['username'], dept27 = final[27]['branch'] + ' ' + final[27]['section'], rollno28 = final[28]['rollno'], user28 = final[28]['username'], dept28 = final[28]['branch'] + ' ' + final[28]['section'], rollno29 = final[29]['rollno'], user29 = final[29]['username'], dept29 = final[29]['branch'] + ' ' + final[29]['section'], rollno30 = final[30]['rollno'], user30 = final[30]['username'], dept30 = final[30]['branch'] + ' ' + final[30]['section'])
    if request.method == "POST":
        search_content = str(request.form.get("search_bar"))
        f = open("./data/search.bin", "wb")
        pickle.dump(search_content, f)
        f.close()
        res = make_response(redirect('/search_result'))
        res.set_cookie("branch", "None")
        res.set_cookie("section", "None")
        res.set_cookie("hostel", "None")
        return res




@app.route('/profile/<rollno>', methods=["GET", "POST"])
def madhumitha(rollno):
    if str(request.cookies.get('login_rollno')) == rollno:
        return redirect('/my_profile')
    if request.method == "GET":
        return "yo it works!"
        


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/developer')
def developer_information():
    return render_template('developer.html')

@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login_validation():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        content = database.get_login_info()
        rollno = str(request.form.get('rollno'))
        password = str(request.form.get('password'))
        #print('\n\n\n\n{}\n\n{}\n\n\n\n'.format(len(rollno), len(password)))
        #return "username = {} password = {}".format(rollno, password)
        if rollno not in content.keys():
            return make_response(redirect("/login"))
        if content[rollno] == password:
            res = make_response(render_template('login_success.html'))
            username = database.get_user_info(rollno)['username']
            res.set_cookie('login_status', 'True')
            res.set_cookie('login_rollno', rollno)
            res.set_cookie('login_username', username)
            return res
        else:
            return redirect("./login")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    if request.method == "POST":
        name = str(request.form.get('name'))
        rollno = str(request.form.get('rollno'))
        password1 = str(request.form.get('password1'))
        password2 = str(request.form.get('password2'))
        gender = str(request.form.get('gender'))
        programme = str(request.form.get('programme'))
        branch = str(request.form.get('branch'))
        section = str(request.form.get('section'))
        username = str(request.form.get('username'))
        hostel = str(request.form.get('hostel'))
        f = open("./data/user_data/{}.bin".format(rollno), "wb")
        content = [[], []]  #[[following], [followers]]
        pickle.dump(content, f)
        f.close()
        if database.check_signup(name, rollno, password1, password2, gender, programme, branch, section, username, hostel)[0]:
            return render_template('signup_success.html')
        else:
            return database.check_signup(name, rollno, password1, password2, gender, programme, branch, section, username, hostel)[1]


@app.route('/logout', methods=["POST", "GET"])
def logout():
    if request.method == 'GET':
        res = make_response(redirect('./login'))
        res.set_cookie('login_status', "false")
        res.set_cookie('login_rollno', '')
        res.set_cookie('login_username', '')
        return res

@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")
    if request.method == "POST":
        rollno = request.form.get('rollno')
        f = open('./data/otp.bin', "wb")
        otp = str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        print(otp)
        pickle.dump([rollno, otp], f)
        f.close()
        email_bot.send_otp(str(rollno)+"@nitt.edu", otp)
        return render_template("forgot_password_step_2.html")

@app.route('/forgot_password/otp_accepted', methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template('forgot_password_Step_2.html')
    if request.method == "POST":
        f = open("./data/otp.bin", 'rb')
        rollno, given_otp = list(pickle.load(f))
        f.close()
        otp = request.form.get('otp')
        newpassword1 = request.form.get('newpassword1')
        newpassword2 = request.form.get('newpassword2')
        if otp == given_otp and newpassword1 == newpassword2:
            database.put_login_info(rollno, newpassword1)
            return render_template('password_changed.html')
        else:
            return "error"



@app.route('/my_profile', methods=["POST", "GET"])
def my_profile():
    return render_template('my_profile.html')


@app.route('/settings', methods=["POST", "GET"])
def settings():
    return render_template('settings.html')








   
if __name__ == '__main__':
    app.run(port='5000')