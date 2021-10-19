
@app.route('/posts', methods=['GET', 'POST'])
def posts_route():
    if request.method=='POST':
        post_title=request.form['title']
        post_content=request.form['content']
        post_author=request.form['author']
        new_post =BlogPost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        print('here')
        all_posts=BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('index.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post=BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>',methods=['POST','GET'])
def edit(id):
    if request.method=='POST':
        post=BlogPost.query.get_or_404(id)
        post.title=request.form['title']
        post.content=request.form['content']
        post.author=request.form['author']
        db.session.commit()
        return redirect('/posts')

    else:
        post=BlogPost.query.get_or_404(id)
        return render_template('edit.html',post=post)


@app.route('/posts/new',methods=['GET','POST'])
def new_post():
    if request.method=='POST':
        post=BlogPost.query.get_or_404(id)
        post.title=request.form['title']
        post.content=request.form['content']
        post.author=request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('newPost.html')
