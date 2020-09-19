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

        # alpha = self._alpha(seq)
        #
        # # 汇总
        # prob = 0.0
        # for i in range(0, self.N):
        #     prob += alpha[i][len(seq) - 1]

        beta = self._beta(seq)
        print(beta)

        # 汇总
        prob = 0.0
        for i in range(0, self.N):
            prob += self.B[i][seq[0]] * self.Pi[i] * beta[i][0]

        return prob

    def _alpha(self, seq):
        # alpha(i)_t, i in [1, N], t in [1, T]
        alpha = np.zeros([self.N, len(seq)])

        # 初始化, alpha(i)_1
        for i in range(0, self.N):
            alpha[i][0] = self.Pi[i] * self.B[i][seq[0]]

        # 递推
        for t in range(1, len(seq)):
            for i in range(0, self.N):
                for j in range(0, self.N):
                    alpha[i][t] += alpha[j][t - 1] * self.A[j][i]
                alpha[i][t] *= self.B[i][seq[t]]

        return alpha

    def _beta(self, seq):
        # beta(i)_t, i in [1, N], t in [1, T]
        beta = np.zeros([self.N, len(seq)])

        # 初始化, beta(i)_T = 1
        for i in range(0, self.N):
            beta[i][len(seq) - 1] = 1

        # 递推
        for t in range(len(seq) - 2, -1, -1):
            for i in range(0, self.N):
                for j in range(0, self.N):
                    beta[i][t] += self.A[i][j] * self.B[j][seq[t+1]] * beta[j][t+1]

        return beta

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

    def _gamma(self, seq):
        gamma = np.zeros([len(seq), self.N])
        alpha = self._alpha(seq)
        beta = self._beta(seq)

        for t in range(len(seq)):
            frac = 0
            for i in range(self.N):
                frac += alpha[i][t] * beta[i][t]
            for i in range(self.N):
                gamma[t][i] = alpha[i][t] * beta[i][t] / frac

        return gamma

    def _epsilon(self, seq):
        epsilon = np.zeros([len(seq), self.N, self.N])
        alpha = self._alpha(seq)
        beta = self._beta(seq)

        for t in range(len(seq) - 1):
            frac = 0
            for i in range(self.N):
                for j in range(self.N):
                    frac += alpha[i][t] * self.A[i][j] * self.B[j][seq[t+1]] * beta[j][t+1]
            for i in range(self.N):
                for j in range(self.N):
                    epsilon[t][i][j] = alpha[i][t] * self.A[i][j] * self.B[j][seq[t+1]] * beta[j][t+1] / frac

        return epsilon

    def _train_without_tag(self, seqs):
        """
        如果使用一个正态随机分布的初始值，那么每次输出的结果都不一样，并没有收敛到一个地方。
        这是 bug 呢，还是算法本身的缺陷呢？
        """
        seq = seqs[0]
        # 猜一个初始值
        # self.Pi = np.random.normal(size=[self.N])
        # self.A = np.random.normal(size=[self.N, self.N])
        # self.B = np.random.normal(size=[self.N, self.M])
        self.Pi = np.ones([self.N]) / self.N
        self.A = np.ones(([self.N, self.N])) / (self.N * self.N)
        self.B = np.ones([self.N, self.M]) / (self.N * self.M)

        print('-------------------初始状况开始--------------------')
        print(self.Pi)
        print(self.A)
        print(self.B)
        print('-------------------初始状况结束--------------------')

        while True:
            gamma = self._gamma(seq)
            epsilon = self._epsilon(seq)

            # 计算 Pi
            Pi = np.zeros([self.N])
            for i in range(self.N):
                Pi[i] = gamma[0][i]

            # 计算 A
            A = np.zeros([self.N, self.N])
            for i in range(self.N):
                for j in range(self.N):
                    a = 0
                    b = 0
                    for t in range(len(seq) - 1):
                        a += epsilon[t][i][j]
                        b += gamma[t][i]
                    A[i][j] = a / b

            # 计算 B
            B = np.zeros([self.N, self.M])
            for i in range(self.N):
                for j in range(self.M):
                    a = 0
                    b = 0
                    for t in range(len(seq)):
                        # 相等的时候加；对于输入的要求是 vk = k
                        if seq[t] == j:
                            a += gamma[t][j]
                        b += gamma[t][j]
                    B[i][j] = a / b

            sub_Pi = self.Pi - Pi
            sub_A = self.A - A
            sub_B = self.B - B
            diff = np.sum(np.abs(sub_Pi)) + np.sum(np.abs(sub_A)) + np.sum(np.abs(sub_B))
            if diff < 0.001:
                break
            else:
                self.Pi = Pi
                self.A = A
                self.B = B

    def decode(self, seq):
        """
        预测/解码问题：给定模型，给定观测序列，求解状态序列。viterbi 算法
        """
        pass


def main():
    # 概率计算
    A = np.array([[0.5, 0.2, 0.3], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]])
    B = np.array([[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]])
    Pi = np.array([[0.2], [0.4], [0.4]])
    hmm = HMM(3, 2)
    hmm.set(A, B, Pi)
    prob = hmm.prob([0, 1, 0])
    print(prob)

    # 学习，Baum-Welch 仅学习一个序列
    hmm = HMM(3, 3)
    hmm.train([[0, 1, 1, 1, 0, 1, 0, 1, 0, 2, 1, 2, 1, 2, 1]])
    prob = hmm.prob([0, 1, 1, 1, 0])
    print(prob)


if __name__ == '__main__':
    main()

