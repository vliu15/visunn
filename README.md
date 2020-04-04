# Visuai: Aesthetic and Informative Visualizations of Neural Networks
Visuai is a tool that leverages functional and modular visualizations to provide a suite of useful debugging tools that would otherwise have high barrier to usability. Some basic functionality that Visuai provides currently includes:
 - (modular) visualization of neural networks
 - visualization of weights and gradients throughout training

## Setup
To be compatible with libraries such as Pytorch, the Visuai backend and user API is in Python (all `pip` dependencies can be found in `requiements.txt`) and serves a frontend consisting of a fusion of React and Three.js (all `npm` dependencies can be found in `frontend/package.json`).

Support for containerized deployment with Docker is still in progress. Visuai will hopefully become a Python package so as to hide all dependencies from users and facilitate usage.

## APIs
Visuai can be interpreted as 2 separate APIs. Note that all APIs are currently only compatible with Pytorch (`torch==1.4.0`). The following examples will use the `ThreeLayerMLP` model that can be found in `models/three_layer_mlp.py`.

### User API: `Visu`
`Visu` is the API that users can use to log important information (that will later be served to the web app) and is designed to integrate easily with existing scripts with only a couple changes in code. Internally, `Visu` converts the model to GraphDef proto format, prunes unnecessarry nodes, and modularizes the topology. Currently,
```python
# Initialize Visu object with model
visu = Visu(model, dataloader, logdir='test')
# Log training
visu.update(iteration, optimizer, loss)
```

### Backend API: `Modu`
`Modu` distills modular model topology into the format of a file system, saved in an intermediate file between when the user initializes `Visu` and accesses logged information in the web app. The saved topology is used by the backend to serve the frontend when requested by the user. Currently,
```python
# Initialize Modu object with GraphDef proto
modu = Modu(proto, root='/')
# Retrieve GraphDef proto for a specified module name
mod_proto = modu.to_mod_proto('ThreeLayerMLP/Sequential[layers]')
# Retrieve Graphdef proto for entire model
flat_proto = modu.to_flat_proto()
```

## Notes
This section is dedicated to laying out next steps, including future features, bug fixes, and unaddressed nuances that come with creating a universal visualization tool.

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
