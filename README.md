# 3D 小陳晉

可愛粽子與萬聖節南瓜公仔，包含 6 個版本、17 份 `.3mf`，以及完整 HTML 組裝與列印說明。

**網站：[https://zyyuy0u.github.io/3d-xiao-chenjin/](https://zyyuy0u.github.io/3d-xiao-chenjin/)**

- [萬聖節南瓜版](https://zyyuy0u.github.io/3d-xiao-chenjin/%E8%90%AC%E8%81%96%E7%AF%80_%E7%B5%84%E8%A3%9D%E8%AA%AA%E6%98%8E.html)：南瓜身體、彩色臉、頭髮三件組裝，約 10 公分。
- [粽子原色三件版](https://zyyuy0u.github.io/3d-xiao-chenjin/%E7%B2%BD%E5%AD%90%E4%B8%89%E4%BB%B6%E5%8E%9F%E8%89%B2_%E7%B5%84%E8%A3%9D%E8%AA%AA%E6%98%8E.html)：保留膚色臉、黑色五官、藍灰色眼鏡。
- 其他版本包含單色三件、八件分色組裝、單件四色及單件單色。

範例設定為 **Bambu Lab X1 Carbon / 0.4 mm 噴嘴 / PLA**。請在 Bambu Studio 以專案開啟 3MF，按實際設備與耗材重新切片。彩色臉需要 AMS／相容多色設備；零件先試配，再點膠固定。

萬聖節版可沿用原色三件版的臉與頭髮，只印南瓜身體約 3 小時 14 分鐘；整套估計約 13 小時 16 分鐘。估計不含換盤、清理與組裝，尚未實體試印。

## 檔案

- `index.html`：作品總覽；其他 HTML 為各版本說明。
- 根目錄 `.3mf`：可直接下載的模型專案。
- `assets/`：實際模型渲染圖。
- `docs/`：列印文字說明、幾何與切片驗證摘要。
- `models.json`：17 份列印檔的大小與 SHA-256。

## 本機預覽

```sh
python3 -m http.server 8000
```

開啟 `http://localhost:8000/`。網站使用相對連結，可部署在 GitHub Pages 專案路徑。

## 發布檢查

```sh
python3 tools/validate_site.py
```

網站保留可愛公仔內容，沒有原始人像照片、真人模型或臉部比對頁。
