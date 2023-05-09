from flask import Flask, render_template, request, redirect, flash, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
from werkzeug.utils import secure_filename
from PIL import Image
import  base64

app = Flask(__name__)
app.secret_key = "thisissecretkey"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db=SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin,db.Model):
    id = db.Column('users_id', db.Integer, primary_key = True)
    usr_name = db.Column(db.String(100),nullable=True)
    fname = db.Column(db.String(100),nullable=True)
    lname = db.Column(db.String(100),nullable=True)
    em = db.Column(db.String(100),nullable=True)
    pswd = db.Column(db.String(100),nullable=True)

    def __str__(self):
        return self.fname
    
    
#image tabale
class Image(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Pic Name: {self.name}'

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)

@app.route("/")
@app.route("/home")
def main():
    all_photos = Image.query.all()
    img = Image.query.filter_by()
    print("...")
    print(img)
    print(".....")

    d={"all_photos":all_photos}
    print(d["all_photos"])
    return render_template('main.html',d=d)



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":

        # getting all data from UI
        uname=request.form.get('uname')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')
        paswd=request.form.get('paswd')

        #adding to database
        all_users = Users(usr_name=uname, fname=fname, lname=lname, em=email, pswd=paswd)
        db.session.add(all_users)
        db.session.commit()


        flash('user has been registered successfully ', 'success')
        return redirect("/login")


    return render_template('register.html')

@app.route('/login',methods=["GET","POST"])
def index():
    if request.method =="POST":
        uname=request.form.get('uname')
        paswd=request.form.get('paswd')

        all_user = Users.query.filter_by(usr_name=uname,pswd=paswd).first()
        print("#############################")
        print(all_user)
        print("#############################")
        if all_user:
            login_user(all_user)
            return redirect('/home')
        else:
            flash("invaild user and Password","warning")
    

    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/home')


# uploading files to database
@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "POST":

        pic= request.files['pic']
        # allpic= Image.query.all()

        if not pic:
            flash("no pic uploaded.","warning")
            return redirect("/upload")
        
        # flash("pic uploaded.","success")
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        img = Image(img=pic.read(),mimetype=mimetype,name=filename)
        db.session.add(img)

        try:
            db.session.commit()
        except:
            flash("pic shoud  be diffErent...","warning")
            return redirect("/upload")
        else:
            db.session.commit()
            flash("pic uploaded.","success")
        # return redirect("/home")
            
    return render_template('post.html')

@app.route('/photos')
def photos():
    return redirect("/home")

@app.route("/pic/<int:id>",methods=["GET","POST"])
def pic(id):

    img= Image.query.filter_by(id=id).first()
    print("************")
    print(img)
    print("****************")
    if not id:
        flash("no pic uploaded.","warning")
        return redirect("/upload")
    # else:
    #     return Response(img.img,mimetype=img.mimetype)
    encoded_image = base64.b64encode(img.img).decode('utf-8')

    return render_template('pic.html',img=encoded_image)

if __name__ == "__main__":
    app.run(debug=True)