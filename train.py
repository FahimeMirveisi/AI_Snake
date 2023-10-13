import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv('dataset/dataset.csv', header=None)
#data = data.isnull().dropna()
print(data.head(40))

X = data.iloc[1:, :-1].astype(int).values
Y = data.iloc[1:, -1].astype(int).values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=True)

print("Shapes before reshapes")
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(9, activation='sigmoid'),
    tf.keras.layers.Dense(40, activation='relu'),
    tf.keras.layers.Dense(30, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])

Y_train = Y_train.reshape(-1, 1)
Y_test = Y_test.reshape(-1, 1)

print("Shapes after reshapes")
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

output = model.fit(X_train, Y_train, epochs=200)


test_loss, test_accuracy = model.evaluate(X_test, Y_test)
print("Test loss:", test_loss, "Test accuracy:", test_accuracy)

plt.plot(output.history["loss"], label='Train loss')
plt.plot(output.history["accuracy"], label='Train accuracy')
plt.title('Train loss and accuracy')
plt.xlabel("epochs")
plt.ylabel("loss_accuracy")
plt.legend()
plt.show()

#tf.keras.models.save_model(model, 'weights/my_snake_model.h5')
model.save('weights/my_snake_model.h5')
print('finish')