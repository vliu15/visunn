from .three_layer_conv_net import ThreeLayerConvNet
from .three_layer_mlp import ThreeLayerMLP
from torchvision.models import \
    vgg11, vgg11_bn, vgg13, vgg13_bn, vgg16, vgg16_bn, vgg19, vgg19_bn, \
    resnet18, resnet34, resnet50, resnet101, resnet152, \
    squeezenet1_0, squeezenet1_1, \
    densenet121, densenet161, densenet169, densenet201, \
    inception_v3, \
    googlenet, \
    shufflenet_v2_x0_5, shufflenet_v2_x1_0, shufflenet_v2_x1_5, \
        shufflenet_v2_x2_0, \
    mobilenet_v2, \
    resnext50_32x4d, resnext101_32x8d, \
    wide_resnet50_2, wide_resnet101_2, \
    mnasnet0_5, mnasnet0_75, mnasnet1_0, mnasnet1_3


torch_models = {
    # custom
    'ThreeLayerConvNet': ThreeLayerConvNet,
    'ThreeLayerMLP': ThreeLayerMLP,
    # default: vgg
    'vgg11': vgg11,
    'vgg11_bn': vgg11_bn,
    'vgg11': vgg13,
    'vgg11_bn': vgg13_bn,
    'vgg11': vgg16,
    'vgg11_bn': vgg16_bn,
    'vgg11': vgg19,
    'vgg11_bn': vgg19_bn,
    # default: resnet
    'resnet18': resnet18,
    'resnet34': resnet34,
    'resnet50': resnet50,
    'resnet101': resnet101,
    'resnet152': resnet152,
    # default: squeezenet
    'squeezenet1_0': squeezenet1_0,
    'squeezenet1_1': squeezenet1_1,
    # default: densenet
    'densenet121': densenet121,
    'densenet161': densenet161,
    'densenet169': densenet169,
    'densenet201': densenet201,
    # default: inception
    'inception_v3': inception_v3,
    # default googlenet
    'googlenet': googlenet,
    # default: shufflenet v2
    'shufflenet_v2_x0_5': shufflenet_v2_x0_5,
    'shufflenet_v2_x1_0': shufflenet_v2_x1_0,
    'shufflenet_v2_x1_5': shufflenet_v2_x1_5,
    'shufflenet_v2_x2_0': shufflenet_v2_x2_0,
    # default: mobilenet v2
    'mobilenet_v2': mobilenet_v2,
    # default: resnext
    'resnext50_32x4d': resnext50_32x4d,
    'resnext101_32x8d': resnext101_32x8d,
    # default: wide resnet
    'wide_resnet50_2': wide_resnet50_2,
    'wide_resnet101_2': wide_resnet101_2,
    # default: mnasnet
    'mnasnet0_5': mnasnet0_5,
    'mnasnet0_75': mnasnet0_75,
    'mnasnet1_0': mnasnet1_0,
    'mnasnet1_3': mnasnet1_3
}

__all__ = ['torch_models']
