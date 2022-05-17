# million

株価を予測するためのアプリケーションです。
SARIMA, RNN, Prophet(Facebookが開発した時系列予測ライブラリ)の3つの時系列分析を用いて予測を行います。
1週間から1年先までの予測を行い、グラフに表示します。

URL : https://yoshimine-mizuki.github.io/million/
※CGIを利用できないので動きません。
 

```
million/
├── Detail/ : 株価詳細ページ
│   ├── index.html : 株価の詳細を表示するページです。
│   └── post.html : Ajaxによりサーバーと通信を行うためのファイルです。
├── canvsjs/ グラフ表示のためのライブラリが格納されています。
├── cgi-bin/
│   ├── arma.py : Pythonのstatsmodelsライブラリを用いてSARIMAモデルを作成します。
│   ├── rnn.py : Kerasを用いてRNNモデルを作成します。
│   └── prophet.py : Facebookが開発した時系列予測ライブラリProphetを用いて株価予測を行います。
├── resources/
│   ├── css/style.css : スタイルシートです。
│   ├── js/canvsjs.min.js : グラフ表示のためのライブラリです。
│   └── ●●.json : 指数のデータです。
├── commodities.html : 商品先物ページ
├── cryptocurrency.html : 暗号通貨ページ
├── exchange.html : 為替ページ
├── future.html : 株価指数先物ページ
├── index.html : 株価指数ページ
├── post.html : Ajaxによりサーバーと通信を行うためのファイルです。
└── stock.html : 株式ページ
```
