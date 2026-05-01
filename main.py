from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import SessionLocal, User, Profile
from pydantic import BaseModel
import json
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = "super_secret_key_for_mvp"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 1 week


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str

class ProfileUpdate(BaseModel):
    skin_type: str
    concerns: str
    budget: str

class BoxOrder(BaseModel):
    items: list
    city: str
    address: str
    phone: str

# API Routes
@app.post("/api/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create empty profile
    new_profile = Profile(user_id=new_user.id, skin_type="", concerns="", budget="", active_subscription=0, box_history="[]")
    db.add(new_profile)
    db.commit()
    return {"msg": "User created successfully"}

@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    to_encode = {"sub": user.email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@app.get("/api/me")
def read_users_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    return {
        "email": current_user.email,
        "profile": {
            "skin_type": profile.skin_type if profile else "",
            "concerns": profile.concerns if profile else "",
            "budget": profile.budget if profile else "",
            "active_subscription": profile.active_subscription if profile else 0,
            "box_history": profile.box_history if profile else "[]"
        }
    }

@app.post("/api/profile")
def update_profile(profile_data: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile:
        profile.skin_type = profile_data.skin_type
        profile.concerns = profile_data.concerns
        profile.budget = profile_data.budget
        db.commit()
    return {"msg": "Profile updated successfully"}

@app.post("/api/order_box")
def order_box(order_data: BoxOrder, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Profile not found")
    
    # Generate an order record
    try:
        history = json.loads(profile.box_history)
    except:
        history = []
        
    new_order = {
        "date": datetime.now().strftime("%d %B %Y"),
        "items": order_data.items,
        "city": order_data.city,
        "address": order_data.address,
        "phone": order_data.phone
    }
    history.insert(0, new_order) # pre-pend new box
    
    profile.active_subscription = 1
    profile.box_history = json.dumps(history)
    db.commit()
    
    return {"msg": "Box ordered successfully"}


# Mount static files
if os.path.exists("public/css"):
    app.mount("/css", StaticFiles(directory="public/css"), name="css")
if os.path.exists("public/js"):
    app.mount("/js", StaticFiles(directory="public/js"), name="js")
if os.path.exists("public/images"):
    app.mount("/images", StaticFiles(directory="public/images"), name="images")

# Serve HTML files
@app.get("/")
def read_index():
    return FileResponse("public/index.html")

@app.get("/login")
def read_login():
    return FileResponse("public/login.html")

@app.get("/dashboard")
def read_dashboard():
    return FileResponse("public/dashboard.html")

@app.get("/terms")
def read_terms():
    return FileResponse("public/terms.html")

@app.get("/privacy")
def read_privacy():
    return FileResponse("public/privacy.html")

@app.get("/blog")
def read_blog():
    return FileResponse("public/blog.html")

@app.get("/history")
def read_history():
    return FileResponse("public/history.html")

@app.get("/rules")
def read_rules():
    return FileResponse("public/rules.html")

@app.get("/contacts")
def read_contacts():
    return FileResponse("public/contacts.html")

