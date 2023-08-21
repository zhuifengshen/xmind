# SLIP模型

## 机器人动力学建模

### 机器人物理模型参数整定

通过SolidWorks进行机器人的建模，然后可以通过solidworks导出机器人的urdf和相应的质量惯量参数，但是可能不太准，需要通过称重的方式进行校准。可以通过进行重力补偿控制的方式进行机器人物理模型参数的验证。但是这中间会涉及到摩擦力的处理，现在还没有对机器人关节处的摩擦力进行建模

###  机器人运动中的 Equation of Motion

建立系统的动力学方程有两种方法：牛顿-欧拉方法（通过运动学方程推导）和拉格朗日方法（通过系统能量推导）

#### 牛顿欧拉方法

1.   定义参考坐标系
2.   画出结构关系图
3.   对系统受力进行分析得到EOM（分别对平动和旋转进行分析）

$$
\sum F = \frac{d(mv)}{dt} = m \ddot{x} \\
\sum T = \frac{d(I \omega)}{dt} = I \ddot{\theta}
$$

#### 拉格朗日方程方法

1.   定义广义坐标系$q$
2.   建立系统动能$T$、系统势能$U$、广义力$Q$
3.   建立拉格朗日项$L = T - U$
4.   形成系统动力学方程(其中q是描述系统的多个变量，有多少个变量就能形成多少个动力学方程)，利用欧拉-拉格朗日方程

$$
Q = \frac{\partial}{\partial t}(\frac{\partial L}{\partial \dot{q}}) - \frac{\partial L}{\partial q} =  \frac{\partial}{\partial t}(\frac{\partial L}{\partial \dot{q}}) - \frac{\partial T}{\partial q} + \frac{\partial U}{\partial q}
$$

一个利用拉格朗日方法求EoM的例子  simple pendulum

