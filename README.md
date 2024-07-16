# Exam2-Software

## Integrantes:
- Fabrizzio Vilchez Espinoza
- Jeffrey Monja Castro

## Pregunta 1

El código se realizó en el framework de `FastAPI`. Los códigos se encuentran en la carpeta `backend/main.py`.

Para ejecutar el servidor de backend, correr el siguiente comando: 

```bash
./run.bat
```

Esto ejecutará el servidor en el puerto 8000.

En la carpeta raíz se encuentra una colección de postman para probar la API.

## Pregunta 2

Para ejecutar los test, dirigirse a la carpeta `test` y ejecutar el siguiente comando:

```bash
pytest ./unit_test.py
```


## Respuestas de la pregunta 3

### Cambios necesarios en el código

Para soportar un valor máximo de 200 soles a transferir por día, se necesitarían los siguientes cambios en el código:

1. **Clase `UsuarioDB`**:
   - **Añadir un campo para el total transferido en el día actual**: Se necesitaría un nuevo campo para rastrear cuánto ha transferido el usuario en el día actual.
   - **Añadir un campo para la fecha del último reinicio del contador diario**: Otro campo sería necesario para almacenar la fecha en que se reseteó por última vez el contador diario de transferencias.

2. **Método `pagar`**:
   - **Reiniciar el contador diario si es necesario**: Verificar si la fecha actual es diferente de la fecha almacenada del último reinicio. Si es diferente, reiniciar el contador diario de transferencias y actualizar la fecha del último reinicio.
   - **Verificar el límite de transferencia diaria**: Antes de realizar una transferencia, comprobar si la cantidad a transferir, sumada a la cantidad ya transferida en el día, excede los 200 soles. Si excede, rechazar la operación con un mensaje de error adecuado.
   - **Actualizar el contador diario de transferencias**: Si la transferencia es válida, actualizar el campo que rastrea el total transferido en el día.

### Nuevos casos de prueba necesarios:

1. **Transferencia menor al límite diario**:
   - Realizar una transferencia que no exceda el límite diario de 200 soles y verificar que se realice con éxito.

2. **Transferencia que excede el límite diario**:
   - Intentar realizar una transferencia que, sumada a las transferencias anteriores del día, exceda los 200 soles. Verificar que la transferencia se rechace con un mensaje de error adecuado.

3. **Varias transferencias dentro del límite diario**:
   - Realizar múltiples transferencias en un mismo día, asegurándose de que la suma total no exceda los 200 soles. Verificar que todas las transferencias se realicen con éxito.

4. **Reinicio del contador diario**:
   - Realizar una transferencia después de que haya pasado un día desde la última transferencia. Verificar que el contador diario se reinicie y la transferencia se realice con éxito.

### Garantía de que los casos de prueba existentes no introduzcan errores:

Para asegurar que los cambios no introduzcan errores en la funcionalidad existente, se deben seguir estos pasos:

1. **Ejecución de casos de prueba existentes**:
   - Ejecutar todos los casos de prueba actuales para verificar que continúan funcionando correctamente tras los cambios.

2. **Cobertura de pruebas**:
   - Revisar la cobertura de las pruebas para asegurarse de que todas las rutas y lógicas críticas del sistema están cubiertas.

3. **Pruebas de regresión**:
   - Realizar pruebas de regresión para identificar cualquier fallo introducido por los nuevos cambios. Esto incluye la verificación de que las funcionalidades básicas (creación de usuario, obtención de contactos, realización de pagos, consulta de historial) funcionan como se espera.

4. **Revisión de código**:
   - Realizar revisiones de código para verificar que los cambios no introduzcan efectos secundarios no deseados y que sigan las buenas prácticas de desarrollo.