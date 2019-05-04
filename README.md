# Deep Hashing for Yalefaces

This work tries to retrieve [yalefaces](http://vision.ucsd.edu/content/yale-face-database) dataset. Yalefaces is a human faces dataset which contains 165 greyscale images. We use PyTorch and the method introduced in [HashNet](https://arxiv.org/abs/1702.00758) to conduct the experiment.

### Results

| Method  | Bits Number | Precision |
| ------- | ----------- | --------- |
| HashNet | 32          | 100%      |

### Dataset

Original dataset contains 15 humans' faces and each category has 11 different expressions. We first crop them to 100 x 100 resolution and then randomly select 2 images in each category to make a test dataset and the train dataset is made up for the rest of them. Then we extract the HOG features of these images.

To use the data:

```bash
$ cd <Repository Root>/yuhang
$ python pre_process.py
```

This will generate two npz files. These two npz files also have been stored in traindata and testdata root.

### HashNet

We use LeNet-5 structure with more channels to learn the hash codes. To run the training:

```bash
$ cd <Repository Root>/yuhang
$ python main.py 
```

 The trained hash codes also have been provided. To do the evaluation:

```bash
$ cd <Repository Root>/MNIST/
$ python main.py --evaluate
```







