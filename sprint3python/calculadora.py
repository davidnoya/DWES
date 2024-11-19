from operaciones import suma, resta, multiplicacion, division

def main():
    while True:
        print("Calculadora:")
        num1 = float(input("Introduce el primer número: "))
        num2 = float(input("Introduce el segundo número: "))
        print("Elige una operación:")
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicación")
        print("4. División")
        opcion = input("Opción: ")

        if opcion == "1":
            print(f"Resultado: {suma(num1, num2)}")
        elif opcion == "2":
            print(f"Resultado: {resta(num1, num2)}")
        elif opcion == "3":
            print(f"Resultado: {multiplicacion(num1, num2)}")
        elif opcion == "4":
            print(f"Resultado: {division(num1, num2)}")
        else:
            print("Opción no válida.")

        continuar = input("¿Deseas realizar otra operación? (s/n): ")
        if continuar.lower() != "s":
            break
        
if __name__ == "__main__":
    main()