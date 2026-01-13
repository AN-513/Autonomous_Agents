# Autonomous Agents

Este repositório contém a implementação de agentes autónomos utilizando **NEAT**.

## Execução

Para executar o código, entra na pasta `NEAT` e executa o ficheiro pretendido:

- **`NEAT_GUI_Display.py`**  
  Executa um dos agentes (aleatório, *greedy* ou NEAT) com interface gráfica.

- **`NEAT_Testing.py`**  
  Executa um conjunto de testes em mapas aleatórios e, no final, gera **três gráficos**, que são utilizados no relatório.

- **`NEAT_Trainning.py`**  
  Treina agentes NEAT com base nos sensores definidos na função `get_sensors()`, a memória está no inicio do ficheiro na constante `MEMORY_SIZE`.  O `RECURSIVE_SIZE` foi uma funcionalidade que não melhorou o desempenho do agente daí deixarmos a zero, conforme explicado na secção de sensores do relatório.
    O melhor agente será guardado com o nome `neat_[fitness].pickle` 

  
  **Nota importante:**  
  Sempre que o número de sensores ou as suas configurações forem alteradas, é necessário atualizar também o ficheiro `config.txt`, garantindo que o número de *inputs* coincide com a nova configuração dos sensores.

## Requisitos

    pip install neat-python
    pip install matplotlib
    pip install numpy

## Trabalho realizado por:
- Afonso Nóia 123288
- Tomás Francisco 124107