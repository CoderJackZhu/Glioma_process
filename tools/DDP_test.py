import torch
import torch.nn as nn
import torch.optim as optim
import torch.distributed as dist
import torchvision
import torchvision.transforms as transforms
from torch.utils.data.distributed import DistributedSampler

# 初始化进程组
def init_processes(rank, size, fn, backend='nccl'):
    """初始化进程组"""
    dist.init_process_group(backend=backend, init_method='tcp://localhost:23456',
                            rank=rank, world_size=size)
    fn(rank, size)

# 定义模型
class ResNet(nn.Module):
    def __init__(self):
        super(ResNet, self).__init__()
        self.resnet = torchvision.models.resnet18(pretrained=False, num_classes=10)

    def forward(self, x):
        x = self.resnet(x)
        return x

# 定义训练函数
def train(rank, size):
    torch.manual_seed(0)
    # 使用DistributedSampler分发数据集
    train_set = torchvision.datasets.CIFAR10(root='./data', train=True, download=True,
                                             transform=transforms.ToTensor())
    train_sampler = DistributedSampler(train_set, num_replicas=size, rank=rank)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=128, sampler=train_sampler)

    # 初始化模型、优化器和损失函数
    model = ResNet().cuda(rank)
    model = nn.parallel.DistributedDataParallel(model, device_ids=[rank])
    optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()

    # 训练模型
    for epoch in range(50):
        train_sampler.set_epoch(epoch)
        for i, (inputs, labels) in enumerate(train_loader, 0):
            inputs = inputs.cuda(rank)
            labels = labels.cuda(rank)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            if i % 10 == 0:
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, loss.item()))

if __name__ == '__main__':
    size = 2  # 使用两张卡
    processes = []
    for rank in range(size):
        p = torch.multiprocessing.Process(target=init_processes, args=(rank, size, train))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()