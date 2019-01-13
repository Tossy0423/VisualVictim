# Name

VisualVictimDetector_v1<br>
視覚的被災者検知システム_v1

# Overview
RoboCupJunior2017以降,RescueMazeでは熱源の被災者に加えて,視覚的被災者(VisualVictim)を検知しなければならないルールが追加された.視覚的被災者(以降VVとする)を検知する方法はいろいろあるが,本プログラムはwebカメラを用いて検知を行うものである. <br>


# Dependency

## Language
* Python 3.7 

## Library(Python Module)
* OpenCV3.4.0 <br>
    <dd> 画像を処理するために使用 </dd>
    
* time
    <dd> プログラムの動作速度を計測するために使用. <br> デバッガとしても使っtた.</dd>

* numpy
    <dd> OpenCVでは画像は2次元配列として扱うため使用.使った記憶はないがおまじない.

# Setup

## Enviroment
* PC <br>
    <dd> MacBook Pro (Retina, 13-inch, Early 2015), mojave(10.14.2) </dd>

* WebCamera <br>
    <dd> Logicool C270 </dd>

* IDE <br>
    <dd> PyCharm 2018.3.2 (Community Edition) </dd>

# Usage

IDE(Pycharm)とPython3.7はすでにPCに入っているとする.

1. C270とPCを接続する.
2. 以降は動作目的に応じて変更してほしい.<br>

## カメラ番号設定
"x"には任意の数値を指定.PCが起動して認識した順番に番号が振り分けられる.
PC内蔵webカメラと外部webカメラだと,だいたい0 or 1.

> cap = cv2.VideoCapture(x)

## DEBUG Monitor



(使い方,できるだけ具体的に詳しく)

# Licence(MIT)
Copyright <2018> 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Author
Syunya Tanaka <br>
[GitHub]https://github.com/Tossy0423

# Created day
2018/12/23

# References

How to write README.md <br>
[online]https://karaage.hatenadiary.jp/entry/2018/01/19/073000

The MIT License <br>
[online]https://opensource.org/licenses/MIT

