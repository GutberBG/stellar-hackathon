"""Authentication & Pollar Invisible Account endpoints."""
import hashlib
import time
from typing import Optional
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status, Header
from app.api.v1.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    PollarOAuthRequest,
    UserResponse,
    AuthTokenResponse,
    ProducerResponse,
)
from app.api.v1.dependencies import get_user_repo, get_producer_repo, get_pollar_adapter
from app.infrastructure.repositories import UserRepository, ProducerRepository
from app.domain.ports.pollar_port import PollarPort
from app.infrastructure.orm_models import UserORM, ProducerORM
from app.domain.models import UserRole

router = APIRouter()


def _hash_password(password: str) -> str:
    return hashlib.sha256(f"AYNI_SALT_{password}".encode("utf-8")).hexdigest()


def _generate_mock_jwt(user_id: int, email: str, role: str) -> str:
    timestamp = int(time.time())
    token_seed = f"{user_id}:{email}:{role}:{timestamp}"
    signature = hashlib.sha256(token_seed.encode("utf-8")).hexdigest()[:32]
    return f"ayni_jwt_{user_id}_{role.lower()}_{signature}"


@router.post(
    "/register",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register user with invisible Pollar wallet and role profile",
)
async def register(
    req: UserRegisterRequest,
    user_repo: UserRepository = Depends(get_user_repo),
    producer_repo: ProducerRepository = Depends(get_producer_repo),
    pollar_port: PollarPort = Depends(get_pollar_adapter),
) -> AuthTokenResponse:
    existing = await user_repo.get_by_email(req.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado.",
        )

    # 1. Create invisible wallet via Pollar Port
    wallet_info = await pollar_port.create_invisible_wallet(req.email, req.full_name)

    # 2. Persist User
    user_orm = UserORM(
        email=req.email,
        hashed_password=_hash_password(req.password),
        full_name=req.full_name,
        role=req.role.value,
        pollar_wallet_address=wallet_info.get("stellar_address"),
    )
    saved_user = await user_repo.create(user_orm)

    # 3. If role is PRODUCTOR, generate initial ProducerORM profile
    saved_producer = None
    if req.role == UserRole.PRODUCTOR:
        timestamp = int(time.time()) % 100000
        plot_code = f"BO-LPZ-AB-{req.community[:4].upper()}-{timestamp:04d}"
        producer_orm = ProducerORM(
            user_id=saved_user.id,
            name=req.full_name,
            ci_number=req.ci_number,
            community=req.community or "Sapecho (Alto Beni)",
            cooperative=req.cooperative or "Central de Cooperativas El Ceibo",
            eudr_latitude=-15.5412,
            eudr_longitude=-67.3298,
            eudr_plot_code=plot_code,
            parcel_hectares=req.parcel_hectares or 2.5,
            eudr_certified=True,
            phone=req.phone or "+59171234567",
            bank_account_hint="Bisa / Simple QR",
            compliance_score=0.95,
            risk_tier="BAJO",
        )
        saved_producer = await producer_repo.create(producer_orm)

    token = _generate_mock_jwt(saved_user.id, saved_user.email, saved_user.role)
    user_resp = UserResponse.model_validate(saved_user)
    prod_resp = ProducerResponse.model_validate(saved_producer) if saved_producer else None

    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        user=user_resp,
        producer=prod_resp,
    )


@router.post(
    "/login",
    response_model=AuthTokenResponse,
    summary="Login with email and password",
)
async def login(
    req: UserLoginRequest,
    user_repo: UserRepository = Depends(get_user_repo),
    producer_repo: ProducerRepository = Depends(get_producer_repo),
) -> AuthTokenResponse:
    user = await user_repo.get_by_email(req.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    # Check password
    if user.hashed_password != _hash_password(req.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    producer = await producer_repo.get_by_user_id(user.id)
    token = _generate_mock_jwt(user.id, user.email, user.role)

    user_resp = UserResponse.model_validate(user)
    prod_resp = ProducerResponse.model_validate(producer) if producer else None

    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        user=user_resp,
        producer=prod_resp,
    )


@router.post(
    "/pollar-oauth",
    response_model=AuthTokenResponse,
    summary="Simulated 1-click Google & Pollar Auth login",
)
async def pollar_oauth(
    req: PollarOAuthRequest,
    user_repo: UserRepository = Depends(get_user_repo),
    producer_repo: ProducerRepository = Depends(get_producer_repo),
    pollar_port: PollarPort = Depends(get_pollar_adapter),
) -> AuthTokenResponse:
    user = await user_repo.get_by_email(req.email)
    if not user:
        # Create user immediately
        wallet_info = await pollar_port.create_invisible_wallet(req.email, req.full_name)
        user_orm = UserORM(
            email=req.email,
            hashed_password=_hash_password("pollar_oauth_default"),
            full_name=req.full_name,
            role=req.role.value,
            pollar_wallet_address=wallet_info.get("stellar_address"),
        )
        user = await user_repo.create(user_orm)

        if req.role == UserRole.PRODUCTOR:
            timestamp = int(time.time()) % 100000
            plot_code = f"BO-LPZ-AB-OAUTH-{timestamp:04d}"
            producer_orm = ProducerORM(
                user_id=user.id,
                name=req.full_name,
                community="Sapecho (Alto Beni)",
                cooperative="Central de Cooperativas El Ceibo",
                eudr_latitude=-15.5412,
                eudr_longitude=-67.3298,
                eudr_plot_code=plot_code,
                parcel_hectares=2.5,
                eudr_certified=True,
                phone="+59171234567",
                bank_account_hint="Bisa / Simple QR",
                compliance_score=0.96,
                risk_tier="BAJO",
            )
            await producer_repo.create(producer_orm)

    producer = await producer_repo.get_by_user_id(user.id)
    token = _generate_mock_jwt(user.id, user.email, user.role)
    user_resp = UserResponse.model_validate(user)
    prod_resp = ProducerResponse.model_validate(producer) if producer else None

    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        user=user_resp,
        producer=prod_resp,
    )


@router.get(
    "/me",
    response_model=AuthTokenResponse,
    summary="Get profile of authenticated user",
)
async def get_me(
    user_repo: UserRepository = Depends(get_user_repo),
    producer_repo: ProducerRepository = Depends(get_producer_repo),
    authorization: Optional[str] = Header(None),
) -> AuthTokenResponse:
    user = None
    if authorization and "ayni_jwt_" in authorization:
        parts = authorization.replace("Bearer ", "").split("_")
        if len(parts) >= 3 and parts[2].isdigit():
            user_id = int(parts[2])
            user = await user_repo.get_by_id(user_id)

    if not user:
        # Default to first user or demo user
        user = await user_repo.get_by_email("mateo@aynicacao.bo")
        if not user:
            users = await user_repo.session.execute(select(UserORM).limit(1))
            user = users.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authenticated user.")

    producer = await producer_repo.get_by_user_id(user.id)
    token = _generate_mock_jwt(user.id, user.email, user.role)

    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
        producer=ProducerResponse.model_validate(producer) if producer else None,
    )
