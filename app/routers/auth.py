from datetime import datetime
from fastapi import APIRouter, Request, status, HTTPException
from app.database import User
from app.email import send_email
from .. import schemas, utils

router = APIRouter()

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.CreateUserSchema, request: Request):
    # Check if user already exist
    user = User.find_one({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    if  not (utils.is_email(payload.email.lower())):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Must be valid email format')
    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    #  Hash the password
    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    payload.verified = False
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    new_user = User.find_one({'_id': result.inserted_id})
    try:
        verification_code = utils.get_code()
        User.find_one_and_update({"_id": result.inserted_id}, {
            "$set": {"verification_code": verification_code, "updated_at": datetime.utcnow()}})
        await send_email( user["email"], verification_code  )
    except Exception as error:
        pass
    return {'status': 'success', 'message': 'Verification code successfully sent to your email ,  code : {} :, i print there the code juste for test without SMTP :) '.format(verification_code)}


@router.get('/verifyemail/{token}')
def verify_me(token: str):
    verification_code = token
    db_user = User.find_one({"verification_code": verification_code})
    if db_user:
        if utils.get_seconds( str(db_user["created_at"]) ,  str(datetime.utcnow()))  > 60 :
            result = User.find_one_and_update({"verification_code": verification_code}, {
            "$set": {"verification_code": None, "verified": False, "updated_at": datetime.utcnow()}}, new=True)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='The activation code has expired')
    result = User.find_one_and_update({"verification_code": verification_code}, {
        "$set": {"verification_code": None, "verified": True, "updated_at": datetime.utcnow()}}, new=True)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code or account already verified')
    return {
        "status": "success",
        "message": "Account verified successfully"
    }
