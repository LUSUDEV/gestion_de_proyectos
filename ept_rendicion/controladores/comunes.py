def get_select_porcentaje(desde,hasta):
    porc=[]
    for i in range(desde,hasta):
        porc.append((str(i),str(i)+'%'))
    return porc


def compara_movimientos(x, y) :
    # x e y son objetos de los que se desea ordenar
        if x.create_date < y.create_date :
          rst = -1
        elif x.create_date > y.create_date :
          rst = 1
        else :
          rst = 0
        return rst
        
        
def compara(x, y) :
    # x e y son objetos de los que se desea ordenar
        if x.sequence < y.sequence :
          rst = -1
        elif x.sequence > y.sequence :
          rst = 1
        else :
          rst = 0
        return rst
        
def compara_o2m(x, y) :
    # x e y son objetos de los que se desea ordenar
        if x[0] > y[0] :
          rst = -1
        elif x[0] < y[0] :
          rst = 1
        else :
          rst = 0

        return rst
