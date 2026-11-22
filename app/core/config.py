"""Application configuration and constants."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Ayni Cacao Backend"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Financial Constants (Alto Beni Cacao & Bolivian Markets)
    EXCHANGE_RATE_USDC_BOB: float = 6.96
    BASE_CACAO_PRICE_USDC_PER_KG: float = 4.80
    VAQUITA_POOL_INITIAL_LIQUIDITY_USDC: float = 25000.00
    VAQUITA_COMMISSION_PCT: float = 0.02   # 2.0% for Vaquita Liquidity Providers
    AYNI_COMMISSION_PCT: float = 0.005     # 0.5% Ayni Cacao origination fee

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./ayni_cacao.db"

    # ML Model
    ML_MODEL_PATH: str = "./ayni_risk_model.joblib"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # External Integration Mocks / Configs
    STELLAR_USE_REAL_NETWORK: bool = True
    STELLAR_NETWORK: str = "TESTNET"
    STELLAR_HORIZON_URL: str = "https://horizon-testnet.stellar.org"
    STELLAR_ISSUING_ACCOUNT: str = "GBMOCKSTELLARAYNICACAO7777777777777777777777777777777777"
    STELLAR_SECRET_KEY: str = ""
    POLLAR_API_BASE_URL: str = "https://sdk.api.pollar.xyz/v3"
    VAQUITA_POOL_ID: str = "pool_vaquita_altobeni_01"
    TRUSTLESS_WORK_ESCROW_FACTORY: str = "CBHMOCKTRUSTLESSWORKESCROWCONTRACT0000000000000000000000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