![image-20230710143929838](https://ultramarine-image.oss-cn-beijing.aliyuncs.com/img/image-20230710143929838.png)

### 轨迹优化

机器人的轨迹优化的目的是对未来期望状态的规划控制，产生所需的前馈信号让系统完成复杂的轨迹运动，反馈控制是用来修正轨迹过程中的误差。轨迹不完全是空间中的一个三维轨迹，也可以是系统状态，机器人的每个关节如何运动

轨迹优化分为离线与在线，因为像MPC一样考虑未来很长时间运动变化的对计算的要求很高，没法做到实时规划，所以离线规划，再通过前馈+反馈进行控制。而在实时规划中，要减小计算量就要采用简化模型，比如跳跃采用的SLIP模型产生轨迹，利用前馈+反馈进行跟踪

### SLIP模型

SLIP模型经典的就是分为两个状态，支撑相和飞行相。对于飞行相主要是受到重力影响

人型机器人控制中walking利用ballistic walking inverted pendulum模型，质心在行走过程的中点达到最大高度，runnng采用spring-mass model，质点在跑步过程的中点达到最低高度

<img src="https://ultramarine-image.oss-cn-beijing.aliyuncs.com/img/image-20230706111857952.png" alt="image-20230706111857952" style="zoom:50%;" />

#### EoM of SLIP Model

$$
\left\{
\begin{array}{}
\ddot{\theta} - gl^{-1}\sin(\theta - \gamma) = 0\\
\ddot{\phi} + gl^{-1} \sin\phi\cos(\theta - \gamma) = \ddot{\theta}
\end{array}
\right.
$$

<img src="https://ultramarine-image.oss-cn-beijing.aliyuncs.com/img/image-20230706120022138.png" alt="image-20230706120022138" style="zoom:50%;" />

forward kinematics

![image-20230707173151398](https://ultramarine-image.oss-cn-beijing.aliyuncs.com/img/image-20230707173151398.png)

![image-20230707173823580](https://ultramarine-image.oss-cn-beijing.aliyuncs.com/img/image-20230707173823580.png)

- asdgfg
- 无序列表1
    - adfg
    - 无序列表2
    - 无序j列表2
        - 无序列表3
        - sadgfd
    - 无序d列表2
- 无序列表1
    - asgfhfg
    - 无序列表2

1. 有序列表1
2. 有序列表1
    1. 有序列表2
    2. 有序列表2
    asldkjflkjg
    asdfdf

#### 1D-SLIP Equation of Motion

$$
X = 
\begin{bmatrix}
x \\ 
\dot{x}
\end{bmatrix}
$$



-   飞行相

$$
\dot{X} = 
\begin{bmatrix}
0 & 1\\
0 & 0 \\
\end{bmatrix}
 X + 
 \begin{bmatrix}
 0 \\
 -g \\
 \end{bmatrix}
$$

-   支撑相

$$
\dot{X} =
\begin{bmatrix}
0 & 1\\
-\frac{K}{m} & -D\\
\end{bmatrix}
X + 
\begin{bmatrix}
0 \\
-g
\end{bmatrix}
$$

其中K是弹簧刚度  D是弹簧阻尼系数

#### 2D-SLIP Equation of Motion

![image-20230710151755125](https://ultramarine-image.oss-cn-beijing.aliyuncs.com/img/image-20230710151755125.png)

-   飞行相

定义状态
$$
X = 
\begin{bmatrix}
x \\
z \\
\dot{x} \\
\dot{z} \\
\end{bmatrix}, 
\qquad
\dot{X} = 
\begin{bmatrix}
\dot{x} \\
\dot{z} \\
0 \\
-g\\
\end{bmatrix}
$$

-   支撑相

$$
X = 
\begin{bmatrix}
r \\
\theta \\
\dot{r} \\
\dot{\theta} \\
\end{bmatrix}
$$



通过拉格朗日方程建立系统运动方程
$$
\begin{aligned}
T = \frac{1}{2}mr^{2}\dot{\theta}^{2} + \frac{1}{2}m \dot{r}^{2}\\
U = \frac{1}{2}k(l_{0} - r)^{2} + mgr\cos{\theta} \\
L = T - U
\end{aligned}
$$
通过欧拉-拉格朗日公式得出系统的运动学方程为
$$
\begin{aligned}
m \ddot{r} - mr\dot{\theta}^{2} - k(l_{0} - r) + mg \cos{\theta} = 0\\
2 m \dot{\theta} r \dot{r} + mr^{2}\ddot{\theta} - mgr\sin{\theta} = 0
\end{aligned}
$$

得出的系统更新方程为
$$
\begin{aligned}
\ddot{r} = r \dot{\theta}^{2} + \frac{k}{m}(l_{0} - r) - g \cos \theta \\
\ddot{\theta} = \frac{g}{r}\sin \theta - \frac{2\dot{\theta}}{r}\dot{r}
\end{aligned}
$$


-   从飞行相到支撑相的转换条件

$$
z - l_{0}\cos \theta \leq 0
$$

​	因为使用了不同的状态变量，因此在切换状态的时候还要进行状态的更新

​	这个状态切换的部分可以用drake中的`MakeWitnessFunction`来实现，very elegant

​	使用的公式为：
$$
\begin{aligned}
&x = -r\sin \theta, \quad z = r\cos \theta \\
\Rightarrow & \dot{x} = -\dot{r}\sin \theta - r \dot{\theta} \cos \theta \\
\Rightarrow & \dot{z} = \dot{r}\cos \theta - r \dot{\theta}\sin \theta \\
\end{aligned}
$$

$$
\begin{aligned}
r^{2} = x^{2} + z^{2} \\
\Rightarrow \dot{r} = \sin \theta \cdot \dot{x} + \cos\theta \cdot \dot{z}
\end{aligned}
$$

最后
$$
\begin{aligned}
\dot{r} = \sin \theta \cdot \dot{x} + \cos \theta \cdot \dot{z} \\
\dot{\theta} = - \frac{1}{r \cos \theta}(\dot{r} \sin\theta + \dot{x})
\end{aligned}
$$

-   从支撑相到飞行相的转化条件

$$
r \geq l_{0}
$$

​	更新的时候使用的方程为
$$
\begin{aligned}
&x = -r\sin \theta, \quad z = r\cos \theta \\
\Rightarrow & \dot{x} = -\dot{r}\sin \theta - r \dot{\theta} \cos \theta \\
\Rightarrow & \dot{z} = \dot{r}\cos \theta - r \dot{\theta}\sin \theta \\
\end{aligned}
$$

​	通过再对上面的方程进行求导可以得到质心的更新方程
$$
\begin{aligned}
\ddot{x} = -\ddot{l}\sin\theta - 2 \dot{\theta}\dot{l}\cos\theta + l\ddot{\theta}\cos\theta + l \dot{\theta}^{2}\sin\theta \\
\ddot{z} = \ddot{l}\cos\theta - 2 \dot{l}\dot{\theta}\sin\theta - \ddot{\theta}l\sin\theta - l\dot{\theta}\cos\theta
\end{aligned}
$$
#### 单足SLIP规划

这部分为`slip_jump.cc`中`Trajectory`类`Update`函数行为的分析，这部分规划的是单足机器人利用SLIP模型进行跳跃。Trajectory类的输入为机器人现在的状态`state_est`，进行实时规划出机器人下一步的轨迹，并输出机器人在下一次更新前的预期状态`state_des`。

>   程序中`getTheta`函数的运行逻辑  为什么会用到该函数
>
>   getTheta的作用是从空中飞行的速度映射到落地的角度，在空中飞行的过程中调整落地脚的位置和速度
>
>   后面用一个近似直线函数来拟合，在一定范围内可以看成是近似直线

在轨迹规划的过程中，用上一状态的pre_state_des来更新下一状态的信息，在这个过程中前馈不利用测量估计的状态信息，然后在flight的过程中因为要对控制的腿进行姿态的调整，对长度和角度都要添加反馈器，利用两个反馈器对前馈规划进行反馈。

打算在进行状态转移的时候  从支撑相到飞行相 飞行相到支撑相的时候将机器人的实际状态赋值给期望状态，进行下一阶段的规划

#### 动平衡

initial thought: 如果只是小幅度的扰动就都在 controller 的鲁棒性范围内，但是如果涉及大幅度的扰动就要通过轨迹规划来实现机器人的迈步的减少动量的范畴，通过 MPC 实现
