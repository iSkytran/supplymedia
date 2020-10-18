from flask import Flask, request, redirect, render_template, url_for
import gridfs, random, uuid, os
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
            # static_url_path = '',
            # static_folder = 'static',
            # template_folder = 'templates')

photos = UploadSet('photos', IMAGES)
app.config['UPLOAD_FOLDER'] = 'images_store'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# SQL form items
class PostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80), unique=False, nullable=False)
    storeItem = db.Column(db.String(80), unique=False, nullable=False)
    avalability = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<ID %r>' % self.id

db.create_all()
# post = PostItem(name="John", storeItem="Hand Sanatizer", avalability="Avaliable")
# db.session.add(post)
# db.session.commit()
# print(PostItem.query.all())

# Render webpages
@app.route("/")
def render_index():
    return render_template("index.html")

@app.route("/upload", methods=['GET', 'POST'])
def render_upload():

    # Get form data
    if request.method == 'POST':

        # Check if the form is empty
        if 'photo' not in request.files:
            return 'there is no photo in form'

        if '--------' == request.form.get('storeItem'):
            return 'no store item selected'

        if '' == request.form.get('radio'):
            return 'none selected'

        # Save to database
        post = PostItem(storeItem = request.form.get('storeItem'), avalability = request.form.get('radio'))
        db.session.add(post)
        db.session.commit()

        # Save the photo in the upload folder
        photo = request.files['photo']
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(post.id))
        photo.save(path)

        # Print test
        print(str(post.id) + post.storeItem + post.avalability)

        return redirect(url_for('render_index'))

    return render_template("upload.html")
