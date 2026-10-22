# Batch 7 (Hinglish)
def S(u, a, m, s):
    return {"users": u, "asks": a, "message": m, "steps": s}


SCENARIOS = [
    S(
        [
            "Retirement ke baad se andar se khaali lagta hai",
            "Paintees saal kaam kiya aur ab din bekaar lagte hain",
            "Aath mahine se. Bachche vyast hain, unhe nahi bataya",
            "Jaldi uth jaata hoon, kuch kaam nahi hota aur sair bhi chhod di",
        ],
        [
            ("Mujhse share karne ke liye shukriya. Aajkal aapke din kaise guzarte "
             "hain?"),
            ("Itni lambi naukri ke baad badlav bada hota hai. Yeh kab se hai, aur "
             "kisi se baat ki?"),
            "Aapki khulkar baat achhi lagi. Khana aur routine kaisa hai?",
        ],
        ("Lambi naukri ke baad khaalipan mehsoos hona bahut aam hai. Bhagavatam "
         "yaad dilata hai ki jeevan chhota hai aur har din keemti hai, isliye jo "
         "samay hriday ko uthata hai woh bekar nahi jaata. Yeh un cheezon ke "
         "aas-paas naya routine banane ka mauka ho sakta hai jo aapko pasand "
         "hain."),
        [
            "Subah ki sair tay samay par shuru kijiye.",
            "Ek gatividhi chuniye, jaise padhna, bagwani ya kisi ki madad.",
            "Bachchon se kahiye ki aap unke saath niyamit samay bitana chahte hain.",
            "Kisi local satsang ya samooh se judiye jahan log milein.",
            "Agar khaalipan bhaari rahe to doctor ya counsellor se baat kijiye.",
        ],
    ),
    S(
        [
            "Ghar mein mujhe koi dekhta hi nahi",
            "Saara ghar ka kaam main karti hoon aur koi dhanyavaad nahi kehta",
            "Saalon se. Shikayat nahi karna chahti isliye kisi ko nahi batati",
            "Sabke baad khaana khaati hoon aur shaam tak thak jaati hoon",
        ],
        [
            "Batane ke liye shukriya. Ek aam din ghar mein kaisa hota hai?",
            ("Itna sab karke bhi sarahna na milna dukh deta hai. Yeh kab se hai, aur "
             "kisi se kaha hai?"),
            "Yeh kehna himmat ka kaam hai. Apna khana aur routine kaisa hai?",
        ],
        ("Ghar ka kaam bhi asli kaam hai, aur chahna swabhavik hai ki use dekha "
         "aur saraha jaye. Bhagavatam achhe logon ki sangat ko hriday ke liye "
         "poshan batata hai, isliye ek aisi saheli dhoondhna jo sune madad kar "
         "sakta hai. Shaanti se apni zaroorat batane se ghar waale bhi samajh "
         "sakte hain."),
        [
            "Ghar ke kisi ek sadasya ko batayiye ki aapko kya sarahna dega.",
            "Kuch kaam doosron ke saath baant lijiye, chhote hi sahi.",
            "Apna khana tay samay par khaiye, sabse aakhir mein nahi.",
            "Roz tees minute sirf apne liye rakhiye, jaise sair ya prarthna.",
            "Agar zyadatar din udaas lagein to doctor ya counsellor se baat kijiye.",
        ],
    ),
    S(
        [
            "Lagta hai maine apni zindagi barbaad kar di",
            "Main chaalis ka hoon aur jo karna chahta tha kabhi nahi kiya",
            "Pichhle janamdin se, ek saal. Ghar waale sochte hain main theek hoon",
            "Neend theek hai par roz sab feeka lagta hai",
        ],
        [
            "Itni imaandari se batane ke liye shukriya. Aap kya karna chahte the?",
            "Yeh sochna bhaari hota hai. Yeh kab se hai, aur kisi apne se baat ki?",
            "Aapki khulkar baat achhi lagi. Khana aur routine kaisa hai?",
        ],
        ("Chaalis mein peeche dekhkar pachhtawa hona dikhata hai ki aapke liye "
         "kuch zaroori adhoora raha, aur woh hissa abhi zinda hai. Bhagavatam "
         "yaad dilata hai ki jeevan chhota hai aur har din keemti hai, isliye "
         "yeh shuruaat karne ki wajah hai, niraasha ki nahi. Jo chahte the usi "
         "ki taraf ek chhota kadam bhi jaan wapas la sakta hai."),
        [
            ("Likhiye ki aap kya karna chahte the aur is mahine ek chhota hissa "
             "chuniye."),
            "Hafte mein tees minute us par lagaiye, shuruaati hone par bhi.",
            "Apne kisi apne ko is sapne ke baare mein batayiye.",
            "Roz thodi sair kijiye taaki urja badhe.",
            "Agar feeka-pan hafton tak rahe to counsellor se baat kijiye.",
        ],
    ),
    S(
        [
            "Mera startup musibat mein hai",
            "Do mahine ka paisa bacha hai aur investors jawab nahi de rahe",
            ("Teen mahine ka tanav. Co-founder se behas hoti hai aur ghar mein nahi "
             "bataya"),
            "Khana skip karta hoon aur chaar ghante sota hoon",
        ],
        [
            "Yeh bhaari bojh lagta hai. Abhi sthiti kya hai?",
            ("Do mahine bahut kam samay hai. Yeh dabav kab se hai, aur company ke "
             "bahar kisi se baat ki?"),
            "Batane ke liye shukriya. Khana aur routine kaisa hai?",
        ],
        ("Paisa khatam hone ka darr sachcha hai aur aapka tanav samajh mein aata "
         "hai. Bhagavatam kathinaiyon ko dhairya aur vinamrata ke saath sweekar "
         "karne ki baat karta hai, aur shaant dimaag aur aaram kiya hua sharir "
         "ghabraaye hue dimaag se behtar faisle leta hai. Co-founder aur kisi "
         "mentor se imaandari se baat karna aise raaste dikha sakta hai jo akele "
         "nahi dikhte."),
        [
            "Ek page par apna paisa, kharch aur vikalp likh dijiye.",
            "Co-founder se agle kadam par imaandari se baat kijiye.",
            "Is hafte kisi mentor ya anubhavi founder se milkar baat kijiye.",
            "Niyamit khana khaiye aur kam se kam chhe ghante soiye.",
            "Agar tanav bahut zyada lage to counsellor se baat kijiye.",
        ],
    ),
    S(
        [
            "Mujhe ab kuch mehsoos nahi hota",
            "Jo cheezein pasand thi ab unka koi matlab nahi",
            "Lagbhag do mahine se. Kisi ko nahi bataya kyunki samjhane ko kuch nahi",
            "Bahut sota hoon aur khana tabhi khata hoon jab yaad aaye",
        ],
        [
            "Batane ke liye shukriya. Yeh feeling aapko pehli baar kab mehsoos hui?",
            ("Yeh bahut bhaari lagta hai, chahe samjhana mushkil ho. Yeh kab se hai, "
             "aur kisi ko bataya?"),
            "Mujhe khushi hai aapne yeh share kiya. Khana aur routine kaisa hai?",
        ],
        ("Do mahine tak sunn mehsoos karna aam udasi se zyada hai aur ise sahi "
         "dekhbhal chahiye. Aap isme kamzor nahi hain. Main aapko pyaar se salah "
         "deta hoon ki jaldi kisi doctor ya counsellor se milein aur ek bharose "
         "ke vyakti ko batayein. Khana, dhoop aur chhoti sair jaise saral "
         "aadatein madad ke milne tak sahara de sakti hain."),
        [
            ("Agle kuch dino mein doctor ya counsellor se zaroor milne ki koshish "
             "kijiye."),
            ("Kisi ek bharose ke vyakti ko bataiye ki aap kaisa mehsoos kar rahe "
             "hain."),
            "Tay samay par teen saral bhojan khaiye aur paani peeyiye.",
            "Roz dhoop mein das minute chaliye.",
            ("Agar kabhi surakshit na lage ya khud ko nuksan pahunchane ka khayal "
             "aaye to turant Tele-MANAS 14416 par call kijiye."),
        ],
    ),
    S(
        [
            "Mujhe darr hai ki meri mummy beemar na pad jaaye",
            ("Pichhle saal unhe dil ki pareshani hui thi aur ab har chhote dard par "
             "ghabrahat hoti hai"),
            ("Hospital se aane ke baad se, lagbhag ek saal. Maine unhe nahi bataya "
             "ki main kitna darta hoon"),
            "Har ghante unhe dekhta hoon aur mushkil se sota hoon",
        ],
        [
            ("Main samajh sakta hoon aap unse kitna pyaar karte hain. Unki tabiyat "
             "theek na lage to aapko kya hota hai?"),
            ("Ek saal tak yeh chinta thaka deti hai. Yeh kab se hai, aur kisi se "
             "baat ki?"),
            "Batane ke liye shukriya. Khana aur routine kaisa hai?",
        ],
        ("Aapka darr gehre pyaar se aata hai, aur ek saal tak har lakshan dekhna "
         "aapko bhi thaka deta hai. Bhagavatam sikhata hai ki darr tab aata hai "
         "jab hum apni asli pehchan bhool kar asthaayi sharir ko hi swayam maan "
         "lete hain, aur dhairya aur vinamrata ke saath kathinaiyon ko sweekar "
         "karne ki baat bhi karta hai. Unke doctor ke saath shaant yojna banane "
         "se har samay dekhne ki zaroorat kam ho sakti hai."),
        [
            "Unke doctor se poochiye ki kaun se lakshan par dhyan dena hai.",
            "Har ghante ki jagah tay samay par unhe dekhiye.",
            "Apni chinta unse ya ghar ke kisi aur se batayiye.",
            ("Ghabrahat badhne par paanch minute shaanti se prarthna ya saans par "
             "dhyan dijiye."),
            "Agar chinta se hafton tak neend na aaye to counsellor se baat kijiye.",
        ],
    ),
    S(
        [
            "Mujhe Bhagwan par gussa aa raha hai",
            "Papa ke theek hone ki prarthna ki thi phir bhi woh chale gaye",
            "Chhe mahine pehle. Maine prarthna band kar di aur uska bhi guilt hai",
            "Der se sota hoon aur mandir jaane se bachta hoon",
        ],
        [
            ("Aapke papa ke liye mujhe bahut dukh hai. Yeh aapke liye kaisa raha "
             "hai?"),
            ("Yeh bahut dard bhara nuksan hai, aur gussa dukh ka hissa ho sakta hai. "
             "Yeh chhe mahine kaise rahe, aur kisi se baat ki?"),
            "Mujhe batane ke liye shukriya. Khana aur routine kaisa hai?",
        ],
        ("Papa ko khone ke baad gussa aana dukh ka swabhavik hissa hai, aur "
         "aapki aastha sachchi bhavnaon ko bhi sambhal sakti hai. Bhagavatam "
         "kathinaiyon ko dhairya aur vinamrata ke saath sweekar karne ki baat "
         "karta hai, aur achhe logon ki sangat ko hriday ke liye poshan batata "
         "hai. Aapko prarthna zabardasti nahi karni, sirf shaanti se baithna bhi "
         "shuruaat ho sakti hai."),
        [
            "Gusse aur dukh ko bina judge kiye mehsoos hone dijiye.",
            "Papa ki koi yaad ghar ke kisi sadasya ke saath baantiye.",
            ("Jab mann kare tab kuch minute shaanti se baithiye, prarthna ki "
             "zabardasti kiye bina."),
            "Niyamit khana khaiye aur sone ka samay tay rakhiye.",
            "Agar dukh hafton tak roz ke kaam rok de to counsellor se baat kijiye.",
        ],
    ),
    S(
        [
            "Meri sadhna mein mann nahi lag raha",
            "Pehle roz subah jap karta tha ab sirf aadat jaisa lagta hai",
            "Lagbhag teen mahine se. Guilt hota hai par kisi se nahi kaha",
            "Der se uthta hoon aur kaam par bhaagta hoon",
        ],
        [
            ("Imaandari se batane ke liye shukriya. Jab yeh feeka lagne laga tab "
             "aapki zindagi mein kya badla?"),
            ("Kai logon ke liye sookhe daur aate hain. Yeh kab se hai, aur kisi se "
             "baat ki?"),
            "Aapki imaandari achhi lagi. Khana aur routine kaisa hai?",
        ],
        ("Sadhna mein sookhe daur bahut aam hain, aur imaandari se maanna hi "
         "achha sanket hai. Bhagavatam kehta hai ki sachchi chhoti sadhna bhi "
         "keemti hai, isliye thodi par niyamit sadhna bilkul na karne se behtar "
         "hai. Bhagwan ke baare mein sunna aur achhe logon ki sangat bhi taazgi "
         "wapas la sakti hai."),
        [
            ("Sadhna ko chhote samay tak kam kijiye jo aap nibha sakein, jaise "
             "paanch minute."),
            "Das minute jaldi uthiye taaki bhaag-daud na lage.",
            "Kisi pasandida vyakti ke saath ek chhoti baat suniye ya padhiye.",
            "Kisi dost ya bade se apni feeling baat kijiye.",
            ("Apne aap par dhairya rakhiye, har din apne mood se sadhna ko mat "
             "tauliye."),
        ],
    ),
    S(
        [
            "Main kisi ko maaf nahi kar pa raha",
            "Mere cousin ne paise liye aur kabhi wapas nahi kiye",
            ("Ek saal se zyada. Use dekhte hi gussa aata hai aur parents ko nahi "
             "bataya"),
            "Raat ko yahi sochta hoon aur neend udd jaati hai",
        ],
        [
            ("Yeh sunkar bura laga. Kya aap thoda aur bata sakte hain ki usne kya "
             "kiya?"),
            ("Apno se dhokha aur zyada chubhta hai. Yeh kab se hai, aur kisi se baat "
             "ki?"),
            "Batane ke liye shukriya. Khana aur routine kaisa hai?",
        ],
        ("Apno se dhokha dard deta hai, aur wapas na kiye gaye paiso par gussa "
         "hona jaayaz hai. Bhagavatam sikhata hai ki bhautik cheezon ki lalsa "
         "gehra dukh deti hai aur use chhodne se shanti milti hai. Dil se gussa "
         "chhodne ka matlab yeh nahi ki aap uski baat se sehmat hain, aur aap "
         "apne paiso ki raksha karte hue bhi apne mann ka bojh utaar sakte hain."),
        [
            ("Shaanti se tay kijiye ki uske saath baat karni hai ya nahi, zaroorat "
             "ho to kisi aur ko saath rakhiye."),
            "Rakam aur ek uchit tareekh saaf likh lijiye.",
            "Parents ya kisi bade ko batayiye ki kya hua.",
            "Gussa aaye to paanch minute prarthna ya shaant saans lijiye.",
            "Agar gusse se neend kharab rahe to counsellor se baat kijiye.",
        ],
    ),
    S(
        [
            "Mujhe ghar ki bahut yaad aati hai",
            "Master's ke liye videsh aaya hoon aur sab kuch anjaana lagta hai",
            ("Paanch mahine se. Ghar par kehta hoon sab theek hai kyunki woh chinta "
             "karte hain"),
            "Roz wahi khaana khaata hoon aur kamre mein rehta hoon",
        ],
        [
            "Yeh sach mein mushkil hai. Aapko sabse zyada kya yaad aata hai?",
            ("Sab kuch naya hona thaka deta hai. Yeh kab se hai, aur kisi ko asli "
             "haal bataya?"),
            "Batane ke liye shukriya. Neend aur routine kaisa hai?",
        ],
        ("Sab kuch naya hone par ghar ki yaad aana bahut swabhavik hai, aur "
         "paanch mahine abhi shuruaati hi hain. Bhagavatam achhe logon ki sangat "
         "ko hriday ke liye poshan batata hai, isliye apne paas ek bhi dostana "
         "vyakti milna madad kar sakta hai. Ghar waalon ko sach batane se aap "
         "unke aur karib aa sakte hain."),
        [
            ("Ghar waalon ko imaandari se batayiye ki aapko unki yaad aati hai, sirf "
             "yeh nahi ki sab theek hai."),
            ("Koi local samuday dhoondhiye, jaise Indian students ka group ya "
             "mandir."),
            "Hafte mein ek ghar ka pakwaan banaiye.",
            "Roz bahar chhoti sair kijiye aur sone ka samay tay rakhiye.",
            ("Agar yaad bahut bhaari rahe to university ke counselling service se "
             "milein."),
        ],
    ),
    S(
        [
            "Mujhe apne kaam se kabhi santushti nahi hoti",
            "Assignment baar baar banata hoon phir bhi kharab lagta hai",
            "School se hi. Kisi ko nahi bataya, sab sochte hain main mehnati hoon",
            "Der se sota hoon aur marks ki chinta rehti hai",
        ],
        [
            ("Batane ke liye shukriya. Assignment poora karne ke baad aapko kaisa "
             "lagta hai?"),
            ("Yeh thaka dene wala lagta hai. Yeh kab se hai, aur kisi ko bataya ki "
             "aapko kaisa lagta hai?"),
            "Imaandari ke liye shukriya. Khana aur routine kaisa hai?",
        ],
        ("Achha karne ki chahat achhi hai, par kabhi bhi kaafi na lagna thaka "
         "deta hai. Bhagavatam sikhata hai ki darr tab aata hai jab hum apni "
         "asli pehchan bhool jaate hain, aur aapki keemat marks se tay nahi "
         "hoti. Har kaam ke liye rukne ka ek saaf bindu tay karna aapko aaram de "
         "sakta hai."),
        [
            ("Pehle se tay kijiye ki assignment ko kitna samay milna chahiye aur "
             "samay khatam hone par ruk jaiye."),
            ("Ek kaam jama kijiye jo aapko bas theek lagta ho aur dekhiye kya hota "
             "hai."),
            "Kisi teacher ya dost ko batayiye ki marks ki chinta kitni hai.",
            "Raat ko baar baar kaam karne ki jagah tay samay par soiye.",
            "Agar chinta tez rahe to counsellor se baat kijiye.",
        ],
    ),
    S(
        [
            "Presentation se pehle mujhe ghabrahat hoti hai",
            "Shukravaar ko badi presentation hai aur haath abhi se kaanp rahe hain",
            ("Har baar hota hai. Team ko nahi bataya kyunki chahta hoon woh mujhe "
             "confident samjhein"),
            "Neend nahi aati aur nashta skip karta hoon",
        ],
        [
            ("Yeh tanav wala lagta hai. Ghabrahat shuru hone par sharir mein kya "
             "mehsoos hota hai?"),
            ("Kai log yeh mehsoos karte hain, chhupate bhi hain. Yeh kab se hota "
             "hai, aur kisi ko bataya?"),
            "Batane ke liye shukriya. Is hafte khana aur routine kaisa hai?",
        ],
        ("Badi presentation se pehle haath kaanpna tanav ki aam pratikriya hai, "
         "aur kai aatmavishwasi vakta bhi yahi mehsoos karte hain. Bhagavatam "
         "sikhata hai ki darr tab aata hai jab hum apni asli pehchan bhool jaate "
         "hain, aur aap is ghabrahat ke pal se kahin zyada hain. Zor se abhyas "
         "karna aur saans dheemi karna aapko shaant shuruaat de sakta hai."),
        [
            "Shukravaar se pehle presentation teen baar zor se boliye.",
            ("Shuru karne se pehle ek minute 4 ginti saans andar aur 6 ginti bahar "
             "chhodiye."),
            "Us din achhe se nashta kijiye.",
            ("Kisi ek teammate ko bataiye ki aap ghabra rahe hain taaki woh saath "
             "de."),
            "Ho sake to pehli raat kam se kam saat ghante soiye.",
        ],
    ),
]

