import sql
import json
import requests
import csv
from datetime import date
from datetime import datetime
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
from pdf2image import convert_from_path
import sympy
import latex

db = None

settings = {"sql_host":"localhost", 
            "sql_user":"root",
            "sql_passwd":"111",
            "sql_db":"galerkin"
           }

points = []
equations = []
rates = []




from pylatex import Document, LongTable, MultiColumn



def genenerate_longtabu():
    geometry_options = {
        "margin": "2.54cm",
        "includeheadfoot": True
    }
    doc = Document(page_numbers=True, intend = True, geometry_options=geometry_options)

    # Generate data table
    with doc.create(LongTable("l l l")) as data_table:
            data_table.add_hline()
            data_table.add_row(["header 1", "header 2", "header 3"])
            data_table.add_hline()
            data_table.end_table_header()
            data_table.add_hline()
            data_table.add_row((MultiColumn(3, align='r',
                                data='Containued on Next Page'),))
            data_table.add_hline()
            data_table.end_table_footer()
            data_table.add_hline()
            data_table.add_row((MultiColumn(3, align='r',
                                data='Not Containued on Next Page'),))
            data_table.add_hline()
            data_table.end_table_last_footer()
            row = ["Content1", "9", "Longer String"]
            for i in range(150):
                data_table.add_row(row)

    doc.generate_pdf("longtable", clean_tex=False)




def genenerate_table_rates(table_rates):
    doc = Document('basic', indent = True,  page_numbers = False)

    steps = sorted(list(set([t["qty_dx"] for t in table_rates])))
    print(steps)
    basises = sorted(list(set([t["qty_bas"] for t in table_rates])))
    rates_L1 = {}
    rates_L2 = {}
    for t in table_rates:
        rates_L1[str(t["qty_dx"]) + "-" + str(t["qty_bas"])] = t["L1"]
        rates_L2[str(t["qty_dx"]) + "-" + str(t["qty_bas"])] = t["L2"]
    print(rates_L1)    
    format_header = "".join(["|c|" for i in range(len(steps))])
    # Generate data table
    with doc.create(Tabular(format_header)) as table:
        table.add_hline()
        table.add_row(steps)
        table.add_hline()
        for basis in basises:
            row = []
            for step in steps:
                if (str(step) + "-" + str(basis) in rates_L1):
                    row.append(rates_L1[str(step) + "-" + str(basis)])
                else:
                    row.append('')     
            table.add_row(row)        
           
    print(table)
    doc.generate_pdf("rates", clean_tex=False)
    pages = convert_from_path('rates.pdf', 500)
    for page in pages:
        page.save('out.jpg', 'JPEG')
    
#получаем нормы L1 и L2
def getDataRates(id_equation, id_flux):
    global db
    query = "select p.qty_dx, p.qty_bas, r.L1,  r.L2 "
    query += " from galerkin.rates r "
    query += " join galerkin.problem_params p "
    query += " on r.id_problem_params = p.id "
    query += " where p.id_equation = " + str(id_equation)
    query += " and p.id_flux = " + str(id_flux)
    return db.getDictFromQuery(query)


def getJPGFromFormulaLatex(formula, name):
    sympy.preview(formula, viewer='file', filename=name, euler=False)
    
   

def main(): 
    global db, points, equations
    # id, id_problem_params, dxi, fx, gx, dti, time_modif
    id_problem_params = 4
    dti = 69; 
    db = sql.database(settings['sql_host'],  settings['sql_user'],  settings['sql_passwd'], settings['sql_db'])
    points = db.getDictFromQueryRes("galerkin.aprox_decision", {"id_problem_params": id_problem_params, "dti":dti})  
    fluxes = db.getDictFromQueryRes("galerkin.fluxes", None)  
    id_equation = 3
    id_flux = 2
    rates = getDataRates(id_equation, id_flux)
    print(rates)
    genenerate_table_rates(rates)
    getJPGFromFormulaLatex(fluxes[2]["formula_latex"], fluxes[0]["name"])
    #genenerate_longtabu()
    params = db.getDictFromQueryRes("galerkin.problem_params", {"id": id_problem_params})     
    lx = float (params[0]["lx"])
    rx = float (params[0]["rx"]) 
    qty_dx = int (params[0]["qty_dx"])
    dx = (rx - lx) / qty_dx;
    points = [ { "x": lx + p["dxi"] * dx, "fx": p["fx"], "gx": p["gx"]} for p in points]
    print(points)
    
main()    
