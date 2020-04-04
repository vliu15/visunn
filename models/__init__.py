from models.three_layer_conv_net import ThreeLayerConvNet
from models.three_layer_mlp import ThreeLayerMLP
from torchvision.models import resnet18, densenet121

torch_models = {
    'ThreeLayerConvNet': ThreeLayerConvNet,
    'ThreeLayerMLP': ThreeLayerMLP,
    'resnet18': resnet18,
    'densenet121': densenet121
}

__all__ = ['torch_models']
