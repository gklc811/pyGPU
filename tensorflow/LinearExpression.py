import tensorflow as tf

c = tf.constant(10.0, name="c", dtype=tf.float32)
a = tf.constant(5.0, name="a", dtype=tf.float32)
b = tf.constant(13.0, name="b", dtype=tf.float32)

d = tf.Variable(tf.add(tf.multiply(a, c), b))

init = tf.global_variables_initializer()

with tf.Session() as session:
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs", session.graph)
    session.run(init)
    print(session.run(d))

x = tf.placeholder(tf.float32, name="x")
y = tf.placeholder(tf.float32, name="y")

z = tf.multiply(x, y, name="z")

with tf.Session() as session:
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs", session.graph)
    print(session.run(z, feed_dict={x: 2.1, y: 3.0}))

# (deeplearning) C:\Users\gokul>tensorboard --logdir C:\Users\gokul\PycharmProjects\GpuTry\tensorflow\logs
