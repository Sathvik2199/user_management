import uuid
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest, validate_profile_picture_url, validate_url

# Fixtures for common test data
@pytest.fixture
def user_base_data():
    return {
        "nickname": "john_doe_123",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "AUTHENTICATED",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "nickname": "j_doe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
    }

@pytest.fixture
def user_response_data(user_base_data):
    return {
        "id": uuid.uuid4(),
        "nickname": user_base_data["nickname"],
        "first_name": user_base_data["first_name"],
        "last_name": user_base_data["last_name"],
        "role": user_base_data["role"],
        "email": user_base_data["email"],
        # "last_login_at": datetime.now(),
        # "created_at": datetime.now(),
        # "updated_at": datetime.now(),
        "links": []
    }

@pytest.fixture
def login_request_data():
    return {"email": "john_doe_123@emai.com", "password": "SecurePassword123!"}

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    # assert user.last_login_at == user_response_data["last_login_at"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)


@pytest.mark.parametrize("invalid_password, error_message", [
    ("weakpass", "Password must include at least one uppercase letter."),
    ("SHORT1!", "Password must include at least one lowercase letter."),
    ("noupper123!", "Password must include at least one uppercase letter."),
    ("NOLOWER123!", "Password must include at least one lowercase letter."),
    ("NoNumber!", "Password must include at least one number."),
    ("NoSpecial123", "Password must include at least one special character"),
])
def test_user_creation_with_invalid_password(invalid_password, error_message, generate_unique_user):
    """
    Test that user creation raises ValidationError for invalid passwords.
    """
    user_data = generate_unique_user
    user_data["password"] = invalid_password

    with pytest.raises(ValidationError) as validation_error:
        UserCreate(**user_data)
    
    assert error_message in str(validation_error.value)

@pytest.fixture
async def bulk_users_with_role(db_session):
    """
    Creates 50 users with the same role but unique email and nickname.
    """
    users_to_create = []
    for _ in range(50):
        users_to_create.append({
            "nickname": f"user_{uuid.uuid4().hex[:6]}",
            "email": f"user_{uuid.uuid4().hex[:6]}@example.com",
            "first_name": "Bulk",
            "last_name": "User",
            "role": "AUTHENTICATED"
        })
    
    db_session.add_all([UserCreate(**user) for user in users_to_create])
    await db_session.commit()
    return users_to_create

@pytest.mark.parametrize("url", [
    "https://example.com/image.bmp",
    "http://example.com/image.gif",
    "https://example.com/image",
    "https://example.com/image.jpg.txt"
])
def test_user_base_profile_picture_invalid_extension(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

@pytest.mark.parametrize("field, value", [
    ("linkedin_profile_url", "ftp://linkedin.com/in/testuser"),
    ("github_profile_url", "randomstring"),
])
def test_invalid_social_urls(field, value, user_base_data):
    user_base_data[field] = value
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

def test_user_create_password_too_short(user_create_data):
    user_create_data["password"] = "A1@a"
    with pytest.raises(ValidationError) as e:
        UserCreate(**user_create_data)
    assert "at least 8 characters" in str(e.value)

def test_user_update_no_fields():
    with pytest.raises(ValidationError) as e:
        UserUpdate()
    assert "At least one field must be provided for update" in str(e.value)


def test_user_update_all_fields(user_update_data):
    user = UserUpdate(**user_update_data)
    assert user.nickname == user_update_data["nickname"]
    assert user.profile_picture_url == user_update_data["profile_picture_url"]

def test_invalid_email_in_user_create(user_create_data):
    user_create_data["email"] = "invalid-email"
    with pytest.raises(ValidationError):
        UserCreate(**user_create_data)


def test_user_base_optional_fields_none(user_base_data):
    user_base_data["bio"] = None
    user_base_data["linkedin_profile_url"] = None
    user_base_data["github_profile_url"] = None
    user = UserBase(**user_base_data)
    assert user.bio is None

def test_validate_url_accepts_none():
    assert validate_url(None) is None

def test_validate_profile_picture_url_accepts_none():
    assert validate_profile_picture_url(None, None) is None

