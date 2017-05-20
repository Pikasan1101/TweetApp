# TweetApp
ツイートできるやつ
### トークン情報
conf/token.csvを置き，
```
CK,Consumer_Key
CS,Consumer_Secret
AT,Access_Token
AS,Accesss_Token_Secert
```
とするとトークン情報を読み込みます．

### app化について
- TweetApp.icnsを用意し、

```
pip install pyinstaller
pyinstaller TweetApp.spec
```
とすると、dict以下にTweetApp.appができます。