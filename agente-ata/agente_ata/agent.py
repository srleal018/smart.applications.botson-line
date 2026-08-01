"""Cliente do agente de atas sobre a API da Groq."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from groq import Groq

from agente_ata.prompt import SYSTEM_PROMPT, build_user_prompt

MODELO_PADRAO = "llama-3.3-70b-versatile"


@dataclass
class PedidoAta:
    anotacoes: str
    tipo: str = "reunião"
    gremio: str = ""
    numero_ata: str = ""
    data: str = ""
    local: str = ""
    observacoes: str = ""


class AgenteAta:
    def __init__(self, api_key: str | None = None, modelo: str = MODELO_PADRAO) -> None:
        load_dotenv()
        chave = api_key or os.getenv("GROQ_API_KEY")
        if not chave:
            raise RuntimeError(
                "GROQ_API_KEY não encontrada. Defina a variável de ambiente ou crie um arquivo .env."
            )
        self.modelo = modelo
        self._client = Groq(api_key=chave)

    def gerar(self, pedido: PedidoAta) -> str:
        if not pedido.anotacoes.strip():
            raise ValueError("As anotações da reunião/ação não podem estar vazias.")
        resposta = self._client.chat.completions.create(
            model=self.modelo,
            temperature=0.2,
            max_tokens=4096,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(
                        anotacoes=pedido.anotacoes,
                        tipo=pedido.tipo,
                        gremio=pedido.gremio,
                        numero_ata=pedido.numero_ata,
                        data=pedido.data,
                        local=pedido.local,
                        observacoes=pedido.observacoes,
                    ),
                },
            ],
        )
        return (resposta.choices[0].message.content or "").strip()
