QUESTIONS = {}

QUESTIONS["ru.starter.cyrillic"] = [
    {"id": "ru_cy_001", "type": "choice", "level": "A0", "prompt": "字母'А'的发音是？", "options": ["/a/", "/b/", "/v/", "/g/"], "answer": "/a/", "explanation": "RU: А произносится /a/ | ZH: А发/a/音"},
    {"id": "ru_cy_002", "type": "choice", "level": "A0", "prompt": "字母'Б'的发音是？", "options": ["/b/", "/p/", "/v/", "/d/"], "answer": "/b/", "explanation": "RU: Б произносится /b/ | ZH: Б发/b/音"},
    {"id": "ru_cy_003", "type": "choice", "level": "A0", "prompt": "字母'В'的发音是？", "options": ["/v/", "/b/", "/f/", "/w/"], "answer": "/v/", "explanation": "RU: В произносится /v/ | ZH: В发/v/音"},
    {"id": "ru_cy_004", "type": "choice", "level": "A0", "prompt": "字母'Г'的发音是？", "options": ["/g/", "/k/", "/h/", "/zh/"], "answer": "/g/", "explanation": "RU: Г произносится /g/ | ZH: Г发/g/音"},
    {"id": "ru_cy_005", "type": "choice", "level": "A0", "prompt": "字母'Д'的发音是？", "options": ["/d/", "/t/", "/n/", "/l/"], "answer": "/d/", "explanation": "RU: Д произносится /d/ | ZH: Д发/d/音"},
    {"id": "ru_cy_006", "type": "choice", "level": "A0", "prompt": "字母'Е'的发音是？", "options": ["/ye/", "/e/", "/yo/", "/i/"], "answer": "/ye/", "explanation": "RU: Е произносится /ye/ | ZH: Е发/ye/音"},
    {"id": "ru_cy_007", "type": "choice", "level": "A0", "prompt": "字母'Ж'的发音是？", "options": ["/zh/", "/z/", "/sh/", "/ch/"], "answer": "/zh/", "explanation": "RU: Ж произносится /zh/ | ZH: Ж类似汉语'日'"},
    {"id": "ru_cy_008", "type": "choice", "level": "A0", "prompt": "字母'З'的发音是？", "options": ["/z/", "/s/", "/zh/", "/ts/"], "answer": "/z/", "explanation": "RU: З произносится /z/ | ZH: З发/z/音"},
    {"id": "ru_cy_009", "type": "choice", "level": "A0", "prompt": "字母'Й'叫什么？", "options": ["短И", "长И", "软И", "硬И"], "answer": "短И", "explanation": "RU: Й называется 'краткое' | ZH: 短И，类似/y/"},
    {"id": "ru_cy_010", "type": "choice", "level": "A0", "prompt": "字母'Ы'的发音接近？", "options": ["央元音/ɨ/", "/i/", "/u/", "/e/"], "answer": "央元音/ɨ/", "explanation": "RU: Ы - особый русский звук | ZH: 无对应汉语音，舌后央元音"},
]

