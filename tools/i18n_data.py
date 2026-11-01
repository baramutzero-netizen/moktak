"""All player-facing text in 5 languages: ko (original), en, ja, zh-Hans, zh-Hant.
Run build_i18n() to produce i18n.json for the game bundle."""
import json
LANGS = ['ko', 'en', 'ja', 'zh-Hans', 'zh-Hant']
LANG_LABEL = {'ko': '한국어', 'en': 'English', 'ja': '日本語', 'zh-Hans': '简体中文', 'zh-Hant': '繁體中文'}

def L(ko, en, ja, hans, hant): return {'ko': ko, 'en': en, 'ja': ja, 'zh-Hans': hans, 'zh-Hant': hant}

UI = {
 'title': L('소 귀에 경 읽기', 'Sutras for a Cow', '牛に経文', '对牛诵经', '對牛誦經'),
 'subtitle': L('牛耳讀經 · 목탁 인크리멘탈', '牛耳讀經 · a moktak incremental', '牛耳讀經 · 木魚インクリメンタル', '牛耳读经 · 木鱼放置游戏', '牛耳讀經 · 木魚放置遊戲'),
 'settings': L('설정', 'Menu', '設定', '设置', '設定'),
 'open_settings': L('설정 열기', 'Open settings', '設定を開く', '打开设置', '打開設定'),
 'tab_yard': L('마당', 'Yard', '境内', '庭院', '庭院'),
 'tab_tree': L('수행도', 'Path', '修行図', '修行图', '修行圖'),
 'stage_aria': L('법회 마당. 누르면 목탁을 칩니다.', 'The sermon yard. Tap to strike the moktak.', '法会の境内。タップで木魚を叩きます。', '法会庭院。点按敲木鱼。', '法會庭院。點按敲木魚。'),
 'venue_label': L('도량', 'Venue', '道場', '道场', '道場'),
 'venue_info': L('소 {n} / {cap} · 악단 {p}', 'Cows {n} / {cap} · Band {p}', '牛 {n} / {cap} · 楽団 {p}', '牛 {n} / {cap} · 乐团 {p}', '牛 {n} / {cap} · 樂團 {p}'),
 'tap_aria': L('목탁 치기', 'Strike the moktak', '木魚を叩く', '敲木鱼', '敲木魚'),
 'kinds_aria': L('목탁 소리', 'Moktak sound', '木魚の音', '木鱼音色', '木魚音色'),
 'kind_basic': L('기본', 'Classic', '基本', '基本', '基本'),
 'kind_n': L('목탁 {n}', 'Moktak {n}', '木魚 {n}', '木鱼 {n}', '木魚 {n}'),
 'chant_label': L('지금 읽는 경', 'Now chanting', 'いま読んでいるお経', '正在诵读', '正在誦讀'),
 'path_label': L('심우도 · 소를 찾는 열 단계', 'Ten Ox-Herding Pictures', '十牛図 · 牛を探す十の段階', '十牛图 · 寻牛十阶段', '十牛圖 · 尋牛十階段'),
 'share_btn': L('결과 그림 공유', 'Share result', '結果画像をシェア', '分享结果图', '分享結果圖'),
 'ask_btn': L('문의하기', 'Contact', 'お問い合わせ', '联系我们', '聯絡我們'),
 'privacy': L('개인정보처리방침', 'Privacy policy', 'プライバシーポリシー', '隐私政策', '隱私權政策'),
 'st_taps': L('두드린 횟수', 'Taps', '叩いた回数', '敲击次数', '敲擊次數'),
 'st_total': L('쌓은 카르마', 'Karma earned', '積んだカルマ', '累计业力', '累計業力'),
 'st_time': L('수행 시간', 'Practice time', '修行時間', '修行时间', '修行時間'),
 'tree_aria': L('수행도. 노드를 눌러 선택하고 끌어서 움직입니다.', 'The path. Tap a node to select it, drag to move around.', '修行図。ノードをタップで選択、ドラッグで移動。', '修行图。点按节点选择，拖动浏览。', '修行圖。點按節點選擇，拖動瀏覽。'),
 'lg_owned': L('수행함', 'Done', '修行済み', '已修', '已修'),
 'lg_ready': L('지금 가능', 'Available', '今できる', '可修行', '可修行'),
 'lg_poor': L('카르마 부족', 'Need karma', 'カルマ不足', '业力不足', '業力不足'),
 'lg_locked': L('잠김', 'Locked', 'ロック', '未解锁', '未解鎖'),
 'z_in': L('확대', 'Zoom in', '拡大', '放大', '放大'),
 'z_out': L('축소', 'Zoom out', '縮小', '缩小', '縮小'),
 'z_home': L('가능한 노드로 이동', 'Go to an available node', '修行できるノードへ', '前往可修行的节点', '前往可修行的節點'),
 'sheet_pick': L('노드를 고르세요', 'Pick a node', 'ノードを選んでください', '请选择节点', '請選擇節點'),
 'sheet_hint': L('끌어서 둘러보고, 노드를 눌러 수행합니다.', 'Drag to look around, tap a node to practise it.', 'ドラッグで見回し、ノードをタップで修行します。', '拖动浏览，点按节点修行。', '拖動瀏覽，點按節點修行。'),
 'buy': L('수행', 'Practise', '修行', '修行', '修行'),
 'karma': L('카르마', 'karma', 'カルマ', '业力', '業力'),
 's_tok': L('목탁 소리', 'Moktak sound', '木魚の音', '木鱼声', '木魚聲'),
 's_chant': L('독경 소리', 'Chanting', '読経の声', '诵经声', '誦經聲'),
 's_chant_sub': L('스님의 염불', "The monk's recitation", 'お坊さんの念仏', '僧人的念诵', '僧人的念誦'),
 's_band': L('악단 소리', 'Band', '楽団の音', '乐团声', '樂團聲'),
 's_band_sub': L('동자승 · 메탈 밴드 · 오페라 · 오케스트라 · 법조인 · 개그팀 · 응원단 · 젬베 · 사물놀이', 'Novices · metal band · opera · orchestra · court · comedy · cheer squad · djembe · samulnori', '小僧 · メタルバンド · オペラ · オーケストラ · 法廷 · お笑い · 応援団 · ジャンベ · サムルノリ', '小沙弥 · 金属乐队 · 歌剧 · 管弦乐 · 法庭 · 喜剧 · 啦啦队 · 非洲鼓 · 四物游戏', '小沙彌 · 金屬樂團 · 歌劇 · 管弦樂 · 法庭 · 喜劇 · 啦啦隊 · 非洲鼓 · 四物遊戲'),
 's_lang': L('언어', 'Language', '言語', '语言', '語言'),
 's_contact': L('문의하기', 'Contact', 'お問い合わせ', '联系我们', '聯絡我們'),
 'copy_addr': L('주소 복사', 'Copy address', 'アドレスをコピー', '复制地址', '複製地址'),
 'write_mail': L('메일 쓰기', 'Write email', 'メールを書く', '写邮件', '寫郵件'),
 's_ga': L('방문 통계 보내기', 'Send usage stats', '利用統計を送る', '发送访问统计', '傳送造訪統計'),
 's_ga_sub': L('접속자 수·평균 플레이 시간 집계 (Google Analytics)', 'Visitor count and average play time (Google Analytics)', '訪問者数・平均プレイ時間の集計 (Google Analytics)', '统计访问人数与平均游玩时间 (Google Analytics)', '統計造訪人數與平均遊玩時間 (Google Analytics)'),
 's_priv_sub': L('무엇을 저장하고 무엇을 보내지 않는지', 'What is stored and what is not sent', '何を保存し、何を送らないか', '保存什么、不发送什么', '儲存什麼、不傳送什麼'),
 'view': L('보기', 'View', '見る', '查看', '查看'),
 'credit': L('그림과 기본 목탁·악기 소리는 도트와 합성음으로 만들었습니다. 목탁 1·2·3 소리: 김용배, 한국저작권위원회 공유마당, CC BY. 글꼴 갈무리(OFL).',
             'Pixel art and the classic moktak and instrument sounds were made in-house. Moktak 1-3 sounds: Kim Yong-bae, Korea Copyright Commission Gongu Madang, CC BY. Font: Galmuri (OFL).',
             'ドット絵と基本の木魚・楽器の音は自作です。木魚1・2・3の音: キム・ヨンベ、韓国著作権委員会 公有広場、CC BY。フォント: Galmuri (OFL)。',
             '像素画与基本木鱼、乐器声均为自制。木鱼1·2·3音效：金容培，韩国著作权委员会共享广场，CC BY。字体：Galmuri（OFL）。',
             '像素畫與基本木魚、樂器聲均為自製。木魚1·2·3音效：金容培，韓國著作權委員會共享廣場，CC BY。字型：Galmuri（OFL）。'),
 'close': L('닫기', 'Close', '閉じる', '关闭', '關閉'),
 'end_title': L('열반에 들다', 'Nirvana', '涅槃に入る', '入涅槃', '入涅槃'),
 'end_text': L('절간에서 시작해 콘서트장, 오페라홀, 오케스트라홀, 법원, 웃음 극장, 야구장, 초원, 서울을 지나 지구 전체가 법회장이 되었습니다. 무량대수 번 흘려들은 경이 마침내 모든 소의 마음에 닿았고, 소들은 연꽃 위에서 고요히 열반에 들었습니다.',
               'It began in a small temple, then the concert hall, the opera, the orchestra, the courthouse, the comedy club, the ballpark, the savanna and Seoul, until the whole Earth became a sermon hall. After an immeasurable number of sutras went in one ear and out the other, the words finally reached every cow’s heart, and they entered nirvana, quietly, on lotus flowers.',
               'お寺から始まり、コンサート会場、オペラハウス、オーケストラホール、裁判所、お笑い劇場、野球場、草原、ソウルを経て、地球全体が法会の場になりました。無量大数回聞き流したお経がついにすべての牛の心に届き、牛たちは蓮の上で静かに涅槃に入りました。',
               '从一座小寺开始，经过演唱会场、歌剧院、交响乐厅、法院、喜剧剧场、棒球场、草原和首尔，整个地球都成了法会道场。左耳进右耳出了无量大数遍的经文，终于传到每一头牛的心里，牛儿们在莲花上静静地入了涅槃。',
               '從一座小寺開始，經過演唱會場、歌劇院、交響樂廳、法院、喜劇劇場、棒球場、草原和首爾，整個地球都成了法會道場。左耳進右耳出了無量大數遍的經文，終於傳到每一頭牛的心裡，牛兒們在蓮花上靜靜地入了涅槃。'),
 'end_share': L('결과 그림 공유', 'Share result', '結果画像をシェア', '分享结果图', '分享結果圖'),
 'again': L('다시 윤회하기', 'Be reborn again', 'もう一度輪廻する', '再次轮回', '再次輪迴'),
 'xp_label': L('다른 게임도 해보기', 'Try another game', 'ほかのゲームも遊ぶ', '试试另一款游戏', '試試另一款遊戲'),
 'xp_title': L('조삼모사 (朝三暮四)', 'Three at Dawn, Four at Dusk (朝三暮四)', '朝三暮四', '朝三暮四', '朝三暮四'),
 'xp_desc': L('원숭이들에게 아침에 셋, 저녁에 넷. 도토리는 언제나 7개인데 포장만 바뀌는 인크리멘탈 게임입니다.', 'Three acorns for the monkeys at dawn, four at dusk. The total is always seven; only the packaging changes. (Korean only)', 'サルたちに朝は三つ、夕は四つ。どんぐりはいつも7個で、包装だけが変わる放置ゲームです。(韓国語のみ)', '早上给猴子三个，晚上四个。橡子永远是7个，变的只有包装的放置游戏。(仅韩语)', '早上給猴子三個，晚上四個。橡實永遠是7個，變的只有包裝的放置遊戲。(僅韓語)'),
 'xp_go': L('조삼모사 하러 가기', 'Play it', '遊びに行く', '去玩', '去玩'),
 'xp2_title': L('앙천이타 (仰天而唾)', 'Spitting at the Sky (仰天而唾)', '仰天而唾 (天に唾する)', '仰天而唾', '仰天而唾'),
 'xp2_desc': L('누워서 위로 뱉은 말은 결국 전부 내 얼굴로 돌아오는 풍자 인크리멘탈 게임입니다.', 'Lie on your back and spit insults at the sky. Everything you send up comes back down on your own face. (Korean only)', '寝転んで空に吐いた言葉は、結局すべて自分の顔に返ってくる風刺放置ゲームです。(韓国語のみ)', '躺着朝天吐出的话，最后全都落回自己脸上的讽刺放置游戏。(仅韩语)', '躺著朝天吐出的話，最後全都落回自己臉上的諷刺放置遊戲。(僅韓語)'),
 'xp2_go': L('앙천이타 하러 가기', 'Play it', '遊びに行く', '去玩', '去玩'),
 'xp3_title': L('소 잃고 외양간 고친다', 'Fixing the Barn Too Late', '牛を失ってから牛舎を直す', '亡羊补牢', '亡羊補牢'),
 'xp3_desc': L('소부터 손님, 시청자, 신뢰, 건강까지 잃고 나서야 고치는 사후약방문 인크리멘탈 게임입니다. 이 절간의 소들도 나옵니다.', 'Lose the cow, then the customers, the viewers, the trust, your health, and only then fix things. The cows from this temple appear too. (Korean only)', '牛から客、視聴者、信頼、健康まで、失ってから直す放置ゲームです。このお寺の牛たちも登場します。(韓国語のみ)', '从牛到客人、观众、信任、健康，总是丢了才补的放置游戏。这座寺里的牛也会出场。(仅韩语)', '從牛到客人、觀眾、信任、健康，總是丟了才補的放置遊戲。這座寺裡的牛也會出場。(僅韓語)'),
 'xp3_go': L('외양간 고치러 가기', 'Play it', '遊びに行く', '去玩', '去玩'),
 'share_title': L('결과 그림', 'Result card', '結果画像', '结果图', '結果圖'),
 'share_native': L('공유하기', 'Share', 'シェア', '分享', '分享'),
 'share_save': L('이미지 저장', 'Save image', '画像を保存', '保存图片', '儲存圖片'),
 'share_copy': L('자랑 문구+링크 복사', 'Copy brag + link', '自慢文+リンクをコピー', '复制炫耀文案+链接', '複製炫耀文案+連結'),
 'share_hint': L('휴대폰에서는 공유하기를 누르면 카카오톡을 고를 수 있습니다. 저장이 안 되면 그림을 길게 눌러 저장하세요.', 'On a phone, Share opens your share sheet. If saving fails, long-press the image to save it.', 'スマホではシェアから好きなアプリを選べます。保存できない場合は画像を長押ししてください。', '在手机上点分享即可选择应用。若无法保存，请长按图片保存。', '在手機上點分享即可選擇應用程式。若無法儲存，請長按圖片儲存。'),
 'rate': L('초당 약 {x}', 'about {x}/s', '毎秒 約{x}', '每秒约 {x}', '每秒約 {x}'),
 'rate_tap': L(' · 목탁을 쳐 주세요', ' · tap the moktak', ' · 木魚を叩いてください', ' · 请敲木鱼', ' · 請敲木魚'),
 'time_m': L('{m}분', '{m} min', '{m}分', '{m}分钟', '{m}分鐘'),
 'time_hm': L('{h}시간 {m}분', '{h} h {m} min', '{h}時間{m}分', '{h}小时{m}分钟', '{h}小時{m}分鐘'),
 'time_ms': L('{m}분 {s}초', '{m} min {s} s', '{m}分{s}秒', '{m}分{s}秒', '{m}分{s}秒'),
 'stage_toast': L('심우도 {n}단계 · {name}', 'Ox-herding stage {n} · {name}', '十牛図 第{n}段階 · {name}', '十牛图 第{n}阶段 · {name}', '十牛圖 第{n}階段 · {name}'),
 'end_stats': L('수행 시간 {t} · 목탁 {taps}번 · 흘려들은 공덕 {k} 카르마', 'Practice time {t} · {taps} taps · {k} karma let in one ear and out the other', '修行時間 {t} · 木魚 {taps}回 · 聞き流した功徳 {k} カルマ', '修行时间 {t} · 木鱼 {taps}次 · 左耳进右耳出的功德 {k} 业力', '修行時間 {t} · 木魚 {taps}次 · 左耳進右耳出的功德 {k} 業力'),
 'reset': L('처음부터 다시', 'Start over', '最初からやり直す', '从头开始', '從頭開始'),
 'reset_warn': L('모든 수행이 사라집니다.', 'All progress will be erased.', 'すべての修行が消えます。', '所有修行进度将被清除。', '所有修行進度將被清除。'),
 'erase': L('지우기', 'Erase', '消去', '清除', '清除'),
 'cancel': L('취소', 'Cancel', 'キャンセル', '取消', '取消'),
 'ga_on': L('방문 통계를 보냅니다', 'Sending usage stats', '利用統計を送ります', '将发送访问统计', '將傳送造訪統計'),
 'ga_off': L('방문 통계를 보내지 않습니다', 'Not sending usage stats', '利用統計を送りません', '不再发送访问统计', '不再傳送造訪統計'),
 'share_text': L('소 귀에 경 읽기 · {venue}에서 {n}마리 소에게 경을 읽어 {k} 카르마를 모았어요.{nir}\n같이 목탁 쳐요 👉 {url}',
                 'Sutras for a Cow · I read sutras to {n} cows at the {venue} and earned {k} karma.{nir}\nCome strike the moktak 👉 {url}',
                 '牛に経文 · {venue}で{n}頭の牛にお経を読んで{k}カルマを集めました。{nir}\n一緒に木魚を叩こう 👉 {url}',
                 '对牛诵经 · 我在{venue}给{n}头牛诵经，攒了{k}业力。{nir}\n一起来敲木鱼 👉 {url}',
                 '對牛誦經 · 我在{venue}給{n}頭牛誦經，攢了{k}業力。{nir}\n一起來敲木魚 👉 {url}'),
 'share_nir': L(' 소들이 열반에 들었습니다.', ' The cows entered nirvana.', ' 牛たちは涅槃に入りました。', ' 牛儿们入了涅槃。', ' 牛兒們入了涅槃。'),
 'card_karma': L('쌓은 카르마', 'Karma earned', '積んだカルマ', '累计业力', '累計業力'),
 'card_cows': L('모인 소', 'Cows gathered', '集まった牛', '聚集的牛', '聚集的牛'),
 'card_band': L('악단', 'Band', '楽団', '乐团', '樂團'),
 'card_time': L('수행 시간', 'Practice time', '修行時間', '修行时间', '修行時間'),
 'n_cows': L('{n}마리', '{n}', '{n}頭', '{n}头', '{n}頭'),
 'n_people': L('{n}명', '{n}', '{n}人', '{n}人', '{n}人'),
 'card_path': L('심우도 {n}/10 · {stage}', 'Ox-herding {n}/10 · {stage}', '十牛図 {n}/10 · {stage}', '十牛图 {n}/10 · {stage}', '十牛圖 {n}/10 · {stage}'),
 'share_fail': L('공유를 열 수 없습니다. 이미지 저장을 이용해 주세요', 'Sharing is unavailable here. Please use Save image.', 'シェアを開けません。画像保存を使ってください', '无法打开分享，请使用保存图片', '無法開啟分享，請使用儲存圖片'),
 'saved': L('저장했습니다', 'Saved', '保存しました', '已保存', '已儲存'),
 'save_started': L('저장을 시작했습니다. 안 되면 그림을 길게 눌러 저장하세요', 'Download started. If nothing happens, long-press the image.', '保存を開始しました。できない場合は画像を長押ししてください', '已开始保存。若无反应，请长按图片', '已開始儲存。若無反應，請長按圖片'),
 'longpress': L('그림을 길게 눌러 저장하세요', 'Long-press the image to save it', '画像を長押しして保存してください', '请长按图片保存', '請長按圖片儲存'),
 'copy_blocked': L('복사가 막혀 있습니다. 직접 선택해 복사해 주세요', 'Copying is blocked here. Please select and copy it yourself.', 'コピーできません。手動で選択してコピーしてください', '无法复制，请手动选择复制', '無法複製，請手動選擇複製'),
 'copied_share': L('자랑 문구와 게임 링크를 복사했습니다. 카카오톡에 붙여 넣으세요', 'Copied the brag and the game link. Paste it anywhere.', '自慢文とゲームのリンクをコピーしました。好きな所に貼り付けてください', '已复制炫耀文案与游戏链接，粘贴分享吧', '已複製炫耀文案與遊戲連結，貼上分享吧'),
 'copied_mail': L('메일 주소를 복사했습니다', 'Copied the email address', 'メールアドレスをコピーしました', '已复制邮箱地址', '已複製電子郵件地址'),
 'away': L('자리를 비운 사이 악단이 {k} 카르마를 모았습니다', 'While you were away, the band earned {k} karma', '留守の間に楽団が{k}カルマを集めました', '你离开时，乐团攒了{k}业力', '你離開時，樂團攢了{k}業力'),
 'quick_label': L('바로 수행', 'Quick', 'すぐ修行', '快速修行', '快速修行'),
 'quick_next': L('다음 수행: {name} · {cost} 카르마', 'Next: {name} · {cost} karma', '次の修行: {name} · {cost} カルマ', '下一项：{name} · {cost} 业力', '下一項：{name} · {cost} 業力'),
 'quick_done': L('모든 수행을 마쳤습니다', 'Every practice is done', 'すべての修行を終えました', '已完成全部修行', '已完成全部修行'),
 'tok': L('탁!', 'tok!', 'ポク!', 'tok!', 'tok!'),
 # node texts
 'n_root': L('법회 시작', 'The first sermon', '法会のはじまり', '法会开始', '法會開始'),
 'n_root_d': L('스님 한 분과 누렁소 한 마리. 모든 수행이 여기서 갈라져 나갑니다.', 'One monk and one cow. In Korean, so (소) means cow, and every guest you invite has a name ending in -so. Every path branches out from here.', 'お坊さん一人と牛一頭。韓国語で「ソ(소)」は牛のこと。招く客の名前はすべて「〜ソ」で終わります。すべての修行はここから枝分かれします。', '一位僧人和一头牛。在韩语里“소(so)”就是牛，之后来的客人名字都以“~so”结尾。所有修行从这里分出。', '一位僧人和一頭牛。在韓語裡「소(so)」就是牛，之後來的客人名字都以「~so」結尾。所有修行從這裡分出。'),
 'n_moktak': L('목탁 다듬기 {n}', 'Tune the moktak {n}', '木魚を磨く {n}', '打磨木鱼 {n}', '打磨木魚 {n}'),
 'n_moktak_t': L('목탁 다듬기 {n} / 20', 'Tune the moktak {n} / 20', '木魚を磨く {n} / 20', '打磨木鱼 {n} / 20', '打磨木魚 {n} / 20'),
 'n_moktak_d': L('목탁 소리가 한층 맑아집니다.', 'The moktak rings a little clearer.', '木魚の音が一段と澄みます。', '木鱼声更清亮了。', '木魚聲更清亮了。'),
 'n_mul': L('모든 공덕 ×{x}', 'All merit ×{x}', 'すべての功徳 ×{x}', '全部功德 ×{x}', '全部功德 ×{x}'),
 'n_inc': L('{inc} 공양', '{inc} offering', '{inc}の供養', '供{inc}', '供{inc}'),
 'n_inc_d': L('향 공양 {n}단계. 더 귀한 향일수록 연기가 진합니다.', 'Incense tier {n}. The rarer the incense, the thicker the smoke.', 'お香の供養 第{n}段階。貴重な香ほど煙が濃くなります。', '供香第{n}阶。越珍贵的香，烟越浓。', '供香第{n}階。越珍貴的香，煙越濃。'),
 'n_ear_t': L('귀 청소 · {ear}', 'Ear cleaning · {ear}', '耳掃除 · {ear}', '掏耳朵 · {ear}', '掏耳朵 · {ear}'),
 'n_ear_d': L('귀 청소 {n}단계. 귀가 뻥 뚫려 가끔 공덕이 크게 들어옵니다.', 'Ear cleaning tier {n}. With wide-open ears, merit sometimes pours in.', '耳掃除 第{n}段階。耳がすっきりして、ときどき功徳が大きく入ります。', '掏耳朵第{n}阶。耳朵通透了，偶尔会涌入大量功德。', '掏耳朵第{n}階。耳朵通透了，偶爾會湧入大量功德。'),
 'n_ear_e': L('대박 확률 +4% · 대박 배율 ×{x}까지', 'Jackpot chance +4% · jackpot up to ×{x}', '大当たり確率 +4% · 倍率 最大×{x}', '暴击率 +4% · 倍率最高 ×{x}', '暴擊率 +4% · 倍率最高 ×{x}'),
 'n_sutra_d': L("나무아미타불 뒤에 '{line}'를 이어 읽습니다.", "Adds '{line}' after Namu Amitabul.", '南無阿弥陀仏のあとに「{line}」を続けて読みます。', '在南无阿弥陀佛之后接着念“{line}”。', '在南無阿彌陀佛之後接著念「{line}」。'),
 'n_sutra_e': L('경 한 글자 공덕 ×{x}', 'Merit per syllable ×{x}', '経一文字の功徳 ×{x}', '每字功德 ×{x}', '每字功德 ×{x}'),
 'n_venue': L('{venue|ro} 옮기기', 'Move to the {venue}', '{venue}へ移る', '迁往{venue}', '遷往{venue}'),
 'n_venue_d': L('{venue}에 새 자리 {n}곳이 생깁니다.{extra}', 'The {venue} has room for {n} new guests.{extra}', '{venue}に新しい席が{n}つできます。{extra}', '{venue}多出{n}个新座位。{extra}', '{venue}多出{n}個新座位。{extra}'),
 'n_venue_grp': L(' {grp}도 부를 수 있습니다.', ' You can also invite the {grp}.', '{grp}も呼べます。', '还能请来{grp}。', '還能請來{grp}。'),
 'n_venue_earth': L(' 모든 원소가 소가 됩니다.', ' Every element becomes a cow.', 'すべての元素が牛になります。', '所有元素都变成牛。', '所有元素都變成牛。'),
 'n_list_e': L('이 소의 귀: 공덕 ×{x}', "This cow's ears: merit ×{x}", 'この牛の耳: 功徳 ×{x}', '这头牛的耳朵：功德 ×{x}', '這頭牛的耳朵：功德 ×{x}'),
 'n_perf_d': L('{grp} · {desc}.', '{grp} · {desc}.', '{grp} · {desc}。', '{grp} · {desc}。', '{grp} · {desc}。'),
 'n_perf_e': L('마디마다 {n}번, 한 번에 목탁 {x}번 몫', '{n} hits a bar, each worth {x} taps', '1小節に{n}回、1回で木魚{x}回分', '每小节{n}次，每次等于敲{x}下', '每小節{n}次，每次等於敲{x}下'),
 'n_nirvana': L('열반에 들다', 'Enter nirvana', '涅槃に入る', '入涅槃', '入涅槃'),
 'n_nirvana_d': L('모든 노드를 수행하면 열립니다. 무량대수 카르마를 바쳐 소들을 열반으로 이끕니다.', 'Opens once every node is done. Offer an immeasurable (10^68) amount of karma to lead the cows to nirvana.', 'すべてのノードを修行すると開きます。無量大数のカルマを捧げ、牛たちを涅槃へ導きます。', '完成所有节点后开启。献上无量大数的业力，引领牛儿们入涅槃。', '完成所有節點後開啟。獻上無量大數的業力，引領牛兒們入涅槃。'),
 'n_cond_ok': L('조건 충족', 'Ready', '条件達成', '条件已满足', '條件已滿足'),
 'n_cond': L('수행 {a} / {b}', 'Done {a} / {b}', '修行 {a} / {b}', '已修 {a} / {b}', '已修 {a} / {b}'),
 'hidden_d': L('{venue|ro} 옮기면 무엇인지 드러납니다.', 'Revealed once you move to the {venue}.', '{venue}へ移ると明らかになります。', '迁往{venue}后揭晓。', '遷往{venue}後揭曉。'),
 'st_owned': L('수행함', 'Done', '修行済み', '已修', '已修'),
 'st_ready': L('수행 가능', 'Available', '修行できる', '可修行', '可修行'),
 'st_poor': L('카르마 부족', 'Need karma', 'カルマ不足', '业力不足', '業力不足'),
 'st_locked': L('잠김', 'Locked', 'ロック', '未解锁', '未解鎖'),
 'b_later': L('아직', 'Not yet', 'まだ', '尚未', '尚未'),
 'b_prev': L('앞 노드 먼저', 'Previous first', '前のノードから', '先修前一项', '先修前一項'),
 't_listener': L('{name|iga} 왔습니다', '{name} has arrived', '{name}がやって来ました', '{name}来了', '{name}來了'),
 't_venue': L('{venue|ro} 옮겼습니다', 'Moved to the {venue}', '{venue}へ移りました', '已迁往{venue}', '已遷往{venue}'),
 't_sutra': L('이제 {name|eul} 이어 읽습니다', 'Now also chanting the {name}', 'これから{name}も読みます', '开始接着念{name}', '開始接著念{name}'),
 't_perf': L('{name} 합류', '{name} joined', '{name}が加入', '{name}加入', '{name}加入'),
 'perf_novice': L('동자승 {n}호', 'Novice #{n}', '小僧{n}号', '小沙弥{n}号', '小沙彌{n}號'),
 'unit_mult': L('×', '×', '×', '×', '×'),
 'pol_change': L('방침이 바뀌면 이 화면에 시행일과 함께 알립니다.', 'Any change will be announced here with a new effective date.', '方針を変更する場合は、この画面で施行日とともにお知らせします。', '政策如有变更，将在此页面连同生效日期一并公告。', '政策如有變更，將在此頁面連同生效日期一併公告。'),
}

