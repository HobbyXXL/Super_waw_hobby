from .hobbies import Hobby, HobbyCreate
from .users import (
    User, 
    UserRegisterRequest,  # вместо UserCreate
    UserLogin, 
    AccessToken, 
    UserInfo, 
    UserProfileExtended,
    VerificationCodeInput,
    ProfileCompleteRequest,
    ResendCodeRequest
)
from .portfolio import PortfolioWork, PortfolioWorkCreate, LikeResponse
from .chats import Chat, ChatCreate, ChatList, Message, MessageCreate