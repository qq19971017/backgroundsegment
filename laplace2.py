import numpy as np


def f(x, y):
    return x + 2* y

def laplace(x, y, step_x, step_y, epsilon):
    T = np.zeros((x,y))
    for i in range(len(T)):
        for j in range(len(T[0])):
            if i==0 or j==0 or i== len(T)-1 or j==len(T[0])-1:
                T[i][j] = 0
            else:
                T[i][j] = f(j* step_x,i * step_y)


    Epsilon = np.zeros((x,y))
    iterate =0
    while(True):
        for i in range(1, x-1, 1):
            for j in range(1, y-1, 1):
                temp = T[i,j]
                T[i, j] = 0.25 * (T[i+1][j] + T[i-1][j] + T[i][j+1] + T[i][j-1])
                Epsilon[i,j] = abs((T[i,j] - temp)/T[i,j])
        iterate += 1
        if np.all(Epsilon < epsilon):
            break
    return iterate, T

def real(x,y,step_x, step_y):
    T = np.zeros((x, y))
    for i in range(len(T)):
        for j in range(len(T[0])):
            T[i][j] = f(j* step_x,i * step_y)
    return T

if __name__ == '__main__':
    i, T = laplace(10,10,0.5,0.5,0.001)
    T_real = real(10,10,0.5,0.5)
    print("step is：", i)
    print("数值为:\n", T)
    print("解析数值\n", T_real)
    t_error = abs(T_real - T)
    print(t_error)