VENUES = [
 L('절간', 'Temple', 'お寺', '寺院', '寺院'),
 L('콘서트장', 'Concert Hall', 'コンサート会場', '演唱会场', '演唱會場'),
 L('오페라홀', 'Opera House', 'オペラハウス', '歌剧院', '歌劇院'),
 L('오케스트라홀', 'Orchestra Hall', 'オーケストラホール', '交响乐厅', '交響樂廳'),
 L('법원', 'Courthouse', '裁判所', '法院', '法院'),
 L('웃음 극장', 'Comedy Club', 'お笑い劇場', '喜剧剧场', '喜劇劇場'),
 L('야구장', 'Ballpark', '野球場', '棒球场', '棒球場'),
 L('아프리카 초원', 'African Savanna', 'アフリカの草原', '非洲草原', '非洲草原'),
 L('서울', 'Seoul', 'ソウル', '首尔', '首爾'),
 L('지구', 'Earth', '地球', '地球', '地球'),
]

# listener: ko name/tag come from art2.LISTENERS; translations here: (en name, en tag, ja name, ja tag, hans name, hans tag, hant name, hant tag)
LISTENERS = {
 'hanwoo': ('Hanwoo', 'Korean cattle, here from the start. Gentle ears.', '韓牛', '最初からいる韓牛。おとなしい耳。', '韩牛', '一开始就在的韩牛。耳朵很温顺。', '韓牛', '一開始就在的韓牛。耳朵很溫順。'),
 'holstein': ('Spotted cow', 'Every spot soaks up a line of sutra.', 'まだら牛', 'まだらの一つ一つにお経がしみ込む。', '花奶牛', '每块斑点都渗进一行经文。', '花乳牛', '每塊斑點都滲進一行經文。'),
 'heuku': ('Black cow', 'From Jeju. Sutras vanish into the black.', '黒牛', '済州島から来た。お経が黒く吸い込まれる。', '黑牛', '来自济州岛。经文被黑黑地吸进去。', '黑牛', '來自濟州島。經文被黑黑地吸進去。'),
 'chik': ('Brindle cow', 'Chikso, the striped Korean cow. Its stripes wind like sutras.', '縞牛(チクソ)', '縞模様の韓国の牛。模様がお経のようにうねる。', '虎斑牛', '韩国的虎斑牛。花纹像经文一样蜿蜒。', '虎斑牛', '韓國的虎斑牛。花紋像經文一樣蜿蜒。'),
 'hwang': ('Bull', 'Came with a nose ring. Stubbornness is practice too.', '雄牛', '鼻輪までつけて来た。頑固さも修行。', '公牛', '连鼻环都戴来了。倔强也是修行。', '公牛', '連鼻環都戴來了。倔強也是修行。'),
 'haeuso': ('Haeuso', 'Temples call the outhouse "the place that dissolves worries".', '解憂所', 'お寺ではトイレを「憂いを解く所」と呼ぶ。', '解忧所', '寺院把茅房叫作“解忧所”。', '解憂所', '寺院把茅房叫作「解憂所」。'),
 'yak': ('Yak', 'From the Himalayas. Sutras leak out through the ear fur.', 'ヤク', 'ヒマラヤから来た。耳毛の間からお経が漏れる。', '牦牛', '来自喜马拉雅。经文从耳毛间漏出来。', '犛牛', '來自喜馬拉雅。經文從耳毛間漏出來。'),
 'bison': ('Bison', 'Of the prairie. Best headbanger in the room.', 'バイソン', '草原の野牛。ヘドバンが一番激しい。', '野牛', '草原上的野牛。甩头最用力。', '野牛', '草原上的野牛。甩頭最用力。'),
 'goat': ('Goat', 'A goat pretending to be a cow. Listens with its beard.', 'ヤギ', '牛のふりをしたヤギ。あごひげで聞く。', '山羊', '装成牛的山羊。用胡子听经。', '山羊', '裝成牛的山羊。用鬍子聽經。'),
 'bgoat': ('Black goat', 'Looks like it wore a tuxedo. It was just born black.', '黒ヤギ', 'タキシードかと思ったら、元から黒い。', '黑山羊', '还以为穿了燕尾服，其实天生就黑。', '黑山羊', '還以為穿了燕尾服，其實天生就黑。'),
 'danso': ('Danso flute', 'A bamboo flute. Sutras slip out of every hole.', '短簫', '竹の笛。穴ごとにお経が抜けていく。', '短箫', '竹笛。经文从每个孔里溜走。', '短簫', '竹笛。經文從每個孔裡溜走。'),
 'tungso': ('Tungso flute', "The danso's big brother. Takes sutras in a low voice.", '洞簫', '短簫の兄貴分。低い声でお経を受ける。', '洞箫', '短箫的大哥。用低音接住经文。', '洞簫', '短簫的大哥。用低音接住經文。'),
 'eumso': ('Phoneme', 'The smallest unit of sound. Turns back into sound in a cow’s ear.', '音素', '音の最小単位。牛の耳で音に戻る。', '音素', '声音的最小单位。在牛耳里变回声音。', '音素', '聲音的最小單位。在牛耳裡變回聲音。'),
 'goso': ('Complaint', 'Wants to know who read sutras to a cow.', '告訴', '誰が牛に経を読んだのか問いただす。', '告诉', '要追究是谁对牛诵经。', '告訴', '要追究是誰對牛誦經。'),
 'hangso': ('Appeal', 'Rejected the first ruling. Opened its ears again.', '控訴', '一審に不服。耳をもう一度開いた。', '上诉', '不服一审。再次张开耳朵。', '上訴', '不服一審。再次張開耳朵。'),
 'sangso': ('Higher appeal', 'Listens again from a higher bench.', '上訴', 'もっと高い所でもう一度聞く。', '再上诉', '到更高一级再听一次。', '再上訴', '到更高一級再聽一次。'),
 'seungso': ('Victory', 'Won! The court agreed the sutras went in.', '勝訴', '勝った! お経がちゃんと入ったと認められた。', '胜诉', '赢了！法院认定经文确实进了耳朵。', '勝訴', '贏了！法院認定經文確實進了耳朵。'),
 'paeso': ('Defeat', 'Lost. Still keeps listening.', '敗訴', '負けた。それでもお経は聞き続ける。', '败诉', '输了。但还是继续听经。', '敗訴', '輸了。但還是繼續聽經。'),
 'giso': ('Indictment', 'The prosecutor formally indicted sutra reading.', '起訴', '検察が読経を正式に起訴した。', '起诉', '检察官正式起诉了诵经。', '起訴', '檢察官正式起訴了誦經。'),
 'gongso': ('Public charge', 'Reading the indictment aloud is sutra reading too.', '公訴', '起訴状の朗読も結局は読経だ。', '公诉', '宣读起诉书说到底也是诵经。', '公訴', '宣讀起訴書說到底也是誦經。'),
 'jeso': ('Lawsuit', 'A cow filed a suit. The paperwork is udderly in order.', '提訴', '訴状を出します。牛が訴状を出した。', '提诉', '递交诉状。是牛递的。', '提訴', '遞交訴狀。是牛遞的。'),
 'banso': ('Countersuit', 'Cow sues cow.', '反訴', '逆告訴。牛が牛を。', '反诉', '反告。牛告牛。', '反訴', '反告。牛告牛。'),
 'hoso': ('Plea', 'Your Honor, I was only listening.', '哀訴', '裁判長、私はただ聞いていただけです。', '哀诉', '法官大人，我只是听了而已。', '哀訴', '法官大人，我只是聽了而已。'),
 'poksoh': ('Burst of laughter', 'Cracked up in the middle of a sutra.', '爆笑', 'お経の途中で吹き出した。', '爆笑', '听经听到一半笑喷了。', '爆笑', '聽經聽到一半笑噴了。'),
 'silso': ('Snort', 'So absurd it lets out a little snort.', '失笑', 'あきれて思わずプッ。', '失笑', '无语到噗嗤一笑。', '失笑', '無語到噗嗤一笑。'),
 'naengso': ('Sneer', 'Lifts just one corner of its mouth, coldly.', '冷笑', '冷たく片方の口角だけ上げる。', '冷笑', '冷冷地只扬起一边嘴角。', '冷笑', '冷冷地只揚起一邊嘴角。'),
 'joso': ('Mockery', 'Sticks out its tongue. A teasing laugh.', '嘲笑', 'あっかんべー。からかう笑い。', '嘲笑', '吐舌头。取笑人的笑。', '嘲笑', '吐舌頭。取笑人的笑。'),
 'damso': ('Chit-chat', 'Can’t stop gossiping about the sutras.', '談笑', 'お経の話でおしゃべりが止まらない。', '谈笑', '聊经文聊个不停。', '談笑', '聊經文聊個不停。'),
 'hongso': ('Guffaw', 'Laughs till its face turns red.', '哄笑', '顔が赤くなるほどガハハ。', '哄笑', '笑到满脸通红。', '哄笑', '笑到滿臉通紅。'),
 'ilso': ('One smile', 'Laughs once and forgets it all.', '一笑', '一度笑ってすべて忘れる。', '一笑', '一笑置之，全都忘了。', '一笑', '一笑置之，全都忘了。'),
 'bakjang': ('Clapping laugh', 'Claps its hooves and roars with laughter.', '拍手大笑', '手を叩いて大笑い。', '拍掌大笑', '拍着手放声大笑。', '拍掌大笑', '拍著手放聲大笑。'),
 'paan': ('Face-splitting laugh', 'Laughs so hard its face might crack.', '破顔大笑', '顔が割れそうなほど大笑い。', '破颜大笑', '笑得脸都快裂开了。', '破顏大笑', '笑得臉都快裂開了。'),
 'maepyo': ('Ticket booth', 'Two outfield seats, please. Sutras are free.', '切符売り場', '外野席2枚。お経は無料。', '售票处', '外野席两张。经文免费。', '售票處', '外野席兩張。經文免費。'),
 'annae': ('Info booth', 'Sutras enter the left ear and exit the right.', '案内所', 'お経は左の耳から入って右の耳から出ます。', '服务台', '经文从左耳进，右耳出。', '服務台', '經文從左耳進，右耳出。'),
 'hyuge': ('Rest stop', 'A short break at a highway rest stop.', '休憩所', '高速道路の休憩所でひと休み。', '服务区', '在高速公路服务区歇一会儿。', '休息站', '在高速公路休息站歇一會兒。'),
 'rhino': ('Rhino', 'Hears with its horn before its ears.', 'サイ', '耳より先に角が聞く。', '犀牛', '角比耳朵先听见。', '犀牛', '角比耳朵先聽見。'),
 'wrhino': ('White rhino', 'White in name only. Its wide mouth holds a lot of sutra.', 'シロサイ', '名前だけ白い。口が広くお経をたっぷり含む。', '白犀牛', '只有名字是白的。嘴宽，能含很多经文。', '白犀牛', '只有名字是白的。嘴寬，能含很多經文。'),
 'brhino': ('Black rhino', 'An ascetic of the savanna. Walks alone.', 'クロサイ', 'サバンナの修行者。ひとりで歩く。', '黑犀牛', '草原上的修行者。独自前行。', '黑犀牛', '草原上的修行者。獨自前行。'),
 'buffalo': ('Water buffalo', 'Sutras drain out like water in the ear.', '水牛', '耳に入った水のようにお経がよく抜ける。', '水牛', '经文像耳朵进水一样流出去。', '水牛', '經文像耳朵進水一樣流出去。'),
 'pachul': ('Police box', 'An officer came, confusing "sutra" with "police" (both gyeong in Korean).', '派出所', '「経(キョン)」と「警(キョン)」を取り違えた巡査が来た。', '派出所', '把“经”和“警”(韩语同音)搞混的警察来了。', '派出所', '把「經」和「警」(韓語同音)搞混的警察來了。'),
 'bogeon': ('Health center', 'Ear checkups are free.', '保健所', '耳の健康診断は無料です。', '保健站', '耳朵体检免费。', '衛生所', '耳朵健檢免費。'),
 'juyu': ('Gas station', 'Fill it up with sutras, please.', 'ガソリンスタンド', 'お経を満タンでお願いします。', '加油站', '请把经文加满。', '加油站', '請把經文加滿。'),
 'sobang': ('Fire station', 'Really a fire "seo", but answered the call as a fire "so" today.', '消防署', '本当は消防「署(ソ)」。今日だけ消防「所」で出動。', '消防站', '本来是消防“署”，今天以消防“所”出动。', '消防隊', '本來是消防「署」，今天以消防「所」出動。'),
 'samu': ('Office', 'Sutra submissions at window 3.', '事務所', 'お経の受付は3番窓口で。', '办事处', '经文请到3号窗口办理。', '辦事處', '經文請到3號窗口辦理。'),
 'suk': ('Lodging', 'Keeps its ears open even while asleep.', '宿所', '寝ていても耳は開けておく。', '宿舍', '睡着了耳朵也张着。', '宿舍', '睡著了耳朵也張著。'),
 'setak': ('Laundry', 'We wash your ears squeaky clean.', 'クリーニング店', '耳をきれいに洗います。', '洗衣店', '帮你把耳朵洗得干干净净。', '洗衣店', '幫你把耳朵洗得乾乾淨淨。'),
 'ibal': ('Barbershop', 'A neat trim around the ears. Sutras sound clearer.', '理髪店', '耳まわりをすっきり。お経がよく聞こえる。', '理发店', '把耳边头发修整齐，经文听得更清楚。', '理髮店', '把耳邊頭髮修整齊，經文聽得更清楚。'),
 'yeongu': ('Research lab', 'Studying the effects of reading sutras to cows.', '研究所', '牛に経を読む効果を研究中。', '研究所', '正在研究对牛诵经的效果。', '研究所', '正在研究對牛誦經的效果。'),
 'baljeon': ('Power plant', 'Turns leaked sutras into electricity.', '発電所', '流れ出たお経で電気を作る。', '发电站', '用流出来的经文发电。', '發電廠', '用流出來的經文發電。'),
 'suso': ('Hydrogen', 'The lightest "so" in the universe.', '水素', '宇宙で一番軽い「ソ」。', '氢', '宇宙中最轻的“so”。', '氫', '宇宙中最輕的「so」。'),
 'sanso': ('Oxygen', 'Hears sutras with every breath.', '酸素', '息をするたびにお経を聞く。', '氧', '每次呼吸都在听经。', '氧', '每次呼吸都在聽經。'),
 'tanso': ('Carbon', 'The backbone of all life.', '炭素', 'すべての生命の骨組み。', '碳', '一切生命的骨架。', '碳', '一切生命的骨架。'),
 'jilso': ('Nitrogen', '70% of the air. Also lives in chip bags.', '窒素', '空気の7割。お菓子の袋にも住む。', '氮', '空气的七成。也住在零食袋里。', '氮', '空氣的七成。也住在零食袋裡。'),
 'yeomso': ('Chlorine', 'Not the goat from before (both are yeomso in Korean). Smells like a pool.', '塩素', 'さっきのヤギではない(韓国語では同じ「ヨムソ」)。プールの匂い。', '氯', '不是刚才那只山羊(韩语同音)。有泳池的味道。', '氯', '不是剛才那隻山羊(韓語同音)。有泳池的味道。'),
 'hyoso': ('Enzyme', 'Digests the sutras into tiny pieces.', '酵素', '聞いたお経を細かく消化してくれる。', '酶', '把听到的经文消化得细细的。', '酵素', '把聽到的經文消化得細細的。'),
 'yeoprok': ('Chlorophyll', 'Photosynthesises sutras from sunlight.', '葉緑素', '日の光でお経を光合成する。', '叶绿素', '用阳光把经文光合作用。', '葉綠素', '用陽光把經文光合作用。'),
 'wonso': ('Element', 'Not on the periodic table. Symbol: So.', '元素', '周期表にない元素。記号はSo。', '元素', '周期表上没有的元素，符号So。', '元素', '週期表上沒有的元素，符號So。'),
 'miso': ('Smile', 'The flower sermon: the Buddha held up a flower, and a smile answered.', '微笑', '拈華微笑。花を掲げると、にっこり笑った。', '微笑', '拈花微笑。佛陀举起一朵花，便会心一笑。', '微笑', '拈花微笑。佛陀舉起一朵花，便會心一笑。'),
 'white': ('White ox', 'Where all the cows return as one. It awaits nirvana.', '白い牛', 'すべての牛が一つに還る場所。涅槃を待つ。', '白牛', '众牛归一之处。静待涅槃。', '白牛', '眾牛歸一之處。靜待涅槃。'),
}

