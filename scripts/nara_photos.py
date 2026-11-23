# build_nara_data.py が読み込む写真の一覧（表示する順）。文字だけのものは Toshi の写真（images/nara/）、
# W(...) は Wikimedia Commons から借りた写真（撮影者・ライセンス・ファイルのページ。2026-11-21 に Commons の API でライセンスを確認）
PHOTOS = {
    "eki": ["eki-1.jpg", "eki-2.jpg", "eki-3.jpg", "eki-4.jpg"],
    "kofukuji": [W("kofukuji-w1.jpg", "Saigen Jiro", "CC0", "File:Kofuku-ji, chukondou-2.jpg"),
                 W("kofukuji-w2.jpg", "Jakub Hałun", "CC BY-SA 4.0", "File:20100716 Nara Kofuku-ji Nanen-do 2431.jpg"),
                 "kofukuji-1.jpg"],
    "shika": ["shika-1.jpg", "shika-2.jpg"],
    "isuien": [W("isuien-w1.jpg", "Kimon Berlin", "CC BY-SA 4.0", "File:Isuien and Nandaimon.JPG"),
               W("isuien-w2.jpg", "Kimon Berlin", "CC BY-SA 2.0", "File:Isuien garden in Nara (11140708553).jpg"),
               W("isuien-w3.jpg", "Christophe95", "CC BY-SA 4.0", "File:House at Yoshiki-en.jpg")],
    "todaiji": ["todaiji-1.jpg", "todaiji-2.jpg",
                W("todaiji-w1.jpg", "Zairon", "CC BY 4.0", "File:Nara Todai-ji Daibutsuden Interior Daibutsu 07.jpg"),
                W("todaiji-w2.jpg", "Guilhem Vellut", "CC BY 2.0", "File:Nandaimon Gate @ Todai-ji Temple @ Nara (13324415835).jpg")],
    "nigatsudo": [W("nigatsudo-w1.jpg", "Christophe95", "CC BY-SA 4.0", "File:Nigatsu-dō at Todaiji 1.jpg"),
                  W("nigatsudo-w2.jpg", "Nekosuki", "CC BY-SA 4.0", "File:Todai-ji Nigatsu-do National Treasure 国宝東大寺二月堂06.JPG"),
                  W("nigatsudo-w3.jpg", "Nekosuki", "CC BY-SA 4.0", "File:Todai-ji Nigatsu-do National Treasure 国宝東大寺二月堂30.JPG")],
    "wakakusa": [W("wakakusa-w1.jpg", "Naokijp", "CC BY-SA 4.0", "File:Mount Wakakusa, View from Summit of a Mountain 001.jpg"),
                 W("wakakusa-w2.jpg", "Naokijp", "CC BY-SA 4.0", "File:Mount Wakakusa, The First Open Space on the Mountain 001.jpg"),
                 W("wakakusa-w3.jpg", "Naokijp", "CC BY-SA 4.0", "File:Mount Wakakusa, the Foot of the Mountain 001.jpg")],
    "kasuga": [W("kasuga-w1.jpg", "Saigen Jiro", "CC0", "File:Kasuga-taisha, chumon-2.jpg"),
               W("kasuga-w2.jpg", "Gzzz", "CC BY-SA 4.0", "File:Lanterns Kasuga-taisha Nara.jpg"),
               W("kasuga-w3.jpg", "Zairon", "CC BY 4.0", "File:Nara Kasuga-taisha Lanterns & Deer 02.jpg"),
               "kasuga-1.jpg"],
    "naramachi": [W("naramachi-w1.jpg", "Maarten Heerlien", "CC BY 2.0", "File:Street in Naramachi area (6156072416).jpg"),
                  W("naramachi-w2.jpg", "Bernard Gagnon", "CC BY-SA 3.0", "File:Gango-ji Gokurakubo.jpg")],
    # 春鹿（今西清兵衛商店）：Toshi の写真（2022-12-28。店の前・きき酒のグラス・冷蔵庫の瓶）。2026-11-22 に ならまち のスポットから分けた（もとは naramachi-1〜3.jpg）
    "harushika": ["harushika-1.jpg", "harushika-2.jpg", "harushika-3.jpg"],
    "heijo": [W("heijo-w1.jpg", "663highland", "CC BY-SA 4.0", "File:181103 Heijo Palace Daigokuden Nara Japan03bs.jpg"),
              W("heijo-w2.jpg", "Cun Cun", "CC BY-SA 4.0", "File:Suzakumon in Heijo Palace.jpg"),
              W("heijo-w3.jpg", "663highland", "CC BY-SA 4.0", "File:181103 Heijo Palace Daigokuden Nara Japan06s3.jpg")],
    # 法隆寺：公式サイトの「境内における禁止事項」に撮影が入っているので、三十三間堂と同じく境内の外（南大門の前の広場と道）から撮った写真だけ。
    # 2026-11-23 に、境内（西院伽藍の中）で撮られた horyuji-w1〜w3.jpg を外した（ファイルは images/nara/ に残してある）
    "horyuji": [W("horyuji-w4.jpg", "663highland", "CC BY 2.5", "File:Horyu-ji01s3200.jpg"),
                W("horyuji-w5.jpg", "Daderot", "CC0", "File:Nandaimon - Hōryū-ji - Ikaruga, Nara, Japan - DSC07553.jpg"),
                W("horyuji-w6.jpg", "Nodaunji", "CC BY-SA 4.0", "File:奈良自転車道 終点付近.jpg")],
}
