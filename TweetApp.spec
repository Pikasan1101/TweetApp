# -*- mode: python -*-

block_cipher = None


a = Analysis(['TweetApp.py'],
             pathex=['/Users/.../TweetApp'], ##ユーザのTweetApp.pyが存在するディレクトリ
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          Tree('conf',prefix='conf'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='TweetApp',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='TweetApp.icns')
app = BUNDLE(exe,
             name='TweetApp.app',
             info_plist={ 'NSHighResolutionCapable': 'True'},
             icon='TweetApp.icns',
             bundle_identifier=None)