GROUPS = {  # short, title, desc
 'novice': [('동자승', '동자승 들이기', '마디마다 작은 목탁을 두 번 칩니다'), ('novices', 'Take in novices', 'tap a small moktak twice a bar'), ('小僧', '小僧を迎える', '1小節に2回、小さな木魚を叩きます'), ('小沙弥', '收小沙弥', '每小节敲两下小木鱼'), ('小沙彌', '收小沙彌', '每小節敲兩下小木魚')],
 'metal': [('메탈 밴드', '메탈 밴드 섭외', '드럼과 베이스, 기타가 경에 박자를 싣습니다'), ('metal band', 'Book a metal band', 'drums, bass and guitars put a beat on the sutra'), ('メタルバンド', 'メタルバンドを呼ぶ', 'ドラム、ベース、ギターがお経にビートを乗せます'), ('金属乐队', '请金属乐队', '鼓、贝斯和吉他为经文打节拍'), ('金屬樂團', '請金屬樂團', '鼓、貝斯和吉他為經文打節拍')],
 'opera': [('오페라단', '오페라단 초청', '마디마다 화음을 길게 노래합니다'), ('opera company', 'Invite the opera', 'hold long chords every bar'), ('オペラ団', 'オペラ団を招く', '小節ごとに和音を長く歌います'), ('歌剧团', '邀请歌剧团', '每小节唱出悠长的和声'), ('歌劇團', '邀請歌劇團', '每小節唱出悠長的和聲')],
 'orch': [('오케스트라', '오케스트라 모시기', '현악과 관악, 팀파니가 화음을 받칩니다'), ('orchestra', 'Invite the orchestra', 'strings, winds and timpani carry the harmony'), ('オーケストラ', 'オーケストラを招く', '弦と管、ティンパニが和音を支えます'), ('管弦乐团', '邀请管弦乐团', '弦乐、管乐与定音鼓托起和声'), ('管弦樂團', '邀請管弦樂團', '弦樂、管樂與定音鼓托起和聲')],
 'court': [('법조인', '법정 사람들 모시기', '의사봉과 이의 제기, 타자 소리로 재판이 열립니다'), ('court officers', 'Call the court', 'a gavel, objections and typing open the trial'), ('法曹', '法廷の人々を呼ぶ', '小槌と異議、タイプ音で裁判が始まります'), ('法律人', '请来法庭众人', '法槌、异议与打字声开启审判'), ('法律人', '請來法庭眾人', '法槌、異議與打字聲開啟審判')],
 'comedy': [('개그팀', '개그팀 섭외', '개그와 림샷, 웃음과 박수가 터집니다'), ('comedy troupe', 'Book the comedians', 'jokes, rimshots, laughter and applause'), ('お笑い芸人', '芸人を呼ぶ', 'ギャグとリムショット、笑いと拍手が起きます'), ('喜剧团', '请喜剧团', '笑话、军鼓收尾、笑声与掌声'), ('喜劇團', '請喜劇團', '笑話、軍鼓收尾、笑聲與掌聲')],
 'cheer': [('응원단', '응원단 부르기', '메가폰과 박수, 북과 트럼펫으로 응원합니다'), ('cheer squad', 'Call the cheer squad', 'megaphones, claps, drums and a trumpet'), ('応援団', '応援団を呼ぶ', 'メガホンと拍手、太鼓とトランペットで応援します'), ('啦啦队', '叫来啦啦队', '用喇叭、掌声、鼓和小号加油'), ('啦啦隊', '叫來啦啦隊', '用大聲公、掌聲、鼓和小號加油')],
 'djembe': [('젬베 연주자', '젬베 연주자 모시기', '초원의 리듬을 겹겹이 쌓습니다'), ('djembe players', 'Invite djembe players', 'layer the rhythm of the savanna'), ('ジャンベ奏者', 'ジャンベ奏者を招く', '草原のリズムを重ねます'), ('非洲鼓手', '邀请非洲鼓手', '层层叠起草原的节奏'), ('非洲鼓手', '邀請非洲鼓手', '層層疊起草原的節奏')],
 'samul': [('사물놀이패', '사물놀이패 모시기', '꽹과리 · 장구 · 북 · 징이 휘몰아칩니다'), ('samulnori troupe', 'Invite a samulnori troupe', 'kkwaenggwari, janggu, buk and jing whirl together'), ('サムルノリ', 'サムルノリを招く', 'ケンガリ・チャング・プク・チンが渦巻きます'), ('四物游戏团', '邀请四物游戏团', '小锣、长鼓、鼓与大锣齐鸣'), ('四物遊戲團', '邀請四物遊戲團', '小鑼、長鼓、鼓與大鑼齊鳴')],
}

