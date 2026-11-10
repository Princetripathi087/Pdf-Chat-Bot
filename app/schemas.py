from datetime import datetime
from pydantic import BaseModel,  EmailStr, constr
from typing import Optional
from typing import List
from fastapi import UploadFile, File
from typing import Union


class UserBaseSchema(BaseModel):
    name: str
    email: str
    role: Union[str, None] = None
    #role: str | None = None
    #created_at: datetime | None = None
    #updated_at: datetime | None = None

    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False

class IngestRequest(BaseModel):
    base_id: str
    files: List[UploadFile] = File(...)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema

class PayLoad(BaseModel):
    questions: List[str]

class searchPayLoad(BaseModel):
    question: str
    
class controlDescriptionPayLoad(BaseModel):
    description: str

class queryPayLoad(BaseModel):
    question: str
    user_id: str
    
class chatbotQueryPayLoad(BaseModel):
    question: str
    
# class grc_queryPayLoad(BaseModel):
#     user_id: str
#     policy_id:str
#     doc_type:str
#     control_codes:List[str]
#     control_quetions:List[str]

class grcPolicyControl(BaseModel):
    control_code: str
    control_quetion: str

class grcPolicyEvidence(BaseModel):
    evidence_code: str
    evidence_artifact: str

class grcPolicy(BaseModel):
    policy_name: str
    policy_code: str
    controls: List[grcPolicyControl]
    evidences: List[grcPolicyEvidence]

class grc_queryPayLoad(BaseModel):
    user_id: str
    doc_type:str
    policies: List[grcPolicy]
     
class grc_evidencePayLoad(BaseModel):
    user_id: str
    evidence_id:str
    doc_type:str
    evidences:List[grcPolicyEvidence]
    

class contractPayLoad(BaseModel):
    question: str
    file_name: str  

class url(BaseModel):
    url: str


class url(BaseModel):
    url: str

class text(BaseModel):
    txt: str

class upload(BaseModel):
    fileUrl: str

class promptChat(BaseModel):
    user_prompt: str
    system_prompt: str = "You are a helpful, respectful and honest assistant."
    temperature: float = 0.7
    max_tokens:int = 128
    top_p:int = 0.95
    repetition_penalty: int = 1.15

# Define a request model for queries
class QueryRequest(BaseModel):
    query: str

# Define a response model for queries
class QueryResponse(BaseModel):
    response: str


class TextRequest(BaseModel):
    text: str

