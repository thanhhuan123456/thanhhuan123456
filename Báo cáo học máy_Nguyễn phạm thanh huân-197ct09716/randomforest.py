import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Đọc dữ liệu
test_data = pd.read_csv('test.csv')  

train_data = pd.read_csv('train.csv')

# Tiền xử lý dữ liệu
# Xử lý các giá trị thiếu
train_data = train_data.dropna(subset=['Churn'])

# Chuyển đổi các cột dạng chuỗi thành dạng số (Encoding)
label_encoder = LabelEncoder()
train_data['Gender'] = label_encoder.fit_transform(train_data['Gender'])
train_data['Payment Method'] = label_encoder.fit_transform(train_data['Payment Method'])
train_data['Product Category'] = label_encoder.fit_transform(train_data['Product Category'])

# Chọn đặc trưng và nhãn
X = train_data[['Product Price', 'Quantity', 'Total Purchase Amount', 'Customer Age', 'Gender', 'Payment Method', 'Product Category']]
y = train_data['Churn']

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tạo mô hình Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Huấn luyện mô hình
rf_model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = rf_model.predict(X_test)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

