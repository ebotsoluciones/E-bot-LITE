from flask import Blueprint, Response, render_template
import json
from storage import get_data  # usa tu función actual

panel_bp = Blueprint('panel', __name__, template_folder='templates')

@panel_bp.route("/panel")
def panel():
    return render_template("panel.html")

def generar_csv(data):
    import io, csv

    output = io.StringIO()
    writer = csv.writer(output)

    if len(data) > 0:
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())

    return output.getvalue()

@panel_bp.route("/export/<tipo>")
def export(tipo):
    data = get_data(tipo)

    contenido = json.loads(data)
    registros = contenido.get("data", [])

    csv_data = generar_csv(registros)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={tipo}.csv"}
    )
