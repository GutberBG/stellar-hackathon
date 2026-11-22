"""
Script to reset KAIRO demo database to clean initial state.
Useful before starting a new recording take for the Stellar Hackathon.
"""
import asyncio
import logging
import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.infrastructure.database import engine, Base
from app.main import seed_initial_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kairo_reset")

async def reset_demo():
    logger.info("Restoring KAIRO database to pristine demo state...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await seed_initial_data()
    logger.info("✅ Database reset complete: 3 demo producers and 5 historical notarized deliveries restored.")

if __name__ == "__main__":
    asyncio.run(reset_demo())
