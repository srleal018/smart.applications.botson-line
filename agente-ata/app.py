"""Interface web simples para o agente de atas."""

from flask import Flask, render_template, request

from agente_ata.agent import AgenteAta, PedidoAta

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    ata = None
    erro = None
    form = request.form
    if request.method == "POST":
        try:
            ata = AgenteAta().gerar(
                PedidoAta(
                    anotacoes=form.get("anotacoes", ""),
                    tipo=form.get("tipo", "reunião"),
                    gremio=form.get("gremio", ""),
                    numero_ata=form.get("numero", ""),
                    data=form.get("data", ""),
                    local=form.get("local", ""),
                    observacoes=form.get("observacoes", ""),
                )
            )
        except (RuntimeError, ValueError) as e:
            erro = str(e)
        except Exception as e:  # falha de rede/API
            erro = f"Falha ao chamar a API da Groq: {e}"
    return render_template("index.html", ata=ata, erro=erro, form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
