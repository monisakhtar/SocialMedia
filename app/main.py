from fastapi import FastAPI
from fastapi import Path, status, HTTPException, Response
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title" : "New_post1", "content" : "Post number 1", "id": 1},
            {"title" : "New_post2", "content" : "Post number 2", "id": 2}]

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for ind, p in enumerate(my_posts):
        if p['id'] == id:
            return ind

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating : Optional[int] = None

@app.get("/")
def root():
    return {"message": "Welcome To My API!!"}

@app.get("/items/")
async def read_item(xskip: int = 0, limit: int = 10, xlimit: int = 10):
    return xskip
    # return fake_items_db[xskip : xskip + limit]

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0, 1000)
    my_posts.append(post_dict)
    print(my_posts)
    # return {"new_post": f"title : {new_post.title}, content : {new_post.content}"}
    return 

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id : {id} not found")
    print(id)
    return {"post" : post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    ind = find_index_post(id)
    if not ind:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id : {id} not found")
    else:
        my_posts.pop(ind)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    post_dict = post.model_dump()
    ind = find_index_post(id)
    if not ind:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id : {id} not found")
    else:
        post_dict['id'] = id
        my_posts[ind] = post_dict

    return {"updated post" : post_dict}