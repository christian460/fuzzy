import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Desactivar la visualización automática
plt.ioff()

# Definir las variables de entrada y salida
num_autos = ctrl.Antecedent(np.arange(0, 101, 1), 'num_autos')
tiempo_verde = ctrl.Antecedent(np.arange(0, 101, 1), 'tiempo_verde')
cambiar_color = ctrl.Consequent(np.arange(0, 2, 1), 'cambiar_color')

# Definir las funciones de membresía para las variables de entrada y salida
num_autos['poco_congestionado'] = fuzz.trimf(num_autos.universe, [0, 0, 20])
num_autos['medio_congestionado'] = fuzz.trimf(num_autos.universe, [0, 20, 50])
num_autos['congestionado'] = fuzz.trimf(num_autos.universe, [20, 50, 100])

tiempo_verde['corto'] = fuzz.trimf(tiempo_verde.universe, [0, 0, 30])  # Ajustado a 30 segundos
tiempo_verde['medio'] = fuzz.trimf(tiempo_verde.universe, [10, 30, 60])  # Ajustado a 60 segundos con un mínimo de 10 segundos
tiempo_verde['largo'] = fuzz.trimf(tiempo_verde.universe, [30, 60, 100])  # Ajustado a 60 segundos

cambiar_color['no_cambiar'] = fuzz.trimf(cambiar_color.universe, [0, 0, 1])
cambiar_color['cambiar'] = fuzz.trimf(cambiar_color.universe, [1, 1, 1])

# Visualizar las funciones de membresía
num_autos.view()
tiempo_verde.view()
cambiar_color.view()

# Definir reglas difusas
regla1 = ctrl.Rule(num_autos['poco_congestionado'] & tiempo_verde['corto'], cambiar_color['cambiar'])
regla2 = ctrl.Rule(num_autos['poco_congestionado'] & tiempo_verde['medio'], cambiar_color['no_cambiar'])
regla3 = ctrl.Rule(num_autos['poco_congestionado'] & tiempo_verde['largo'], cambiar_color['no_cambiar'])
regla4 = ctrl.Rule(num_autos['medio_congestionado'] & tiempo_verde['corto'], cambiar_color['cambiar'])
regla5 = ctrl.Rule(num_autos['medio_congestionado'] & tiempo_verde['medio'], cambiar_color['no_cambiar'])
regla6 = ctrl.Rule(num_autos['medio_congestionado'] & tiempo_verde['largo'], cambiar_color['no_cambiar'])
regla7 = ctrl.Rule(num_autos['congestionado'] & tiempo_verde['corto'], cambiar_color['no_cambiar'])
regla8 = ctrl.Rule(num_autos['congestionado'] & tiempo_verde['medio'], cambiar_color['no_cambiar'])
regla9 = ctrl.Rule(num_autos['congestionado'] & tiempo_verde['largo'], cambiar_color['no_cambiar'])

# Crear el sistema difuso
sistema_semaforo = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9])
controlador_semaforo = ctrl.ControlSystemSimulation(sistema_semaforo)

# Menú para ingresar casos
while True:
    print("\nMenú:")
    print("1. Ingresar valores para num_autos y tiempo_verde")
    print("0. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        num_autos_valor = float(input("Ingrese el valor de num_autos (entre 0 y 20): "))
        tiempo_verde_valor = float(input("Ingrese el valor de tiempo_verde (entre 0 y 60): "))

        # Verificar restricciones
        if num_autos_valor > 20:
            print("\n¡Advertencia! El número de autos no debe ser mayor a 20.")
            continue
        elif tiempo_verde_valor > 60:
            print("\n¡Advertencia! El tiempo en verde no debe ser mayor a 60 segundos.")
            continue

        # Establecer valores de entrada
        controlador_semaforo.input['num_autos'] = num_autos_valor
        controlador_semaforo.input['tiempo_verde'] = tiempo_verde_valor

        # Computar la salida
        controlador_semaforo.compute()

        # Obtener el valor de salida
        cambiar_color_valor = controlador_semaforo.output['cambiar_color']

        # Verificar el tiempo mínimo en verde
        if cambiar_color_valor == 1 and tiempo_verde_valor < 10:
            print("\n¡Advertencia! El tiempo en verde es inferior a 10 segundos. No se cambiará el semáforo.")
            cambiar_color_valor = 0  # Establecer el valor en 0 para reflejar que no se debe cambiar

        # Imprimir el resultado
        cambiar_color_bool = bool(round(cambiar_color_valor))
        print("\n¿Cambiar de color el semáforo?:", cambiar_color_bool)

        # Visualizar la salida
        cambiar_color.view(sim=controlador_semaforo)

        # Mostrar los gráficos
        plt.show()

    elif opcion == "0":
        break

    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
