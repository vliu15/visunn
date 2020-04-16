# Visuai: Aesthetic and Informative Visualizations of Neural Networks
Visuai is a tool that leverages functional and modular visualizations to provide a suite of useful debugging tools that would otherwise have high barrier to usability. Some basic functionality that Visuai provides currently includes:
 - (modular) visualization of neural networks
 - visualization of weights and gradients throughout training

## Setup
To be compatible with libraries such as Pytorch, the Visuai backend and user API is in Python (all `pip` dependencies can be found in `requirements.txt`) and serves a frontend consisting of a fusion of React and Three.js (all `npm` dependencies can be found in `frontend/package.json`).

Support for containerized deployment with Docker is still in progress. Visuai will hopefully become a Python package so as to hide all dependencies from users and facilitate usage.

## Usage
1. Integrate into native code
```python
# Import
from visuai import Visu
# Initialize
visu = Visu(model, dataloader, logdir='sample', name='model')
```
2. Launch web app
```bash
# Launch backend
python run.py -l sample
# Launch frontend
cd frontend && npm start
```

## Metrics
Below are time and space metrics for a few sample models. These can be obtained by running `python debug.py`, which prints metrics of the 5 steps required to create a modularized topology (run on CIFAR-10)
1. Convert model to protobuf (built in Pytorch function)
2. Convert protobuf to dict
3. Prune trivial nodes
4. Prune trivial modules
5. Build modularized topology
 > Steps 1 and 3 are the largest bottlenecks in the algorithm.

| Model              | Step 1   | Step 2  | Step 3  | Step 4  | Step 5  | Space     |
|--------------------|----------|---------|---------|---------|---------|-----------|
| ThreeLayerMLP      |  0.076 s | 0.000 s | 0.001 s | 0.000 s | 0.001 s |  19.00 kb |
| ThreeLayerConvNet  |  0.102 s | 0.000 s | 0.001 s | 0.000 s | 0.001 s |  22.31 kb |
| resnet18           |  1.385 s | 0.000 s | 0.014 s | 0.001 s | 0.013 s | 242.46 kb |
| resnet152          |  8.384 s | 0.003 s | 0.329 s | 0.011 s | 0.074 s |   1.49 Mb |
| densenet121        |  4.474 s | 0.002 s | 0.222 s | 0.021 s | 0.107 s |   1.47 Mb |
| densenet201        |  7.568 s | 0.004 s | 0.571 s | 0.051 s | 0.292 s |   2.80 Mb |
| googlenet          |  2.382 s | 0.001 s | 0.066 s | 0.003 s | 0.031 s | 735.41 kb |
| shufflenet_v2_x2_0 |  2.181 s | 0.001 s | 0.100 s | 0.020 s | 0.038 s | 625.82 kb |
| mobilenet_v2       |  1.782 s | 0.001 s | 0.053 s | 0.009 s | 0.024 s | 542.38 kb |
| resnext101_32x8d   | 12.129 s | 0.002 s | 0.160 s | 0.007 s | 0.049 s |   1.09 Mb |
| wide_resnet101_2   | 13.495 s | 0.002 s | 0.165 s | 0.007 s | 0.054 s |   1.10 Mb |
| mnasnet1_3         |  1.573 s | 0.001 s | 0.050 s | 0.010 s | 0.025 s | 520.47 kb |

## Notes
This section is dedicated to address nuances that come with the Pytorch backend export.

### Recycling layers
This problem is exemplified with the following example. Consider the following variation of `ThreeLayerMLP`:
```python
class Model(nn.Module):
    def __init__(self, num_classes=10, **kwargs):
        self.flatten = nn.Flatten(1, -1)
        self.linear1 = nn.Linear(32*32*3, 1024, bias=True)
        self.linear2 = nn.Linear(1024, 256, bias=True)
        self.linear3 = nn.Linear(256, num_classes, bias=True)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.flatten(x)
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        x = self.relu(x)
        x = self.linear3(x)
        return x
```
Note how `self.relu = nn.ReLU()` is reused multiple times. While this is not incorrect in any way. However, from a graph perspective, there is one `self.relu = ReLU()` node, which has multiple input and output nodes. Rendering this topology declaration will show cycles in the graph due to the multiple passes through the recycled node. A potential solution would be to split all nodes that consist of >1 unconnected graph.

### Weights and Biases
With how `torch==1.4.0` constructs the graph protobuf, it is not possible to acquire the `_output_shapes` attribute from the weights and biases nodes (recoverable for all other nodes). We thus opt to leave those fields empty when aggregating attributes.
