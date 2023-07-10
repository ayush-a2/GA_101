from flask import Flask, request, jsonify

app = Flask(__name__)

posts = []
post_id_counter = 1


@app.route('/post', methods=['POST'])
def create_post():
    global post_id_counter
    
    data = request.get_json()
    username = data.get('username')
    caption = data.get('caption')
    
    if not username or not caption:
        return jsonify({'error': 'Username and caption are required.'}), 400
    
    post = {
        'id': post_id_counter,
        'username': username,
        'caption': caption,
        'likes': 0,
        'comments': []
    }
    
    posts.append(post)
    post_id_counter += 1
    
    return jsonify({'message': 'Post created successfully.', 'post': post}), 201


@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify({'posts': posts})


@app.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if not post:
        return jsonify({'error': 'Post not found.'}), 404
    
    posts.remove(post)
    
    return jsonify({'message': 'Post deleted successfully.'})


@app.route('/post/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if not post:
        return jsonify({'error': 'Post not found.'}), 404
    
    post['likes'] += 1
    
    return jsonify({'message': 'Post liked successfully.'})

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def comment_on_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if not post:
        return jsonify({'error': 'Post not found.'}), 404
    
    data = request.get_json()
    comment = data.get('comment')
    
    if not comment:
        return jsonify({'error': 'Comment is required.'}), 400
    
    post['comments'].append(comment)
    
    return jsonify({'message': 'Comment added successfully.'})

if __name__ == '__main__':
    app.run()
