本系统是基于多模型的DGA检测系统。

训练数据为alexa100万，以及jk数据的700万

可以实现在线及时检测域名。

DGA_detection主要是模型的调用以及训练和预测

feature_extraction主要用于特征的提取，在web展示中，暂时不需要这个文件。

requirement中介绍了所需环境，包的版本

本系统在python3.6的环境进行编写和运行，具体见requirements.txt

部署好环境之后，只需要运行run.py即可，通过浏览器可以访问。