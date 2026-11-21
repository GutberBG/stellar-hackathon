"""Port interface for Stellar blockchain notarization and USDC settlements."""
from abc import ABC, abstractmethod
from typing import Any, Dict


class StellarPort(ABC):
    """
    Hexagonal Port for Stellar Network integration.
    Responsible for notarizing delivery receipts on-chain (Soroban contract or memo hash)
    and handling USDC token settlement rails.
    """

    @abstractmethod
    async def notarize_delivery(
        self,
        delivery_hash: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Notarizes an immutable cacao delivery receipt on the Stellar ledger.
        Returns transaction hash and ledger metadata.
        """
        pass

    @abstractmethod
    async def transfer_usdc(
        self,
        destination_account: str,
        amount_usdc: float,
        memo: str,
    ) -> Dict[str, Any]:
        """
        Executes a Stellar payment operation with USDC asset trustline.
        """
        pass