QUESTIONS["ru.starter.greetings"] = [
    {"id": "ru_gr_001", "type": "choice", "level": "A0", "prompt": "你好是？", "options": ["Привет", "Пока", "Спасибо", "Пожалуйста"], "answer": "Привет", "explanation": "RU: Привет - неформальное приветствие | ZH: 非正式你好"},
    {"id": "ru_gr_002", "type": "choice", "level": "A0", "prompt": "正式你好是？", "options": ["Здравствуйте", "Привет", "Пока", "Ладно"], "answer": "Здравствуйте", "explanation": "RU: Здравствуйте - официальное | ZH: 正式问候"},
    {"id": "ru_gr_003", "type": "choice", "level": "A0", "prompt": "谢谢是？", "options": ["Спасибо", "Извините", "Пожалуйста", "Привет"], "answer": "Спасибо", "explanation": "RU: Спасибо - благодарность | ZH: 谢谢"},
    {"id": "ru_gr_004", "type": "choice", "level": "A0", "prompt": "不客气是？", "options": ["Пожалуйста", "Спасибо", "Извините", "Пока"], "answer": "Пожалуйста", "explanation": "RU: Пожалуйста - ответ на спасибо | ZH: 不客气"},
    {"id": "ru_gr_005", "type": "choice", "level": "A0", "prompt": "对不起是？", "options": ["Извините", "Спасибо", "Привет", "Ладно"], "answer": "Извините", "explanation": "RU: Извините - извинение | ZH: 对不起(正式)"},
    {"id": "ru_gr_006", "type": "choice", "level": "A0", "prompt": "再见(非正式)是？", "options": ["Пока", "Здравствуйте", "Спасибо", "Да"], "answer": "Пока", "explanation": "RU: Пока - неформальное прощание | ZH: 非正式再见"},
    {"id": "ru_gr_007", "type": "choice", "level": "A0", "prompt": "正式再见是？", "options": ["До свидания", "Пока", "Привет", "Нет"], "answer": "До свидания", "explanation": "RU: До свидания - официальное прощание | ZH: 正式再见"},
    {"id": "ru_gr_008", "type": "choice", "level": "A0", "prompt": "早上好是？", "options": ["Доброе утро", "Добрый день", "Добрый вечер", "Спокойной ночи"], "answer": "Доброе утро", "explanation": "RU: Доброе утро - утреннее приветствие | ZH: 早上好"},
    {"id": "ru_gr_009", "type": "choice", "level": "A0", "prompt": "晚上好是？", "options": ["Добрый вечер", "Доброе утро", "Добрый день", "До свидания"], "answer": "Добрый вечер", "explanation": "RU: Добрый вечер - вечернее приветствие | ZH: 晚上好"},
    {"id": "ru_gr_010", "type": "choice", "level": "A0", "prompt": "晚安是？", "options": ["Спокойной ночи", "Добрый вечер", "До свидания", "Пока"], "answer": "Спокойной ночи", "explanation": "RU: Спокойной ночи | ZH: 晚安"},
]

QUESTIONS["ru.starter.numbers"] = [
    {"id": "ru_nb_001", "type": "choice", "level": "A0", "prompt": "数字1是？", "options": ["один", "два", "три", "четыре"], "answer": "один", "explanation": "RU: один = 1 | ZH: 一"},
    {"id": "ru_nb_002", "type": "choice", "level": "A0", "prompt": "数字2是？", "options": ["два", "один", "пять", "семь"], "answer": "два", "explanation": "RU: два = 2 | ZH: 二"},
    {"id": "ru_nb_003", "type": "choice", "level": "A0", "prompt": "数字3是？", "options": ["три", "четыре", "шесть", "восемь"], "answer": "три", "explanation": "RU: три = 3 | ZH: 三"},
    {"id": "ru_nb_004", "type": "choice", "level": "A0", "prompt": "数字4是？", "options": ["четыре", "три", "девять", "десять"], "answer": "четыре", "explanation": "RU: четыре = 4 | ZH: 四"},
    {"id": "ru_nb_005", "type": "choice", "level": "A0", "prompt": "数字5是？", "options": ["пять", "семь", "восемь", "девять"], "answer": "пять", "explanation": "RU: пять = 5 | ZH: 五"},
    {"id": "ru_nb_006", "type": "choice", "level": "A0", "prompt": "数字6是？", "options": ["шесть", "пять", "семь", "два"], "answer": "шесть", "explanation": "RU: шесть = 6 | ZH: 六"},
    {"id": "ru_nb_007", "type": "choice", "level": "A0", "prompt": "数字7是？", "options": ["семь", "шесть", "восемь", "три"], "answer": "семь", "explanation": "RU: семь = 7 | ZH: 七"},
    {"id": "ru_nb_008", "type": "choice", "level": "A0", "prompt": "数字8是？", "options": ["восемь", "семь", "девять", "четыре"], "answer": "восемь", "explanation": "RU: восемь = 8 | ZH: 八"},
    {"id": "ru_nb_009", "type": "choice", "level": "A0", "prompt": "数字9是？", "options": ["девять", "восемь", "семь", "пять"], "answer": "девять", "explanation": "RU: девять = 9 | ZH: 九"},
    {"id": "ru_nb_010", "type": "choice", "level": "A0", "prompt": "数字10是？", "options": ["десять", "девять", "двенадцать", "одиннадцать"], "answer": "десять", "explanation": "RU: десять = 10 | ZH: 十"},
]

