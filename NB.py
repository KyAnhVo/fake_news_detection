import torch

class NB:
    device: torch.device

    x: torch.Tensor
    y: torch.Tensor
    Phi: torch.Tensor
    P: torch.Tensor

    m: int
    n: int
    k: int

    def __init__(self, x: torch.Tensor, y: torch.Tensor, k: int):
        assert(x.dim() == 2 and y.dim() == 1), 'expect matrix x and y'
        assert(x.size()[0] == y.size()[0]), 'expect x: (m, n) and y: (m,)'
        assert(isinstance(k, int) and k >= 2), 'expect class to be positive integer greater than or equal to 2'

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.x = x.to(device= self.device, dtype= torch.float32)
        self.y = torch.nn.functional.one_hot(tensor= y, num_classes= k).to(device= self.device, dtype= torch.float32)

        self.m, self.n = self.x.size()
        self.k = k

        self.__calculateP()
        self.__calculatePhi()

    def predict(self, x: torch.Tensor):
        x = x.to(dtype= torch.float32, device= self.device)
        assert (x.dim() == 1 and x.size() == (self.n,)), f'expect 1D array of size (n,), instead received {x.size()}'

        x = x.unsqueeze(dim= 0)
        ret = (x @ torch.log(self.Phi) + (1 - x) @ torch.log(1 - self.Phi) + torch.log(self.P.T)).squeeze()
        return torch.argmax(ret)

    def __calculateP(self):
        self.P = torch.mean(input= self.y, dim= 0, dtype= torch.float32, keepdim= True).T

    def __calculatePhi(self):
        numerator = self.x.T @ self.y + 1
        denominator = self.y.sum(dim= 0, keepdim= True).expand_as(other= numerator) + 2
        self.Phi = numerator / denominator

# for testing
def main():
    pass

if __name__ == '__main__':
    main()
