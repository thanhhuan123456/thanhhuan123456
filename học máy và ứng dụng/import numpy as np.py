import numpy as np
import matplotlib.pyplot as plt


X = np.array([180, 162, 183, 174, 160, 163, 180, 165, 175, 170, 170, 169,
              168, 175, 169, 171, 155, 158, 175, 165]).reshape(-1,1)


y = np.array([86, 55, 86.5, 70, 62, 54, 60, 72, 93, 89, 60, 82, 59, 75,
              56, 89, 45, 60, 60, 72]).reshape((-1,1))


X = np.insert(X, 0, 1, axis=1)

theta = np.linalg.inv(X.T.dpt(X)).dot(X.T).dot(y)
print("theta:",theta)
x1 = 150
y1 = theta[0] + theta[1] * x1  # y1 = 150 * 0.5 = 75

x2 = 190
y2 = theta[0] + theta[1] * x2  # y2 = 190 * 0.5 = 95
X_new = np.array([150,160,170,180,190])
y_pred = theta[0] + theta[1] * X_new
plt.plot([x1,x2],[y1,y2], 'r-')
plt.plot(X[:,1],y,'bo')
plt.plot(X_new,y_pred,'go--')
plt.xlabel('Chiều cao (cm)')
plt.ylabel('Cân nặng(kg)')
plt.title('Chiều cao và căn nặng của sinh viên VLU')
plt.legend()
plt.show()

