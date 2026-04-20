# Exemplo: Classe Abstrata em Python (Codex)

```python
from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def parse(self, raw: str) -> dict:
        raise NotImplementedError

class JsonParser(Parser):
    def parse(self, raw: str) -> dict:
        import json
        return json.loads(raw)
```

## Como validar no fluxo Codex
- Buscar uso local: `rg "from abc import ABC" src`
- Executar testes: `pytest` ou comando nativo do projeto
