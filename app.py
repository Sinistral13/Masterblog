import json
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


def load_posts():
    """Load posts from a .json file."""
    with open('posts.json', 'r') as file:
        return json.load(file)


def save_posts(posts):
    """Save posts to a .json file."""
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    """Render index page."""
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Render add page.
    Shows a form for input the post data
    and a button to save the data.
    """
    if request.method == 'POST':
        blog_posts = load_posts()

        new_post = {
            "id": max([post["id"] for post in blog_posts], default=0) + 1,
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "content": request.form.get("content")
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Delete post on index page.
    Redirecting back to updated index page instead of blank delete page.
    """
    with open('posts.json', 'r') as file:
        posts = json.load(file)

    posts = [post for post in posts if post['id'] != post_id]

    with open('posts.json', 'w') as file:
        json.dump(posts, file)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update post on index page.
    Redirect to update page with same form as add page.
    redirect to index page after updating
    """
    with open('posts.json', 'r') as file:
        posts = json.load(file)

    post = next((post for post in posts if post['id'] == post_id), None)

    #not possible in this structure, added for scaling
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        with open('posts.json', 'w') as file:
            json.dump(posts, file)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