PERF = {  # key: (ko, en, ja, hans, hant); {n} for numbered
 'm_drum': ('드러머', 'Drummer', 'ドラマー', '鼓手', '鼓手'), 'm_bass': ('베이시스트', 'Bassist', 'ベーシスト', '贝斯手', '貝斯手'),
 'm_rhythm': ('리듬 기타', 'Rhythm guitar', 'リズムギター', '节奏吉他', '節奏吉他'), 'm_lead': ('리드 기타', 'Lead guitar', 'リードギター', '主音吉他', '主音吉他'),
 'o_ten': ('테너', 'Tenor', 'テノール', '男高音', '男高音'), 'o_sop': ('소프라노', 'Soprano', 'ソプラノ', '女高音', '女高音'),
 'o_bar': ('바리톤', 'Baritone', 'バリトン', '男中音', '男中音'), 'o_mez': ('메조소프라노', 'Mezzo-soprano', 'メゾソプラノ', '女中音', '女中音'),
 'o_choir': ('합창단', 'Choir', '合唱団', '合唱团', '合唱團'),
 'r_cond': ('지휘자', 'Conductor', '指揮者', '指挥', '指揮'), 'r_vln': ('바이올린', 'Violin', 'バイオリン', '小提琴', '小提琴'),
 'r_vc': ('첼로', 'Cello', 'チェロ', '大提琴', '大提琴'), 'r_fl': ('플루트', 'Flute', 'フルート', '长笛', '長笛'),
 'r_hn': ('호른', 'Horn', 'ホルン', '圆号', '法國號'), 'r_timp': ('팀파니', 'Timpani', 'ティンパニ', '定音鼓', '定音鼓'),
 'j_judge': ('판사', 'Judge', '裁判官', '法官', '法官'), 'j_pros': ('검사', 'Prosecutor', '検察官', '检察官', '檢察官'),
 'j_lawyer': ('변호사', 'Lawyer', '弁護士', '律师', '律師'), 'j_steno': ('속기사', 'Stenographer', '速記官', '速记员', '速記員'),
 'h_comic': ('개그맨', 'Comedian', '芸人', '喜剧演员', '喜劇演員'), 'h_drum': ('림샷 드러머', 'Rimshot drummer', 'リムショット係', '效果鼓手', '效果鼓手'),
 'h_crowd': ('웃음 관객', 'Laughing audience', '笑う観客', '笑场观众', '笑場觀眾'), 'h_clap': ('박수 부대', 'Clapping crew', '拍手隊', '鼓掌团', '鼓掌團'),
 'c_leader': ('응원단장', 'Cheer captain', '応援団長', '啦啦队长', '啦啦隊長'),
 'c_cheer0': ('치어리더 1', 'Cheerleader 1', 'チアリーダー1', '啦啦队员1', '啦啦隊員1'), 'c_cheer1': ('치어리더 2', 'Cheerleader 2', 'チアリーダー2', '啦啦队员2', '啦啦隊員2'),
 'c_cheer2': ('치어리더 3', 'Cheerleader 3', 'チアリーダー3', '啦啦队员3', '啦啦隊員3'),
 'c_drum': ('응원 북', 'Cheer drum', '応援太鼓', '助威鼓', '助威鼓'), 'c_trumpet': ('트럼펫', 'Trumpet', 'トランペット', '小号', '小號'),
 'd_djembe0': ('젬베 연주자 1', 'Djembe player 1', 'ジャンベ奏者1', '非洲鼓手1', '非洲鼓手1'), 'd_djembe1': ('젬베 연주자 2', 'Djembe player 2', 'ジャンベ奏者2', '非洲鼓手2', '非洲鼓手2'),
 'd_djembe2': ('젬베 연주자 3', 'Djembe player 3', 'ジャンベ奏者3', '非洲鼓手3', '非洲鼓手3'),
 's_kkwaeng': ('꽹과리', 'Kkwaenggwari', 'ケンガリ', '小锣', '小鑼'), 's_janggu': ('장구', 'Janggu', 'チャング', '长鼓', '長鼓'),
 's_buk': ('북', 'Buk drum', 'プク', '鼓', '鼓'), 's_jing': ('징', 'Jing gong', 'チン', '大锣', '大鑼'),
}

