# 2chproxy.py

2chproxy.plのpythonによる簡易実装  
Sikiに対して動作する　  
https://sikiapp.net/

2chproxy.plのほとんどの条件処理をすっ飛ばしている  
cgi-dat変換とCONNECTメソッド処理を実装している。  
それで、5chを見る上では問題ない。

## 経緯

2chproxy.pl  
<https://github.com/yama-natuki/2chproxy.pl>  
が自分のPC（M1Mac）上で動作しなかったので作った。  
（板更新が動作しなかった。CONNECTメソッドを処理する部分に問題がある様子）

## 動作

requests, beautifulsoup４を入れて　　

```sh
python server.py
```

で、127.0.0.1:8080で動き始めます。　　
