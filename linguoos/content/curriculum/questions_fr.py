# French question bank aligned with French modules

QUESTIONS = {}

QUESTIONS['fr.starter.alphabet'] = [
    {'id': 'fr_al_001', 'type': 'choice', 'level': 'A0', 'prompt': '法语字母e单独读作什么？', 'options': ['/e/', '/ɛ/', '/ə/', '/i/'], 'answer': '/ə/', 'explanation': 'FR: La lettre e se prononce /ə/. | ZH: 字母e单独读/ə/'},
    {'id': 'fr_al_002', 'type': 'choice', 'level': 'A0', 'prompt': '字母u的标准读音是？', 'options': ['/u/', '/y/', '/o/', '/i/'], 'answer': '/y/', 'explanation': 'FR: u se prononce /y/. | ZH: u读/ü/音'},
    {'id': 'fr_al_003', 'type': 'choice', 'level': 'A0', 'prompt': '法语中h通常如何发音？', 'options': ['强读/h/', '不发音', '读/g/', '读/k/'], 'answer': '不发音', 'explanation': 'FR: h est généralement muet. | ZH: h通常不发音'},
    {'id': 'fr_al_004', 'type': 'choice', 'level': 'A0', 'prompt': '字母j的读音是？', 'options': ['/ʒi/', '/dʒi/', '/ji/', '/ʃi/'], 'answer': '/ʒi/', 'explanation': 'FR: j se lit /ʒi/. | ZH: j读/ʒi/'},
    {'id': 'fr_al_005', 'type': 'choice', 'level': 'A0', 'prompt': '字母r在法语中的典型发音是？', 'options': ['/r/卷舌', '/ʁ/小舌颤音', '/l/', '/h/'], 'answer': '/ʁ/小舌颤音', 'explanation': 'FR: r se prononce /ʁ/. | ZH: r为小舌音/ʁ/'},
    {'id': 'fr_al_006', 'type': 'choice', 'level': 'A0', 'prompt': '“ç”表示什么音？', 'options': ['/s/', '/k/', '/ʃ/', '/z/'], 'answer': '/s/', 'explanation': 'FR: ç = /s/ devant a/o/u. | ZH: ç表示/s/音'},
    {'id': 'fr_al_007', 'type': 'choice', 'level': 'A0', 'prompt': '重音符号é一般读作？', 'options': ['/e/', '/ɛ/', '/ə/', '/i/'], 'answer': '/e/', 'explanation': 'FR: é se prononce /e/. | ZH: é读/e/'},
    {'id': 'fr_al_008', 'type': 'choice', 'level': 'A0', 'prompt': '“oi”组合读作？', 'options': ['/wa/', '/oi/', '/oɑ/', '/wi/'], 'answer': '/wa/', 'explanation': 'FR: oi se prononce /wa/. | ZH: oi读/wa/'},
    {'id': 'fr_al_009', 'type': 'choice', 'level': 'A0', 'prompt': '“an/en”鼻化元音常读作？', 'options': ['/ɑ̃/', '/ɛ̃/', '/ɔ̃/', '/a/'], 'answer': '/ɑ̃/', 'explanation': 'FR: an/en = /ɑ̃/. | ZH: an/en常为/ɑ̃/'},
    {'id': 'fr_al_010', 'type': 'choice', 'level': 'A0', 'prompt': '“in/ain”鼻化元音常读作？', 'options': ['/ɛ̃/', '/ɑ̃/', '/ɔ̃/', '/e/'], 'answer': '/ɛ̃/', 'explanation': 'FR: in/ain = /ɛ̃/. | ZH: in/ain为/ɛ̃/'},
]

