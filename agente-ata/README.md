# Agente de Atas — Grêmio Estudantil

Agente que transforma anotações informais de reuniões ou ações do grêmio estudantil em uma
**ata formal** em português, com estrutura padronizada (abertura, presenças, pauta, discussões,
deliberações, encaminhamentos, encerramento e assinaturas). Usa a API da Groq
(`llama-3.3-70b-versatile`).

## Instalação

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env   # e coloque sua GROQ_API_KEY dentro
```

## Uso — linha de comando

```bash
.venv/bin/python -m agente_ata.cli exemplos/reuniao.txt \
  --gremio "Grêmio Estudantil Unidos" --numero "012/2026" \
  --data "20/03/2026" --local "Sala 12 - Bloco B" -o ata.md
```

Também aceita entrada padrão: `cat notas.txt | .venv/bin/python -m agente_ata.cli`.

Principais opções: `-t/--tipo` (reunião, assembleia, ação/evento), `-g/--gremio`, `-n/--numero`,
`-d/--data`, `-l/--local`, `--observacoes`, `--modelo`, `-o/--saida`.

## Uso — interface web

```bash
.venv/bin/python app.py    # http://localhost:5000
```

## Estrutura

- `agente_ata/prompt.py` — prompt do agente: regras de redação e estrutura obrigatória da ata
- `agente_ata/agent.py` — chamada à API da Groq
- `agente_ata/cli.py` — interface de linha de comando
- `app.py` + `templates/index.html` — interface web
- `exemplos/reuniao.txt` — anotações de exemplo

## Comportamento do agente

- Nunca inventa nomes, votos ou valores: dados faltantes viram `[A PREENCHER: ...]`
- Linguagem formal, impessoal, no pretérito perfeito; datas por extenso no cabeçalho
- Deliberações registram forma de aprovação e placar; encaminhamentos têm responsável e prazo
- Para atas de ação/evento, as seções centrais viram objetivo, execução e resultados

## Segurança

A chave fica somente em `.env` (ignorado pelo git). Nunca a coloque no código nem em commits.
