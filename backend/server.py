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

class AptitudeTestAnswer(BaseModel):
    question_id: str
    selected_option: int

class AptitudeTestSubmission(BaseModel):
    answers: List[AptitudeTestAnswer]

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

@api_router.get("/aptitude-test/questions")
async def get_aptitude_questions(current_user: dict = Depends(get_current_user)):
    questions = await db.aptitude_questions.find({}, {"_id": 0}).to_list(100)
    return {"questions": questions}

@api_router.post("/aptitude-test/submit")
async def submit_aptitude_test(submission: AptitudeTestSubmission, current_user: dict = Depends(get_current_user)):
    questions = await db.aptitude_questions.find({}, {"_id": 0}).to_list(100)
    
    domain_scores = {
        "Science": 0,
        "Technology": 0,
        "Medical": 0,
        "Commerce": 0,
        "Arts": 0,
        "Government_Jobs": 0,
        "Entrepreneurship": 0
    }
    
    for answer in submission.answers:
        question = next((q for q in questions if q['id'] == answer.question_id), None)
        if question and 0 <= answer.selected_option < len(question['options']):
            selected_option = question['options'][answer.selected_option]
            if 'domains' in selected_option:
                for domain in selected_option['domains']:
                    if domain in domain_scores:
                        domain_scores[domain] += selected_option['domains'][domain]
    
    sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
    top_domains = sorted_domains[:3]
    
    career_suggestions = []
    college_recommendations = []
    coding_timeline = []
    roadmap = []
    
    primary_domain = top_domains[0][0]
    
    if primary_domain in ["Technology", "Science"]:
        career_suggestions = [
            {"title": "Software Engineer", "description": "Design and develop software applications", "salary": "₹6-25 LPA"},
            {"title": "Data Scientist", "description": "Analyze and interpret complex data", "salary": "₹8-30 LPA"},
            {"title": "Full Stack Developer", "description": "Build complete web applications", "salary": "₹5-20 LPA"},
            {"title": "AI/ML Engineer", "description": "Develop AI and machine learning models", "salary": "₹10-35 LPA"}
        ]
        
        college_recommendations = [
            {
                "name": "SRM University",
                "location": "Chennai, Tamil Nadu",
                "courses": ["B.Tech CSE", "B.Tech AI&ML", "B.Tech Data Science"],
                "ranking": "NIRF Ranked #26",
                "admission": "SRMJEEE",
                "fees": "₹2.5-3 Lakhs per year",
                "placements": "Average: ₹8 LPA, Highest: ₹42 LPA",
                "website": "https://www.srmist.edu.in"
            },
            {
                "name": "VIT Chennai",
                "location": "Chennai, Tamil Nadu",
                "courses": ["B.Tech CSE", "B.Tech IT", "B.Tech ECE", "B.Tech Mechanical"],
                "ranking": "NIRF Ranked #15",
                "admission": "VITEEE",
                "fees": "₹1.98 Lakhs per year",
                "placements": "Average: ₹7.5 LPA, Highest: ₹41.6 LPA",
                "website": "https://vit.ac.in"
            },
            {
                "name": "IIT Madras",
                "location": "Chennai, Tamil Nadu",
                "courses": ["B.Tech", "Dual Degree Programs"],
                "ranking": "NIRF Ranked #1",
                "admission": "JEE Advanced",
                "fees": "₹2 Lakhs per year",
                "placements": "Average: ₹16 LPA, Highest: ₹1.5 Cr",
                "website": "https://www.iitm.ac.in"
            },
            {
                "name": "Anna University",
                "location": "Chennai, Tamil Nadu",
                "courses": ["B.E/B.Tech in various specializations"],
                "ranking": "NIRF Ranked #18",
                "admission": "TNEA",
                "fees": "₹50,000-1 Lakh per year",
                "placements": "Average: ₹4.5 LPA",
                "website": "https://www.annauniv.edu"
            }
        ]
        
        coding_timeline = [
            {
                "week": "Week 1-2",
                "focus": "Basics & Setup",
                "topics": ["Programming fundamentals", "Data structures basics"],
                "platforms": ["CodeChef (Beginner problems)", "HackerRank"],
                "practice": "Solve 5 easy problems daily on CodeChef",
                "goal": "Build foundation"
            },
            {
                "week": "Week 3-4",
                "focus": "Arrays & Strings",
                "topics": ["Array manipulation", "String algorithms"],
                "platforms": ["CodeChef (Easy-Medium)", "LeetCode"],
                "practice": "3-4 medium problems daily",
                "goal": "Master basic data structures"
            },
            {
                "week": "Week 5-8",
                "focus": "Algorithms",
                "topics": ["Sorting", "Searching", "Recursion"],
                "platforms": ["CodeChef Long Challenge", "Codeforces"],
                "practice": "Participate in CodeChef contests",
                "goal": "Competitive programming basics"
            },
            {
                "week": "Week 9-12",
                "focus": "Advanced DS",
                "topics": ["Trees", "Graphs", "Dynamic Programming"],
                "platforms": ["CodeChef", "GeeksforGeeks"],
                "practice": "2-3 hard problems daily",
                "goal": "Advanced problem solving"
            }
        ]
        
        roadmap = [
            {
                "month": "Month 1",
                "title": "Foundation Building",
                "tasks": [
                    "Learn programming basics (Python/C++/Java)",
                    "Start CodeChef practice (Beginner level)",
                    "Study data structures fundamentals",
                    "Join online coding communities"
                ],
                "milestone": "Solve 50+ easy problems on CodeChef"
            },
            {
                "month": "Month 2",
                "title": "Core DSA",
                "tasks": [
                    "Deep dive into arrays, strings, linked lists",
                    "Practice on CodeChef and LeetCode",
                    "Start competitive programming",
                    "Build small projects"
                ],
                "milestone": "Participate in first CodeChef contest"
            },
            {
                "month": "Month 3",
                "title": "Algorithm Mastery",
                "tasks": [
                    "Study sorting and searching algorithms",
                    "Learn recursion and backtracking",
                    "Solve CodeChef Long Challenge problems",
                    "Work on portfolio projects"
                ],
                "milestone": "Achieve 2-star rating on CodeChef"
            },
            {
                "month": "Month 4",
                "title": "Advanced Topics",
                "tasks": [
                    "Master trees and graph algorithms",
                    "Introduction to dynamic programming",
                    "Participate in multiple contests",
                    "Start open-source contributions"
                ],
                "milestone": "Solve 200+ problems across platforms"
            },
            {
                "month": "Month 5",
                "title": "Specialization",
                "tasks": [
                    "Choose focus area (Web Dev/AI/Mobile)",
                    "Advanced DP and graph problems",
                    "Build major project",
                    "Prepare for internships"
                ],
                "milestone": "Complete one full-stack project"
            },
            {
                "month": "Month 6",
                "title": "Career Preparation",
                "tasks": [
                    "Mock interviews practice",
                    "System design basics",
                    "Resume building",
                    "Apply for internships/college admissions"
                ],
                "milestone": "Ready for placements/admissions"
            }
        ]
    
    elif primary_domain == "Medical":
        career_suggestions = [
            {"title": "Doctor (MBBS)", "description": "Practice medicine and treat patients", "salary": "₹8-25 LPA"},
            {"title": "Dentist (BDS)", "description": "Specialize in dental care", "salary": "₹6-20 LPA"},
            {"title": "Physiotherapist", "description": "Help patients with physical rehabilitation", "salary": "₹4-12 LPA"},
            {"title": "Medical Researcher", "description": "Conduct medical research", "salary": "₹6-18 LPA"}
        ]
        
        college_recommendations = [
            {
                "name": "AIIMS Delhi",
                "location": "Delhi",
                "courses": ["MBBS", "B.Sc Nursing"],
                "ranking": "Top Medical College in India",
                "admission": "NEET",
                "fees": "Minimal (Government college)",
                "placements": "Government appointments and private practice",
                "website": "https://www.aiims.edu"
            },
            {
                "name": "CMC Vellore",
                "location": "Vellore, Tamil Nadu",
                "courses": ["MBBS", "BDS", "B.Sc Nursing"],
                "ranking": "NIRF Ranked #3 (Medical)",
                "admission": "NEET",
                "fees": "₹85,000 per year",
                "placements": "Excellent hospital placements",
                "website": "https://www.cmch-vellore.edu"
            }
        ]
        
        roadmap = [
            {"month": "Month 1", "title": "NEET Preparation Start", "tasks": ["Join coaching", "NCERT mastery", "Biology focus"], "milestone": "Complete 20% syllabus"},
            {"month": "Month 2", "title": "Physics & Chemistry", "tasks": ["Daily practice", "Mock tests", "Doubt clearing"], "milestone": "Complete 40% syllabus"},
            {"month": "Month 3", "title": "Intensive Practice", "tasks": ["Full-length tests", "Weak areas focus", "Speed improvement"], "milestone": "Score 600+/720 in mocks"},
            {"month": "Month 4", "title": "Revision Phase", "tasks": ["Complete revision", "Previous year papers", "Time management"], "milestone": "Complete all topics"},
            {"month": "Month 5", "title": "Final Preparation", "tasks": ["Daily full tests", "Formula revision", "Stay healthy"], "milestone": "Consistent 650+ scores"},
            {"month": "Month 6", "title": "NEET & Counseling", "tasks": ["Appear for NEET", "College research", "Counseling preparation"], "milestone": "Clear NEET, secure admission"}
        ]
    
    elif primary_domain == "Commerce":
        career_suggestions = [
            {"title": "Chartered Accountant (CA)", "description": "Financial audit and consulting", "salary": "₹7-25 LPA"},
            {"title": "Company Secretary (CS)", "description": "Corporate governance expert", "salary": "₹6-20 LPA"},
            {"title": "Investment Banker", "description": "Financial services and investments", "salary": "₹10-35 LPA"},
            {"title": "Financial Analyst", "description": "Analyze financial data and trends", "salary": "₹5-18 LPA"}
        ]
        
        college_recommendations = [
            {
                "name": "Shri Ram College of Commerce (SRCC)",
                "location": "Delhi",
                "courses": ["B.Com (Hons)", "BA Economics"],
                "ranking": "NIRF Ranked #1 (Commerce)",
                "admission": "CUET",
                "fees": "₹20,000 per year",
                "placements": "Average: ₹8 LPA",
                "website": "https://www.srcc.edu"
            }
        ]
        
        roadmap = [
            {"month": "Month 1", "title": "Commerce Basics", "tasks": ["Accountancy fundamentals", "Business studies", "Economics basics"], "milestone": "Clear concepts"},
            {"month": "Month 2-3", "title": "CA Foundation Prep", "tasks": ["Register for CA", "Study CA Foundation syllabus", "Mock tests"], "milestone": "Complete 50% syllabus"},
            {"month": "Month 4-5", "title": "Advanced Topics", "tasks": ["Corporate accounting", "Taxation basics", "Practice problems"], "milestone": "Ready for CA Foundation"},
            {"month": "Month 6", "title": "Exams & College Prep", "tasks": ["Appear for CA Foundation", "CUET preparation", "College applications"], "milestone": "Clear exams"}
        ]
    
    elif primary_domain == "Arts":
        career_suggestions = [
            {"title": "Civil Services (IAS/IPS)", "description": "Administrative and police services", "salary": "₹56,000-2.5 Lakhs/month"},
            {"title": "Journalist", "description": "Media and news reporting", "salary": "₹4-15 LPA"},
            {"title": "Content Writer", "description": "Creative writing for digital media", "salary": "₹3-12 LPA"},
            {"title": "Psychologist", "description": "Mental health counseling", "salary": "₹4-15 LPA"}
        ]
        
        college_recommendations = [
            {
                "name": "St. Stephen's College",
                "location": "Delhi",
                "courses": ["BA (Various subjects)"],
                "ranking": "Top Arts College",
                "admission": "CUET",
                "fees": "₹40,000 per year",
                "placements": "Civil services and corporate",
                "website": "https://www.ststephens.edu"
            }
        ]
        
        roadmap = [
            {"month": "Month 1-2", "title": "Stream Selection", "tasks": ["Choose BA subjects", "UPSC/State PSC research", "Reading habit"], "milestone": "Clear goal"},
            {"month": "Month 3-4", "title": "CUET Preparation", "tasks": ["Domain subjects prep", "General test practice", "Mock tests"], "milestone": "CUET ready"},
            {"month": "Month 5-6", "title": "Admission & Start", "tasks": ["College admission", "Join UPSC coaching", "Start preparation"], "milestone": "Secure admission"}
        ]
    
    result = {
        "id": str(uuid.uuid4()),
        "user_id": current_user['id'],
        "domain_scores": domain_scores,
        "top_domains": [{"domain": d[0], "score": d[1]} for d in top_domains],
        "primary_domain": primary_domain,
        "career_suggestions": career_suggestions,
        "college_recommendations": college_recommendations,
        "coding_timeline": coding_timeline,
        "roadmap": roadmap,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    result_copy = result.copy()
    await db.aptitude_results.insert_one(result_copy)
    
    return result

@api_router.get("/aptitude-test/results")
async def get_user_results(current_user: dict = Depends(get_current_user)):
    results = await db.aptitude_results.find(
        {"user_id": current_user['id']},
        {"_id": 0}
    ).sort("created_at", -1).limit(5).to_list(5)
    return {"results": results}

@api_router.get("/aptitude-test/result/{result_id}")
async def get_result_detail(result_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.aptitude_results.find_one(
        {"id": result_id, "user_id": current_user['id']},
        {"_id": 0}
    )
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return {"result": result}

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
    
    questions_count = await db.aptitude_questions.count_documents({})
    if questions_count == 0:
        aptitude_questions = [
            {
                "id": str(uuid.uuid4()),
                "question": "What type of activities do you enjoy the most?",
                "options": [
                    {"text": "Solving mathematical problems and logical puzzles", "domains": {"Technology": 3, "Science": 2}},
                    {"text": "Understanding how things work scientifically", "domains": {"Science": 3, "Medical": 2}},
                    {"text": "Managing money and business planning", "domains": {"Commerce": 3, "Entrepreneurship": 2}},
                    {"text": "Creative writing, art, and expressing ideas", "domains": {"Arts": 3}},
                    {"text": "Helping people and community service", "domains": {"Medical": 2, "Government_Jobs": 2}}
                ],
                "category": "interests"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Which subject do you find most interesting?",
                "options": [
                    {"text": "Computer Science and Programming", "domains": {"Technology": 3}},
                    {"text": "Physics and Chemistry", "domains": {"Science": 3}},
                    {"text": "Biology and Life Sciences", "domains": {"Medical": 3, "Science": 1}},
                    {"text": "Mathematics and Statistics", "domains": {"Technology": 2, "Commerce": 2}},
                    {"text": "Accountancy and Economics", "domains": {"Commerce": 3}},
                    {"text": "History, Political Science, Literature", "domains": {"Arts": 3, "Government_Jobs": 1}}
                ],
                "category": "academics"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What kind of career appeals to you the most?",
                "options": [
                    {"text": "Working with technology and innovation", "domains": {"Technology": 3}},
                    {"text": "Conducting research and experiments", "domains": {"Science": 3}},
                    {"text": "Treating patients and healthcare", "domains": {"Medical": 3}},
                    {"text": "Managing finances and businesses", "domains": {"Commerce": 2, "Entrepreneurship": 2}},
                    {"text": "Public service and administration", "domains": {"Government_Jobs": 3}},
                    {"text": "Creative fields like media, arts, writing", "domains": {"Arts": 3}}
                ],
                "category": "career"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "How do you prefer to solve problems?",
                "options": [
                    {"text": "Using logic and algorithms", "domains": {"Technology": 3, "Science": 1}},
                    {"text": "Through experimentation and observation", "domains": {"Science": 3}},
                    {"text": "By understanding people and their needs", "domains": {"Medical": 2, "Arts": 2}},
                    {"text": "Analyzing data and financial information", "domains": {"Commerce": 3}},
                    {"text": "Using rules, policies, and frameworks", "domains": {"Government_Jobs": 3}}
                ],
                "category": "problem_solving"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What motivates you the most?",
                "options": [
                    {"text": "Building innovative products and solutions", "domains": {"Technology": 3, "Entrepreneurship": 2}},
                    {"text": "Making scientific discoveries", "domains": {"Science": 3}},
                    {"text": "Helping people live healthier lives", "domains": {"Medical": 3}},
                    {"text": "Financial success and business growth", "domains": {"Commerce": 2, "Entrepreneurship": 3}},
                    {"text": "Serving society and making policy changes", "domains": {"Government_Jobs": 3}},
                    {"text": "Creative expression and cultural impact", "domains": {"Arts": 3}}
                ],
                "category": "motivation"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Which work environment suits you best?",
                "options": [
                    {"text": "Tech companies and startups", "domains": {"Technology": 3, "Entrepreneurship": 1}},
                    {"text": "Research labs and universities", "domains": {"Science": 3}},
                    {"text": "Hospitals and clinics", "domains": {"Medical": 3}},
                    {"text": "Corporate offices and banks", "domains": {"Commerce": 3}},
                    {"text": "Government offices and administration", "domains": {"Government_Jobs": 3}},
                    {"text": "Creative studios and media houses", "domains": {"Arts": 3}}
                ],
                "category": "environment"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What are your key strengths?",
                "options": [
                    {"text": "Programming and technical skills", "domains": {"Technology": 3}},
                    {"text": "Analytical and research abilities", "domains": {"Science": 3, "Technology": 1}},
                    {"text": "Empathy and patient care", "domains": {"Medical": 3, "Arts": 1}},
                    {"text": "Financial planning and business acumen", "domains": {"Commerce": 3, "Entrepreneurship": 2}},
                    {"text": "Leadership and public speaking", "domains": {"Government_Jobs": 2, "Entrepreneurship": 2}},
                    {"text": "Creativity and communication", "domains": {"Arts": 3}}
                ],
                "category": "strengths"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Which competitive exam interests you?",
                "options": [
                    {"text": "JEE (Engineering entrance)", "domains": {"Technology": 3, "Science": 2}},
                    {"text": "NEET (Medical entrance)", "domains": {"Medical": 3}},
                    {"text": "CA/CS/CMA exams", "domains": {"Commerce": 3}},
                    {"text": "UPSC Civil Services", "domains": {"Government_Jobs": 3, "Arts": 1}},
                    {"text": "CUET/University entrances", "domains": {"Arts": 2, "Science": 1}}
                ],
                "category": "exams"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "How do you spend your free time?",
                "options": [
                    {"text": "Coding projects or tech experiments", "domains": {"Technology": 3}},
                    {"text": "Reading science articles and documentaries", "domains": {"Science": 3}},
                    {"text": "Volunteering for health/social causes", "domains": {"Medical": 2, "Government_Jobs": 1}},
                    {"text": "Following business news and markets", "domains": {"Commerce": 3, "Entrepreneurship": 1}},
                    {"text": "Writing, art, music, or creative hobbies", "domains": {"Arts": 3}}
                ],
                "category": "hobbies"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What is your career goal?",
                "options": [
                    {"text": "Become a software engineer or tech entrepreneur", "domains": {"Technology": 3, "Entrepreneurship": 2}},
                    {"text": "Work as a scientist or researcher", "domains": {"Science": 3}},
                    {"text": "Become a doctor or healthcare professional", "domains": {"Medical": 3}},
                    {"text": "Build a successful business or work in finance", "domains": {"Commerce": 2, "Entrepreneurship": 3}},
                    {"text": "Join civil services (IAS/IPS/IFS)", "domains": {"Government_Jobs": 3}},
                    {"text": "Work in creative fields (media, arts, literature)", "domains": {"Arts": 3}}
                ],
                "category": "goals"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Which skill would you like to develop further?",
                "options": [
                    {"text": "Programming and software development", "domains": {"Technology": 3}},
                    {"text": "Scientific research methods", "domains": {"Science": 3}},
                    {"text": "Medical knowledge and patient care", "domains": {"Medical": 3}},
                    {"text": "Financial analysis and accounting", "domains": {"Commerce": 3}},
                    {"text": "Public policy and governance", "domains": {"Government_Jobs": 3}},
                    {"text": "Creative arts and communication", "domains": {"Arts": 3}}
                ],
                "category": "skills"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What type of impact do you want to make?",
                "options": [
                    {"text": "Technological innovation and digital transformation", "domains": {"Technology": 3}},
                    {"text": "Scientific breakthroughs and discoveries", "domains": {"Science": 3}},
                    {"text": "Improving public health and saving lives", "domains": {"Medical": 3}},
                    {"text": "Economic growth and job creation", "domains": {"Commerce": 2, "Entrepreneurship": 3}},
                    {"text": "Policy changes and social reforms", "domains": {"Government_Jobs": 3, "Arts": 1}},
                    {"text": "Cultural influence and artistic expression", "domains": {"Arts": 3}}
                ],
                "category": "impact"
            }
        ]
        await db.aptitude_questions.insert_many(aptitude_questions)
        logger.info("Aptitude test questions seeded")