QUESTIONS["ru.elementary.nouns_gender"] = [
    {"id": "ru_ng_001", "type": "choice", "level": "A1", "prompt": "俄语名词性别：стол(桌子)是？", "options": ["阳性", "阴性", "中性", "无性别"], "answer": "阳性", "explanation": "RU: стол - мужской род | ZH: 辅音结尾一般为阳性"},
    {"id": "ru_ng_002", "type": "choice", "level": "A1", "prompt": "俄语名词性别：книга(书)是？", "options": ["阴性", "阳性", "中性", "无性别"], "answer": "阴性", "explanation": "RU: книга - женский род | ZH: 结尾-а/-я一般为阴性"},
    {"id": "ru_ng_003", "type": "choice", "level": "A1", "prompt": "俄语名词性别：окно(窗户)是？", "options": ["中性", "阳性", "阴性", "无性别"], "answer": "中性", "explanation": "RU: окно - средний род | ZH: 结尾-о/-е为中性"},
    {"id": "ru_ng_004", "type": "choice", "level": "A1", "prompt": "俄语名词性别：мать(母亲)是？", "options": ["阴性", "阳性", "中性", "无性别"], "answer": "阴性", "explanation": "RU: мать - женский род | ZH: 软符结尾需记忆"},
    {"id": "ru_ng_005", "type": "choice", "level": "A1", "prompt": "俄语名词性别：время(时间)是？", "options": ["中性", "阳性", "阴性", "无性别"], "answer": "中性", "explanation": "RU: время - средний род (-мя结尾) | ZH: -мя结尾为中性"},
    {"id": "ru_ng_006", "type": "choice", "level": "A1", "prompt": "阳性形容词词尾是？", "options": ["-ый/-ий", "-ая/-яя", "-ое/-ее", "-ые/-ие"], "answer": "-ый/-ий", "explanation": "RU: мужской род -ый/-ий | ZH: 阳性形容词词尾"},
    {"id": "ru_ng_007", "type": "choice", "level": "A1", "prompt": "阴性形容词词尾是？", "options": ["-ая/-яя", "-ый/-ий", "-ое/-ее", "-ые/-ие"], "answer": "-ая/-яя", "explanation": "RU: женский род -ая/-яя | ZH: 阴性形容词词尾"},
    {"id": "ru_ng_008", "type": "choice", "level": "A1", "prompt": "中性形容词词尾是？", "options": ["-ое/-ее", "-ый/-ий", "-ая/-яя", "-ые/-ие"], "answer": "-ое/-ее", "explanation": "RU: средний род -ое/-ее | ZH: 中性形容词词尾"},
    {"id": "ru_ng_009", "type": "choice", "level": "A1", "prompt": "俄语名词性别：день(天/白天)是？", "options": ["阳性", "阴性", "中性", "无性别"], "answer": "阳性", "explanation": "RU: день - мужской род | ZH: 软符结尾阳性"},
    {"id": "ru_ng_010", "type": "choice", "level": "A1", "prompt": "俄语名词性别：ночь(夜晚)是？", "options": ["阴性", "阳性", "中性", "无性别"], "answer": "阴性", "explanation": "RU: ночь - женский род | ZH: 软符结尾阴性"},
]

QUESTIONS["ru.elementary.family"] = [
    {"id": "ru_fa_001", "type": "choice", "level": "A1", "prompt": "父亲是？", "options": ["отец", "мать", "брат", "сын"], "answer": "отец", "explanation": "RU: отец = отец | ZH: 父亲"},
    {"id": "ru_fa_002", "type": "choice", "level": "A1", "prompt": "母亲是？", "options": ["мать", "отец", "дочь", "дядя"], "answer": "мать", "explanation": "RU: мать = мать | ZH: 母亲"},
    {"id": "ru_fa_003", "type": "choice", "level": "A1", "prompt": "哥哥/弟弟是？", "options": ["брат", "сестра", "дедушка", "кузина"], "answer": "брат", "explanation": "RU: брат = брат | ZH: 兄弟"},
    {"id": "ru_fa_004", "type": "choice", "level": "A1", "prompt": "姐姐/妹妹是？", "options": ["сестра", "брат", "бабушка", "сын"], "answer": "сестра", "explanation": "RU: сестра = сестра | ZH: 姐妹"},
    {"id": "ru_fa_005", "type": "choice", "level": "A1", "prompt": "儿子是？", "options": ["сын", "дочь", "внук", "дядя"], "answer": "сын", "explanation": "RU: сын = сын | ZH: 儿子"},
    {"id": "ru_fa_006", "type": "choice", "level": "A1", "prompt": "女儿是？", "options": ["дочь", "сын", "внучка", "тётя"], "answer": "дочь", "explanation": "RU: дочь = дочь | ZH: 女儿"},
    {"id": "ru_fa_007", "type": "choice", "level": "A1", "prompt": "爷爷/外公是？", "options": ["дедушка", "бабушка", "дядя", "двоюродный брат"], "answer": "дедушка", "explanation": "RU: дедушка = дедушка | ZH: 祖父/外公"},
    {"id": "ru_fa_008", "type": "choice", "level": "A1", "prompt": "奶奶/外婆是？", "options": ["бабушка", "дедушка", "тётя", "сестра"], "answer": "бабушка", "explanation": "RU: бабушка = бабушка | ZH: 祖母/外婆"},
    {"id": "ru_fa_009", "type": "choice", "level": "A1", "prompt": "叔叔/舅舅是？", "options": ["дядя", "тётя", "двоюродный брат", "племянник"], "answer": "дядя", "explanation": "RU: дядя = дядя | ZH: 叔叔/舅舅"},
    {"id": "ru_fa_010", "type": "choice", "level": "A1", "prompt": "阿姨/姑妈是？", "options": ["тётя", "дядя", "сестра", "бабушка"], "answer": "тётя", "explanation": "RU: тётя = тётя | ZH: 阿姨/姑妈"},
]

