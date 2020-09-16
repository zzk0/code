import numpy as np


class HMM(object):
    """
    隐马尔可夫模型，分为三个问题：概率计算问题，学习问题，预测问题。
    要求在概率计算和预测之前，必须先学习。
    """

    def __init__(self, N, M):
        """
        N: 状态数
        M: 观测数
        """
        self.N = N
        self.M = M

        self.A = np.zeros([N, N])
        self.B = np.zeros([N, M])
        self.Pi = np.zeros([N])

    def set(self, A, B, Pi):
        self.N = len(A)
        self.M = len(B[0])
        self.A = A
        self.B = B
        self.Pi = Pi

    def prob(self, seq):
        """
        概率计算问题: 给定模型，给定观测序列，计算概率
        使用前向算法
        """

        # alpha(i)_t, i in [1, N], t in [1, T]
        alpha = np.zeros([self.N, len(seq)])

        # 初始化, alpha(i)_1
        for i in range(0, self.N):
            alpha[i][0] = self.Pi[i] * self.B[i][seq[0]]

        # 递推
        for t in range(1, len(seq)):
            for i in range(0, self.N):
                for j in range(0, self.N):
                    alpha[i][t] += alpha[j][t-1] * self.A[j][i]
                alpha[i][t] *= self.B[i][seq[t]]

        # 汇总
        prob = 0.0
        for i in range(0, self.N):
            prob += alpha[i][len(seq) - 1]

        return prob

    def train(self, seqs, states=None):
        """
        学习问题：给定观测序列，求解模型；如果有状态序列，那么直接计算；如果没有，那么使用 Baum-Welch 算法
        """
        if states is None:
            self._train_without_tag(seqs)
        else:
            self._train_with_tag(seqs, states)

    def _train_with_tag(self, seqs, states):
        # 统计频率
        Pi = np.zeros([self.N])
        A = np.zeros([self.N, self.N])
        B = np.zeros([self.N, self.M])

        for seq, state in zip(seqs, states):
            Pi[seq[0]] += 1
            for i in range(0, len(seq) - 1):
                A[seq[i]][seq[i+1]] += 1
            for i in range(0, len(seq)):
                B[seq[i]][state[i]] += 1

        # 直接计算
        self.Pi = Pi / np.sum(Pi)

        row_sum = np.sum(A, axis=1)
        row_sum = row_sum.reshape([len(row_sum), 1])
        self.A = A / row_sum

        row_sum = np.sum(B, axis=1)
        row_sum = row_sum.reshape([len(row_sum), 1])
        self.B = B / row_sum

    def _train_without_tag(self, seqs):
        pass

    def decode(self, seq, algo='viterbi'):
        """
        预测/解码问题：给定模型，给定观测序列，求解状态序列。有两种方法：近似法、viterbi
        算法选择有：近似算法, viterbi 算法
        """
        if algo == 'viterbi':
            self._decode_viterbi(seq)
        else:
            self._decode_approximate(seq)

    def _decode_viterbi(self, seq):
        pass

    def _decode_approximate(self, seq):
        pass


def main():
    B = np.array([[2, 3], [1, 1], [3, 4]])
    row_sum = np.sum(B, axis=1)
    row_sum = row_sum.reshape([len(row_sum), 1])
    B = B / row_sum
    print(B)

    A = np.array([[0.5, 0.2, 0.3], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]])
    B = np.array([[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]])
    Pi = np.array([[0.2], [0.4], [0.4]])
    hmm = HMM(3, 2)
    hmm.set(A, B, Pi)
    prob = hmm.prob([0, 1, 0])
    print(prob)


if __name__ == '__main__':
    main()

