"""Mock adapter for Stellar Network notarization and USDC rails."""
import hashlib
import time
from typing import Any, Dict
from app.domain.ports.stellar_port import StellarPort
from app.core.config import settings


class MockStellarAdapter(StellarPort):
    """
    Simulated implementation of Stellar/Soroban blockchain integration.
    Provides deterministic and realistic transaction hashes, ledger sequence numbers,
    and Soroban contract events for hackathon demo reproducibility.

    # TODO: Integrar SDK real de Stellar (stellar-sdk y Soroban RPC client)
    # Ejemplo de migración futura:
    # from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
    # server = Server(settings.STELLAR_HORIZON_URL)
    """

    def __init__(self, network_passphrase: str = "Test SDF Network ; September 2015"):
        self.network_passphrase = network_passphrase

    async def notarize_delivery(
        self,
        delivery_hash: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Simulates on-chain notarization of a cacao collection ticket.
        In production, this submits a Soroban invocation or a Stellar transaction with a MEMO_HASH.
        """
        # Deterministic transaction hash simulation
        timestamp = int(time.time())
        raw_seed = f"STELLAR_TX:{delivery_hash}:{timestamp}"
        tx_hash = hashlib.sha256(raw_seed.encode("utf-8")).hexdigest()

        # Simulated Soroban contract ledger info
        simulated_ledger = 5243100 + (timestamp % 10000)

        return {
            "status": "SUCCESS",
            "tx_hash": tx_hash,
            "ledger": simulated_ledger,
            "network": settings.STELLAR_NETWORK,
            "memo_hash": delivery_hash,
            "contract_id": "CAYNICACAOEUDRNOTARYSOROBAN7777777777777777777777777777777",
            "explorer_url": f"https://stellar.expert/explorer/testnet/tx/{tx_hash}",
            "notarized_at": timestamp,
        }

    async def transfer_usdc(
        self,
        destination_account: str,
        amount_usdc: float,
        memo: str,
    ) -> Dict[str, Any]:
        """
        Simulates transferring USDC on the Stellar network.
        """
        timestamp = int(time.time())
        tx_hash = hashlib.sha256(f"USDC_TRANSFER:{destination_account}:{amount_usdc}:{timestamp}".encode()).hexdigest()
        return {
            "status": "SUCCESS",
            "tx_hash": tx_hash,
            "amount_usdc": amount_usdc,
            "destination": destination_account,
            "asset": "USDC:GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
            "memo": memo,
        }
