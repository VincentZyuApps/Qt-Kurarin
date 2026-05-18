
## Migrate assets from Win-kurarin

From the repository root:

```shell
python ./scripts/migrate_win_kurarin.py <absolute-path>
```

For example:

```powershell
python .\scripts\migrate_win_kurarin.py D:\aaaStuffsaaa\from_git\github\Win-kurarin
```

The script will:

- extract `String1` from `KyukurarinForm\asset.resx`
- write it to `python\data\script.txt`
- copy all `.png` and `.mp3` files from `KyukurarinForm\Resources\` into `python\resources\`
