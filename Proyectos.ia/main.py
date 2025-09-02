X = float(input("diga el numero X:"))
Y = float(input("diga el numero Y:"))
print("Diga la Operacion que quiere Realizar a continuacion--->")
print("Presione 1 para Suma \n"
      "Presione 2 para Resta \n"
      "Presione 3 para Multiplicacion \n"
      "Presione 4 para Division ")
Op = int(input("Digite su Opcion "))
if(Op.is_integer()==False):print("esa no es una opcion valida")
elif (Op < 1 or Op > 4): print("Esa no era una opcion valida")
elif (Op == 1):
    print("El resultado de dicha suma es:", (X + Y))
elif (Op == 2):
    print("El resultado de dicha resta es:", (X - Y))
elif (Op == 3):
    print("El resultado de multiplicacion es:", (X * Y))
elif (Op == 4):
    if(Y==0):print("No se puede dividir entre 0")
    print("El resultado de division es:", (X / Y))
