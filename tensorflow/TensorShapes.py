import numpy as np
import tensorflow as tf

tensor_1d = np.array([1.45, -1, 0.2, 102.1])
print(tensor_1d)
print(tensor_1d.ndim)

print(tensor_1d.shape)
print(tensor_1d.dtype)

tensor = tf.convert_to_tensor(tensor_1d, dtype=tf.float64)

with tf.Session() as session:
    print(session.run(tensor))
    print(session.run(tensor[0]))
    print(session.run(tensor[1]))