STAGES = {  # hanja names per script; descriptions per language
 'ko': [('심우 尋牛', '소를 찾아 나서다'), ('견적 見跡', '소의 발자국을 보다'), ('견우 見牛', '소를 보다'), ('득우 得牛', '소를 얻다'), ('목우 牧牛', '소를 길들이다'), ('기우귀가 騎牛歸家', '소를 타고 집으로 돌아오다'), ('망우존인 忘牛存人', '소는 잊고 사람만 남다'), ('인우구망 人牛俱忘', '소도 사람도 모두 잊다'), ('반본환원 返本還源', '근원으로 돌아가다'), ('입전수수 入廛垂手', '저잣거리로 들어가 손을 드리우다')],
 'en': [('Searching for the Ox', '尋牛'), ('Seeing the Traces', '見跡'), ('Seeing the Ox', '見牛'), ('Catching the Ox', '得牛'), ('Taming the Ox', '牧牛'), ('Riding the Ox Home', '騎牛歸家'), ('Ox Forgotten, Self Remains', '忘牛存人'), ('Both Forgotten', '人牛俱忘'), ('Returning to the Source', '返本還源'), ('Into the Marketplace', '入廛垂手')],
 'ja': [('尋牛', '牛を探しに出る'), ('見跡', '牛の足跡を見つける'), ('見牛', '牛を見る'), ('得牛', '牛をつかまえる'), ('牧牛', '牛を飼い慣らす'), ('騎牛帰家', '牛に乗って家に帰る'), ('忘牛存人', '牛を忘れ、人だけが残る'), ('人牛倶忘', '牛も人も忘れる'), ('返本還源', '本源に還る'), ('入鄽垂手', '町に入り、手を差し伸べる')],
 'zh-Hans': [('寻牛', '出发寻找牛'), ('见迹', '看见牛的足迹'), ('见牛', '看见了牛'), ('得牛', '抓住了牛'), ('牧牛', '驯服了牛'), ('骑牛归家', '骑牛回家'), ('忘牛存人', '忘了牛，只剩人'), ('人牛俱忘', '人与牛都忘了'), ('返本还源', '回到本源'), ('入廛垂手', '走进市集，垂手助人')],
 'zh-Hant': [('尋牛', '出發尋找牛'), ('見跡', '看見牛的足跡'), ('見牛', '看見了牛'), ('得牛', '抓住了牛'), ('牧牛', '馴服了牛'), ('騎牛歸家', '騎牛回家'), ('忘牛存人', '忘了牛，只剩人'), ('人牛俱忘', '人與牛都忘了'), ('返本還源', '回到本源'), ('入廛垂手', '走進市集，垂手助人')],
}

