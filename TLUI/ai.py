import math
import random
# import matplotlib.pyplot as plt  # 注：matplotlib严格来说是第三方库，此处仅用于可视化，可移除

# 1. 基础数学工具（替代NumPy的部分功能）
def dot_product(a, b):
    """计算两个向量的点积"""
    return sum(x * y for x, y in zip(a, b))

def vector_add(a, b):
    """向量加法"""
    return [x + y for x, y in zip(a, b)]

def vector_subtract(a, b):
    """向量减法"""
    return [x - y for x, y in zip(a, b)]

def scalar_multiply(scalar, vector):
    """标量乘以向量"""
    return [scalar * x for x in vector]

def mean(x):
    """计算平均值"""
    return sum(x) / len(x)

# 2. 激活函数（引入非线性）
def relu(x):
    """ReLU激活函数"""
    return max(0, x)

def relu_derivative(x):
    """ReLU导数（用于反向传播）"""
    return 1 if x > 0 else 0

def tanh(x):
    """tanh激活函数"""
    return math.tanh(x)

def tanh_derivative(x):
    """tanh导数"""
    return 1 - math.tanh(x) ** 2

# 3. 神经网络类（多层感知器）
class SimpleNN:
    def __init__(self, input_size=3, hidden_size=8, output_size=1):
        # 初始化权重和偏置（随机值）
        self.weights1 = [
            [random.uniform(-0.5, 0.5) for _ in range(input_size)]
            for _ in range(hidden_size)
        ]
        self.biases1 = [random.uniform(-0.5, 0.5) for _ in range(hidden_size)]
        
        self.weights2 = [
            [random.uniform(-0.5, 0.5) for _ in range(hidden_size)]
            for _ in range(output_size)
        ]
        self.biases2 = [random.uniform(-0.5, 0.5) for _ in range(output_size)]
        
        # 学习率
        self.learning_rate = 0.001

    def forward(self, x):
        """前向传播计算"""
        # 隐藏层计算
        self.hidden = []
        for i in range(len(self.weights1)):
            activation = dot_product(self.weights1[i], x) + self.biases1[i]
            self.hidden.append(relu(activation))  # 应用ReLU激活
        
        # 输出层计算
        output = []
        for i in range(len(self.weights2)):
            activation = dot_product(self.weights2[i], self.hidden) + self.biases2[i]
            output.append(activation)  # 输出层不使用激活函数
        
        return output[0]

    def backward(self, x, y, y_pred):
        """反向传播计算梯度"""
        # 输出层误差
        output_error = y - y_pred
        
        # 隐藏层误差
        hidden_errors = [0] * len(self.hidden)
        for i in range(len(hidden_errors)):
            for j in range(len(self.weights2)):
                hidden_errors[i] += self.weights2[j][i] * output_error
        
        # 更新输出层权重和偏置
        for i in range(len(self.weights2)):
            for j in range(len(self.weights2[i])):
                self.weights2[i][j] += self.learning_rate * output_error * self.hidden[j]
            self.biases2[i] += self.learning_rate * output_error
        
        # 更新隐藏层权重和偏置
        for i in range(len(self.weights1)):
            for j in range(len(self.weights1[i])):
                self.weights1[i][j] += self.learning_rate * hidden_errors[i] * relu_derivative(self.hidden[i]) * x[j]
            self.biases1[i] += self.learning_rate * hidden_errors[i] * relu_derivative(self.hidden[i])

    def train(self, X, y, epochs=1000):
        """训练模型"""
        for epoch in range(epochs):
            total_loss = 0
            for i in range(len(X)):
                # 前向传播
                y_pred = self.forward(X[i])
                
                # 计算损失（MSE）
                loss = (y[i] - y_pred) ** 2
                total_loss += loss
                
                # 反向传播更新
                self.backward(X[i], y[i], y_pred)
            
            # 打印训练进度
            if (epoch + 1) % 100 == 0:
                avg_loss = total_loss / len(X)
                print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.6f}")

# 4. 生成非线性数据（模拟多输入非线性关系）
def generate_data(num_samples=1000):
    X = []
    y = []
    for _ in range(num_samples):
        # 3个输入特征
        x1 = random.uniform(-2, 2)
        x2 = random.uniform(-2, 2)
        x3 = random.uniform(-2, 2)
        
        # 非线性目标函数：y = x1² + sin(x2) + x3³ + 噪声
        target = x1**2 + math.sin(x2) + x3**3 + random.gauss(0, 0.1)
        
        X.append([x1, x2, x3])
        y.append(target)
    return X, y

# 5. 主程序
if __name__ == "__main__":
    # 生成训练数据
    X_train, y_train = generate_data(500)
    
    # 创建并训练模型
    model = SimpleNN(input_size=3, hidden_size=16)
    model.train(X_train, y_train, epochs=100)
    
    # 测试模型
    X_test, y_test = generate_data(100)
    y_pred = [model.forward(x) for x in X_test]
    
    # 计算测试集误差
    test_loss = mean([(y_test[i] - y_pred[i])**2 for i in range(len(y_test))])
    print(f"\n测试集平均损失: {test_loss:.6f}")
    
    # 示例预测
    sample_input = [100.2, -0.8, 0.5]
    prediction = model.forward(sample_input)
    print(f"\n输入 {sample_input} 的预测结果: {prediction:.4f}")
    print(f"实际值参考: {sample_input[0]**2 + math.sin(sample_input[1]) + sample_input[2]**3:.4f}")

    # （可选）可视化结果（需要matplotlib）
    try:
        plt.scatter(y_test, y_pred, alpha=0.6)
        plt.xlabel("真实值")
        plt.ylabel("预测值")
        plt.title("纯Python神经网络预测结果")
        plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
        plt.show()
    except:
        pass  # 如果没有matplotlib则跳过可视化
