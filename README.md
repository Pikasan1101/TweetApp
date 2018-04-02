# TweetApp
ツイートできるやつ

### ライブラリのインストール
```
pip install -r requirements.txt
```

### トークン情報
conf/token.iniを置き，
```
[Tokens]
CK = Consumer_Key
CS = Consumer_Secret
AT = Access_Token
AS = Accesss_Token_Secert
```
とするとトークン情報を読み込みます．

### app化について
- TweetApp.icnsを用意し（sample.icnsをコピーしてTweetApp.icnsに変更してもよい）

```
pyinstaller TweetApp.spec
```
とすると、dict以下にTweetApp.appができます。
