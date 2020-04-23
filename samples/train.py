#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' sample training script for cifar-10 '''

import os
import argparse
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from tqdm import tqdm
from copy import deepcopy

from models import torch_models
from visunn import Visu, DATA_DIR, LOG_DIR

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'


def train(train_data, test_data, model, objective, optimizer, device,
          epochs=100, scheduler=None, logdir='', name='model'):
    ''' trains and tests a model for 100 epochs

        train_data  (utils.data.DataLoader)      : train dataset
        test_data   (utils.data.DataLoader)      : test dataset
        model       (nn.Module)                  : model to be trained
        objective   (nn._Loss, nn._WeightedLoss) : loss function
        optimizer   (optim.Optimizer)            : optimizer for training
        device      (str)                        : 'cuda' or 'cpu'
        epochs      (int)                        : number of training epochs
        scheduler   (optim.LRScheduler)          : scheduler for learning rate
        logdir      (str)                        : path to logging directory
        name        (str)                        : model name, no real use
    '''
    best_loss = float('inf')
    best_model = None

    visu = Visu(model, train_data, logdir=logdir, name=name)

    for epoch in range(1, epochs+1):

        train_loss = 0.0
        test_loss = 0.0

        model.train()
        for _, (batch, targets) in tqdm(
                                    enumerate(train_data),
                                    total=len(train_data),
                                    desc='Train '):
            batch.to(device)
            targets.to(device)

            model.zero_grad()
            optimizer.zero_grad()

            logits = model(batch)
            loss = objective(logits, targets)

            loss.backward()
            optimizer.step()

            if scheduler is not None:
                scheduler.step()

            train_loss += loss.item()

        model.eval()
        with torch.no_grad():
            for _, (batch, targets) in tqdm(
                                        enumerate(test_data),
                                        total=len(test_data),
                                        desc='Test  '):
                batch.to(device)
                targets.to(device)

                logits = model(batch)
                loss = objective(logits, targets)

                test_loss += loss.item()

        print('Epoch {}. Train loss: {:.3f}. Test loss: {:.3f}'
              .format(epoch, train_loss/len(train_data),
                      test_loss/len(test_data)))

        if test_loss < best_loss:
            best_loss = test_loss
            best_model = deepcopy(model)

    return best_model


def main(args):
    # set up hardware
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # retrieve, initialize, & optionally load model
    model = torch_models.get(args.name, None)
    if model is None:
        print('Valid name specifications are {}'
                .format(', '.join(torch_models.keys())))
        raise RuntimeError
    else:
        model = model(num_classes=10)

    # set up dataloader
    download = False
    cifar_dir = os.path.join(DATA_DIR, 'cifar10')
    if not os.path.exists(cifar_dir):
        os.makedirs(cifar_dir)
        download = True
    train_data = DataLoader(
        datasets.CIFAR10(
            cifar_dir,
            download=True,
            train=True,
            transform=transforms.ToTensor()
        ),
        batch_size=128,
        shuffle=True,
        drop_last=False
    )

    # train and save best model
    test_data = DataLoader(
        datasets.CIFAR10(
            cifar_dir,
            download=True,
            train=True,
            transform=transforms.ToTensor()
        ),
        batch_size=128,
        shuffle=False,
        drop_last=False
    )

    objective = nn.CrossEntropyLoss(reduction='sum')
    scheduler = None
    optimizer = optim.Adam(
        model.parameters(), lr=1e-3)

    model = train(
        train_data, test_data, model, objective, optimizer, device,
        epochs=100, scheduler=scheduler, logdir=args.logdir, name=args.name
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, default='ThreeLayerMLP',
                        help='string of callable (torchvision) model')
    parser.add_argument('-l', '--logdir', type=str, default=LOG_DIR,
                        help='where to log model for web app use')
    args = parser.parse_args()

    main(args)
