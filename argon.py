import re
import tkinter as tk
from tkinter import messagebox

class ArgonParser:
    def __init__(self, entrada):
        self.entrada = entrada.strip()
        self.indice = 0
        self.error = None

    def consumir_espacios(self):
        while self.indice < len(self.entrada) and self.entrada[self.indice].isspace():
            self.indice += 1

    def match(self, pattern):
        self.consumir_espacios()
        match_obj = re.match(pattern, self.entrada[self.indice:])
        if match_obj:
            self.indice += match_obj.end()
            return match_obj.group(0).strip()
        return None

    def declaracion_variable(self):
        tipo = self.match(r'(int|float|bool|string|char)')
        if tipo:
            nombre = self.match(r'[a-zA-Z][a-zA-Z0-9]*')
            if nombre:
                if self.match(r':'):
                    if self.match(r'='):
                        if tipo in ['int', 'float']:
                            valor = self.match(r'\d+(\.\d+)?')
                        elif tipo == 'bool':
                            valor = self.match(r'(true|false)')
                        elif tipo == 'string':
                            valor = self.match(r'"[^"]*"')
                        elif tipo == 'char':
                            valor = self.match(r"'.'")
                        if valor:
                            return True
                        else:
                            self.error = f'Error: valor incorrecto para la variable {nombre}'
                            return False
                    else:
                        self.error = f'Error: falta el signo igual en la asignación de valor para la variable {nombre}'
                        return False
                else:
                    self.error = f'Error: falta el signo dos puntos para la variable {nombre}'
                    return False
            else:
                self.error = f'Error: nombre de variable inválido'
                return False
        else:
            self.error = f'Error: tipo de variable no reconocido'
            return False

    def funcion(self):
        if self.match(r'function'):
            nombre_funcion = self.match(r'[a-zA-Z][a-zA-Z0-9]*')
            if nombre_funcion:
                if self.match(r'\('):
                    if self.match(r'\)'):
                        if self.match(r':'):
                            if self.match(r'\{'):
                                while self.contenido():
                                    pass
                                if self.match(r'\}'):
                                    return True
                            else:
                                self.error = 'Error: se esperaba una llave de apertura para el cuerpo de la función'
                                return False
                        else:
                            self.error = f'Error: falta el signo dos puntos en la definición de la función {nombre_funcion}'
                            return False
                    else:
                        self.error = 'Error: se esperaba un signo paréntesis de cierre luego del nombre de la función'
                        return False
                else:
                    self.error = 'Error: se esperaba un signo paréntesis de apertura luego del nombre de la función'
                    return False
            else:
                self.error = 'Error: se esperaba un nombre de función válido'
                return False
        else:
            return False

    def ciclo(self):
        if self.match(r'loop'):
            if self.match(r'\('):
                condicion = self.comparacion()
                if condicion:
                    if self.match(r'\)'):
                        if self.match(r':'):
                            if self.match(r'\{'):
                                while self.contenido():
                                    pass
                                if self.match(r'\}'):
                                    return True
                            else:
                                self.error = 'Error: se esperaba una llave de apertura para el cuerpo del ciclo'
                                return False
                        else:
                            self.error = 'Error: se esperaba un signo dos puntos después de la condición del ciclo'
                            return False
                    else:
                        self.error = 'Error: se esperaba un signo paréntesis de cierre luego de la condición del ciclo'
                        return False
                else:
                    self.error = 'Error: se esperaba una comparación para la condición del ciclo'
                    return False
            else:
                self.error = 'Error: se esperaba un signo paréntesis de apertura para la condición del ciclo'
                return False
        else:
            return False

    def condicional(self):
        if self.match(r'assuming'):
            condicion = self.comparacion()
            if condicion:
                if self.match(r':'):
                    if self.match(r'\{'):
                        while self.contenido():
                            pass
                        if self.match(r'\}'):
                            if self.elif_condicional():
                                return True
                            elif self.match(r'otherwise'):
                                if self.match(r':'):
                                    if self.match(r'\{'):
                                        while self.contenido():
                                            pass
                                        if self.match(r'\}'):
                                            return True
                                    else:
                                        self.error = 'Error: se esperaba una llave de apertura para el cuerpo del bloque "otherwise"'
                                        return False
                                else:
                                    self.error = 'Error: se esperaba un signo dos puntos después del bloque "otherwise"'
                                    return False
                            else:
                                return True
                    else:
                        self.error = 'Error: se esperaba una llave de apertura para el cuerpo del bloque "assuming"'
                        return False
                else:
                    self.error = 'Error: se esperaba un signo dos puntos después de la condición del bloque "assuming"'
                    return False
            else:
                self.error = 'Error: se esperaba una comparación para la condición del bloque "assuming"'
                return False
        else:
            return False

    def elif_condicional(self):
        if self.match(r'elif'):
            condicion = self.comparacion()
            if condicion:
                if self.match(r':'):
                    if self.match(r'\{'):
                        while self.contenido():
                            pass
                        if self.match(r'\}'):
                            if self.elif_condicional():
                                return True
                            elif self.match(r'otherwise'):
                                if self.match(r':'):
                                    if self.match(r'\{'):
                                        while self.contenido():
                                            pass
                                        if self.match(r'\}'):
                                            return True
                                    else:
                                        self.error = 'Error: se esperaba una llave de apertura para el cuerpo del bloque "otherwise"'
                                        return False
                                else:
                                    self.error = 'Error: se esperaba un signo dos puntos después del bloque "otherwise"'
                                    return False
                            else:
                                return True
                    else:
                        self.error = 'Error: se esperaba una llave de apertura para el cuerpo del bloque "elif"'
                        return False
                else:
                    self.error = 'Error: se esperaba un signo dos puntos después de la condición del bloque "elif"'
                    return False
            else:
                self.error = 'Error: se esperaba una comparación para la condición del bloque "elif"'
                return False
        else:
            return False

    def contenido(self):
        return self.declaracion_variable() or self.funcion() or self.ciclo() or self.condicional()

    def comparacion(self):
        operadores = r'(==|!=|<=|>=|<|>)'
        izquierda = self.match(r'[a-zA-Z][a-zA-Z0-9]*')
        if izquierda:
            resto_izquierda = self.match(r'[a-zA-Z0-9]*')
            while resto_izquierda:
                izquierda += resto_izquierda
                resto_izquierda = self.match(r'[a-zA-Z0-9]*')
            if self.match(operadores):
                derecha = self.match(r'[a-zA-Z][a-zA-Z0-9]*')
                if derecha:
                    resto_derecha = self.match(r'[a-zA-Z0-9]*')
                    while resto_derecha:
                        derecha += resto_derecha
                        resto_derecha = self.match(r'[a-zA-Z0-9]*')
                    return True
                else:
                    self.error = 'Error: se esperaba un identificador después del operador de comparación'
                    return False
            else:
                self.error = 'Error: se esperaba un operador de comparación después del identificador'
                return False
        else:
            valor = self.match(r'[0-9]+(\.[0-9]+)?')
            if valor:
                if self.match(operadores):
                    izquierda = self.match(r'[a-zA-Z][a-zA-Z0-9]*')
                    if izquierda:
                        resto_izquierda = self.match(r'[a-zA-Z0-9]*')
                        while resto_izquierda:
                            izquierda += resto_izquierda
                            resto_izquierda = self.match(r'[a-zA-Z0-9]*')
                        return True
                    else:
                        self.error = 'Error: se esperaba un identificador después del operador de comparación'
                        return False
                else:
                    self.error = 'Error: se esperaba un operador de comparación después del valor numérico'
                    return False
            else:
                self.error = 'Error: se esperaba un identificador o valor numérico en la comparación'
                return False

    def analizar(self):
        while self.indice < len(self.entrada):
            if not self.contenido():
                self.error = f'Error de sintaxis en la posición {self.indice}: {self.entrada[self.indice:]}'
                return False
        return True

class ArgonApp:
    def __init__(self, root):
        self.parser = ArgonParser('')
        self.text = tk.Text(root, width=40, height=10)
        self.text.pack(padx=10, pady=10)
        self.validate_button = tk.Button(root, text="Validar", command=self.validate)
        self.validate_button.pack(pady=5)
        self.grammar_label = tk.Label(root, text="Cuando presione validar verá un mensaje que afirme si fue correcta su entrada, si hay error se indicará. Entiéndase 'po' como posición")
        self.grammar_label.pack(pady=10)

    def validate(self):
        code = self.text.get("1.0", tk.END).strip()
        self.parser = ArgonParser(code)
        is_valid = self.parser.analizar()
        if is_valid:
            messagebox.showinfo("Validación", "El código es válido según la gramática de Argon.")
        else:
            messagebox.showerror(
                "Error", f'{self.parser.error}\nLa posición del error es: po{self.parser.indice}'
            )

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Validador de Gramática Argon")
    app = ArgonApp(root)
    root.mainloop()