QUESTIONS['fr.starter.greetings'] = [
    {'id': 'fr_gr_001', 'type': 'choice', 'level': 'A0', 'prompt': '法语中“你好”最常见的说法是？', 'options': ['Merci', 'Bonjour', 'Au revoir', 'Pardon'], 'answer': 'Bonjour', 'explanation': 'FR: Bonjour = Hello/Good day. | ZH: Bonjour表示你好'},
    {'id': 'fr_gr_002', 'type': 'choice', 'level': 'A0', 'prompt': '晚上见面应说？', 'options': ['Bonsoir', 'Bonjour', 'Salut', 'Merci'], 'answer': 'Bonsoir', 'explanation': 'FR: Bonsoir = Good evening. | ZH: 晚上用Bonsoir'},
    {'id': 'fr_gr_003', 'type': 'choice', 'level': 'A0', 'prompt': '“再见”是？', 'options': ['S’il vous plaît', 'Au revoir', 'De rien', 'Enchanté'], 'answer': 'Au revoir', 'explanation': 'FR: Au revoir = Goodbye. | ZH: Au revoir表示再见'},
    {'id': 'fr_gr_004', 'type': 'choice', 'level': 'A0', 'prompt': '与朋友打招呼更口语的说法？', 'options': ['Salut', 'Bonsoir', 'Bienvenue', 'Merci'], 'answer': 'Salut', 'explanation': 'FR: Salut = Hi (informal). | ZH: Salut较口语'},
    {'id': 'fr_gr_005', 'type': 'choice', 'level': 'A0', 'prompt': '“很高兴认识你”是？', 'options': ['Enchanté', 'Pardon', 'À bientôt', 'Excusez-moi'], 'answer': 'Enchanté', 'explanation': 'FR: Enchanté = Nice to meet you. | ZH: Enchanté表示很高兴认识你'},
    {'id': 'fr_gr_006', 'type': 'choice', 'level': 'A0', 'prompt': '礼貌询问“你好吗？”是？', 'options': ['Ça va ?', 'Comment tu t’appelles ?', 'Où es-tu ?', 'Quel âge as-tu ?'], 'answer': 'Ça va ?', 'explanation': 'FR: Ça va ? = How are you? | ZH: Ça va? 表示你好吗'},
    {'id': 'fr_gr_007', 'type': 'choice', 'level': 'A0', 'prompt': '“不客气”可说？', 'options': ['De rien', 'Merci', 'Bonjour', 'Salut'], 'answer': 'De rien', 'explanation': 'FR: De rien = You’re welcome. | ZH: De rien表示不客气'},
    {'id': 'fr_gr_008', 'type': 'choice', 'level': 'A0', 'prompt': '“请”是？', 'options': ['S’il vous plaît', 'Merci', 'Pardon', 'Au revoir'], 'answer': 'S’il vous plaît', 'explanation': 'FR: S’il vous plaît = Please. | ZH: S’il vous plaît表示请'},
    {'id': 'fr_gr_009', 'type': 'choice', 'level': 'A1', 'prompt': '正式场合称呼陌生人应使用？', 'options': ['Tu', 'Vous', 'Moi', 'Eux'], 'answer': 'Vous', 'explanation': 'FR: Vous est formel. | ZH: 正式场合用vous'},
    {'id': 'fr_gr_010', 'type': 'choice', 'level': 'A0', 'prompt': '“待会儿见”是？', 'options': ['À tout à l’heure', 'Au revoir', 'Bonsoir', 'Enchanté'], 'answer': 'À tout à l’heure', 'explanation': 'FR: À tout à l’heure = See you later. | ZH: 待会儿见'},
]

