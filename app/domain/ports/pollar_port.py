"""Port interface for Pollar invisible account and Bolivian banking QR cash-out."""
from abc import ABC, abstractmethod
from typing import Any, Dict


class PollarPort(ABC):
    """
    Hexagonal Port for Pollar integration.
    Provides invisible self-custody / embedded wallets and on/off-ramp disbursement
    directly to Bolivian interbank Simple QR in Bolivianos (BOB).
    """

    @abstractmethod
    async def create_invisible_wallet(
        self,
        email: str,
        full_name: str,
    ) -> Dict[str, Any]:
        """
        Creates an embedded invisible Stellar wallet for the user via Pollar Auth.
        """
        pass

    @abstractmethod
    async def disburse_to_qr(
        self,
        producer_id: int,
        producer_phone: str,
        amount_bob: float,
        concept: str,
    ) -> Dict[str, Any]:
        """
        Generates an interbank Simple QR code disbursement in Bolivianos (BOB)
        and initiates local settlement to the cooperative producer.
        """
        pass

    @abstractmethod
    async def check_payout_status(self, payout_id: str) -> Dict[str, Any]:
        """
        Checks the clearance status of an issued QR cash-out.
        """
        pass