INFO = [
    {
        "question": "Jeevan ka uddeshya kya hai?",
        "message": ("Bhagavatam kehta hai ki sabke liye sabse oonchi dharm bhagwan ki prem-"
         "bhakti hai, jo swarth ke bina aur bina ruke kiya jaaye, kyunki wahi "
         "aatma ko poori santushti deta hai. Yeh bhi yaad dilata hai ki jeevan "
         "chhota hai aur har din keemti hai."),
        "steps": [
            "Likhiye ki aapke liye sabse zaroori kya hai.",
            ("Ek chhoti roz ki sadhna chuniye, jaise paanch minute prarthna ya naam-"
             "jap."),
            "Kisi anubhavi aur dayalu vyakti se apne sawaal poochiye.",
            "Roz kisi ke liye ek chhota achha kaam kijiye.",
        ],
    },
    {
        "question": "Adhyatmik sadhna kaise shuru karein?",
        "message": ("Aap chhote aur saral tareeke se shuru kar sakte hain. Bhagavatam kehta "
         "hai ki samajhdaar vyakti sadhna jaldi shuru karta hai, aur sachchi "
         "chhoti sadhna bhi keemti hai. Yeh bhi kehta hai ki bhagwan ke baare "
         "mein sunna aur naam-jap tatha achhe logon ki sangat hriday ko poshan "
         "deti hai."),
        "steps": [
            "Ek tay samay aur shaant jagah chuniye.",
            "Sirf paanch minute naam-jap ya maun prarthna se shuru kijiye.",
            "Roz ek chhota ansh padhiye ya suniye.",
            "Dayalu aur samaan soch wale logon ke saath samay bitaiye.",
            "Samay dheere dheere badhaiye, khud par zor mat daaliye.",
        ],
    },
    {
        "question": "Asafalta ka saamna kaise karein?",
        "message": ("Asafalta dukh deti hai, par ek result aapki keemat tay nahi karta. "
         "Bhagavatam kathinaiyon ko dhairya aur vinamrata ke saath sweekar karne "
         "ki baat karta hai, aur yaad dilata hai ki jeevan chhota hai aur har "
         "din keemti hai."),
        "steps": [
            "Likhiye ki kya hua aur usse kya seekh sakte hain.",
            "Apni feeling kisi bharose ke vyakti se baat kijiye.",
            "Ek chhota vyavaharik agla kadam chuniye.",
            "Apne aap se waise hi pyaar se baat kijiye jaise dost se karte.",
            "Agar niraasha hafton tak bhaari rahe to counsellor se baat kijiye.",
        ],
    },
]