QUESTIONS['fr.starter.numbers'] = [
    {'id': 'fr_nu_001', 'type': 'choice', 'level': 'A0', 'prompt': '21用法语怎么说？', 'options': ['vingt-un', 'vingt-et-un', 'vingt-deux', 'vingt-unne'], 'answer': 'vingt-et-un', 'explanation': 'FR: 21 = vingt-et-un. | ZH: 21是vingt-et-un'},
    {'id': 'fr_nu_002', 'type': 'choice', 'level': 'A0', 'prompt': '70在法语中常说？', 'options': ['soixante-dix', 'septante', 'soixante-onze', 'soixante-douze'], 'answer': 'soixante-dix', 'explanation': 'FR: 70 = soixante-dix (France). | ZH: 法国用soixante-dix'},
    {'id': 'fr_nu_003', 'type': 'choice', 'level': 'A0', 'prompt': '80在法语中常说？', 'options': ['quatre-vingts', 'octante', 'quatre-vingt-dix', 'quatre-vingt-un'], 'answer': 'quatre-vingts', 'explanation': 'FR: 80 = quatre-vingts. | ZH: 80是quatre-vingts'},
    {'id': 'fr_nu_004', 'type': 'choice', 'level': 'A0', 'prompt': '200是？', 'options': ['deux cents', 'deux cent', 'deux centes', 'deux-vingts'], 'answer': 'deux cents', 'explanation': 'FR: 200 = deux cents. | ZH: 200为deux cents'},
    {'id': 'fr_nu_005', 'type': 'choice', 'level': 'A0', 'prompt': '“半”常用表达是？', 'options': ['demi', 'moitié', 'quart', 'tier'], 'answer': 'demi', 'explanation': 'FR: demi = half. | ZH: demi表示半'},
    {'id': 'fr_nu_006', 'type': 'choice', 'level': 'A0', 'prompt': '3:15可以说？', 'options': ['trois heures et quart', 'trois heures et demi', 'trois heures moins le quart', 'trois heures et cinq'], 'answer': 'trois heures et quart', 'explanation': 'FR: 3:15 = trois heures et quart. | ZH: 3:15是三点一刻'},
    {'id': 'fr_nu_007', 'type': 'choice', 'level': 'A0', 'prompt': '“星期一”是？', 'options': ['mardi', 'lundi', 'mercredi', 'jeudi'], 'answer': 'lundi', 'explanation': 'FR: lundi = Monday. | ZH: lundi是星期一'},
    {'id': 'fr_nu_008', 'type': 'choice', 'level': 'A1', 'prompt': '“一月”是？', 'options': ['février', 'janvier', 'mars', 'avril'], 'answer': 'janvier', 'explanation': 'FR: janvier = January. | ZH: janvier是一月'},
    {'id': 'fr_nu_009', 'type': 'choice', 'level': 'A0', 'prompt': '“多少？”是？', 'options': ['où', 'combien', 'quand', 'pourquoi'], 'answer': 'combien', 'explanation': 'FR: combien = how many/how much. | ZH: combien表示多少'},
    {'id': 'fr_nu_010', 'type': 'choice', 'level': 'A0', 'prompt': '“第一个”是？', 'options': ['un', 'premier', 'troisième', 'deuxième'], 'answer': 'premier', 'explanation': 'FR: premier = first. | ZH: premier是第一'},
]

