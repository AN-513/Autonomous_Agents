# Autonomous Agents

This repository contains the implementation of autonomous agents using **NEAT**.

## Execution

To run the code, simply navigate to the `neat` folder and execute the desired file:

- ### **`gui_display.py`**  
  Runs one of the agents (random, *greedy*, or NEAT) with a graphical interface as selected in the `_agent` constant.

- ### **`testing.py`**  
  Runs a set of tests on random maps and, at the end, generates **three charts**, which are used in the report.

- ### **`training.py`**  
  Trains NEAT agents based on the sensors defined in the `get_sensors()` function, the memory is at the beginning of the file in the `MEMORY_SIZE` constant. `RECURSIVE_SIZE` was a feature that didn't improve the agent's performance, hence we leave it at zero, as explained in the sensors section of the report.
  The best agent will be saved with the name `neat_[fitness].pickle`.

  **Important Note:**  
  Whenever the number of sensors or their configurations are changed, it is necessary to also update the `config.txt` file, ensuring that the number of *inputs* matches the new sensor configuration.

## Requirements

    pip install neat-python
    pip install matplotlib
    pip install numpy

## Work done by:
- Afonso Nóia 123288
- Tomás Francisco 124107