import numpy as np


def laplace(x, y, step_x, step_y, top, botton, left, right, error):
    T = np.zeros((x,y))
    T[0,:] = botton
    T[:,0] = left
    T[x-1,:] = top
    T[:,y-1] = right
    Epsilon = np.zeros((x,y))
    iterate =0
    while(True):
        for i in range(1, x-1, step_x):
            for j in range(1, y-1, step_y):
                temp = T[i,j]
                T[i, j] = 0.25 * (T[i+1][j] + T[i-1][j] + T[i][j+1] + T[i][j-1])
                Epsilon[i,j] = abs((T[i,j] - temp)/T[i,j])
        iterate += 1
        if np.all(Epsilon < error):
            break
    return iterate, T

if __name__ == '__main__':
    i, T = laplace(40,40,1,1,100,0,100,30,0.0001)
    print("step is：", i)
    print("result is:\n", T)