QUESTIONS['fr.elementary.articles'] = [
    {'id': 'fr_ar_001', 'type': 'choice', 'level': 'A1', 'prompt': '“书”在法语中是阳性名词，应选？', 'options': ['la livre', 'le livre', 'les livre', 'un livre'], 'answer': 'le livre', 'explanation': 'FR: livre est masculin. | ZH: livre为阳性'},
    {'id': 'fr_ar_002', 'type': 'choice', 'level': 'A1', 'prompt': '“桌子”table为阴性，应选？', 'options': ['le table', 'la table', 'les table', 'un table'], 'answer': 'la table', 'explanation': 'FR: table est féminin. | ZH: table为阴性'},
    {'id': 'fr_ar_003', 'type': 'choice', 'level': 'A1', 'prompt': '元音开头名词前的定冠词通常写作？', 'options': ['le', 'la', 'l’', 'les'], 'answer': 'l’', 'explanation': 'FR: l’ devant voyelle. | ZH: 元音前用l’'},
    {'id': 'fr_ar_004', 'type': 'choice', 'level': 'A1', 'prompt': '复数定冠词是？', 'options': ['les', 'des', 'la', 'le'], 'answer': 'les', 'explanation': 'FR: les = plural definite article. | ZH: 复数定冠词为les'},
    {'id': 'fr_ar_005', 'type': 'choice', 'level': 'A1', 'prompt': '“一些苹果”应使用？', 'options': ['des pommes', 'les pommes', 'la pomme', 'une pomme'], 'answer': 'des pommes', 'explanation': 'FR: des = some plural. | ZH: 一些用des'},
    {'id': 'fr_ar_006', 'type': 'choice', 'level': 'A1', 'prompt': '“一个朋友”是？', 'options': ['un ami', 'une ami', 'des amis', 'le ami'], 'answer': 'un ami', 'explanation': 'FR: ami est masculin; un ami. | ZH: ami阳性用un'},
    {'id': 'fr_ar_007', 'type': 'choice', 'level': 'A1', 'prompt': '“一个老师(女)”应选？', 'options': ['un professeur', 'une professeur', 'la professeur', 'des professeur'], 'answer': 'une professeur', 'explanation': 'FR: une professeur pour femme. | ZH: 女性用une'},
    {'id': 'fr_ar_008', 'type': 'choice', 'level': 'A1', 'prompt': '“漂亮的房子”正确搭配？', 'options': ['belle maison', 'beau maison', 'bel maison', 'belle maisons'], 'answer': 'belle maison', 'explanation': 'FR: maison féminin -> belle. | ZH: maison阴性用belle'},
    {'id': 'fr_ar_009', 'type': 'choice', 'level': 'A1', 'prompt': '“新朋友(男)”应选？', 'options': ['nouveau ami', 'nouvel ami', 'nouvelle ami', 'neuf ami'], 'answer': 'nouvel ami', 'explanation': 'FR: nouvel devant voyelle masculine. | ZH: 元音前用nouvel'},
    {'id': 'fr_ar_010', 'type': 'choice', 'level': 'A1', 'prompt': '“法国菜”应选？', 'options': ['cuisine français', 'cuisine française', 'cuisine françaisse', 'cuisine le français'], 'answer': 'cuisine française', 'explanation': 'FR: cuisine féminin -> française. | ZH: cuisine阴性，形容词阴性'},
]

QUESTIONS['fr.elementary.family'] = [
    {'id': 'fr_fa_001', 'type': 'choice', 'level': 'A1', 'prompt': '“母亲”是？', 'options': ['père', 'mère', 'frère', 'soeur'], 'answer': 'mère', 'explanation': 'FR: mère = mother. | ZH: mère是母亲'},
    {'id': 'fr_fa_002', 'type': 'choice', 'level': 'A1', 'prompt': '“弟弟/哥哥”是？', 'options': ['soeur', 'frère', 'fille', 'oncle'], 'answer': 'frère', 'explanation': 'FR: frère = brother. | ZH: frère是兄弟'},
    {'id': 'fr_fa_003', 'type': 'choice', 'level': 'A1', 'prompt': '“姐姐/妹妹”是？', 'options': ['soeur', 'tante', 'nièce', 'cousine'], 'answer': 'soeur', 'explanation': 'FR: soeur = sister. | ZH: soeur是姐妹'},
    {'id': 'fr_fa_004', 'type': 'choice', 'level': 'A1', 'prompt': '“我的父亲”正确表达？', 'options': ['ma père', 'mon père', 'mes père', 'le père'], 'answer': 'mon père', 'explanation': 'FR: père masculin -> mon. | ZH: père阳性用mon'},
    {'id': 'fr_fa_005', 'type': 'choice', 'level': 'A1', 'prompt': '“我的母亲”正确表达？', 'options': ['mon mère', 'ma mère', 'mes mère', 'la mère'], 'answer': 'ma mère', 'explanation': 'FR: mère féminin -> ma. | ZH: mère阴性用ma'},
    {'id': 'fr_fa_006', 'type': 'choice', 'level': 'A1', 'prompt': '“我的姐姐(元音开头)”中“mon”用于？', 'options': ['mon soeur', 'ma soeur', 'mon soeur(s)', 'mes soeur'], 'answer': 'ma soeur', 'explanation': 'FR: soeur féminin -> ma. | ZH: soeur阴性用ma'},
    {'id': 'fr_fa_007', 'type': 'choice', 'level': 'A1', 'prompt': '“他们的孩子(复数)”应选？', 'options': ['leur enfant', 'leurs enfants', 'leurs enfant', 'leur enfants'], 'answer': 'leurs enfants', 'explanation': 'FR: plural: leurs enfants. | ZH: 复数用leurs'},
    {'id': 'fr_fa_008', 'type': 'choice', 'level': 'A1', 'prompt': '“叔叔”是？', 'options': ['tante', 'oncle', 'cousin', 'neveu'], 'answer': 'oncle', 'explanation': 'FR: oncle = uncle. | ZH: oncle是叔叔'},
    {'id': 'fr_fa_009', 'type': 'choice', 'level': 'A1', 'prompt': '“堂兄/表兄”是？', 'options': ['cousin', 'neveu', 'beau-père', 'gendre'], 'answer': 'cousin', 'explanation': 'FR: cousin = cousin (male). | ZH: cousin是堂表兄'},
    {'id': 'fr_fa_010', 'type': 'choice', 'level': 'A1', 'prompt': '“我有两个姐妹。”法语中姐妹是？', 'options': ['soeur', 'soeurs', 'soires', 'sours'], 'answer': 'soeurs', 'explanation': 'FR: plural of soeur = soeurs. | ZH: soeur复数为soeurs'},
]