INC = L(['선향', '백단향', '침향', '정향', '유향', '안식향', '용연향', '전단향', '우담화향'],
        ['stick incense', 'sandalwood', 'agarwood', 'clove', 'frankincense', 'benzoin', 'ambergris', 'chandan', 'udumbara'],
        ['線香', '白檀', '沈香', '丁子', '乳香', '安息香', '龍涎香', '栴檀', '優曇華香'],
        ['线香', '白檀香', '沉香', '丁香', '乳香', '安息香', '龙涎香', '栴檀香', '优昙华香'],
        ['線香', '白檀香', '沉香', '丁香', '乳香', '安息香', '龍涎香', '栴檀香', '優曇華香'])
EAR = L(['귀이개', '면봉', '귀지 흡입기', '물 세척', '초음파 세척', '이명 치료', '귀 마사지', '반야 귀청소', '천이통'],
        ['Ear pick', 'Cotton swab', 'Wax vacuum', 'Water rinse', 'Ultrasonic clean', 'Tinnitus care', 'Ear massage', 'Prajna ear-clean', 'Divine ear'],
        ['耳かき', '綿棒', '耳垢吸引', '水洗浄', '超音波洗浄', '耳鳴り治療', '耳マッサージ', '般若の耳掃除', '天耳通'],
        ['耳挖勺', '棉签', '耳垢吸引', '水冲洗', '超声波清洁', '耳鸣治疗', '耳部按摩', '般若掏耳', '天耳通'],
        ['耳挖', '棉花棒', '耳垢吸引', '水沖洗', '超音波清潔', '耳鳴治療', '耳部按摩', '般若掏耳', '天耳通'])

