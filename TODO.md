# Discount_Notf_Bot 

- 輸入商品網址並持續追蹤物品價格，若特價時發出訊息
- 預期指令：
  - `/add`
  - `/del`
  - `/list`
  - `/help`

# add 

- 新增商品網址
  - ```/add https://xxx```
- 尋找物品名稱和價格
- 寫入json

# del

- `/del "text"`
- if text
  - 刪除所有`prod_name`包含`text`的資料
- else
  - InlineKeyboard
    - 一次顯示3個，換頁

# list

- `/list "store_name"` 
- 呈現方式
  - 用網站區分
  - 訊息
    - 超連結
  - InlineKeyboard
    - 一次顯示3個，換頁

# good info

- json

1. - chat_id

   - prods
     1. - prod_name
        - url
        - price
     2. - prod_name
        - url
        - price
     3.  ......

2. - chat_id
   - ......