QUESTIONS['fr.elementary.daily'] = [
    {'id': 'fr_da_001', 'type': 'choice', 'level': 'A1', 'prompt': '“我早上七点起床”中“起床”是？', 'options': ['se coucher', 'se lever', 'se laver', 'se promener'], 'answer': 'se lever', 'explanation': 'FR: se lever = get up. | ZH: se lever表示起床'},
    {'id': 'fr_da_002', 'type': 'choice', 'level': 'A1', 'prompt': '“吃早餐”是？', 'options': ['prendre le petit déjeuner', 'faire le déjeuner', 'manger le soir', 'boire la nuit'], 'answer': 'prendre le petit déjeuner', 'explanation': 'FR: prendre le petit déjeuner = eat breakfast. | ZH: 吃早餐'},
    {'id': 'fr_da_003', 'type': 'choice', 'level': 'A1', 'prompt': '“我去上班”中的“去”常用动词？', 'options': ['aller', 'venir', 'partir', 'arriver'], 'answer': 'aller', 'explanation': 'FR: aller = to go. | ZH: 去用aller'},
    {'id': 'fr_da_004', 'type': 'choice', 'level': 'A1', 'prompt': '“做作业”常用表达？', 'options': ['faire les devoirs', 'prendre les devoirs', 'donner les devoirs', 'lire les devoirs'], 'answer': 'faire les devoirs', 'explanation': 'FR: faire les devoirs = do homework. | ZH: 做作业'},
    {'id': 'fr_da_005', 'type': 'choice', 'level': 'A1', 'prompt': '“我通常八点上班”中“通常”是？', 'options': ['souvent', 'toujours', 'parfois', 'habituellement'], 'answer': 'habituellement', 'explanation': 'FR: habituellement = usually. | ZH: 通常=habituellement'},
    {'id': 'fr_da_006', 'type': 'choice', 'level': 'A1', 'prompt': '“晚上”常用词是？', 'options': ['le matin', 'le soir', 'la nuit', 'le midi'], 'answer': 'le soir', 'explanation': 'FR: le soir = evening. | ZH: 晚上=le soir'},
    {'id': 'fr_da_007', 'type': 'choice', 'level': 'A1', 'prompt': '“现在几点？”是？', 'options': ['Quel âge as-tu ?', 'Quelle heure est-il ?', 'Où est-il ?', 'Qui est-il ?'], 'answer': 'Quelle heure est-il ?', 'explanation': 'FR: Quelle heure est-il ? = What time is it? | ZH: 现在几点'},
    {'id': 'fr_da_008', 'type': 'choice', 'level': 'A1', 'prompt': '“我喜欢散步”中“散步”是？', 'options': ['se promener', 'se perdre', 'se préparer', 'se reposer'], 'answer': 'se promener', 'explanation': 'FR: se promener = take a walk. | ZH: 散步=se promener'},
    {'id': 'fr_da_009', 'type': 'choice', 'level': 'A1', 'prompt': '“周末”是？', 'options': ['la semaine', 'le week-end', 'le mois', 'l’année'], 'answer': 'le week-end', 'explanation': 'FR: week-end = weekend. | ZH: 周末=le week-end'},
    {'id': 'fr_da_010', 'type': 'choice', 'level': 'A1', 'prompt': '“我每天运动”中“每天”是？', 'options': ['toujours', 'chaque jour', 'jamais', 'parfois'], 'answer': 'chaque jour', 'explanation': 'FR: chaque jour = every day. | ZH: 每天=chaque jour'},
]

