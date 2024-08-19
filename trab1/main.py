from tabulate import tabulate

def traceBack(matriz, matriz_trace, x, y, ali1, ali2):

  #Limites para parar a recursão
  #Parar
  if x == lMat -2 and y == 1:
    return ali1, ali2
  
  #Borda inferior
  elif x == lMat -2:
    ali1.append("-")
    ali2.append(matriz[lMat-1][y])
    return traceBack(matriz, matriz_trace, x, y-1, ali1, ali2)
    
  #Borda esquerda
  elif y == 1:
    ali1.append(matriz[x][0])
    ali2.append("-")
    return traceBack(matriz, matriz_trace, x+1, y, ali1, ali2)
    
    
  #Não borda
  else:
    #Meio
    if matriz_trace[x][y][2] == 1:
      ali1.append(matriz[x][0])
      ali2.append(matriz[lMat-1][y])
      return traceBack(matriz, matriz_trace, x+1, y-1, ali1, ali2)
      
    #Esquerda
    if matriz_trace[x][y][0] == 1:
      ali1.append("-")
      ali2.append(matriz[lMat-1][y])
      return traceBack(matriz, matriz_trace, x, y-1, ali1, ali2)
      
    #Baixo
    if matriz_trace[x][y][1] == 1:
      ali1.append(matriz[x][0])
      ali2.append("-")
      return traceBack(matriz, matriz_trace, x+1, y, ali1, ali2)

if __name__ == "__main__":

  """
  Formato do arquivo:
  SEQUENCIA1
  SEQUENCIA2
  GAP
  MIS
  MATCH
  """

  # Nome do arquivo de entrada
  nome = "input.txt"
  
  with open(nome, 'r') as arquivo:
      linhas = arquivo.readlines()
  
  #Salva as sequencias e os valores
  vertical = linhas[0].strip()
  horizontal = linhas[1].strip()
  gap = int(linhas[2].strip())
  mismatch = int(linhas[3].strip())
  match = int(linhas[4].strip())
  
  
  #Analisa as sequencias para montar a matriz
  vertical = list(vertical)
  horizontal = list(horizontal)
  vLen = len(vertical)
  hLen = len(horizontal)
  
  lMat = vLen + 2
  cMat = hLen + 2
  
  #Matriz que iremos trabalhar em cima
  matriz = [[0] * cMat for _ in range(lMat)]
  
  matriz_trace = [[[0] * 3 for _ in range(cMat)] for _ in range(lMat)]
  
  matriz[lMat-1][0] = "X"
  matriz[lMat-2][0] = "U"
  matriz[lMat-1][1] = "U"
  
  aux = 0
  decrescente = gap
  for i in range(lMat - 2, 0, -1):
    matriz[i - 1][0] = vertical[aux]
    matriz[i - 1][1] = decrescente
    aux += 1
    decrescente += gap
  
  decrescente = gap
  for j in range(0, hLen):
    matriz[lMat - 1][j + 2] = horizontal[j]
    matriz[lMat - 2][j + 2] = decrescente
    decrescente += gap
  
  #Calculos na matriz
  custos = [0,0,0]
  
  for i in range(lMat - 3, -1, -1):
    for j in range(2, cMat):
  
      #Custo esquerda
      custos[0] = matriz[i][j - 1] + gap
  
      #Custo baixo
      custos[1] = matriz[i + 1][j] + gap
  
      #Custo meio
      if (matriz[lMat - 1][j] == matriz[i][0]):
        custos[2] = (matriz[i + 1][j - 1] + match)
      else:
        custos[2] = (matriz[i + 1][j - 1] + mismatch)
  
      #Verifica o(s) maior(es) custo(s)
      maior_custo = max(custos)
  
      matriz[i][j] = maior_custo
  
      for k in range(0,3):
        if custos[k] == maior_custo:
          matriz_trace[i][j][k] = 1
  
  ali1 = []
  ali2 = []
  ali1, ali2 = traceBack(matriz, matriz_trace, 0, cMat-1, ali1, ali2)
  
  print("Matriz")
  print(tabulate(matriz, tablefmt="grid"))
  print("\n")

  print("Alinhamento")
  print(f"SCORE: {matriz[0][cMat-1]}")
  print(f"Match: {match} Mismatch: {mismatch} Gap: {gap}")
  print(ali1[::-1])
  print(ali2[::-1])

  # Saída do arquivo output.txt
  with open("output.txt", "w") as output_file:
      output_file.write("Matriz:\n")
      output_file.write(tabulate(matriz, tablefmt="grid"))
      output_file.write("\n")
      output_file.write("Alinhamento:\n")
      output_file.write("".join(ali1[::-1]) + "\n")
      output_file.write("".join(ali2[::-1]) + "\n")
      output_file.write(f"SCORE: {matriz[0][cMat-1]}\n")
      output_file.write(f"Match: {match} Mismatch: {mismatch} Gap: {gap}\n")