from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from models.image import ImageFeed

# aws necessity
from instagram_web.util.helpers import unique_filename, upload_file_to_s3
from config import S3_BUCKET


images_blueprint = Blueprint('images', __name__, template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')


@images_blueprint.route('/', methods=['POST'])
@login_required
def create():

    # if no files entered, show warning
    if 'new_image' not in request.files:
        flash('Please provide a picture to brag !', 'text-warning')
        return redirect(url_for('images.new'))

    # take in image & caption argument from user
    file = request.files['new_image']
    enterred_caption = request.form['image_caption']

    # if wrong kind of file being provided, show warning
    if not file or file.filename == "":
        flash('Please provide an image file, not any other kind of file', 'text-warning')
        return redirect(url_for('images.new'))

    # enforce caption
    if not len(enterred_caption) > 0:
        flash('Provide a caption! you cannot brag without any caption!', 'text-warning')
        return redirect(url_for('images.new'))

    # upload post picture to AWS
    file.filename = unique_filename(file)
    uploaded_picture = upload_file_to_s3(file, S3_BUCKET)
    # breakpoint()

    # if not uploaded to aws, show warning
    if not uploaded_picture:
        flash('There are issue in uploading the picture to server (AWS), should be okay now. try again!', 'text-danger')
        return redirect(url_for('images.new'))

    new_feed = ImageFeed(
        logged_in_user=current_user.id,
        picture_name=file.filename,
        caption=enterred_caption
    )

    new_feed.save()

    # if new_feed not uploaded to psql, show warning
    if not new_feed:
        flash('Unable to create new post, check your internet connection! ', 'text-danger')
        return redirect(url_for('images.new'))

    # flash `upload success` & take user to `home`
    flash('New post has been successfully created!', 'text-success')
    return redirect(url_for('home'))