QUESTIONS['fr.intermediate.past_tense'] = [
    {'id': 'fr_pt_001', 'type': 'choice', 'level': 'B1', 'prompt': '“我昨天去了巴黎”应使用哪种时态？', 'options': ['现在时', '复合过去时', '未完成过去时', '将来时'], 'answer': '复合过去时', 'explanation': 'FR: action completed -> passé composé. | ZH: 完成动作用复合过去时'},
    {'id': 'fr_pt_002', 'type': 'choice', 'level': 'B1', 'prompt': '“我小时候常去海边”更适合？', 'options': ['复合过去时', '未完成过去时', '将来时', '条件式'], 'answer': '未完成过去时', 'explanation': 'FR: habitual past -> imparfait. | ZH: 过去习惯用未完成过去时'},
    {'id': 'fr_pt_003', 'type': 'choice', 'level': 'B1', 'prompt': '动词“aller”复合过去时的助动词是？', 'options': ['avoir', 'être', 'faire', 'aller'], 'answer': 'être', 'explanation': 'FR: aller uses être. | ZH: aller用être作助动词'},
    {'id': 'fr_pt_004', 'type': 'choice', 'level': 'B1', 'prompt': '“她去了”正确形式？', 'options': ['elle a allé', 'elle est allée', 'elle est allé', 'elle a allée'], 'answer': 'elle est allée', 'explanation': 'FR: être + allée (accord féminin). | ZH: 用être并与阴性一致'},
    {'id': 'fr_pt_005', 'type': 'choice', 'level': 'B1', 'prompt': '“我已经吃了”正确形式？', 'options': ['j’ai mangé', 'je suis mangé', 'j’ai mange', 'je suis mange'], 'answer': 'j’ai mangé', 'explanation': 'FR: manger uses avoir -> j’ai mangé. | ZH: manger用avoir'},
    {'id': 'fr_pt_006', 'type': 'choice', 'level': 'B1', 'prompt': '“他正在睡觉时我打电话”中“正在睡觉”用？', 'options': ['复合过去时', '未完成过去时', '将来时', '条件式'], 'answer': '未完成过去时', 'explanation': 'FR: background action -> imparfait. | ZH: 背景动作用未完成过去时'},
    {'id': 'fr_pt_007', 'type': 'choice', 'level': 'B1', 'prompt': '“我们突然听到了消息”更适合？', 'options': ['复合过去时', '未完成过去时', '现在时', '近未来'], 'answer': '复合过去时', 'explanation': 'FR: sudden event -> passé composé. | ZH: 突发事件用复合过去时'},
    {'id': 'fr_pt_008', 'type': 'choice', 'level': 'B1', 'prompt': '“她每天都在学习”过去习惯用？', 'options': ['imparfait', 'passé composé', 'futur', 'conditionnel'], 'answer': 'imparfait', 'explanation': 'FR: habitual past -> imparfait. | ZH: 习惯过去用imparfait'},
    {'id': 'fr_pt_009', 'type': 'choice', 'level': 'B1', 'prompt': '“他们到了”正确形式？', 'options': ['ils sont arrivés', 'ils ont arrivés', 'ils sont arrivé', 'ils ont arrivé'], 'answer': 'ils sont arrivés', 'explanation': 'FR: arriver uses être + plural agreement. | ZH: arriver用être并复数一致'},
    {'id': 'fr_pt_010', 'type': 'choice', 'level': 'B1', 'prompt': '“我那时不知道”更适合？', 'options': ['passé composé', 'imparfait', 'futur', 'subjonctif'], 'answer': 'imparfait', 'explanation': 'FR: state in past -> imparfait. | ZH: 过去状态用未完成过去时'},
]

