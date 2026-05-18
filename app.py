from flask import Flask, render_template, request, redirect
from supabase import create_client, Client
import os

app = Flask(__name__)

# Supabase Config
url = "https://tjzxyupwbhwkkccxulwj.supabase.co"
key = "sb_publishable_zAGtAuYOhsdW6tMcWmC0qA_axxjvXyy"

supabase: Client = create_client(url, key)

BUCKET_NAME = "gallery"

@app.route('/', methods=['GET', 'POST'])
def home():

    # Upload Image
    if request.method == 'POST':

        file = request.files['image']

        if file:

            file_data = file.read()

            supabase.storage.from_(BUCKET_NAME).upload(
                file.filename,
                file_data,
                {"content-type": file.content_type}
            )

        return redirect('/')

    # Get Images
    files = supabase.storage.from_(BUCKET_NAME).list()

    image_urls = []

    for file in files:

        filename = file['name']

        image_url = f"{url}/storage/v1/object/public/{BUCKET_NAME}/{filename}"

        image_urls.append({
            "name": filename,
            "url": image_url
        })

    return render_template(
        'index.html',
        images=image_urls,
        total=len(image_urls)
    )

@app.route('/delete/<filename>')
def delete_image(filename):

    supabase.storage.from_(BUCKET_NAME).remove([filename])

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)