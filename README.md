# 2chproxy.py
2chproxy.plのpythonによる簡易実装  
Sikiに対して動作する

2chproxy.plのほとんどの条件処理をすっ飛ばしている。
CONNECTと5chのread.cgi->dat変換のみ実装

*バグだらけなので適当に直して使ってください*

##  経緯
2chproxy.pl  
https://github.com/yama-natuki/2chproxy.pl  
が自分のPC（M1Mac）上で動作しなかったので作った。  
（板更新が動作しなかった。CONNECTメソッドを処理する部分に問題があるかも（？））  

## 動作
requests, beautifulsoup４を入れて
```
python server.py
```
で、127.0.0.1:8080で動き始めます。