QUESTIONS["ru.elementary.daily"] = [
    {"id": "ru_da_001", "type": "choice", "level": "A1", "prompt": "起床是？", "options": ["вставать", "спать", "есть", "идти"], "answer": "вставать", "explanation": "RU: вставать = вставать | ZH: 起床"},
    {"id": "ru_da_002", "type": "choice", "level": "A1", "prompt": "睡觉是？", "options": ["спать", "учиться", "работать", "ходить"], "answer": "спать", "explanation": "RU: спать = спать | ZH: 睡觉"},
    {"id": "ru_da_003", "type": "choice", "level": "A1", "prompt": "吃饭是？", "options": ["есть/кушать", "пить", "готовить", "покупать"], "answer": "есть/кушать", "explanation": "RU: есть/кушать = есть | ZH: 吃饭"},
    {"id": "ru_da_004", "type": "choice", "level": "A1", "prompt": "喝水是？", "options": ["пить воду", "есть хлеб", "смотреть ТВ", "читать"], "answer": "пить воду", "explanation": "RU: пить воду | ZH: 喝水"},
    {"id": "ru_da_005", "type": "choice", "level": "A1", "prompt": "上班是？", "options": ["идти на работу", "идти в кино", "идти в парк", "идти домой"], "answer": "идти на работу", "explanation": "RU: идти на работу | ZH: 去上班"},
    {"id": "ru_da_006", "type": "choice", "level": "A1", "prompt": "学习是？", "options": ["учиться", "отдыхать", "петь", "танцевать"], "answer": "учиться", "explanation": "RU: учиться = учиться | ZH: 学习"},
    {"id": "ru_da_007", "type": "choice", "level": "A1", "prompt": "做饭是？", "options": ["готовить", "убирать", "спать", "путешествовать"], "answer": "готовить", "explanation": "RU: готовить = готовить | ZH: 做饭"},
    {"id": "ru_da_008", "type": "choice", "level": "A1", "prompt": "打扫是？", "options": ["убирать", "платить", "бежать", "плавать"], "answer": "убирать", "explanation": "RU: убирать = убирать | ZH: 打扫"},
    {"id": "ru_da_009", "type": "choice", "level": "A1", "prompt": "散步是？", "options": ["гулять", "работать", "учиться", "спать"], "answer": "гулять", "explanation": "RU: гулять = гулять | ZH: 散步"},
    {"id": "ru_da_010", "type": "choice", "level": "A1", "prompt": "购物是？", "options": ["ходить за покупками", "идти на работу", "идти в парк", "идти домой"], "answer": "ходить за покупками", "explanation": "RU: ходить за покупками | ZH: 购物"},
]

