from fastapi import APIRouter, Request, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.post import PostSchema, Post, Posts
from src.models.response import ServiceResponse
from src.routes.services.post import PostService

app = APIRouter()
service = PostService()


@app.get(
    "",
    name="Get all posts",
    responses={**ServiceResponse(Posts).multi("get_posts", obj="Post")},
)
def get_posts():
    try:

        # ? Get total of post, and the posts data
        count, posts = service.get_posts()

        # ? Check if posts is not empty
        if posts:

            # * Return 200 if posts is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all posts",
                    "total": count,
                    "data": posts.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if posts is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Posts not found"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all post",
        )


@app.get("/{id}", responses={**ServiceResponse(Post).get("get_post", obj="Post")})
def get_post(id: str = Path(..., description="Post id")):
    try:
        # ? Check if post is not empty
        if post := service.get_post(id):

            # * Return 200 if posts is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": post.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if post is empty, which means there is no post with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Post not found"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed get post"
        )


@app.post(
    "",
    status_code=201,
    responses={**ServiceResponse(Post).creation("add_post", obj="Post")},
)
def add_post(data: PostSchema):
    try:
        post = service.add_post(data)

        # * Return 201, and the post
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Post created successfully",
                "data": post.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed add post"
        )


@app.put("/{id}", responses={**ServiceResponse(Post).update("update_post", obj="Post")})
def update_post(data: PostSchema, id: str = Path(..., description="Post id")):
    try:
        # ? Check if post is updated successfully
        if service.update_post(id, data):

            # * Return 200, and id of the post
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Post updated successfully", "id": id},
            )

        # ! Return 404 if updated is return 0, which means there is no post with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Post not found"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed add post"
        )


@app.delete(
    "/{id}", responses={**ServiceResponse(Post).delete("delete_post", obj="Post")}
)
def delete_post(id: str = Path(..., description="Post id")):
    try:
        # ? Check if post is deleted successfully
        if service.delete_post(id):

            # * Return 200, and id of the post
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Post deleted successfully", "id": id},
            )

        # ! Return 404 if deleted is return 0, which means there is no post with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Post not found"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed add post"
        )