QUESTIONS['fr.intermediate.shopping'] = [
    {'id': 'fr_sh_001', 'type': 'choice', 'level': 'B1', 'prompt': '“这个多少钱？”法语是？', 'options': ['C’est combien ?', 'C’est où ?', 'C’est qui ?', 'C’est quand ?'], 'answer': 'C’est combien ?', 'explanation': 'FR: C’est combien ? = How much is it? | ZH: 多少钱'},
    {'id': 'fr_sh_002', 'type': 'choice', 'level': 'B1', 'prompt': '“我想试穿”是？', 'options': ['Je veux payer', 'Je veux essayer', 'Je veux partir', 'Je veux manger'], 'answer': 'Je veux essayer', 'explanation': 'FR: essayer = try on. | ZH: essayer表示试穿'},
    {'id': 'fr_sh_003', 'type': 'choice', 'level': 'B1', 'prompt': '“大号”法语是？', 'options': ['taille petite', 'taille moyenne', 'taille grande', 'taille lourde'], 'answer': 'taille grande', 'explanation': 'FR: grande = large size. | ZH: 大号=taille grande'},
    {'id': 'fr_sh_004', 'type': 'choice', 'level': 'B1', 'prompt': '“可以打折吗？”常用表达？', 'options': ['C’est gratuit ?', 'Vous avez une réduction ?', 'Où est la caisse ?', 'C’est fini ?'], 'answer': 'Vous avez une réduction ?', 'explanation': 'FR: réduction = discount. | ZH: 是否有折扣'},
    {'id': 'fr_sh_005', 'type': 'choice', 'level': 'B1', 'prompt': '“收银台”是？', 'options': ['la caisse', 'la cuisine', 'la chambre', 'la gare'], 'answer': 'la caisse', 'explanation': 'FR: la caisse = cashier. | ZH: 收银台'},
    {'id': 'fr_sh_006', 'type': 'choice', 'level': 'B1', 'prompt': '“太贵了”是？', 'options': ['C’est pas cher', 'C’est trop cher', 'C’est cher', 'C’est trop bon'], 'answer': 'C’est trop cher', 'explanation': 'FR: trop cher = too expensive. | ZH: 太贵了'},
    {'id': 'fr_sh_007', 'type': 'choice', 'level': 'B1', 'prompt': '“便宜一点”是？', 'options': ['un peu plus cher', 'un peu moins cher', 'très cher', 'trop léger'], 'answer': 'un peu moins cher', 'explanation': 'FR: moins cher = cheaper. | ZH: 便宜一点'},
    {'id': 'fr_sh_008', 'type': 'choice', 'level': 'B1', 'prompt': '“我用卡支付”是？', 'options': ['Je paie en carte', 'Je paie par carte', 'Je paie avec cash', 'Je paie par argent'], 'answer': 'Je paie par carte', 'explanation': 'FR: payer par carte. | ZH: 用卡支付'},
    {'id': 'fr_sh_009', 'type': 'choice', 'level': 'B1', 'prompt': '“有更小的尺寸吗？”是？', 'options': ['Avez-vous plus grand ?', 'Avez-vous plus petit ?', 'Avez-vous moins cher ?', 'Avez-vous plus tard ?'], 'answer': 'Avez-vous plus petit ?', 'explanation': 'FR: plus petit = smaller size. | ZH: 更小尺寸'},
    {'id': 'fr_sh_010', 'type': 'choice', 'level': 'B1', 'prompt': '“试衣间”是？', 'options': ['cabine d’essayage', 'salle de classe', 'salle de bain', 'bureau'], 'answer': 'cabine d’essayage', 'explanation': 'FR: cabine d’essayage = fitting room. | ZH: 试衣间'},
]

