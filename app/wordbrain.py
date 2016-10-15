import unicodedata
from copy import deepcopy

class letra(object):
    x = -1
    y = -1
    caracter = '.'

    def strDetail(self):
        return "%s [%s][%s]" % (self.caracter, self.x, self.y)

    def __str__(self):
        return "%s" % (self.caracter)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.caracter = globalGrid[x][y]

def removerAcentos(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def carregaDicionario():
    f = open('./dicionario_pt_br.txt', 'r')
    i = 0
    for linha in f.readlines():
        i += 1
        palavra = linha.split(" ")[0]
        if (palavra[0] == '#') or palavra[0] == '\n':
            continue
        derivadas = palavra.split(':')

        if len(derivadas) > 1:
            for x in derivadas[1].split(','):
                text = ('%s%s' % (derivadas[0],x))
                text = text.replace('\n', '')
                dicionario.append(text)
                if text != removerAcentos(text):
                    dicionario.append(removerAcentos(text))

        else:
            text = derivadas[0]
            text = text.replace('\n', '')
            dicionario.append(text)
            if text != removerAcentos(text):
                dicionario.append(removerAcentos(text))

    f.close()


def printGrid(matrix):
    for palavra in matrix:
        str_palavra = ''
        str_palavraDetail = ''
        for letra in palavra:
            str_palavra=str_palavra+str(letra)
            str_palavraDetail = str_palavraDetail + '-'*3 + letra.strDetail() + '\n'
        if (str_palavra in dicionario):
            print str_palavraDetail
            print str_palavra


def _obtemAdjacente(x, y, grid):
    if x >= 0 and y >= 0 and x < qtdLinhas and y < qtdColunas:
        if grid[x][y] != '.':
            return letra(x,y)
    return None

def adjacente(x, y, grid):
    retorno = []
    diff = [-1,0,1]

    for diff_x in diff:
        for diff_y in diff:
            ret = _obtemAdjacente(x+diff_x, y+diff_y, grid)
            if ret:
                retorno.append(ret)

    return retorno



def f_recursiva_acha_palavra(palavra=[], letra=None, tamanho_palavra=-1, grid=None, contador=1):

    if grid[letra.x][letra.y] == '.':
        return None

    palavra.append(letra)

    if len(palavra) == tamanho_palavra:
        return palavra

    novo_grid = deepcopy(grid)
    novo_grid[letra.x][letra.y] = '.'

    for letra_adjacente in adjacente(letra.x, letra.y, novo_grid):
        nova_palavra = deepcopy(palavra)
        achou = f_recursiva_acha_palavra(palavra=nova_palavra, letra=letra_adjacente, tamanho_palavra=tamanho_palavra, grid=novo_grid, contador=contador + 1)
        if achou:
            listaPalavras.append(achou)
    return None


#---------------------------------------------------------------------------------




dicionario = []

listaPalavras = []
globalGrid = [
    ['b','o','o','n'],
    ['a','m','o','e'],
    ['l','b','o','t'],
    ['a','o','v','r'],
]




qtdLinhas = len(globalGrid)
qtdColunas = min(len(x) for x in globalGrid)





carregaDicionario()

print 'Total de palavras carregadas: %s ' % (len(dicionario))
print '=' * 30

print 'Grid para descobrir palavras:'

for linha in globalGrid:
    print linha

print '=' * 30

# Forca bruta
for x in range(0,qtdLinhas):
    for y in range(0,qtdColunas):
        inicio = letra(x,y)
        listaPalavras = []
        f_recursiva_acha_palavra(palavra=[], letra=inicio, tamanho_palavra=8, grid=globalGrid)
        printGrid(listaPalavras)
