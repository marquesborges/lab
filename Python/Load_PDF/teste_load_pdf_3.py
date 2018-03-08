import pdfquery

PDFFile = pdfquery.PDFQuery("C:\\Users\\alexandreborges\\Downloads\\NotaDeCorretagem_12058.pdf")
#PDFFile = pdfquery.PDFQuery("C:\\Users\\alexandreborges\\Downloads\\NotaDeCorretagem_105732.pdf")
#PDFFile = pdfquery.PDFQuery("C:\\Users\\alexandreborges\\Downloads\\Nota de Corretagem_Modal.pdf")
#PDFFile = pdfquery.PDFQuery("C:\\Users\\alexandreborges\\Downloads\\Nota de Corretagem_Socopa.pdf")

# LOAD() tem lentidao por conta da associacao de todos os tipos no PDFMiner
PDFFile.load(0)


#NCTitle = PDFFile.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % ('246.151', '794.847', '349.08', '806.897')).text()
#PDFFile.tree.write("C:\\Users\\alexandreborges\\Downloads\\Nota de Corretagem_Socopa.xml", pretty_print=True, encoding="utf-8")


#NCTitle = PDFFile.pq('LTRect\LTTextLineHorizontal').text()

IniQuadro = PDFFile.pq('LTTextBoxHorizontal:contains("Negócios Realizados")')
FimQuadro = PDFFile.pq('LTTextBoxHorizontal:contains("Resumo Financeiro")')
x0 = float(IniQuadro.attr('x0'))
y0 = float(FimQuadro.attr('y0'))+50
x1 = float(IniQuadro.attr('x1'))+700
y1 = float(IniQuadro.attr('y1'))-20

#print(x0, y0, x1, y1)

Quadro = PDFFile.extract([
    ('with_parent','LTPage'),
    ('TextBox', 'LTTextBoxHorizontal:in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)),
    ('TextLine', 'LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1))
    ])

if (len(Quadro['TextBox'][0]) > 0):
    QdoNegocio = 'TextBox'
else:
    QdoNegocio = 'TextLine'

Movto=[]
for idxLinha in range(0, len(Quadro[QdoNegocio][0])):
    #Txt=''
    Oper=[]
    #print('Linha=',idxLinha)
    for idxColuna in range(0, len(Quadro[QdoNegocio])):
        #print('Coluna=',idxColuna)
        Oper.append(Quadro[QdoNegocio][idxColuna][idxLinha].text.encode('UTF-8').strip().decode('UTF-8'))
        #Txt += '[' + Quadro[QdoNegocio][idxColuna][idxLinha].text.encode('UTF-8').strip().decode('UTF-8') + ']'
    #print(Txt)
    Movto.append(Oper)

Cabecalho = {'Cliente': None,
             'Nr. Nota': None,
             'Folha': None,
             'Data pregão': None,
             'Código cliente': None,
             'Assessor': None,
             'Banco': None,
             'Agência': None,
             'Conta Corrente': None}

for NotaKey in Cabecalho.keys():
    Campo = PDFFile.pq('LTTextBoxHorizontal:contains("%s")' % NotaKey)
    x0 = float(Campo.attr('x0'))
    y0 = float(Campo.attr('y0'))-(float(Campo.attr('height'))*2)
    x1 = float(Campo.attr('x1'))+(float(Campo.attr('width'))+10)
    y1 = float(Campo.attr('y1'))
    Valor = PDFFile.pq('LTTextBoxHorizontal:in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1))
    Cabecalho[NotaKey] = Valor[1].text.strip()
print(Cabecalho)


IniQuadro = PDFFile.pq('LTTextLineHorizontal:contains("CBLC")')
x0 = float(IniQuadro[0].attrib['x0'])
y0 = float(IniQuadro[1].attrib['y0'])
x1 = float(IniQuadro[0].attrib['x1'])+(float(IniQuadro[0].attrib['width'])+10)
y1 = float(IniQuadro[0].attrib['y1'])

#print(x0, y0, x1, y1)
CBLC = PDFFile.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1))

#for c in Quadro['LinNegocios']:
#    print(c.text.encode('UTF-8').strip())
    
