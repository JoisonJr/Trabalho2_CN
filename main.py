import tkinter as tk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox, filedialog
from metodos import *

# Configuração global do matplotlib (modo escuro)
plt.style.use("dark_background")

# ==========================
# Interface principal
# ==========================

class Aplicativo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Projeto Unidade 2 - Cálculo Numérico")
        self.geometry("1100x700")
        self.configure(bg="#1E1E1E")
        self._estilo_dark()
        self._montar_interface()

    def _estilo_dark(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background="#1E1E1E")
        style.configure("TLabel", background="#1E1E1E", foreground="white", font=("Segoe UI", 11))

        style.configure("Instruction.TLabel",
                        background="#1E1E1E",
                        foreground="#DCDCDC",
                        font=("Segoe UI", 12))

        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, relief="flat",
                        background="#333333", foreground="white")
        style.map("TButton",
                  background=[("active", "#4E4E4E"), ("pressed", "#5E5E5E")],
                  foreground=[("disabled", "#777777")])
        style.configure("TEntry", fieldbackground="#2E2E2E", foreground="white")

    def _montar_interface(self):
        COR_FUNDO_LATERAL = "#2c3e50"
        COR_BOTAO_NORMAL = "#3498db"
        COR_BOTOES_HOVER = "#2980b9"
        COR_TEXTO_BOTAO = "#ffffff"
        COR_TEXTO_LATERAL = "#ecf0f1"

        style = ttk.Style(self)

        style.configure('Sidebar.TFrame', background=COR_FUNDO_LATERAL)
        style.configure('MenuTitle.TLabel',
                        background=COR_FUNDO_LATERAL, foreground=COR_TEXTO_LATERAL, font=("TkDefaultFont", 18, "bold")
                        )
        style.configure('MenuButton.TButton',
                        borderwidth=3, padding=12, relief="flat", background=COR_BOTAO_NORMAL,
                        foreground=COR_TEXTO_BOTAO, font=("TkDefaultFont", 10, "bold")
                        )
        style.map('MenuButton.TButton', background=[('active', COR_BOTOES_HOVER)], relief=[('active', 'raised')])

        # Painel lateral
        lateral = ttk.Frame(self, width=250, style='Sidebar.TFrame')
        lateral.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(lateral, text="📘 Menu de Tópicos", style='MenuTitle.TLabel').pack(pady=(80, 40))

        # mudança nos nomes dos tópicos 2 e 4, de maneira que seguissem o "formato":
        # título (tipo de método utilizado)
        botoes = [
            ("Tópico 1 - Sistemas Lineares (Direto)", self.topico1),
            ("Tópico 2 - Ponte de Wheatstone (Gauss-Siedel)", self.topico2),
            ("Tópico 3 - Lei de Moore (Regressão)", self.topico3),
            ("Tópico 4 - Integração Numérica (Trapézio e Simpson repetidas)", self.topico4)
        ]

        for txt, cmd in botoes:
            ttk.Button(
                lateral, text=txt, command=cmd, style='MenuButton.TButton'
            ).pack(fill=tk.X, pady=8, padx=15)

        # Área principal
        self.area_principal = ttk.Frame(self)
        self.area_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.area_principal,
                  text="Selecione um tópico à esquerda para começar.",
                  font=("Segoe UI", 14, "bold"), foreground="#00BFFF").pack(pady=50)

    def limpar_area(self):
        for w in self.area_principal.winfo_children():
            w.destroy()

    # ==========================
    # Tópico 1 – Sistemas Diretos
    # ==========================
    def topico1(self):
        self.limpar_area()
        ttk.Label(self.area_principal, text="Tópico 1 – Sistema Linear (Método Direto)",
                  font=("Segoe UI", 22, "bold"), foreground="#00BFFF").pack(pady=15)

        ttk.Label(self.area_principal,
                  text="Insira os coeficientes do sistema (3x3) e o vetor de necessidades.",
                  style='Instruction.TLabel').pack()

        quadro = ttk.Frame(self.area_principal)
        quadro.pack(pady=8)
        entradas = [[ttk.Entry(quadro, width=10) for _ in range(3)] for _ in range(3)]
        # definição das entradas na grade do aplicativo
        for i, linha in enumerate(entradas):
            for j, e in enumerate(linha):
                e.grid(row=i, column=j, padx=4, pady=4)
        # valores padrão para os limites
        rhs_vars = [tk.StringVar(value=v) for v in ("4800", "5800", "5700")]
        frame_rhs = ttk.Frame(self.area_principal)
        frame_rhs.pack(pady=6)
        ttk.Label(frame_rhs, text="Necessidades (areia, fino, grosso): ").pack(side=tk.LEFT)
        # entradas para a matriz coluna b
        rhs_entradas = [ttk.Entry(frame_rhs, width=8, textvariable=v) for v in rhs_vars]
        for e in rhs_entradas:
            e.pack(side=tk.LEFT, padx=3)
        # criação da caixa de texto da saída
        saida = tk.Text(self.area_principal, height=6, bg="#2A2A2A", fg="white", relief="ridge",
                        font=("TkDefaultFon", 10))
        saida.pack(fill=tk.X, pady=8)

        # dá a opção de utilizaro exemplo já presente no tópico
        def preencher_exemplo():
            exemplo = [[0.55, 0.25, 0.25], [0.30, 0.45, 0.20], [0.15, 0.30, 0.55]]
            for i in range(3):
                for j in range(3):
                    entradas[i][j].delete(0, tk.END)
                    entradas[i][j].insert(0, str(exemplo[i][j]))

        def resolver():
            try:
                # lê os valores de ambos os vetores e os converte para as matrizes A e B
                A = [[float(entradas[i][j].get()) for j in range(3)] for i in range(3)]
                b = [float(e.get()) for e in rhs_entradas]
                # resolução de Ax=b pelo método direto, como está presente em metodos.py
                x = resolver_sistema_direto(A, b)
                saida.delete(1.0, tk.END)
                # exibe os resultados
                for i, xi in enumerate(x):
                    saida.insert(tk.END, f"Mina {i + 1}: {xi:.2f} m³\n")
            except Exception as e:
                # mensagem de erro
                messagebox.showerror("Erro", str(e))

        botoes = ttk.Frame(self.area_principal)
        botoes.pack(pady=6)
        ttk.Button(botoes, text="Carregar exemplo", command=preencher_exemplo).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Resolver Sistema", command=resolver).pack(side=tk.LEFT, padx=5)

    # ==========================
    # Tópico 2 – Gauss-Seidel
    # ==========================
    def topico2(self):
        self.limpar_area()
        ttk.Label(self.area_principal, text="Tópico 2 – Ponte de Wheatstone (Gauss-Seidel)",
                  font=("Segoe UI", 22, "bold"), foreground="#00BFFF").pack(pady=15)

        instruction_label = ttk.Label(self.area_principal,
                                      text="Insira os valores dos componentes e a tolerância para resolver o sistema de correntes pelo método iterativo.",
                                      style='Instruction.TLabel')
        instruction_label.pack(pady=5)

        # Variáveis de controle
        E = tk.DoubleVar(value=30.0)
        R1 = tk.DoubleVar(value=20.0)
        Rn = tk.DoubleVar(value=120.0)
        tol = tk.DoubleVar(value=1e-4)

        # Entradas (Diagrama removido)
        frame_inputs = ttk.Frame(self.area_principal)
        frame_inputs.pack(pady=10)

        ttk.Label(frame_inputs, text="Tensão E (V):").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        ttk.Entry(frame_inputs, textvariable=E, width=10).grid(row=0, column=1, padx=8, pady=4)

        ttk.Label(frame_inputs, text="Resistor R1 (Ω):").grid(row=0, column=2, sticky=tk.W, padx=4, pady=4)
        ttk.Entry(frame_inputs, textvariable=R1, width=10).grid(row=0, column=3, padx=8, pady=4)

        ttk.Label(frame_inputs, text="Outros Resistores R2-R5 (Ω):").grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        ttk.Entry(frame_inputs, textvariable=Rn, width=10).grid(row=1, column=1, padx=8, pady=4)

        ttk.Label(frame_inputs, text="Tolerância:").grid(row=1, column=2, sticky=tk.W, padx=4, pady=4)
        ttk.Entry(frame_inputs, textvariable=tol, width=10).grid(row=1, column=3, padx=8, pady=4)

        saida = tk.Text(self.area_principal, height=10, bg="#2A2A2A", fg="white", relief="ridge",
                        font=("TkDefaultFon", 10))
        saida.pack(fill=tk.X, pady=10)

        # Construção do sistema por meio do método das correntes nas malhas
        def construir_sistema(Ev, R1v, Rv):
            R2 = R3 = R4 = R5 = Rv
            A = np.array([
                [(-R1v - R4), R1v, R4],
                [R1v, (-R1v - R2 - R5), R5],
                [R4, R5, (-R3 - R4 - R5)]
            ], dtype=float)

            b = np.array([-Ev, 0, 0], dtype=float)
            return A, b

        def executar():
            try:
                A, b = construir_sistema(E.get(), R1.get(), Rn.get())

                # Checagem de diagonal dominante
                for i in range(len(A)):
                    diag = abs(A[i, i])
                    off_diag = np.sum(abs(A[i, :])) - diag
                    if diag <= off_diag:
                        messagebox.showwarning("Atenção",
                                               "A matriz não é estritamente diagonal dominante. A convergência não é garantida.")
                        break
                # estimativa inicial
                x0 = [b[i] / A[i, i] for i in range(3)]
                # array das soluções e número de iterações
                sol, it = metodo_gauss_seidel(A, b, x0=x0, tol=tol.get())
                saida.delete(1.0, tk.END)
                saida.insert(tk.END, f"Solução em {it} iterações:\n")
                saida.insert(tk.END, "--------------------------------\n")
                # a solução do sistema são as três correntes de malha ia (malha que contém a fonte de tensão), ib (triângulo superior da ponte),
                # ic (triângulo inferior da ponte)
                ia = sol[0]
                ib = sol[1]
                ic = sol[2]

                # cálculo das correntes "finais" com base nas correntes nas malhas
                correntes_calculadas = [ia - ib, ib, ic, ia - ic, ic - ib, ia]

                saida.insert(tk.END, "--- Incógnitas resolvidas (Correntes de Malha) ---\n")
                saida.insert(tk.END, f"ia (malha 1) = {ia:.6f} A\n")
                saida.insert(tk.END, f"ib (malha 2) = {ib:.6f} A\n")
                saida.insert(tk.END, f"ic (malha 3) = {ic:.6f} A\n")
                saida.insert(tk.END, "--------------------------------\n")
                saida.insert(tk.END, "--- Correntes resultantes (Cálculo) ---\n")

                # Exibe as correntes i1 a i6
                for i, val in enumerate(correntes_calculadas):
                    saida.insert(tk.END, f"Corrente i{i + 1} = {val:.6f} A\n")
                saida.insert(tk.END, "--------------------------------\n")

            except Exception as e:
                messagebox.showerror("Erro", str(e))

        # Agrupamento de botões
        botoes = ttk.Frame(self.area_principal)
        botoes.pack(pady=6)
        ttk.Button(botoes, text="Executar Gauss-Seidel", command=executar).pack(padx=5)

    # ==========================
    # Tópico 3 – Lei de Moore
    # ==========================
    def topico3(self):
        self.limpar_area()
        ttk.Label(self.area_principal, text="Tópico 3 – Lei de Moore (Regressão Logarítmica e Previsão)",
                  font=("Segoe UI", 22, "bold"), foreground="#00BFFF").pack(pady=15)

        instruction_label = ttk.Label(self.area_principal,
                                      text="Os dados são transformados em log10(N) e ajustados por uma reta (Regressão Linear). "
                                           "O *gráfico mostra o ajuste* e as previsões para os anos indicados.",
                                      style='Instruction.TLabel')
        instruction_label.pack(pady=5)
        # predefinição dos anos e dos transistores
        anos = [1971, 1974, 1978, 1982, 1985, 1989, 1993, 1997, 1999, 2002, 2006, 2008]
        trans = [2300, 6000, 29000, 120000, 275000, 1180000, 3100000, 7500000,
                 24000000, 220000000, 291000000, 2300000000]

        # Frame principal para entradas
        frame_entradas = ttk.Frame(self.area_principal)
        frame_entradas.pack(pady=8)

        frame_tabela = ttk.Frame(frame_entradas)
        frame_tabela.pack(side=tk.LEFT, padx=30, anchor=tk.N)

        ttk.Label(frame_tabela, text="Ano", font=("Segoe UI", 11, "bold"), width=12).grid(row=0, column=0, pady=2)
        ttk.Label(frame_tabela, text="Nº de Transistores (N)", font=("Segoe UI", 11, "bold"), width=20).grid(row=0,
                                                                                                             column=1,
                                                                                                             pady=2)
        # entradas das quantidades de transistores e seus respectivos anos
        entradas = []
        for i in range(len(anos)):
            e1 = ttk.Entry(frame_tabela, width=12)
            e2 = ttk.Entry(frame_tabela, width=20)
            e1.insert(0, anos[i])
            e2.insert(0, trans[i])
            e1.grid(row=i + 1, column=0, padx=2, pady=1)
            e2.grid(row=i + 1, column=1, padx=2, pady=1)
            entradas.append((e1, e2))

        # Entrada de previsão
        frame_previsao = ttk.Frame(frame_entradas)
        frame_previsao.pack(side=tk.LEFT, padx=30, anchor=tk.N)

        anos_prev = tk.StringVar(value="2010,2020")
        ttk.Label(frame_previsao, text="Anos para previsão (separados por vírgula):").pack(pady=5)
        ttk.Entry(frame_previsao, textvariable=anos_prev, width=25).pack(pady=4)

        # criação da caixa de texto para a saída
        saida = tk.Text(self.area_principal, height=6, bg="#2A2A2A", fg="white", relief="ridge",
                        font=("TkDefaultFon", 10))
        saida.pack(fill=tk.X, pady=10)

        # Agrupamento de botões (inicialmente contém o botão de ajustar)
        botoes = ttk.Frame(self.area_principal)
        botoes.pack(pady=6)
        botao_ajustar = ttk.Button(botoes, text="Ajustar e Gerar Gráficos")
        botao_ajustar.pack(padx=5)

        fig_canvas = None

        # função para o ajuste/aproximação da linha
        def ajustar():
            nonlocal fig_canvas
            nonlocal instruction_label, frame_entradas, botoes
            # leitura dos dados de entrada
            dados = []
            for e1, e2 in entradas:
                if e1.get() and e2.get():
                    try:
                        ano = float(e1.get())
                        N = float(e2.get())
                        # validação para o logaritmo, dado que não pode ser negativo
                        if N <= 0:
                            messagebox.showerror("Erro", "N deve ser maior que zero para usar log10.")
                            return
                        dados.append((ano, math.log10(N)))
                    except:
                        messagebox.showerror("Erro", "Verifique os valores digitados.")
                        return
            # validação da quantidade de pares ordenados
            if len(dados) < 2:
                messagebox.showerror("Erro", "Insira ao menos dois pares (Ano, N).")
                return
            
            # inserção dos dados nos vetores x e y, criando os pares ordenados
            x = np.array([d[0] for d in dados])
            y = np.array([d[1] for d in dados])
            A = np.vstack([x, np.ones_like(x)]).T
            # resolução do sistema pelo método dos mínimos quadrados (lstsq) com uma função que já o implementa
            a, b = np.linalg.lstsq(A, y, rcond=None)[0]

            # saída dos dados
            saida.delete(1.0, tk.END)
            saida.insert(tk.END, f"Ajuste obtido: log10(N) = {a:.6e} * ano + {b:.6e}\n\n")

            # preenchimento dos dados das previsões
            anos_previsao = [int(a.strip()) for a in anos_prev.get().split(",") if a.strip()]
            previsoes = []
            for ano in anos_previsao:
                logN = a * ano + b
                N = 10 ** logN
                previsoes.append((ano, N, logN))
                saida.insert(tk.END, f"Previsão para {ano}: {N:.3e} transistores (log10={logN:.4f})\n")

            # --- Ocultar Inputs e Botão de Ação para focar nos resultados ---
            instruction_label.pack_forget()
            frame_entradas.pack_forget()
            botoes.pack_forget()

            # ---------- GRÁFICOS EM ÊNFASE ----------
            if fig_canvas:
                fig_canvas.get_tk_widget().destroy()

            fig, axes = plt.subplots(1, 2, figsize=(6, 4))
            fig.patch.set_facecolor("#1E1E1E")

            ax1 = axes[0]
            anos_x = np.array([d[0] for d in dados])
            N_orig = 10 ** np.array([d[1] for d in dados])
            ax1.scatter(anos_x, N_orig, color="cyan", label="Dados reais", s=40)
            ax1.set_yscale("log")
            ax1.grid(True, linestyle="--", alpha=0.3)
            ax1.set_title("Evolução real (escala log)", color="white")
            ax1.set_xlabel("Ano");
            ax1.set_ylabel("N (transistores)")
            for ano, N, _ in previsoes:
                ax1.scatter(ano, N, color="orange", marker="*", s=100)
                ax1.text(ano, N, f" {ano}", color="orange", fontsize=9)

            ax2 = axes[1]
            ax2.scatter(x, y, color="cyan", label="log10(N) dados", s=40)
            x_line = np.linspace(min(x) - 1, max(anos_previsao) + 1, 300)
            y_line = a * x_line + b
            ax2.plot(x_line, y_line, color="orange", label="Ajuste linear", linewidth=2)
            ax2.set_xlabel("Ano");
            ax2.set_ylabel("log10(N)")
            ax2.set_title("Ajuste linear (Lei de Moore)", color="white")
            ax2.legend()
            ax2.grid(True, linestyle="--", alpha=0.3)

            fig.tight_layout()
            fig_canvas = FigureCanvasTkAgg(fig, master=self.area_principal)
            fig_canvas.draw()
            fig_canvas.get_tk_widget().pack(pady=8)

            # --- Pergunta de Continuação ---
            ttk.Button(self.area_principal, text="Novo Cálculo / Continuar", command=self.topico3).pack(pady=6)

        botao_ajustar.config(command=ajustar)

    # ==========================
    # Tópico 4 – Integração Numérica
    # ==========================
    def topico4(self):
        self.limpar_area()
        ttk.Label(self.area_principal, text="Tópico 4 – Integração Numérica (Trapézio e Simpson)",
                  font=("Segoe UI", 22, "bold"), foreground="#00BFFF").pack(pady=15)

        instruction_label = ttk.Label(self.area_principal,
                                      text="Insira os pares ordenados (x, y) que definem a seção. 'y' é a profundidade em 'x' (distância). "
                                           "O *gráfico mostra a seção reta* calculada.",
                                      style='Instruction.TLabel')
        instruction_label.pack(pady=5)

        # valores padrão para a inicialização do aplicativo
        xs = [0, 1, 2, 3, 4, 5, 6]
        ys = [0.5, 1.2, 2.3, 3.1, 2.0, 1.0, 0.4]

        frame_inputs = ttk.Frame(self.area_principal)
        frame_inputs.pack(pady=10)

        ttk.Label(frame_inputs, text="Distância (x)", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, padx=5,
                                                                                          pady=2)
        ttk.Label(frame_inputs, text="Profundidade (y)", font=("Segoe UI", 11, "bold")).grid(row=0, column=1, padx=5,
                                                                                             pady=2)
        # entradas de cada par ordenado
        entradas = []
        for i in range(len(xs)):
            e1 = ttk.Entry(frame_inputs, width=15);
            e2 = ttk.Entry(frame_inputs, width=15)
            e1.insert(0, xs[i])
            e2.insert(0, ys[i])
            e1.grid(row=i + 1, column=0, padx=4, pady=2)
            e2.grid(row=i + 1, column=1, padx=4, pady=2)
            entradas.append((e1, e2))
        # cria a caixa de texto da saída
        saida = tk.Text(self.area_principal, height=8, bg="#2A2A2A", fg="white", relief="ridge",
                        font=("TkDefaultFon", 10))
        saida.pack(fill=tk.X, pady=10)

        # Agrupamento de botões
        botoes = ttk.Frame(self.area_principal)
        botoes.pack(pady=6)
        botao_calcular = ttk.Button(botoes, text="Calcular Áreas")
        botao_calcular.pack(padx=5)

        fig_canvas = None

        def calcular():
            nonlocal fig_canvas
            nonlocal instruction_label, frame_inputs, botoes
            try:
                x = [float(e1.get()) for e1, _ in entradas if e1.get().strip()]
                y = [float(e2.get()) for _, e2 in entradas if e2.get().strip()]
                # garante que tenham pares ordenados o suficiente para a integração
                if len(x) != len(y) or len(x) < 2:
                    raise ValueError(
                        "Insira pelo menos 2 pares (x, y) e garanta que o número de entradas (x) e (y) é o mesmo.")

                # saída para a regra do trapézio
                area_trap = regra_trapezio(x, y)
                saida.delete(1.0, tk.END)
                saida.insert(tk.END, f"Área (Trapézio): {area_trap:.4f}\n")

                try:
                    area_simp = regra_simpson(x, y)
                    saida.insert(tk.END, f"Área (Simpson): {area_simp:.4f}\n")
                # mensagens de erro caso não tenha sido possível aplicar a regra de simpson
                except ValueError as ve:
                    saida.insert(tk.END, f"Simpson não aplicável: {ve}\n")
                except Exception as e:
                    saida.insert(tk.END, f"Erro no cálculo Simpson: {e}\n")

                # --- Ocultar Inputs e Botão de Ação ---
                instruction_label.pack_forget()
                frame_inputs.pack_forget()
                botoes.pack_forget()

                # --- GRÁFICO EM ÊNFASE ---
                if fig_canvas:
                    fig_canvas.get_tk_widget().destroy()

                fig = plt.Figure(figsize=(6, 3.5))
                ax = fig.add_subplot(111)
                ax.plot(x, y, marker='o', color="cyan")
                ax.fill_between(x, y, color="skyblue", alpha=0.4)
                ax.set_xlabel("x (Distância)");
                ax.set_ylabel("y (Profundidade)")
                ax.set_title("Seção Reta do Rio", color="white")
                ax.invert_yaxis()  # Inverte o Y para que pareça com uma seção de rio (profundidade)
                fig_canvas = FigureCanvasTkAgg(fig, self.area_principal)
                fig_canvas.draw()
                fig_canvas.get_tk_widget().pack(pady=8)

                # --- Pergunta de Continuação ---
                ttk.Button(self.area_principal, text="Novo Cálculo / Continuar", command=self.topico4).pack(pady=6)

            except Exception as e:
                messagebox.showerror("Erro", str(e))

        botao_calcular.config(command=calcular)


# ==========================
# Executar aplicação
# ==========================
if __name__ == "__main__":
    app = Aplicativo()
    app.mainloop()