QUESTIONS["ru.intermediate.cases"] = [
    {"id": "ru_ca_001", "type": "choice", "level": "B1", "prompt": "主格(Именительный)回答什么问题？", "options": ["кто/что", "кого/чего", "кому/чему", "кем/чем"], "answer": "кто/что", "explanation": "RU: Именительный: кто/что | ZH: 主格回答谁/什么"},
    {"id": "ru_ca_002", "type": "choice", "level": "B1", "prompt": "宾格(Винительный)回答什么问题？", "options": ["кого/что", "кто/что", "кому/чему", "о ком/чём"], "answer": "кого/что", "explanation": "RU: Винительный: кого/что | ZH: 宾格表示直接宾语"},
    {"id": "ru_ca_003", "type": "choice", "level": "B1", "prompt": "属格(Родительный)回答什么问题？", "options": ["кого/чего", "кому/чему", "кто/что", "кем/чем"], "answer": "кого/чего", "explanation": "RU: Родительный: кого/чего | ZH: 属格表示所属"},
    {"id": "ru_ca_004", "type": "choice", "level": "B1", "prompt": "与格(Дательный)回答什么问题？", "options": ["кому/чему", "кого/чего", "кто/что", "кем/чем"], "answer": "кому/чему", "explanation": "RU: Дательный: кому/чему | ZH: 与格表示间接宾语"},
    {"id": "ru_ca_005", "type": "choice", "level": "B1", "prompt": "造格(Творительный)回答什么问题？", "options": ["кем/чем", "кому/чему", "кого/чего", "о ком/чём"], "answer": "кем/чем", "explanation": "RU: Творительный: кем/чем | ZH: 造格表示工具/手段"},
    {"id": "ru_ca_006", "type": "choice", "level": "B1", "prompt": "前置格(Предложный)与哪个介词连用？", "options": ["о/об/в/на", "из/от/до", "к/по", "за/под"], "answer": "о/об/в/на", "explanation": "RU: Предложный с о/в/на | ZH: 前置格常与о/в/на连用"},
    {"id": "ru_ca_007", "type": "choice", "level": "B1", "prompt": "Я вижу дом(дом变格)dом在此为？", "options": ["宾格", "主格", "属格", "与格"], "answer": "宾格", "explanation": "RU: вижу → Винительный | ZH: 看见→宾格"},
    {"id": "ru_ca_008", "type": "choice", "level": "B1", "prompt": "нет книги(书的)книги在此为？", "options": ["属格", "主格", "宾格", "与格"], "answer": "属格", "explanation": "RU: нет → Родительный | ZH: 没有→属格"},
    {"id": "ru_ca_009", "type": "choice", "level": "B1", "prompt": "Я иду в школу(到学校)школу在此为？", "options": ["宾格", "前置格", "属格", "与格"], "answer": "宾格", "explanation": "RU: в + движение → Винительный | ZH: 去向→宾格"},
    {"id": "ru_ca_010", "type": "choice", "level": "B1", "prompt": "Я живу в школе(在学校)школе在此为？", "options": ["前置格", "宾格", "属格", "与格"], "answer": "前置格", "explanation": "RU: в + место → Предложный | ZH: 位置→前置格"},
]

QUESTIONS["ru.intermediate.shopping"] = [
    {"id": "ru_sh_001", "type": "choice", "level": "B1", "prompt": "这个多少钱？", "options": ["Сколько стоит это?", "Где это?", "Который час?", "Кто это?"], "answer": "Сколько стоит это?", "explanation": "RU: Сколько стоит? | ZH: 多少钱"},
    {"id": "ru_sh_002", "type": "choice", "level": "B1", "prompt": "能便宜点吗？", "options": ["Можно скидку?", "Можно подождать?", "Можно посмотреть?", "Можно войти?"], "answer": "Можно скидку?", "explanation": "RU: скидку = скидку | ZH: 打折"},
    {"id": "ru_sh_003", "type": "choice", "level": "B1", "prompt": "我想试穿", "options": ["Можно примерить?", "Можно попробовать?", "Можно посмотреть?", "Можно купить?"], "answer": "Можно примерить?", "explanation": "RU: примерить = примерить | ZH: 试穿"},
    {"id": "ru_sh_004", "type": "choice", "level": "B1", "prompt": "有更大的尺码吗？", "options": ["Есть размер побольше?", "Есть размер поменьше?", "Это красиво?", "Где это?"], "answer": "Есть размер побольше?", "explanation": "RU: размер побольше | ZH: 更大的尺码"},
    {"id": "ru_sh_005", "type": "choice", "level": "B1", "prompt": "我要这个", "options": ["Я возьму это", "Я не хочу это", "Я смотрю", "Я ухожу"], "answer": "Я возьму это", "explanation": "RU: возьму это | ZH: 我要这个"},
    {"id": "ru_sh_006", "type": "choice", "level": "B1", "prompt": "可以刷卡吗？", "options": ["Можно картой?", "Только наличные?", "У меня нет денег", "У меня есть наличные"], "answer": "Можно картой?", "explanation": "RU: картой = картой | ZH: 能刷卡吗"},
    {"id": "ru_sh_007", "type": "choice", "level": "B1", "prompt": "我用现金付款", "options": ["Я плачу наличными", "Я плачу картой", "Я не плачу", "Я только смотрю"], "answer": "Я плачу наличными", "explanation": "RU: наличными = наличными | ZH: 用现金"},
    {"id": "ru_sh_008", "type": "choice", "level": "B1", "prompt": "需要收据吗？", "options": ["Вам нужен чек?", "Вам нужен пакет?", "Вам нужно больше?", "Вам нужно сесть?"], "answer": "Вам нужен чек?", "explanation": "RU: чек = чек | ZH: 收据"},
    {"id": "ru_sh_009", "type": "choice", "level": "B1", "prompt": "有其他颜色吗？", "options": ["Есть другой цвет?", "Есть другая улица?", "Есть другой день?", "Есть другое место?"], "answer": "Есть другой цвет?", "explanation": "RU: другой цвет | ZH: 其他颜色"},
    {"id": "ru_sh_010", "type": "choice", "level": "B1", "prompt": "请打包带走", "options": ["С собой, пожалуйста", "Здесь поем", "Не хочу", "Спасибо"], "answer": "С собой, пожалуйста", "explanation": "RU: с собой = с собой | ZH: 打包带走"},
]