SUTRA_NAMES = L(['염불', '천수경', '반야심경', '금강경', '아미타경', '지장경', '관음경', '법구경', '법화경', '능엄경', '화엄경', '열반경'],
                ['Yeombul', 'Thousand Hands Sutra', 'Heart Sutra', 'Diamond Sutra', 'Amitabha Sutra', 'Ksitigarbha Sutra', 'Avalokiteshvara Sutra', 'Dhammapada', 'Lotus Sutra', 'Shurangama Sutra', 'Avatamsaka Sutra', 'Nirvana Sutra'],
                ['念仏', '千手経', '般若心経', '金剛経', '阿弥陀経', '地蔵経', '観音経', '法句経', '法華経', '楞厳経', '華厳経', '涅槃経'],
                ['念佛', '千手经', '般若心经', '金刚经', '阿弥陀经', '地藏经', '观音经', '法句经', '法华经', '楞严经', '华严经', '涅槃经'],
                ['念佛', '千手經', '般若心經', '金剛經', '阿彌陀經', '地藏經', '觀音經', '法句經', '法華經', '楞嚴經', '華嚴經', '涅槃經'])
# hanja for every chanted syllable (1:1 with the Korean syllables), traditional form
HANJA = ['南無阿彌陀佛', '修里修里 摩訶修里 修修里 娑婆訶', '色卽是空 空卽是色', '應無所住 而生其心', '極樂世界 無量光佛', '地藏菩薩 摩訶薩',
         '南無 觀世音菩薩', '諸惡莫作 衆善奉行', '南無妙法蓮華經', '跢姪他 唵 阿那隷 毗舍提', '一切唯心造', '諸行無常 是生滅法']
TO_JA = str.maketrans({'彌': '弥', '佛': '仏', '卽': '即', '應': '応', '樂': '楽', '藏': '蔵', '觀': '観', '惡': '悪', '經': '経', '舍': '舎'})
TO_HANS = str.maketrans({'無': '无', '彌': '弥', '訶': '诃', '卽': '即', '應': '应', '極': '极', '樂': '乐', '薩': '萨', '觀': '观', '諸': '诸', '惡': '恶', '衆': '众', '蓮': '莲', '華': '华', '經': '经', '隷': '隶', '滅': '灭'})
TO_HANT = str.maketrans({'卽': '即'})

