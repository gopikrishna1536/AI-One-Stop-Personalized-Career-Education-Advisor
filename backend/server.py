from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
import random
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'edupath_india')]

JWT_SECRET = os.environ.get('JWT_SECRET', 'edupath_india_secret_key_2026')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_DAYS = int(os.environ.get('JWT_EXPIRATION_DAYS', 30))
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

app = FastAPI()
api_router = APIRouter(prefix="/api")
security = HTTPBearer()

class UserRegister(BaseModel):
    full_name: str
    gender: str
    date_of_birth: str
    mobile_number: str
    email: EmailStr
    password: str
    state: str
    district: str
    location_type: str
    category: Optional[str] = None
    current_class: str
    board: str
    medium_of_instruction: str
    marks_percentage: Optional[float] = None
    subjects_studied: List[str]
    preferred_stream: Optional[str] = None
    preferred_language: str = "english"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

class ResetPassword(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class ChatMessage(BaseModel):
    message: str
    language: str = "english"

class CollegeFilter(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    stream: Optional[str] = None
    course: Optional[str] = None

class College(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    state: str
    district: str
    university_affiliation: str
    courses_offered: List[str]
    streams: List[str]
    entrance_exam: Optional[str] = None
    cutoff_marks: Optional[Dict[str, float]] = None
    hostel_facility: bool = False
    medium_of_instruction: List[str]
    website: Optional[str] = None
    contact: Optional[str] = None

class TimelineEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    event_date: str
    event_type: str
    stream: Optional[str] = None
    target_class: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_id: str, email: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRATION_DAYS)
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': expiration
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@api_router.post("/auth/register")
async def register(user_data: UserRegister):
    existing_user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user_data.model_dump()
    user_dict['id'] = str(uuid.uuid4())
    user_dict['password'] = hash_password(user_data.password)
    user_dict['email_verified'] = False
    user_dict['created_at'] = datetime.now(timezone.utc).isoformat()
    user_dict['role'] = 'student'
    
    otp = str(random.randint(100000, 999999))
    user_dict['otp'] = otp
    user_dict['otp_expires'] = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
    
    await db.users.insert_one(user_dict)
    
    print(f"OTP for {user_data.email}: {otp}")
    
    token = create_jwt_token(user_dict['id'], user_data.email)
    
    return {
        "message": "Registration successful. OTP sent to email.",
        "token": token,
        "user": {
            "id": user_dict['id'],
            "email": user_data.email,
            "full_name": user_data.full_name,
            "email_verified": False
        },
        "otp_for_demo": otp
    }

@api_router.post("/auth/login")
async def login(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not verify_password(credentials.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_jwt_token(user['id'], user['email'])
    
    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "full_name": user['full_name'],
            "email_verified": user.get('email_verified', False),
            "role": user.get('role', 'student'),
            "preferred_language": user.get('preferred_language', 'english')
        }
    }

@api_router.post("/auth/send-otp")
async def send_otp(request: OTPRequest):
    user = await db.users.find_one({"email": request.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    otp = str(random.randint(100000, 999999))
    await db.users.update_one(
        {"email": request.email},
        {"$set": {
            "otp": otp,
            "otp_expires": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
        }}
    )
    
    print(f"OTP for {request.email}: {otp}")
    
    return {"message": "OTP sent successfully", "otp_for_demo": otp}

@api_router.post("/auth/verify-otp")
async def verify_otp(request: OTPVerify):
    user = await db.users.find_one({"email": request.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.get('otp') != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    otp_expires = datetime.fromisoformat(user.get('otp_expires', datetime.now(timezone.utc).isoformat()))
    if datetime.now(timezone.utc) > otp_expires:
        raise HTTPException(status_code=400, detail="OTP expired")
    
    await db.users.update_one(
        {"email": request.email},
        {"$set": {"email_verified": True}, "$unset": {"otp": "", "otp_expires": ""}}
    )
    
    return {"message": "Email verified successfully"}

@api_router.post("/auth/reset-password")
async def reset_password(request: ResetPassword):
    user = await db.users.find_one({"email": request.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.get('otp') != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    otp_expires = datetime.fromisoformat(user.get('otp_expires', datetime.now(timezone.utc).isoformat()))
    if datetime.now(timezone.utc) > otp_expires:
        raise HTTPException(status_code=400, detail="OTP expired")
    
    hashed_password = hash_password(request.new_password)
    await db.users.update_one(
        {"email": request.email},
        {"$set": {"password": hashed_password}, "$unset": {"otp": "", "otp_expires": ""}}
    )
    
    return {"message": "Password reset successfully"}

@api_router.get("/user/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

@api_router.put("/user/profile")
async def update_profile(updates: Dict[str, Any], current_user: dict = Depends(get_current_user)):
    allowed_fields = ['full_name', 'mobile_number', 'state', 'district', 'current_class', 
                      'marks_percentage', 'subjects_studied', 'preferred_stream', 'preferred_language']
    
    update_data = {k: v for k, v in updates.items() if k in allowed_fields}
    
    if update_data:
        await db.users.update_one({"id": current_user['id']}, {"$set": update_data})
    
    updated_user = await db.users.find_one({"id": current_user['id']}, {"_id": 0, "password": 0})
    return {"message": "Profile updated successfully", "user": updated_user}

@api_router.post("/chatbot/message")
async def chat_with_bot(message: ChatMessage, current_user: dict = Depends(get_current_user)):
    try:
        session_id = f"user_{current_user['id']}_session"
        
        system_message = f"""
You are an AI Career Guidance Assistant for Indian students called 'EduPath AI'. 
You help students after Class 10 and 12 choose the right stream, degree, and government college.

User Info:
- Name: {current_user.get('full_name', 'Student')}
- Class: {current_user.get('current_class', 'Not specified')}
- Board: {current_user.get('board', 'Not specified')}
- Subjects: {', '.join(current_user.get('subjects_studied', []))}
- Marks: {current_user.get('marks_percentage', 'Not specified')}%
- Preferred Stream: {current_user.get('preferred_stream', 'Not decided')}
- State: {current_user.get('state', 'India')}

Your role:
1. Ask about interests, strengths, and career goals
2. Recommend streams (Science/Commerce/Arts)
3. Suggest specific degrees (B.Tech, MBBS, B.Com, BA, etc.)
4. Recommend Indian Government Colleges (IITs, NITs, Delhi University, Anna University, etc.)
5. Provide career roadmaps with government jobs, private sector, and competitive exams
6. Be conversational, encouraging, and culturally aware

Communicate in {message.language}.
"""
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=system_message
        ).with_model("gemini", "gemini-3-flash-preview")
        
        user_message = UserMessage(text=message.message)
        response = await chat.send_message(user_message)
        
        chat_record = {
            "id": str(uuid.uuid4()),
            "user_id": current_user['id'],
            "user_message": message.message,
            "bot_response": response,
            "language": message.language,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.chat_history.insert_one(chat_record)
        
        return {"response": response, "timestamp": chat_record['timestamp']}
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")

@api_router.get("/chatbot/history")
async def get_chat_history(current_user: dict = Depends(get_current_user)):
    history = await db.chat_history.find(
        {"user_id": current_user['id']},
        {"_id": 0}
    ).sort("timestamp", 1).limit(50).to_list(50)
    return {"history": history}

@api_router.get("/colleges")
async def get_colleges(state: Optional[str] = None, district: Optional[str] = None, 
                       stream: Optional[str] = None, course: Optional[str] = None):
    query = {}
    if state:
        query['state'] = state
    if district:
        query['district'] = district
    if stream:
        query['streams'] = stream
    if course:
        query['courses_offered'] = course
    
    colleges = await db.colleges.find(query, {"_id": 0}).limit(100).to_list(100)
    return {"colleges": colleges, "count": len(colleges)}

@api_router.get("/colleges/{college_id}")
async def get_college_detail(college_id: str):
    college = await db.colleges.find_one({"id": college_id}, {"_id": 0})
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    return {"college": college}

@api_router.get("/streams")
async def get_streams():
    streams = [
        {"id": "science", "name": "Science Stream", "icon": "flask"},
        {"id": "commerce", "name": "Commerce Stream", "icon": "chart-line"},
        {"id": "arts", "name": "Arts & Humanities", "icon": "palette"}
    ]
    return {"streams": streams}

@api_router.get("/degrees")
async def get_degrees(stream: Optional[str] = None):
    degrees_data = {
        "science": [
            {"id": "btech", "name": "B.Tech (Engineering)", "stream": "science"},
            {"id": "mbbs", "name": "MBBS (Medicine)", "stream": "science"},
            {"id": "bsc", "name": "B.Sc (Various specializations)", "stream": "science"},
            {"id": "bca", "name": "BCA (Computer Applications)", "stream": "science"},
            {"id": "nursing", "name": "B.Sc Nursing", "stream": "science"},
            {"id": "pharmacy", "name": "B.Pharm (Pharmacy)", "stream": "science"}
        ],
        "commerce": [
            {"id": "bcom", "name": "B.Com (Commerce)", "stream": "commerce"},
            {"id": "bba", "name": "BBA (Business Administration)", "stream": "commerce"},
            {"id": "ca", "name": "CA (Chartered Accountancy)", "stream": "commerce"},
            {"id": "cs", "name": "CS (Company Secretary)", "stream": "commerce"},
            {"id": "cma", "name": "CMA (Cost Management)", "stream": "commerce"}
        ],
        "arts": [
            {"id": "ba", "name": "BA (Arts)", "stream": "arts"},
            {"id": "ballb", "name": "BA-LLB (Law)", "stream": "arts"},
            {"id": "design", "name": "Design Courses", "stream": "arts"},
            {"id": "journalism", "name": "Journalism & Mass Communication", "stream": "arts"},
            {"id": "social_work", "name": "Social Work", "stream": "arts"}
        ]
    }
    
    if stream:
        return {"degrees": degrees_data.get(stream, [])}
    
    all_degrees = []
    for deg_list in degrees_data.values():
        all_degrees.extend(deg_list)
    return {"degrees": all_degrees}

@api_router.get("/career-path/{degree_id}")
async def get_career_path(degree_id: str):
    career_paths = {
        "btech": {
            "degree": "B.Tech (Engineering)",
            "government_jobs": ["ISRO Scientist", "DRDO Researcher", "Railway Engineer", "PWD Engineer"],
            "private_sector": ["Software Engineer", "Data Scientist", "Project Manager", "Technical Consultant"],
            "competitive_exams": ["GATE", "ESE", "UPSC (Engineering Services)", "State PSC"],
            "higher_studies": ["M.Tech", "MS abroad", "MBA", "PhD"],
            "entrepreneurship": ["Tech Startup", "Consulting Firm", "Product Development"],
            "avg_salary_range": "₹3-15 LPA",
            "growth_opportunities": "High demand in IT, Core Engineering, and Research sectors"
        },
        "mbbs": {
            "degree": "MBBS (Medicine)",
            "government_jobs": ["Government Hospital Doctor", "Medical Officer", "Army Medical Corps"],
            "private_sector": ["Hospital Physician", "Specialist Doctor", "Medical Consultant"],
            "competitive_exams": ["NEET PG", "UPSC (Medical Services)", "State Medical Services"],
            "higher_studies": ["MD/MS", "DNB", "Fellowship"],
            "entrepreneurship": ["Private Clinic", "Diagnostic Center", "Healthcare Startup"],
            "avg_salary_range": "₹6-20 LPA",
            "growth_opportunities": "Always in demand, respect in society, stable career"
        },
        "bcom": {
            "degree": "B.Com (Commerce)",
            "government_jobs": ["Bank PO", "Income Tax Inspector", "Accountant in PSU"],
            "private_sector": ["Accountant", "Financial Analyst", "Tax Consultant", "Auditor"],
            "competitive_exams": ["CA", "CS", "UPSC", "Banking Exams", "SSC CGL"],
            "higher_studies": ["M.Com", "MBA (Finance)", "CA", "CS"],
            "entrepreneurship": ["Tax Consultancy", "Audit Firm", "Financial Services"],
            "avg_salary_range": "₹2.5-10 LPA",
            "growth_opportunities": "Strong foundation for finance and accounting careers"
        },
        "ba": {
            "degree": "BA (Arts)",
            "government_jobs": ["IAS/IPS Officer", "State Civil Services", "Teaching", "Administrative Officer"],
            "private_sector": ["Content Writer", "HR Manager", "Journalist", "Social Worker"],
            "competitive_exams": ["UPSC", "State PSC", "NET/SET", "SSC"],
            "higher_studies": ["MA", "M.Phil", "PhD", "MBA", "LLB"],
            "entrepreneurship": ["NGO", "Content Agency", "Training Institute"],
            "avg_salary_range": "₹2-8 LPA",
            "growth_opportunities": "Diverse career options in civil services, teaching, media"
        }
    }
    
    path = career_paths.get(degree_id, {
        "degree": "Career path information",
        "government_jobs": ["Various government positions"],
        "private_sector": ["Multiple opportunities"],
        "competitive_exams": ["Relevant exams"],
        "higher_studies": ["Advanced degrees"],
        "entrepreneurship": ["Business opportunities"],
        "avg_salary_range": "Varies",
        "growth_opportunities": "Good potential"
    })
    
    return {"career_path": path}

@api_router.get("/timeline/events")
async def get_timeline_events(current_user: dict = Depends(get_current_user)):
    user_class = current_user.get('current_class', '')
    user_stream = current_user.get('preferred_stream', '')
    
    query = {"$or": [
        {"target_class": user_class},
        {"stream": user_stream},
        {"target_class": None, "stream": None}
    ]}
    
    events = await db.timeline_events.find(query, {"_id": 0}).sort("event_date", 1).limit(50).to_list(50)
    return {"events": events}

@api_router.post("/admin/colleges")
async def create_college(college: College, current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    college_dict = college.model_dump()
    await db.colleges.insert_one(college_dict)
    return {"message": "College added successfully", "college": college_dict}

@api_router.post("/admin/timeline")
async def create_timeline_event(event: TimelineEvent, current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    event_dict = event.model_dump()
    event_dict['created_at'] = event_dict['created_at'].isoformat()
    await db.timeline_events.insert_one(event_dict)
    return {"message": "Event added successfully", "event": event_dict}

@api_router.get("/admin/analytics")
async def get_analytics(current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    total_users = await db.users.count_documents({"role": "student"})
    total_colleges = await db.colleges.count_documents({})
    total_chats = await db.chat_history.count_documents({})
    
    stream_distribution = {}
    async for user in db.users.find({"preferred_stream": {"$exists": True}}, {"_id": 0, "preferred_stream": 1}):
        stream = user.get('preferred_stream', 'undecided')
        stream_distribution[stream] = stream_distribution.get(stream, 0) + 1
    
    return {
        "total_users": total_users,
        "total_colleges": total_colleges,
        "total_chats": total_chats,
        "stream_distribution": stream_distribution
    }

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

@app.on_event("startup")
async def seed_initial_data():
    colleges_count = await db.colleges.count_documents({})
    if colleges_count == 0:
        sample_colleges = [
            {
                "id": str(uuid.uuid4()),
                "name": "IIT Madras",
                "state": "Tamil Nadu",
                "district": "Chennai",
                "university_affiliation": "Autonomous",
                "courses_offered": ["B.Tech", "M.Tech", "PhD"],
                "streams": ["science"],
                "entrance_exam": "JEE Advanced",
                "cutoff_marks": {"General": 95.0, "OBC": 92.0, "SC/ST": 85.0},
                "hostel_facility": True,
                "medium_of_instruction": ["English"],
                "website": "https://www.iitm.ac.in",
                "contact": "+91-44-22574000"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Delhi University",
                "state": "Delhi",
                "district": "Delhi",
                "university_affiliation": "Central University",
                "courses_offered": ["B.Sc", "B.Com", "BA", "BCA"],
                "streams": ["science", "commerce", "arts"],
                "entrance_exam": "CUET",
                "cutoff_marks": {"General": 88.0, "OBC": 85.0, "SC/ST": 78.0},
                "hostel_facility": True,
                "medium_of_instruction": ["English", "Hindi"],
                "website": "https://www.du.ac.in",
                "contact": "+91-11-27667725"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "AIIMS Delhi",
                "state": "Delhi",
                "district": "Delhi",
                "university_affiliation": "Autonomous",
                "courses_offered": ["MBBS", "B.Sc Nursing"],
                "streams": ["science"],
                "entrance_exam": "NEET",
                "cutoff_marks": {"General": 99.5, "OBC": 98.0, "SC/ST": 95.0},
                "hostel_facility": True,
                "medium_of_instruction": ["English"],
                "website": "https://www.aiims.edu",
                "contact": "+91-11-26588500"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Anna University",
                "state": "Tamil Nadu",
                "district": "Chennai",
                "university_affiliation": "State University",
                "courses_offered": ["B.Tech", "B.E", "M.Tech"],
                "streams": ["science"],
                "entrance_exam": "TNEA",
                "cutoff_marks": {"General": 85.0, "OBC": 80.0, "SC/ST": 70.0},
                "hostel_facility": True,
                "medium_of_instruction": ["English", "Tamil"],
                "website": "https://www.annauniv.edu",
                "contact": "+91-44-22351001"
            }
        ]
        await db.colleges.insert_many(sample_colleges)
        logger.info("Sample colleges seeded")
    
    events_count = await db.timeline_events.count_documents({})
    if events_count == 0:
        sample_events = [
            {
                "id": str(uuid.uuid4()),
                "title": "JEE Main Registration Opens",
                "description": "Registration for JEE Main 2026 begins",
                "event_date": "2026-02-15",
                "event_type": "exam_registration",
                "stream": "science",
                "target_class": "12th",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "NEET Application Deadline",
                "description": "Last date to apply for NEET 2026",
                "event_date": "2026-03-01",
                "event_type": "application_deadline",
                "stream": "science",
                "target_class": "12th",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "CUET Registration",
                "description": "CUET registration for Delhi University and other central universities",
                "event_date": "2026-03-15",
                "event_type": "exam_registration",
                "stream": None,
                "target_class": "12th",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
        await db.timeline_events.insert_many(sample_events)
        logger.info("Sample timeline events seeded")