QUESTIONS['fr.intermediate.travel'] = [
    {'id': 'fr_tr_001', 'type': 'choice', 'level': 'B1', 'prompt': '“火车站”是？', 'options': ['l’aéroport', 'la gare', 'le port', 'la station-service'], 'answer': 'la gare', 'explanation': 'FR: la gare = train station. | ZH: 火车站'},
    {'id': 'fr_tr_002', 'type': 'choice', 'level': 'B1', 'prompt': '“机票/车票”常用词是？', 'options': ['ticket', 'carte', 'billet', 'papier'], 'answer': 'billet', 'explanation': 'FR: billet = ticket. | ZH: 票=billet'},
    {'id': 'fr_tr_003', 'type': 'choice', 'level': 'B1', 'prompt': '“我想订票”是？', 'options': ['Je veux réserver un billet', 'Je veux acheter une maison', 'Je veux dormir', 'Je veux conduire'], 'answer': 'Je veux réserver un billet', 'explanation': 'FR: réserver un billet = book a ticket. | ZH: 订票'},
    {'id': 'fr_tr_004', 'type': 'choice', 'level': 'B1', 'prompt': '“护照”是？', 'options': ['le visa', 'le passeport', 'la carte', 'le permis'], 'answer': 'le passeport', 'explanation': 'FR: passeport = passport. | ZH: 护照'},
    {'id': 'fr_tr_005', 'type': 'choice', 'level': 'B1', 'prompt': '“登机口”是？', 'options': ['porte d’embarquement', 'porte de sortie', 'salle d’attente', 'départ'], 'answer': 'porte d’embarquement', 'explanation': 'FR: porte d’embarquement = gate. | ZH: 登机口'},
    {'id': 'fr_tr_006', 'type': 'choice', 'level': 'B1', 'prompt': '“我迷路了”是？', 'options': ['Je suis perdu', 'Je suis fatigué', 'Je suis en retard', 'Je suis prêt'], 'answer': 'Je suis perdu', 'explanation': 'FR: Je suis perdu = I am lost. | ZH: 我迷路了'},
    {'id': 'fr_tr_007', 'type': 'choice', 'level': 'B1', 'prompt': '“请问去市中心怎么走？”是？', 'options': ['Comment aller au centre-ville ?', 'Où est la plage ?', 'Quel est le prix ?', 'Quand part le train ?'], 'answer': 'Comment aller au centre-ville ?', 'explanation': 'FR: Comment aller au centre-ville ? | ZH: 去市中心怎么走'},
    {'id': 'fr_tr_008', 'type': 'choice', 'level': 'B1', 'prompt': '“换乘”常用表达？', 'options': ['changer de ligne', 'changer de chambre', 'changer de prix', 'changer de classe'], 'answer': 'changer de ligne', 'explanation': 'FR: changer de ligne = transfer lines. | ZH: 换乘线路'},
    {'id': 'fr_tr_009', 'type': 'choice', 'level': 'B1', 'prompt': '“单程票”是？', 'options': ['aller-retour', 'billet aller simple', 'billet retour', 'billet double'], 'answer': 'billet aller simple', 'explanation': 'FR: aller simple = one-way. | ZH: 单程票'},
    {'id': 'fr_tr_010', 'type': 'choice', 'level': 'B1', 'prompt': '“行李”是？', 'options': ['bagage', 'garage', 'fromage', 'voyage'], 'answer': 'bagage', 'explanation': 'FR: bagage = luggage. | ZH: 行李'},
]
