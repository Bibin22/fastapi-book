from fastapi import FastAPI, Depends, Request, HTTPException, UploadFile, File, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import schemas
import models
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256

Base.metadata.create_all(engine)
import aiofiles
from fastapi.security import OAuth2PasswordBearer


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# for creating end users
def create_user(db_session, form):
    hashed_password = pbkdf2_sha256.hash(form.password)

    user_orm = models.User(name=form.name, username=form.username, email=form.email, phone=form.phone, admin_user=False,
                           password=hashed_password)
    db_session.add(user_orm)
    db_session.commit()
    return user_orm


# for creating admin users
def create_admin(db_session, form):
    hashed_password = pbkdf2_sha256.hash(form.password)

    user_orm = models.User(name=form.name, username=form.username, email=form.email, phone=form.phone, admin_user=True,
                           password=hashed_password)
    db_session.add(user_orm)
    db_session.commit()
    return user_orm


def authenticate_user(db_session, username: str, password: str):
    user = db_session.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    return pbkdf2_sha256.verify(password, user.password)


app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


#####################################login paage ###############################

@app.get("/", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/", response_class=RedirectResponse)
def login(request: Request, form: schemas.LoginForm = Depends(schemas.LoginForm.as_form),
          db: Session = Depends(get_session)):
    # Validate the form and log the user in
    if authenticate_user(db, form.username, form.password):
        user = db.query(models.User).filter(models.User.username == form.username).first()
        if user.admin_user:
            books = db.query(models.Book).all()
            return templates.TemplateResponse("admin_book_list.html", {"request": request, "books": books})

    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")


######################### end user registration #####################

@app.get("/user_registration/", response_class=HTMLResponse)
def get_user_registration(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/user_registration/")
def add_user(request: Request, form: schemas.UserIn = Depends(schemas.UserIn.as_form),
             db: Session = Depends(get_session)):
    create_user(db, form)
    return templates.TemplateResponse("login.html", {"request": request})

############################## admin user registration #######################

@app.get("/admin_registration/", response_class=HTMLResponse)
def get_admin_registration(request: Request):
    return templates.TemplateResponse("admin_register.html", {"request": request})


@app.post("/admin_registration/")
def add_admin(request: Request, form: schemas.UserIn = Depends(schemas.UserIn.as_form),
              db: Session = Depends(get_session)):
    create_admin(db, form)
    return templates.TemplateResponse("login.html", {"request": request})


################################## book list ####################################

@app.get("/admin_book_list", response_class=HTMLResponse)
def get_book_list(request: Request, session: Session = Depends(get_session)):
    books = session.query(models.Book).all()
    return templates.TemplateResponse("admin_book_list.html", {"request": request, "books": books})

################################## Add Book ######################################
@app.get("/admin_book_add", response_class=HTMLResponse)
def get_add_book(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("admin_book_add.html", {"request": request})


@app.post("/admin_book_add", response_class=HTMLResponse)
def post_add_book(request: Request, form: schemas.BookForm = Depends(schemas.BookForm.as_form),
                        session: Session = Depends(get_session)):

    book = models.Book(book_name=form.book_name, author=form.author, prize=form.prize, description=form.description,
                    )
    session.add(book)
    session.commit()
    session.refresh(book)
    books = session.query(models.Book).all()
    return templates.TemplateResponse("admin_book_list.html", {"request": request, "books": books})


####################################### edit boook ##############################

@app.get("/admin_book_edit/{id}", response_class=HTMLResponse)
def get_admin_book_edit(request: Request, id: int, session: Session = Depends(get_session)):
    book = session.query(models.Book).get(id)
    return templates.TemplateResponse("admin_book_edit.html", {"request": request, "book": book, "id":id})


@app.put("/admin_book_edit/{id}", response_class=HTMLResponse)
def put_edit_book(request: Request, form: schemas.BookForm = Depends(schemas.BookForm.as_form),
                  session: Session = Depends(get_session)):
    book = session.query(models.Book).get(id)
    b = request.get('book_name')
    print(b, 'b')
    book.book_name = form.book_name
    book.author = form.author
    book.prize = form.prize
    book.description = form.description
    session.commit()
    books = session.query(models.Book).all()
    return templates.TemplateResponse("admin_book_list.html", {"request": request, "books": books})


##################### Delete book ########################################

@app.get("/admin_book_delete/{id}", response_class=HTMLResponse)
def admin_book_delete(request: Request, id: int, session: Session = Depends(get_session)):
    book = session.query(models.Book).get(id)
    session.delete(book)
    session.commit()
    session.close()
    books = session.query(models.Book).all()
    return templates.TemplateResponse("admin_book_list.html", {"request": request, "books": books})

####################### single book details ##############################

@app.get("/admin_book_detail/{id}", response_class=HTMLResponse)
def get_admin_book_detail(request: Request, id: int, session: Session = Depends(get_session)):
    book = session.query(models.Book).get(id)
    return templates.TemplateResponse("admin_book_details.html", {"request": request, "book": book})


###################### user home page ######################################
@app.get("/home", response_class=HTMLResponse)
def user_home(request: Request, session: Session = Depends(get_session)):
    books = session.query(models.Book).all()
    return templates.TemplateResponse("user_home.html", {"request": request, "books": books})

