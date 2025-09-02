X = float(input("diga el numero X:"))
Y = float(input("diga el numero Y:"))
print("Diga la Operacion que quiere Realizar a continuacion--->")
print("Presione 1 para Suma \n"
      "Presione 2 para Resta \n"
      "Presione 3 para Multiplicacion \n"
      "Presione 4 para Division ")
Op = int(input("Digite su Opcion "))
if (Op < 1 | Op > 4): print("Esa no era una opcion valida")
if (Op == 1):
    print("El resultado de dicha suma es:", (X + Y))
elif (Op == 2):
    print("El resultado de dicha resta es:", (X - Y))
elif (Op == 3):
    print("El resultado de multiplicacion es:", (X * Y))
elif (Op == 4):
    print("El resultado de division es:", (X / Y))
