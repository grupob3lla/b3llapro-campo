# -*- coding: utf-8 -*-
# RETORNO DOS REGISTROS DO APP → aba ACOES_COMERCIAIS (executado na atualização mensal)
# Entrada: planilha de respostas do Google Form exportada (xlsx/csv) OU CSV baixado do app.
# Regras: chave = OportunidadeChave; StatusAcao: Sim/Parcial→"Ganhou" se qtd>0 senão "Contatado"; Não→"Perdeu".
import pandas as pd, sys, openpyxl
from datetime import datetime
src, wbpath = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, sep=None, engine='python') if src.lower().endswith('.csv') else pd.read_excel(src)
df.columns=[c.strip().lower() for c in df.columns]
col=lambda *n: next((c for c in df.columns if c in n), None)
ts,chave,valid,item,qtd,obs,agente=col('carimbo de data/hora','timestamp','ts'),col('chave'),col('validada'),col('item'),col('qtd'),col('obs'),col('agente')
wb=openpyxl.load_workbook(wbpath); ws=wb['ACOES_COMERCIAIS']
existentes={ (str(ws.cell(r,3).value), str(ws.cell(r,9).value)) for r in range(6, 406) if ws.cell(r,2).value }
r=next((r for r in range(6,406) if not ws.cell(r,2).value), None)
n=0
for _,x in df.iterrows():
    if not x[chave] or pd.isna(x[chave]): continue
    o=f"[APP] {x[valid]}" + (f" — {x[obs]}" if obs and pd.notna(x[obs]) and str(x[obs]).strip() else "")
    if (str(x[chave]),o) in existentes: continue
    q=float(x[qtd]) if qtd and pd.notna(x[qtd]) and str(x[qtd]).strip() else 0
    st='Ganhou' if (str(x[valid]).lower() in ('sim','parcial') and q>0) else ('Perdeu' if str(x[valid]).lower()=='não' else 'Contatado')
    d=pd.to_datetime(x[ts]) if ts else datetime.now()
    ws.cell(r,2,d.to_pydatetime()); ws.cell(r,3,str(x[chave])); ws.cell(r,7,'Visita'); ws.cell(r,8,st); ws.cell(r,9,o)
    if q>0: ws.cell(r,10,f"Item: {x[item]} × {int(q)}"); 
    r+=1; n+=1
wb.save(wbpath); print(f"{n} registros do app importados para ACOES_COMERCIAIS ({wbpath}).")
