#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MensajesError:
    # Diccionario de errores comunes y sus sugerencias
    ERRORES_COMUNES = {
        # Errores de sintaxis básica
        ';': {
            'mensaje': 'Falta punto y coma (;) al final de la declaración',
            'sugerencia': 'Añade un punto y coma al final de la línea'
        },
        '{': {
            'mensaje': 'Falta llave de apertura ({)',
            'sugerencia': 'Añade una llave de apertura para iniciar el bloque'
        },
        '}': {
            'mensaje': 'Falta llave de cierre (})',
            'sugerencia': 'Añade una llave de cierre para terminar el bloque'
        },
        '(': {
            'mensaje': 'Falta paréntesis de apertura (()',
            'sugerencia': 'Añade un paréntesis de apertura para la expresión'
        },
        ')': {
            'mensaje': 'Falta paréntesis de cierre ())',
            'sugerencia': 'Añade un paréntesis de cierre para la expresión'
        },
        
        # Errores de TypeScript específicos
        ':': {
            'mensaje': 'Falta tipo en la declaración',
            'sugerencia': 'Añade el tipo después de los dos puntos, por ejemplo: : string'
        },
        '<': {
            'mensaje': 'Falta tipo genérico',
            'sugerencia': 'Añade el tipo genérico, por ejemplo: <T>'
        },
        '>': {
            'mensaje': 'Falta cierre de tipo genérico',
            'sugerencia': 'Cierra el tipo genérico con >'
        },
        '@': {
            'mensaje': 'Decorador mal formado',
            'sugerencia': 'Añade un identificador después del @, por ejemplo: @Component'
        },
        
        # Errores de strings
        '"': {
            'mensaje': 'Cadena de texto sin cerrar',
            'sugerencia': 'Cierra la cadena con comillas dobles (")'
        },
        "'": {
            'mensaje': 'Cadena de texto sin cerrar',
            'sugerencia': 'Cierra la cadena con comillas simples (\')'
        },
        '`': {
            'mensaje': 'Template string sin cerrar',
            'sugerencia': 'Cierra el template string con backtick (`)'
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
            Tupla con (mensaje_error, sugerencia)
        """
        if caracter in MensajesError.ERRORES_COMUNES:
            error_info = MensajesError.ERRORES_COMUNES[caracter]
            mensaje = error_info['mensaje']
            sugerencia = error_info['sugerencia']
            
            if contexto:
                mensaje = f"{mensaje} - {contexto}"
            
            return mensaje, sugerencia
        
        # Mensaje genérico para caracteres no reconocidos
        return (
            f"Carácter '{caracter}' no reconocido en TypeScript",
            "Verifica que el carácter sea válido en TypeScript"
        )

    @staticmethod
    def formatear_mensaje_error(numero, caracter, fila, columna, mensaje, sugerencia):
        """
        Formatea un mensaje de error completo con número, posición y sugerencia.
        
        Args:
            numero: Número del error
            caracter: Carácter que causó el error
            fila: Número de fila
            columna: Número de columna
            mensaje: Mensaje de error
            sugerencia: Sugerencia de corrección
            
        Returns:
            String con el mensaje formateado
        """
        return (
            f"{numero}. Error en Fila {fila}, Columna {columna}:\n"
            f"   Carácter: '{caracter}'\n"
            f"   Mensaje: {mensaje}\n"
            f"   Sugerencia: {sugerencia}\n"
        ) 