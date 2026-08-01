"""CLI do agente de atas: lê anotações de um arquivo ou da entrada padrão."""

import argparse
import sys
from pathlib import Path

from agente_ata.agent import MODELO_PADRAO, AgenteAta, PedidoAta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agente-ata",
        description="Gera atas formais de reunião/ação do grêmio estudantil a partir de anotações.",
    )
    parser.add_argument("arquivo", nargs="?", help="arquivo com as anotações (padrão: stdin)")
    parser.add_argument("-o", "--saida", help="arquivo de saída (padrão: imprime no terminal)")
    parser.add_argument("-t", "--tipo", default="reunião", help="reunião, assembleia, ação/evento...")
    parser.add_argument("-g", "--gremio", default="", help="nome do grêmio estudantil")
    parser.add_argument("-n", "--numero", default="", help="número da ata")
    parser.add_argument("-d", "--data", default="", help="data da sessão")
    parser.add_argument("-l", "--local", default="", help="local da sessão")
    parser.add_argument("--observacoes", default="", help="observações adicionais")
    parser.add_argument("--modelo", default=MODELO_PADRAO, help="modelo Groq a utilizar")
    args = parser.parse_args(argv)

    anotacoes = Path(args.arquivo).read_text(encoding="utf-8") if args.arquivo else sys.stdin.read()

    try:
        ata = AgenteAta(modelo=args.modelo).gerar(
            PedidoAta(
                anotacoes=anotacoes,
                tipo=args.tipo,
                gremio=args.gremio,
                numero_ata=args.numero,
                data=args.data,
                local=args.local,
                observacoes=args.observacoes,
            )
        )
    except (RuntimeError, ValueError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    if args.saida:
        Path(args.saida).write_text(ata + "\n", encoding="utf-8")
        print(f"Ata salva em {args.saida}")
    else:
        print(ata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