# Revised Romanization of Korean, syllable by syllable (for the English chant display)
RR_I = ['g', 'kk', 'n', 'd', 'tt', 'r', 'm', 'b', 'pp', 's', 'ss', '', 'j', 'jj', 'ch', 'k', 't', 'p', 'h']
RR_V = ['a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye', 'o', 'wa', 'wae', 'oe', 'yo', 'u', 'wo', 'we', 'wi', 'yu', 'eu', 'ui', 'i']
RR_F = ['', 'k', 'k', 'k', 'n', 'n', 'n', 't', 'l', 'k', 'm', 'l', 'l', 'l', 'p', 'l', 'm', 'p', 'p', 't', 't', 'ng', 't', 't', 'k', 't', 'p', 't']
def rr(ch):
    c = ord(ch) - 0xAC00
    return RR_I[c // 588] + RR_V[(c % 588) // 28] + RR_F[c % 28]

POLICY = {
 'en': '''<h2 id="pvT" tabindex="-1">Privacy policy</h2>
<p class="pmeta">Effective 30 October 2026 · Sutras for a Cow · This is a translation for convenience; the Korean version prevails.</p>
<h3>1. Personal information we collect</h3><p>There is no sign-up or login, and we never ask for your name, email or phone number. On the official address (baramutzero-netizen.github.io/moktak) we use the analytics tool in section 5 to count visitors and average play time. There is no ad tracking.</p>
<h3>2. Information kept only on your device</h3><p>To let you continue your game, the following is stored only in your browser (localStorage): karma, completed nodes, number of taps, practice time, last save time and sound settings. It is never sent to a server and we cannot see it.</p>
<h3>3. Sharing the result card</h3><p>The result card is made on your device. It is saved or shared only when you choose to, and once shared it follows the policy of the service you picked.</p>
<h3>4. Contact emails</h3><p>If you email us, we receive your address and message. We use them only to reply and delete them within one year after replying. We do not give them to third parties except where the law requires.</p>
<h3>5. Usage statistics (Google Analytics)</h3><p>On the official address, Google Analytics 4 uses cookies to collect: pages visited, visit and engagement time, device, browser and screen size, approximate location (country/city), a random identifier stored in a cookie, and game events (game start, venue reached, nirvana with play time, how the result card was shared). Nothing that directly identifies you, such as your name or email, is sent.</p>
<p>Purpose: to understand visitor numbers, average play time and how far players get, and improve the game. Retention: deleted automatically after Google Analytics' 14-month retention period.</p>
<p>Transfer abroad: the data is sent over the internet to servers of Google LLC (USA) when you visit, and handled under Google's privacy policy (policies.google.com/privacy).</p>
<p>How to refuse: turn off "Send usage stats" in the menu and nothing more is sent. You can also block cookies in your browser. The game works the same either way.</p>
<h3>6. Records kept by the hosting service</h3><p>The service hosting the game (e.g. GitHub Pages, Claude or a web host) may keep access logs under its own policy. We do not collect or use those logs.</p>
<h3>7. Your rights</h3><p>You can erase your saved progress at any time with "Start over" or by clearing site data in your browser. Usage stats can be turned off in the menu. To see or delete an email you sent, write to the address below.</p>
<h3>8. Contact</h3>''',
 'ja': '''<h2 id="pvT" tabindex="-1">プライバシーポリシー</h2>
<p class="pmeta">施行日 2026年10月30日 · 牛に経文 · 本翻訳は便宜のためのもので、韓国語版が優先します。</p>
<h3>1. 収集する個人情報</h3><p>会員登録やログインはなく、名前・メールアドレス・電話番号は受け取りません。ただし公式アドレス(baramutzero-netizen.github.io/moktak)では、訪問者数と平均プレイ時間を知るため、5番の利用統計ツールを使います。広告のトラッキングは行いません。</p>
<h3>2. 端末だけに保存される情報</h3><p>ゲームを続けられるよう、カルマ、修行済みのノード、木魚を叩いた回数、修行時間、最終保存時刻、音の設定をブラウザの保存領域(localStorage)だけに保存します。サーバーには送られず、運営者も見ることはできません。</p>
<h3>3. 結果画像のシェア</h3><p>結果画像は利用者の端末内で作られます。保存やシェアは利用者が自ら選んだときだけ行われ、シェアした画像は選んだサービスのポリシーに従います。</p>
<h3>4. お問い合わせメール</h3><p>メールを送ると、送信元アドレスと内容が運営者に届きます。返信のためだけに使い、返信後1年以内に削除します。法令による場合を除き第三者に提供しません。</p>
<h3>5. 利用統計 (Google Analytics)</h3><p>公式アドレスにアクセスすると、Google Analytics 4がCookieを使って次の情報を自動的に収集します: 閲覧ページ、アクセス・滞在時間、端末・ブラウザ・画面サイズ、おおよその地域(国・都市)、Cookieに保存されたランダムな識別子、ゲームの進行イベント(ゲーム開始、到達した場所、涅槃到達とそれまでのプレイ時間、結果画像のシェア方法)。名前やメールなど個人を直接特定できる情報は送りません。</p>
<p>目的: 訪問者数、平均プレイ時間、どこまで進むかといった利用統計を見てゲームを改善するためです。保存期間: Google Analyticsのデータ保持期間である14か月が過ぎると自動的に削除されます。</p>
<p>国外移転: この情報はアクセス時にインターネットを通じてGoogle LLC(米国)のサーバーに送信・保存され、Googleのプライバシーポリシー(policies.google.com/privacy)に従って処理されます。</p>
<p>拒否の方法: 設定の「利用統計を送る」をオフにすると、それ以降は何も送りません。ブラウザでCookieをブロックしても構いません。拒否してもゲームは同じように遊べます。</p>
<h3>6. ゲームを提供するサービスの記録</h3><p>ゲームを掲載しているサービス(例: GitHub Pages、Claude、Webホスティング事業者)は、独自のポリシーでアクセス記録を残すことがあります。運営者はその記録を収集・利用しません。</p>
<h3>7. 利用者の権利</h3><p>設定の「最初からやり直す」やブラウザのサイトデータ削除で、端末に保存された進行記録をいつでも消せます。利用統計は設定でオフにできます。送ったメールの閲覧や削除は下記アドレスにご依頼ください。</p>
<h3>8. お問い合わせ先</h3>''',
 'zh-Hans': '''<h2 id="pvT" tabindex="-1">隐私政策</h2>
<p class="pmeta">生效日期 2026年10月30日 · 对牛诵经 · 本译文仅供参考，以韩文版本为准。</p>
<h3>1. 收集的个人信息</h3><p>本游戏没有注册或登录，不收集姓名、邮箱或电话号码。但在官方网址(baramutzero-netizen.github.io/moktak)上，为了解访问人数和平均游玩时间，会使用第5条所述的访问统计工具。不进行广告追踪。</p>
<h3>2. 仅保存在设备上的信息</h3><p>为了能继续游戏，以下内容只保存在你的浏览器存储(localStorage)中：业力、已修节点、敲木鱼次数、修行时间、最后保存时间和声音设置。这些信息不会发送到服务器，运营者也看不到。</p>
<h3>3. 分享结果图</h3><p>结果图在你的设备上生成。只有在你主动选择时才会保存或分享，分享后的图片遵循你所选服务的政策。</p>
<h3>4. 联系邮件</h3><p>你发送邮件时，运营者会收到你的邮箱地址和邮件内容。仅用于回复，回复后一年内删除。除法律要求外，不提供给第三方。</p>
<h3>5. 访问统计 (Google Analytics)</h3><p>在官方网址访问时，Google Analytics 4 会通过 Cookie 自动收集：访问的页面、访问与停留时间、设备、浏览器与屏幕尺寸、大致地区(国家/城市)、Cookie 中的随机标识符，以及游戏进度事件(开始游戏、到达的场所、入涅槃及当时的游玩时间、结果图的分享方式)。不会发送姓名、邮箱等可直接识别个人的信息。</p>
<p>目的：查看访问人数、平均游玩时间、玩家进行到哪里等统计，以改进游戏。保存期限：超过 Google Analytics 的14个月数据保留期后自动删除。</p>
<p>跨境传输：上述信息在访问时通过互联网传输并保存至 Google LLC(美国)的服务器，按 Google 隐私政策(policies.google.com/privacy)处理。</p>
<p>拒绝方式：在设置中关闭“发送访问统计”，之后将不再发送任何内容。也可以在浏览器中屏蔽 Cookie。拒绝后游戏照常可玩。</p>
<h3>6. 托管服务的记录</h3><p>托管本游戏的服务(如 GitHub Pages、Claude、网站托管商)可能按其自身政策保留访问记录。运营者不收集或使用这些记录。</p>
<h3>7. 用户权利</h3><p>可随时通过设置中的“从头开始”或清除浏览器网站数据来删除设备上的进度。访问统计可在设置中关闭。如需查看或删除你发送的邮件，请发信至以下地址。</p>
<h3>8. 联系方式</h3>''',
 'zh-Hant': '''<h2 id="pvT" tabindex="-1">隱私權政策</h2>
<p class="pmeta">生效日期 2026年10月30日 · 對牛誦經 · 本譯文僅供參考，以韓文版本為準。</p>
<h3>1. 收集的個人資料</h3><p>本遊戲沒有註冊或登入，不收集姓名、電子郵件或電話號碼。但在官方網址(baramutzero-netizen.github.io/moktak)上，為了解造訪人數與平均遊玩時間，會使用第5條所述的造訪統計工具。不進行廣告追蹤。</p>
<h3>2. 僅儲存在裝置上的資訊</h3><p>為了能繼續遊戲，以下內容只儲存在你的瀏覽器儲存空間(localStorage)：業力、已修節點、敲木魚次數、修行時間、最後儲存時間與聲音設定。這些資訊不會傳送到伺服器，營運者也看不到。</p>
<h3>3. 分享結果圖</h3><p>結果圖在你的裝置上產生。只有在你主動選擇時才會儲存或分享，分享後的圖片依你所選服務的政策處理。</p>
<h3>4. 聯絡郵件</h3><p>你寄信時，營運者會收到你的電子郵件地址與內容。僅用於回覆，回覆後一年內刪除。除法律要求外，不提供給第三方。</p>
<h3>5. 造訪統計 (Google Analytics)</h3><p>在官方網址造訪時，Google Analytics 4 會透過 Cookie 自動收集：瀏覽的頁面、造訪與停留時間、裝置、瀏覽器與螢幕尺寸、大致地區(國家/城市)、Cookie 中的隨機識別碼，以及遊戲進度事件(開始遊戲、到達的場所、入涅槃與當時的遊玩時間、結果圖的分享方式)。不會傳送姓名、電子郵件等可直接識別個人的資訊。</p>
<p>目的：查看造訪人數、平均遊玩時間、玩家進行到哪裡等統計，以改進遊戲。保存期間：超過 Google Analytics 的14個月資料保留期間後自動刪除。</p>
<p>跨境傳輸：上述資訊在造訪時透過網際網路傳輸並儲存至 Google LLC(美國)的伺服器，依 Google 隱私權政策(policies.google.com/privacy)處理。</p>
<p>拒絕方式：在設定中關閉「傳送造訪統計」，之後將不再傳送任何內容。也可以在瀏覽器中封鎖 Cookie。拒絕後遊戲照常可玩。</p>
<h3>6. 託管服務的記錄</h3><p>託管本遊戲的服務(如 GitHub Pages、Claude、網站託管商)可能依其自身政策保留存取記錄。營運者不收集或使用這些記錄。</p>
<h3>7. 使用者權利</h3><p>可隨時透過設定中的「從頭開始」或清除瀏覽器網站資料來刪除裝置上的進度。造訪統計可在設定中關閉。如需查看或刪除你寄出的郵件，請寄信至下列地址。</p>
<h3>8. 聯絡方式</h3>''',
}

def build_i18n(listeners_ko, chant_lines_ko):
    out = {'langs': LANGS, 'labels': LANG_LABEL, 'ui': {}, 'venues': {}, 'listeners': {}, 'groups': {}, 'perf': {},
           'stages': STAGES, 'inc': INC, 'ear': EAR, 'sutra': SUTRA_NAMES, 'chant': {}, 'policy': POLICY}
    for lg in LANGS:
        out['ui'][lg] = {k: v[lg] for k, v in UI.items()}
        out['venues'][lg] = [v[lg] for v in VENUES]
        out['groups'][lg] = {k: list(v[LANGS.index(lg)]) for k, v in GROUPS.items()}
        out['perf'][lg] = {k: v[LANGS.index(lg)] for k, v in PERF.items()}
        out['listeners'][lg] = {}
        for Lk in listeners_ko:
            if lg == 'ko': out['listeners'][lg][Lk['key']] = [Lk['name'], Lk['tag']]
            else:
                t = LISTENERS[Lk['key']]; i = {'en': 0, 'ja': 2, 'zh-Hans': 4, 'zh-Hant': 6}[lg]
                out['listeners'][lg][Lk['key']] = [t[i], t[i + 1]]
    # chant display, aligned syllable-by-syllable with the Korean script
    for lg in LANGS:
        lines = []
        for (name, line), hj in zip(chant_lines_ko, HANJA):
            kw = line.split(); hw = hj.split()
            assert [len(w) for w in kw] == [len(w) for w in hw], (line, hj)
            if lg == 'ko': words = [list(w) for w in kw]
            elif lg == 'en': words = [[rr(c) for c in w] for w in kw]
            elif lg == 'ja': words = [list(w.translate(TO_JA)) for w in hw]
            elif lg == 'zh-Hans': words = [list(w.translate(TO_HANS)) for w in hw]
            else: words = [list(w.translate(TO_HANT)) for w in hw]
            lines.append(words)
        out['chant'][lg] = lines
    return out

if __name__ == '__main__':
    from art2 import LISTENERS as LK
    idx = json.load(open('chant_index.json'))
    d = build_i18n(LK, idx['lines'])
    missing = [L['key'] for L in LK if L['key'] not in LISTENERS]
    assert not missing, missing
    json.dump(d, open('i18n.json', 'w'), ensure_ascii=False)
    print('ok', len(d['ui']['en']), 'ui keys;', d['chant']['en'][1], d['chant']['ja'][2])