QUESTIONS["ru.intermediate.travel"] = [
    {"id": "ru_tr_001", "type": "choice", "level": "B1", "prompt": "机场是？", "options": ["аэропорт", "вокзал", "отель", "порт"], "answer": "аэропорт", "explanation": "RU: аэропорт = аэропорт | ZH: 机场"},
    {"id": "ru_tr_002", "type": "choice", "level": "B1", "prompt": "火车站是？", "options": ["вокзал", "аэропорт", "парк", "рынок"], "answer": "вокзал", "explanation": "RU: вокзал = вокзал | ZH: 火车站"},
    {"id": "ru_tr_003", "type": "choice", "level": "B1", "prompt": "我想预订一个房间", "options": ["Я хочу забронировать номер", "Я хочу убрать номер", "Номеров нет", "Номер маленький"], "answer": "Я хочу забронировать номер", "explanation": "RU: забронировать номер | ZH: 预订房间"},
    {"id": "ru_tr_004", "type": "choice", "level": "B1", "prompt": "入住是？", "options": ["заселение", "выселение", "отправление", "прибытие"], "answer": "заселение", "explanation": "RU: заселение = check-in | ZH: 入住"},
    {"id": "ru_tr_005", "type": "choice", "level": "B1", "prompt": "退房是？", "options": ["выселение", "заселение", "отправление", "прибытие"], "answer": "выселение", "explanation": "RU: выселение = check-out | ZH: 退房"},
    {"id": "ru_tr_006", "type": "choice", "level": "B1", "prompt": "地铁是？", "options": ["метро", "автобус", "такси", "самолёт"], "answer": "метро", "explanation": "RU: метро = метро | ZH: 地铁"},
    {"id": "ru_tr_007", "type": "choice", "level": "B1", "prompt": "公交车是？", "options": ["автобус", "метро", "корабль", "поезд"], "answer": "автобус", "explanation": "RU: автобус = автобус | ZH: 公交车"},
    {"id": "ru_tr_008", "type": "choice", "level": "B1", "prompt": "一张到莫斯科的票", "options": ["Один билет до Москвы", "Один билет из Москвы", "Москва далеко", "Где Москва?"], "answer": "Один билет до Москвы", "explanation": "RU: билет до Москвы | ZH: 到莫斯科的票"},
    {"id": "ru_tr_009", "type": "choice", "level": "B1", "prompt": "洗手间在哪里？", "options": ["Где туалет?", "Где выход?", "Где вход?", "Где багаж?"], "answer": "Где туалет?", "explanation": "RU: туалет = туалет | ZH: 洗手间在哪里"},
    {"id": "ru_tr_010", "type": "choice", "level": "B1", "prompt": "请帮我叫一辆出租车", "options": ["Вызовите такси, пожалуйста", "Не хочу такси", "Еду в метро", "У меня есть машина"], "answer": "Вызовите такси, пожалуйста", "explanation": "RU: вызовите такси | ZH: 请帮我叫出租车"},
]
