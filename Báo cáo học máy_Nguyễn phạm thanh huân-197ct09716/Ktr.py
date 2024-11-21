from datasets import load_dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from torchvision import transforms
import numpy as np
from google.colab import files
from PIL import Image

# Tải tập dữ liệu (thay thế bằng đường dẫn tệp cục bộ)
ds = load_dataset("D:\Đồ án dự đoán hành vi khách hàng trong TMĐT\data.csv")

transform = transforms.Compose ([
    transforms.Resize((32,32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def preprocess(data):
    images = [transform(image).numpy().flatten() for image in data['image']]
    labels = data['label']
    return np.array(images), np.array(labels)

X, y = preprocess(ds['train'])

# Chia dữ liệu thành các tập training và test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "SVM": SVC()
}

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(f"{name} Accuracy:", accuracy_score(y_test, predictions))


def predict_from_path(model, img_path):
    # Load and preprocess the image
    image = Image.open(img_path).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension
    image = image.numpy().flatten().reshape(1, -1)  # Flatten image for the model

    # Make prediction
    prediction = model.predict(image)
    predicted_label = label_mapping[int(prediction[0])]

    print(f"Dự đoán cho ảnh {img_path}: {predicted_label}")
    
from google.colab import drive
drive.mount('/content/drive')

img = 'D:\Đồ án dự đoán hành vi khách hàng trong TMĐT\data.csv'
predict_from_path(models['Random Forest'], img)