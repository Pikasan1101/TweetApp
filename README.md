# TweetApp
ツイートできるやつ
### トークン情報
TweetApp.pyと同じディレクトリにtoken.csvを置き，
```
CK,Consumer_Key
CS,Consumer_Secret
AT,Access_Token
AS,Accesss_Token_Secert
```
とするとトークン情報を読み込みます．

以下のコマンドでapp化
```
pyinstaller --windowed TweetApp.py -i TweetApp.icns
```
