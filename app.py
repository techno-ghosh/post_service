from flask import Flask, request ,jsonify
import requests
import json

app = Flask(__name__)

posts = {
        '1': {'user_id': '1', 'post': 'Hello, world!'},
        '2': {'user_id': '2', 'post': 'My first blog post'}
    }

@app.route('/')
def hello():
    print('hello')
    return posts


# READ OPERATION

@app.route('/post/<id>')
def post(id):
   
    post_info = posts.get(id, {})
    
    # Get user info from User Service
    if post_info:

        response = requests.get(f'http://localhost:5000/user/{post_info["user_id"]}')
        
        if response.status_code == 200:
            post_info['user'] = response.json()

        return jsonify(post_info)
    else:
        return 'Post not found',404

# CREATE OPERATION
@app.route('/post/add',methods=['POST'])
def create():
    post = request.json['post']
    user_id = request.json['user_id']
    
    response = requests.get(f'http://localhost:5000/user/{user_id}')
    
    if response.status_code != 200:
        return 'User not found',404
    
    new_key = int(sorted(posts.keys())[-1]) + 1

    posts[f'{new_key}'] = {
        "user_id" : user_id,
        "post" : post
    }
    return jsonify(posts)


# UPDATE OPERATION
@app.route('/post/update_post', methods=['PUT', 'POST'])
def update():
    if(request.method == 'POST' or request.method == 'PUT'):
        
        if(posts.get(str(request.json['post_id']), {})):
        
            post_text = request.json['post_text']
            user_id = request.json['user_id']
            post_id = request.json['post_id']
                

            posts[f'{post_id}'] = {
                "user_id" : user_id,
                "post" : post_text,
                "post_id" : post_id
            }
            return posts[f'{post_id}']
        else: 
            return "post not found"
    else:
        return 'method not allowed',403

# DELETE OPERATION

@app.route('/post/delete_post', methods=['DELETE'])
def delete():
    
   
    if(request.method == 'DELETE'):
        
        if(posts.get(str(request.json['post_id']), {})):
            
            posts.pop(str(request.json['post_id']))        
            return {
                "message" : "post deleted",
                "remaninig_posts" : posts
            }
        else:
            return 'Post does not exist'
    else:
        return 'method not allowed',403



if __name__ == '__main__':
    app.run('0.0.0.0',port=5001)