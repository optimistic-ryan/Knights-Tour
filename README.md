## 🧠 Knight’s Tour Using a Neural Network  
A simulation of a neural network approach to solving the **Knight’s Tour Problem** on an `n x n` chessboard. Each valid knight move is modeled as a neuron, and the network stabilizes when a Hamiltonian path is found. This implementation is based on the algorithm described in the paper published in **Neurocomputing**.

### 🏆 Key Features:
- Neural network representation of the knight's graph.
- Real-time visualization using **Pygame**.
- Detects stable and repeating patterns during the network evolution.
- Customizable board size via command-line arguments.

### 🕹️ How to Run:
```bash
python knights_tour_neural_network.py --size 8
```
- Press **Enter** to reset the board.
- Press **Space** to manually step through updates.
- Press **Escape** to exit.

### 💜 Background:
This algorithm attempts to find a Knight’s Tour using a neural network inspired approach. Each knight move is treated as a neuron, and the network stabilizes when the knight completes a valid tour (degree-2 subgraph). While it can occasionally produce a valid tour, it often results in multiple disjoint cycles or diverges.

### 📝 References:
- Takefuji, Y., & Lee, K. C. (1991). Neural network approach to the knight's tour problem. **Neurocomputing**, 3(1), 41–46.
- Parberry, I. (1997). An efficient algorithm for the knight's tour problem.

### 🧑‍💻 Requirements:
- **Python 3.x**
- **Pygame**

```bash
pip install pygame
```

