from fastapi import FastAPI
from routers import user, post, comment, category, admin, media_library, authentication

 
app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(category.router)
app.include_router(admin.router)
app.include_router(media_library.router)
app.include_router(authentication.router)



 

    



