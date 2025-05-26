#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MensajesError:
    # Diccionario de errores comunes y sus sugerencias
    ERRORES_COMUNES = {
        # Errores de sintaxis básica
        ';': {
            'mensaje': 'Falta punto y coma (;) al final de la declaración',
            'sugerencia': 'Añade un punto y coma al final de la línea',
            'ejemplo': 'nombre: string; // Correcto\nnombre: string  // Incorrecto',
            'explicacion': 'En TypeScript, las declaraciones de propiedades en interfaces y clases deben terminar con punto y coma.'
        },
        '{': {
            'mensaje': 'Falta llave de apertura ({)',
            'sugerencia': 'Añade una llave de apertura para iniciar el bloque',
            'ejemplo': 'class MiClase { // Correcto\nclass MiClase  // Incorrecto',
            'explicacion': 'Las llaves de apertura son necesarias para definir bloques de código en TypeScript.'
        },
        '}': {
            'mensaje': 'Falta llave de cierre (})',
            'sugerencia': 'Añade una llave de cierre para terminar el bloque',
            'ejemplo': '} // Correcto\n  // Incorrecto (falta llave de cierre)',
            'explicacion': 'Cada llave de apertura debe tener su correspondiente llave de cierre.'
        },
        '(': {
            'mensaje': 'Falta paréntesis de apertura (()',
            'sugerencia': 'Añade un paréntesis de apertura para la expresión',
            'ejemplo': 'function saludar(nombre) { // Correcto\nfunction saludar nombre { // Incorrecto',
            'explicacion': 'Los paréntesis son necesarios para definir los parámetros de una función.'
        },
        ')': {
            'mensaje': 'Falta paréntesis de cierre ())',
            'sugerencia': 'Añade un paréntesis de cierre para la expresión',
            'ejemplo': 'return (a + b); // Correcto\nreturn (a + b  // Incorrecto',
            'explicacion': 'Cada paréntesis de apertura debe tener su correspondiente paréntesis de cierre.'
        },
        
        # Errores de TypeScript específicos
        ':': {
            'mensaje': 'Falta tipo en la declaración',
            'sugerencia': 'Añade el tipo después de los dos puntos, por ejemplo: : string',
            'ejemplo': 'let nombre: string; // Correcto\nlet nombre; // Incorrecto (falta tipo)',
            'explicacion': 'TypeScript requiere que las variables tengan un tipo explícito o inferido.'
        },
        '<': {
            'mensaje': 'Falta tipo genérico',
            'sugerencia': 'Añade el tipo genérico, por ejemplo: <T>',
            'ejemplo': 'class Contenedor<T> { // Correcto\nclass Contenedor< { // Incorrecto',
            'explicacion': 'Los tipos genéricos en TypeScript deben especificar el tipo entre < y >.'
        },
        '>': {
            'mensaje': 'Falta cierre de tipo genérico',
            'sugerencia': 'Cierra el tipo genérico con >',
            'ejemplo': 'Array<string> // Correcto\nArray<string  // Incorrecto',
            'explicacion': 'Los tipos genéricos deben cerrarse con > después de especificar el tipo.'
        },
        '@': {
            'mensaje': 'Decorador mal formado',
            'sugerencia': 'Añade un identificador después del @, por ejemplo: @Component',
            'ejemplo': '@Component() // Correcto\n@ // Incorrecto',
            'explicacion': 'Los decoradores en TypeScript deben tener un identificador después del símbolo @.'
        },
        
        # Errores de strings
        '"': {
            'mensaje': 'Cadena de texto sin cerrar',
            'sugerencia': 'Cierra la cadena con comillas dobles (")',
            'ejemplo': '"Hola mundo" // Correcto\n"Hola mundo // Incorrecto',
            'explicacion': 'Las cadenas de texto en TypeScript deben cerrarse con el mismo tipo de comillas con que se abrieron.'
        },
        "'": {
            'mensaje': 'Cadena de texto sin cerrar',
            'sugerencia': 'Cierra la cadena con comillas simples (\')',
            'ejemplo': "'Hola mundo' // Correcto\n'Hola mundo // Incorrecto",
            'explicacion': 'Las cadenas de texto en TypeScript deben cerrarse con el mismo tipo de comillas con que se abrieron.'
        },
        '`': {
            'mensaje': 'Template string sin cerrar',
            'sugerencia': 'Cierra el template string con backtick (`)',
            'ejemplo': '`Hola ${nombre}` // Correcto\n`Hola ${nombre} // Incorrecto',
            'explicacion': 'Los template strings en TypeScript deben cerrarse con backtick (`).'
        }
    }

    @staticmethod
    def obtener_mensaje_error(caracter, contexto=None):
        """
        Obtiene el mensaje de error y sugerencia para un carácter específico.
        
        Args:
            caracter: El carácter que causó el error
            contexto: Contexto adicional del error (opcional)
            
        Returns:
            Tupla con (mensaje_error, sugerencia, ejemplo, explicacion)
        """
        if caracter in MensajesError.ERRORES_COMUNES:
            error_info = MensajesError.ERRORES_COMUNES[caracter]
            mensaje = error_info['mensaje']
            sugerencia = error_info['sugerencia']
            ejemplo = error_info['ejemplo']
            explicacion = error_info['explicacion']
            
            if contexto:
                mensaje = f"{mensaje} - {contexto}"
            
            return mensaje, sugerencia, ejemplo, explicacion
        
        # Mensaje genérico para caracteres no reconocidos
        return (
            f"Carácter '{caracter}' no reconocido en TypeScript",
            "Verifica que el carácter sea válido en TypeScript",
            "Solo se permiten caracteres ASCII estándar y Unicode básico",
            "TypeScript no acepta caracteres especiales o símbolos no estándar"
        )

    @staticmethod
    def formatear_mensaje_error(numero, caracter, fila, columna, mensaje, sugerencia, ejemplo, explicacion):
        """
        Formatea un mensaje de error completo con número, posición y sugerencia.
        
        Args:
            numero: Número del error
            caracter: Carácter que causó el error
            fila: Número de fila
            columna: Número de columna
            mensaje: Mensaje de error
            sugerencia: Sugerencia de corrección
            ejemplo: Ejemplo de código correcto e incorrecto
            explicacion: Explicación detallada del error
            
        Returns:
            String con el mensaje formateado
        """
        return (
            f"{numero}. Error en Fila {fila}, Columna {columna}:\n"
            f"   Carácter: '{caracter}'\n"
            f"   Mensaje: {mensaje}\n"
            f"   Sugerencia: {sugerencia}\n"
            f"   Ejemplo:\n"
            f"     {ejemplo}\n"
            f"   Explicación: {explicacion}\n"
        ) 