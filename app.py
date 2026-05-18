from flask import Flask, render_template, request, redirect, url_for
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
cloudinary.config(
    cloud_name="ddt9zxomn",
    api_key="927452581847582",
    api_secret="hGXneLpLoM6o0OBHXwb6pyChbVM"
)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        file = request.files['image']

        if file:
            upload_result = cloudinary.uploader.upload(file)
            

            cloud_link = upload_result['secure_url']

            print("Cloud Image URL:", cloud_link)

            with open("cloud_links.txt", "a") as f:
                f.write(file.filename + "|" + cloud_link + "\n")

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            file.seek(0)

            file.save(filepath)
            

    search = request.args.get('search')

    images = os.listdir(app.config['UPLOAD_FOLDER'])

    if search:
        images = [img for img in images if search.lower() in img.lower()]

    cloud_urls = {}

    if os.path.exists("cloud_links.txt"):

        with open("cloud_links.txt", "r") as f:

            for line in f:

                name, url = line.strip().split("|")

                cloud_urls[name] = url
    return render_template('index.html',
                           images=images,
                           search=search,
                           total=len(images),
                            cloud_urls=cloud_urls)

@app.route('/delete/<filename>')
def delete_image(filename):

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)