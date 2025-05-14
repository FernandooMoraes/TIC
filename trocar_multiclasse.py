import os

# Caminho para a pasta onde estão os arquivos de anotação
pasta_anotacoes = 'caminho'

# Função para processar cada arquivo
def processar_arquivo(arquivo_path):
    with open(arquivo_path, 'r') as file:
        linhas = file.readlines()
    
    with open(arquivo_path, 'w') as file:
        for linha in linhas:
            partes = linha.strip().split()
            if len(partes) > 0:
                classe = partes[0]
                if classe == '1':
                    partes[0] = '8' 
                elif classe == '0':
                    partes[0] = '1'  # Substitui a classe 0 por 1 # Exclui a linha se a classe for 1
                elif classe == '2':
                    partes[0] = '0'  # Substitui a classe 2 por 0
 
                # Escreve a linha modificada
                file.write(' '.join(partes) + '\n')


for nome_arquivo in os.listdir(pasta_anotacoes):
    if nome_arquivo.endswith('.txt'):  # Verifica se é um arquivo de anotação
        caminho_arquivo = os.path.join(pasta_anotacoes, nome_arquivo)
        processar_arquivo(caminho_arquivo)

print("Substituição concluída.")