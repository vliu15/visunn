## Visunn
Visunn can be interpreted as 2 separate APIs. Note that all APIs are currently only compatible with Pytorch (`torch==1.4.0`).

### User API: `Visu`
`Visu` is the API that users can use to log important information (that will later be served to the web app) and is designed to integrate easily with existing scripts with only a couple changes in code. Internally, `Visu` converts the model to GraphDef proto format, prunes unnecessarry nodes, and modularizes the topology. Currently,
```python
# Initialize Visu object with model
visu = Visu(model, dataloader, logdir='test', name='model')
# Log training: not implemented
visu.update(iteration, optimizer, loss)
```

### Backend API: `Modu`
`Modu` distills modular model topology into the format of a file system, saved in an intermediate file between when the user initializes `Visu` and accesses logged information in the web app. The saved topology is used by the backend to serve the frontend when requested by the user. Currently,
```python
# Initialize Modu object with GraphDef proto
modu = Modu(proto, root='/')
# Retrieve GraphDef proto for a specified module name
mod_proto = modu.export('specified/module/name')
```
