# hashing_yalefaces

### 1 算法部分：训练图片哈希码

我的想法是采用深度网络的方式训练哈希码：

因为数据集只有165张图片网络结构不需要太复杂：我们先从AlexNet开始训练，后续可以考虑减小网络结构或者其他方法来减小网络结构：量化网络或者更小的网络（e.g. LeNet）

算法使用HashNet解决gradient mismatch问题，用Deep Cauchy Hashing来定义损失函数，并且量化损失由于HashNet的存在是可以抛弃的：

![image-20190227170039933](/Users/liyuhang/Documents/GitHub/hashing_yalefaces/figs/hashnet-ills.png)

![image-20190227170052581](/Users/liyuhang/Library/Application%20Support/typora-user-images/image-20190227170052581.png)

可以提升的点：

1. Less Bits： memory saving and computational efficient 

### 2. 检索程序部分：

我们最后存的数据库有几个：分为32bit，16bit，或者更低，需要设置一下选用哪个数据库进行演示

程序的功能有：需要能上传图片，重点是：**这张图片的哈希码必须要要在程序中自己实现，如果测试图片是固定的，那么我们把测试图片的哈希码也要录入数据库，并且上传图片后能够返回哈希码**

哈希码比对检索：按照汉明距离来检索：考虑到165张数据在32比特里面同一类的图片可能汉明距离差距过大，所以对比数据库的时候要小心设计

展示图片：(*ﾟДﾟ*) 

### 3.文档：

文档也分为算法和程序检索的实现两个部分，要分开来写，这个可以以后商榷

