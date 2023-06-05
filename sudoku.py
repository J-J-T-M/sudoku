import pygame
import sys

# Define as dimensões da janela
LARGURA = 540
ALTURA = 600

# Define as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
AZUL = (0, 0, 255)

# Define as dimensões do quadrado
TAMANHO_QUADRADO = LARGURA // 9

# Inicializa o Pygame
pygame.init()

# Configura a janela do jogo
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Resolutor de Sudoku")

# Carrega a fonte
fonte = pygame.font.SysFont("Arial", 40)

# Define a matriz do Sudoku
sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Define as coordenadas do retângulo selecionado
retangulo_selecionado = None

# Função para desenhar o Sudoku na tela
def desenhar_sudoku():
    for i in range(9):
        for j in range(9):
            valor = sudoku[i][j]
            retangulo = pygame.Rect(j * TAMANHO_QUADRADO, i * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO)
            pygame.draw.rect(janela, BRANCO, retangulo)

            if valor != 0:
                superficie_texto = fonte.render(str(valor), True, PRETO)
                retangulo_texto = superficie_texto.get_rect(center=retangulo.center)
                janela.blit(superficie_texto, retangulo_texto)

            if retangulo == retangulo_selecionado:
                pygame.draw.rect(janela, AZUL, retangulo, 3)

            if (j + 1) % 3 == 0 and j != 8:
                pygame.draw.line(janela, PRETO, (retangulo.right, retangulo.top), (retangulo.right, retangulo.bottom), 4)
            if (i + 1) % 3 == 0 and i != 8:
                pygame.draw.line(janela, PRETO, (retangulo.left, retangulo.bottom), (retangulo.right, retangulo.bottom), 4)

# Função para atualizar o valor no Sudoku
def atualizar_valor(linha, coluna, valor):
    sudoku[linha][coluna] = valor

# Função para encontrar a célula clicada
def obter_celula_clicada(posicao):
    x, y = posicao
    linha = y // TAMANHO_QUADRADO
    coluna = x // TAMANHO_QUADRADO
    return linha, coluna

# Função para resolver o Sudoku
def resolver_sudoku(grid):
    # Encontra a próxima célula vazia
    linha, coluna = encontrar_celula_vazia(grid)

    # Se não houver mais células vazias, o Sudoku está resolvido
    if linha == -1 and coluna == -1:
        return True

    # Testa valores de 1 a 9 na célula vazia
    for num in range(1, 10):
        if verificar_atribuicao_valida(grid, linha, coluna, num):
            # Atribui o número à célula vazia
            grid[linha][coluna] = num

            # Recursivamente tenta resolver o Sudoku com a atribuição atual
            if resolver_sudoku(grid):
                return True

            # Se a atribuição não levar a uma solução, desfaz a atribuição e tenta outro número
            grid[linha][coluna] = 0

    # Retorna False se não for possível encontrar uma solução
    return False

# Função auxiliar para encontrar a próxima célula vazia
def encontrar_celula_vazia(grid):
    for linha in range(9):
        for coluna in range(9):
            if grid[linha][coluna] == 0:
                return linha, coluna
    return -1, -1

# Função auxiliar para verificar a validade de uma atribuição
def verificar_atribuicao_valida(grid, linha, coluna, num):
    # Verifica se o número não está presente na mesma linha
    for x in range(9):
        if grid[linha][x] == num:
            return False

    # Verifica se o número não está presente na mesma coluna
    for x in range(9):
        if grid[x][coluna] == num:
            return False

    # Verifica se o número não está presente no mesmo bloco 3x3
    linha_inicial = (linha // 3) * 3
    coluna_inicial = (coluna // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[linha_inicial + i][coluna_inicial + j] == num:
                return False

    return True

# Função principal
def main():
    global retangulo_selecionado

    # Variável para controlar o loop do jogo
    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    posicao = pygame.mouse.get_pos()
                    retangulo_selecionado = pygame.Rect(obter_celula_clicada(posicao)[1] * TAMANHO_QUADRADO, obter_celula_clicada(posicao)[0] * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO)

        # Chama a função para resolver o Sudoku
        resolver_sudoku(sudoku)

        # Limpa a tela
        janela.fill(CINZA)

        # Desenha o Sudoku na tela
        desenhar_sudoku()

        # Atualiza a janela do jogo
        pygame.display.update()

# Executa o jogo
if __name__ == '__main__':
    main()