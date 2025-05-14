import os

# Caminho para a pasta onde estão os arquivos de anotação
pasta_anotacoes = "caminho"

# Função para substituir valores na primeira coluna
def substituir_valor_primeira_coluna(arquivo_path, valor_antigo, valor_novo):
    with open(arquivo_path, 'r') as file:
        linhas = file.readlines()
    
    with open(arquivo_path, 'w') as file:
        for linha in linhas:
            partes = linha.strip().split()
            if len(partes) > 0:
                # Substitui o valor antigo pelo novo na primeira coluna
                if partes[0] == str(valor_antigo):
                    partes[0] = str(valor_novo)
                # Escreve a linha modificada
                file.write(' '.join(partes) + '\n')

# Itera sobre todos os arquivos na pasta
for nome_arquivo in os.listdir(pasta_anotacoes):
    if nome_arquivo.endswith('.txt'):  # Verifica se é um arquivo de anotação
        caminho_arquivo = os.path.join(pasta_anotacoes, nome_arquivo)
        substituir_valor_primeira_coluna(caminho_arquivo, valor_antigo=0, valor_novo=1)

print("Substituição concluída.")