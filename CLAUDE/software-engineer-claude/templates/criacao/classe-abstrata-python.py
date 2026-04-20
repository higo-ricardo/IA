from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable


class PaymentProvider(ABC):
    """Contrato base para provedores de pagamento."""

    @abstractmethod
    def charge(self, amount_cents: int) -> str:
        """Executa cobranca e retorna id da transacao."""
        raise NotImplementedError


@dataclass
class PixProvider(PaymentProvider):
    key: str

    def charge(self, amount_cents: int) -> str:
        if amount_cents <= 0:
            raise ValueError('amount_cents must be positive')
        return f'pix:{self.key}:{amount_cents}'


def charge_all(provider: PaymentProvider, values: Iterable[int]) -> list[str]:
    return [provider.charge(v) for v in values]


if __name__ == '__main__':
    provider = PixProvider(key='merchant-key')
    print(charge_all(provider, [100, 250]))
