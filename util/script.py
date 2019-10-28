from flask import *
from collections import OrderedDict

import pandas as pd 

app = Flask('contagilAppFlask', template_folder='template')

data = pd.read_csv('../data/NFCE.txt', sep="|")
df = pd.DataFrame(data, columns=['Chave_de_acesso','Valor_total_prod', 'Descricao_do_Produto_ou_servicos'])

@app.route("/")
def main():
    description = request.args.get('description')
    new_df = dataFrameAll()
    if description:
        new_df = dataFrame(str(description))
        return render_template('app.html', tables=[new_df.to_html(classes='data')], titles=df.columns.values), 200

    return render_template('app.html', tables=[new_df.to_html(classes='data')], titles=df.columns.values), 200

def keys(description, keys, ini, fin):
    if ini == fin and df['Descricao_do_Produto_ou_servicos'][i] == description:
        keys.append(df['Chave_de_acesso'][i])
    if ini != fin:
        mid = int(fin/2)
        keys(description, keys, ini, mid)
        keys(description, keys, mid+1, fin)

def allProdKeys(keys, description):
    allProd = []
    for key in keys:
        for el in (createList(key, description)):
            allProd.append(el)
    return allProd

def createList(key, description):
    array = []
    for i in range(len(df)):
        if df['Chave_de_acesso'][i] == key and df['Descricao_do_Produto_ou_servicos'][i] != description and df['Descricao_do_Produto_ou_servicos'][i] not in array:
            array.append(df.loc[i, 'Descricao_do_Produto_ou_servicos'])
    return array

def allProd(df):
    array = []
    for el in df:
        if el not in array:
            array.append(el)
    return array

def valueAcummulated(list):
    summ = []

    for el in list:
        count = 0
        for i in range(len(df)):
            if el == df['Descricao_do_Produto_ou_servicos'][i]:
                strg =  (df['Valor_total_prod'][i]).split(',')
                strg = strg[0] + "." + strg[1]
                count += float(strg)
        
        summ.append(count)
    return summ

def total(values):
    summ = 0
    for value in values:
        summ = summ + value
    return summ

def percent(value, total):
    count = value*100/total
    return (str(round(count, 2)) + "%")

def percentage(valueAcummulated):
    perc = []
    t = total(valueAcummulated)

    for value in valueAcummulated:
        p = percent(value, t)
        perc.append(p)

    return perc

def dataFrameAll():
    allProdList = allProd(df['Descricao_do_Produto_ou_servicos'].array)
    valueAcummulatedList = valueAcummulated(allProdList)
    percentageList = percentage(valueAcummulatedList)
    
    quicksort(valueAcummulatedList, allProdList, percentageList, 0, len(valueAcummulatedList))

    data = OrderedDict({
        'Descricao_do_Produto_ou_servicos': allProdList,
        'Valor_Acumulado': valueAcummulatedList,
        'Percentual': percentageList})

    return pd.DataFrame(data, columns=['Descricao_do_Produto_ou_servicos', 'Valor_Acumulado', 'Percentual'])

def dataFrame(description):
    keysList = []
    keys(description, keysList, 0, len(df))
    allProdList = allProdKeys(keysList, description)
    #valueAcummulatedList = valueAcummulated(allProdList)
    #percentageList = percentage(valueAcummulatedList)

    data = OrderedDict({'Descricao_do_Produto_ou_servicos': allProdList})

    return pd.DataFrame(data, columns=['Descricao_do_Produto_ou_servicos'])

def quicksort(array, arrayProd, arrayPerc, pivot, fin):
    if not(pivot == fin or pivot > fin or fin <= 0):

        indexP = division(pivot, array, arrayProd, arrayPerc, pivot+1, fin)
        if indexP == pivot:
            pivot = pivot+1

        quicksort(array,arrayProd, arrayPerc, indexP+1, fin)
        quicksort(array, arrayProd, arrayPerc, pivot, indexP-1)

def division(indexP, array, arrayProd, arrayPerc,i, j):
    if i >= len(array) or j<=0 or i > j:
        return indexP
    else:
        pivot = array[indexP]
        prod = arrayProd[indexP]
        perc = arrayPerc[indexP]

        if pivot > array[i]:
            return division(indexP, array, arrayProd, arrayPerc, i+1, j)
        else:
            if(indexP+1 != i):
                reorder(array, indexP+1, i)
                reorder(arrayProd, indexP+1, i)
                reorder(arrayPerc, indexP+1, i)

            array[indexP] = array[indexP+1]
            array[indexP+1] = pivot

            arrayProd[indexP] = arrayProd[indexP+1]
            arrayProd[indexP+1] = prod

            arrayPerc[indexP] = arrayPerc[indexP+1]
            arrayPerc[indexP+1] = perc

            return division(indexP+1, array, arrayProd, arrayPerc, i+1, j)

def reorder(array, i, j):
    if i < j:
        el = array[j]
        array[j] = array[j-1]
        array[j-1] = el
        reorder(array, i, j-1)
        
app.run(host='0.0.0.0', port=8080)
def imprime(lista):
    print('==========  Descricao_do_Produto_ou_servicos   ==========         \n')
    for el in lista:
        print(el)
        print('--------------------------------------------------------------------------------------------')

array = [9, 1, 4, 8, 10, 3, 13, 15.1, 12, 11, 0, 100000000000000000000, 9, 1, 4, 9, 1, 4, 8, 10, 3, 13, 15.9, 12, 11, 0, 8, 10, 3, 13, 9, 1, 4, 8, 10, 3, 13, 15, 12, 11, 0, 15, 12, 11, 9, 1, 4, 8, 10, 3, 13, 15.1, 12, 11, 0, 100000000000000000000, 9, 1, 4, 9, 1, 4, 8, 10, 3, 13, 15.9, 12, 11, 0, 8, 10, 3, 13, 9, 1, 4, 8, 10, 3, 13, 9, 1, 4, 8, 10, 3, 13, 15.1, 12, 11, 0, 100000000000000000000, 9, 1, 4, 9, 1, 4, 8, 10, 3, 13, 15.9, 12, 11, 0, 8, 10, 3, 13, 9, 1, 4, 8, 10, 3, 13, 15, 9, 1, 4, 8, 10, 3, 13, 15.1, 12, 11, 0, 100000000000000000000, 9, 1, 4, 9, 1, 4, 8, 10, 3, 13, 15.9, 12, 11, 0, 8, 10, 3, 13, 9, 1, 4, 8, 10, 3, 13, 15, 12, 11, 0, 15, 12, 11, 0, 9, 1, 4, 8, 10, 3, 13, 15, 12, 11, 0, 12, 11, 0, 15, 12, 11, 0, 9, 1, 4, 8, 10, 3, 13, 15, 12, 11, 0, 15, 12, 11, 0, 15, 12, 11, 0, 9, 1, 4, 8, 10, 3, 13, 15, 12, 11, 0, 0, 9, 1, 4, 8, 10, 3, 13, 15, 12, 11, 0]
quicksort(array, 0, len(array))
print(array)