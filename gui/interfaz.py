import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

# Añadir la raíz del proyecto al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analizadores.identificador import IdentificadorAFD
from lexer import AnalizadorLexico
from tokens import Categoria
from gui.mensajes_error import MensajesError

class InterfazLexer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico - TypeScript")
        self.root.geometry("1200x800")  # Ventana más grande
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Definir colores para categorías de tokens
        self.colores_categoria = {
            Categoria.PALABRA_RESERVADA: "blue",
            Categoria.IDENTIFICADOR: "black",
            Categoria.NUMERO_NATURAL: "dark green",
            Categoria.NUMERO_REAL: "green",
            Categoria.CADENA: "purple",
            Categoria.COMENTARIO_LINEA: "gray",
            Categoria.COMENTARIO_BLOQUE: "gray",
            Categoria.OPERADOR_ARITMETICO: "orange red",
            Categoria.OPERADOR_COMPARACION: "orange red",
            Categoria.OPERADOR_LOGICO: "orange red",
            Categoria.OPERADOR_ASIGNACION: "orange red",
            Categoria.OPERADOR_INCREMENTO: "orange red",
            Categoria.OPERADOR_DECREMENTO: "orange red",
            Categoria.OPERADOR_ACCESO: "dark orange",
            Categoria.PARENTESIS_APERTURA: "dark cyan",
            Categoria.PARENTESIS_CIERRE: "dark cyan",
            Categoria.LLAVE_APERTURA: "dark cyan",
            Categoria.LLAVE_CIERRE: "dark cyan",
            Categoria.CORCHETE_APERTURA: "dark slate gray",
            Categoria.CORCHETE_CIERRE: "dark slate gray",
            Categoria.DOS_PUNTOS: "firebrick",
            Categoria.SIGNO_INTERROGACION: "purple4",
            Categoria.OPERADOR_OPTIONAL_CHAINING: "orchid",
            Categoria.OPERADOR_NULISH_COALESCING: "orchid",
            Categoria.TERMINAL: "magenta",
            Categoria.SEPARADOR: "magenta",
            Categoria.TIPO: "magenta",
            Categoria.DECORADOR: "magenta",
            Categoria.GENERICO: "magenta",
            Categoria.MODIFICADOR_ACCESO: "magenta",
            Categoria.ANGULAR_APERTURA: "dark cyan",
            Categoria.ANGULAR_CIERRE: "dark cyan",
            Categoria.ERROR: "red"
        }
        
        # Configuración de la interfaz
        self.configure_ui()
        
        # Inicializar analizador léxico
        self.analizador = AnalizadorLexico()
        
        # Configurar eventos del editor
        self.editor.bind('<KeyRelease>', self.resaltar_sintaxis)
        
    def configurar_estilo(self):
        """Configura el estilo visual de la interfaz"""
        style = ttk.Style()
        
        # Configurar colores y estilos
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))
        style.configure("TButton", font=("Arial", 10))
        style.configure("Treeview", font=("Consolas", 9))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
    def configure_ui(self):
        """Configura todos los elementos de la interfaz gráfica"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo para el editor
        left_frame = ttk.LabelFrame(main_frame, text="Editor de Código TypeScript", padding="5")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Barra de herramientas del editor
        toolbar = ttk.Frame(left_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        self.btn_analizar = ttk.Button(toolbar, text="Analizar Código", command=self.analizar_codigo)
        self.btn_analizar.pack(side=tk.LEFT, padx=(0, 5))
        
        self.btn_limpiar = ttk.Button(toolbar, text="Limpiar", command=self.limpiar)
        self.btn_limpiar.pack(side=tk.LEFT)
        
        # Editor con fuente monoespaciada
        self.editor = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            width=50,
            height=30,
            font=("Consolas", 11)
        )
        self.editor.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para resaltado de sintaxis
        for categoria, color in self.colores_categoria.items():
            self.editor.tag_configure(categoria, foreground=color)
        
        # Panel derecho para resultados
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Panel para la tabla de Tokens
        tokens_frame = ttk.LabelFrame(right_frame, text="Tokens Identificados", padding="5")
        tokens_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Configurar tabla de tokens
        columns = ("lexema", "categoria", "fila", "columna")
        self.tabla_tokens = ttk.Treeview(
            tokens_frame,
            columns=columns,
            show="headings",
            height=10
        )
        
        # Configurar encabezados
        self.tabla_tokens.heading("lexema", text="Lexema")
        self.tabla_tokens.heading("categoria", text="Categoría")
        self.tabla_tokens.heading("fila", text="Fila")
        self.tabla_tokens.heading("columna", text="Columna")
        
        # Configurar columnas
        self.tabla_tokens.column("lexema", width=150, anchor=tk.W)
        self.tabla_tokens.column("categoria", width=150, anchor=tk.W)
        self.tabla_tokens.column("fila", width=50, anchor=tk.CENTER)
        self.tabla_tokens.column("columna", width=50, anchor=tk.CENTER)
        
        # Configurar tags para colores
        for categoria, color in self.colores_categoria.items():
            tag_name = categoria.split('.')[-1] if '.' in categoria else categoria
            self.tabla_tokens.tag_configure(tag_name, foreground=color)
        
        # Scrollbar para la tabla
        scrollbar_tokens = ttk.Scrollbar(tokens_frame, orient=tk.VERTICAL, command=self.tabla_tokens.yview)
        self.tabla_tokens.configure(yscroll=scrollbar_tokens.set)
        
        self.tabla_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tokens.pack(side=tk.RIGHT, fill=tk.Y)

        # Panel para Errores Léxicos
        errores_frame = ttk.LabelFrame(right_frame, text="Errores Léxicos", padding="5")
        errores_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de texto para errores con fuente monoespaciada
        self.texto_errores = scrolledtext.ScrolledText(
            errores_frame,
            wrap=tk.WORD,
            width=40,
            height=10,
            font=("Consolas", 10),
            state=tk.DISABLED
        )
        self.texto_errores.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para errores
        self.texto_errores.tag_configure("error", foreground="red")
        self.texto_errores.tag_configure("sugerencia", foreground="blue")
        self.texto_errores.tag_configure("posicion", foreground="dark green")
        self.texto_errores.tag_configure("ejemplo", foreground="purple")
        self.texto_errores.tag_configure("explicacion", foreground="dark gray")
             
    def analizar_codigo(self):
        """Analiza el código completo usando el analizador léxico"""
        self.limpiar_resultados()
        
        codigo = self.editor.get("1.0", tk.END)
        if not codigo.strip():
            messagebox.showinfo("Aviso", "Por favor ingresa código para analizar.")
            return
            
        tokens, errores = self.analizador.analizar(codigo)
        
        # Mostrar tokens en la tabla
        for token in tokens:
            categoria_completa = token.categoria
            categoria_simple = categoria_completa.split('.')[-1] if '.' in categoria_completa else categoria_completa
            tag_aplicar = categoria_simple
            
            self.tabla_tokens.insert("", "end", values=(
                token.lexema, 
                categoria_simple,
                token.fila, 
                token.columna
            ), tags=(tag_aplicar,))
        
        # Mostrar errores en el panel de errores
        self.texto_errores.config(state=tk.NORMAL)
        self.texto_errores.delete("1.0", tk.END)
        if errores:
            for i, error in enumerate(errores, 1):
                # Obtener mensaje y sugerencia para el error
                mensaje, sugerencia, ejemplo, explicacion = MensajesError.obtener_mensaje_error(error.lexema)
                
                # Formatear el mensaje completo
                mensaje_completo = MensajesError.formatear_mensaje_error(
                    i, error.lexema, error.fila, error.columna,
                    mensaje, sugerencia, ejemplo, explicacion
                )
                
                # Insertar el mensaje con los tags apropiados
                self.texto_errores.insert(tk.END, f"{i}. Error en ", "posicion")
                self.texto_errores.insert(tk.END, f"Fila {error.fila}, Columna {error.columna}:\n", "posicion")
                self.texto_errores.insert(tk.END, f"   Carácter: '{error.lexema}'\n", "error")
                self.texto_errores.insert(tk.END, f"   Mensaje: {mensaje}\n", "error")
                self.texto_errores.insert(tk.END, f"   Sugerencia: {sugerencia}\n", "sugerencia")
                self.texto_errores.insert(tk.END, f"   Ejemplo:\n", "ejemplo")
                self.texto_errores.insert(tk.END, f"     {ejemplo}\n", "ejemplo")
                self.texto_errores.insert(tk.END, f"   Explicación: {explicacion}\n", "explicacion")
                self.texto_errores.insert(tk.END, "\n")
            
            messagebox.showwarning(
                "Errores Léxicos Encontrados", 
                f"Se encontraron {len(errores)} errores léxicos. Revise el panel de errores."
            )
        else:
            self.texto_errores.insert(tk.END, "No se encontraron errores léxicos.\n")
        self.texto_errores.config(state=tk.DISABLED)
    
    def resaltar_sintaxis(self, event=None):
        """Resalta la sintaxis del código en tiempo real"""
        # Obtener el código actual
        codigo = self.editor.get("1.0", tk.END)
        
        # Limpiar todos los tags
        for tag in self.colores_categoria.keys():
            self.editor.tag_remove(tag, "1.0", tk.END)
        
        # Analizar el código
        tokens, _ = self.analizador.analizar(codigo)
        
        # Aplicar resaltado
        for token in tokens:
            # Calcular la posición del token
            start_pos = f"{token.fila}.{token.columna-1}"
            end_pos = f"{token.fila}.{token.columna-1+len(token.lexema)}"
            
            # Aplicar el tag correspondiente
            self.editor.tag_add(token.categoria, start_pos, end_pos)
    
    def limpiar_tabla_tokens(self):
        """Limpia la tabla de tokens"""
        for item in self.tabla_tokens.get_children():
            self.tabla_tokens.delete(item)

    def limpiar_panel_errores(self):
        """Limpia el panel de errores"""
        self.texto_errores.config(state=tk.NORMAL)
        self.texto_errores.delete("1.0", tk.END)
        self.texto_errores.config(state=tk.DISABLED)
            
    def limpiar_resultados(self):
        self.limpiar_tabla_tokens()
        self.limpiar_panel_errores()

    def limpiar(self):
        """Limpia editor y todos los resultados"""
        self.editor.delete("1.0", tk.END)
        self.limpiar_resultados()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLexer(root)
    root.mainloop()