#!/usr/bin/env python3
"""Build Anki-importable .tsv files into decks/ for a Spanish A1 deck.

Four columns:  Front <TAB> Back <TAB> Note <TAB> Tags

The gloss lives in its own Note field rather than inside Back, so that
{{tts es_ES:Back}} reads the Spanish and nothing else. Grey styling for the
gloss belongs in the note type's CSS, not in the data.

Two note types, because the two directions need the speaker on opposite
sides: everything is "Spanish Production" (English prompt -> Spanish answer)
except the sentence deck, which is "Spanish Comprehension".

Add cards to the lists below and re-run:  python3 build_anki.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decks")

PRODUCTION = "Spanish Production"      # Front = English, Back = Spanish
COMPREHENSION = "Spanish Comprehension"  # Front = Spanish, Back = English


# Fronts in the verb deck, filled in once it is written, so the other files
# never collide with it (Anki flags same-first-field notes as duplicates).
EXISTING = set()


def write(filename, rows, notetype, guard=True):
    kept, dropped = [], []
    seen = set()
    for row in rows:
        front = row[0]
        if (guard and front in EXISTING) or front in seen:
            dropped.append(front)
        else:
            seen.add(front)
            kept.append(row)
    rows = kept
    if dropped:
        print(f"  {filename}: skipped {len(dropped)} already in the verb deck: "
              + "; ".join(dropped))
    path = os.path.join(OUT, filename)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        # these headers tell Anki which note type to use and where the tags
        # are, so the import dialog needs no fiddling
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write(f"#notetype:{notetype}\n")
        f.write("#tags column:4\n")
        for front, back, note, tags in rows:
            for cell in (front, back, note, tags):
                if "\t" in cell or "\n" in cell:
                    raise SystemExit(f"tab/newline in cell: {cell!r}")
            f.write("\t".join([front, back, note, tags]) + "\n")
    print(f"{filename}: {len(rows)} cards")
    return len(rows)


def vocab(en, es, note, tags):
    """Core vocabulary: English prompt -> Spanish production."""
    return (en, es, note, tags)


def grammar(task, answer, note, tags):
    """Transformation drill: instruction -> Spanish answer."""
    return (task, answer, note, tags)


def sentence(es, en, note, tags):
    """Comprehension: Spanish sentence -> English + word breakdown."""
    return (es, en, note, tags)


def verb(prompt, answer, note, tags):
    """Verb drill: fill-in-the-blank or EN->ES, with the gloss in Note.

    On the fill-in cards the gloss translates the whole sentence, so the form
    is never drilled without knowing what it means.
    """
    return (prompt, answer, note, tags)


VERBS = [
    # ---- ser -------------------------------------------------------------
    verb("Yo ___ de Suecia. (ser)", "soy", "I'm from Sweden &middot; ser for origin", "A1::verbs A1::ser"),
    verb("María ___ muy simpática. (ser)", "es", "María is very nice &middot; ser for what someone is like", "A1::verbs A1::ser"),
    verb("Nosotros ___ estudiantes. (ser)", "somos", "We're students &middot; no un/una before a role or job", "A1::verbs A1::ser"),
    verb("¿De dónde ___ tú? (ser)", "eres", "Where are you from? &middot; de dónde + ser for origin", "A1::verbs A1::ser"),
    verb("Ellos ___ españoles. (ser)", "son", "They're Spanish &middot; nationalities are lowercase", "A1::verbs A1::ser"),

    # ---- estar -----------------------------------------------------------
    verb("Yo ___ cansado hoy. (estar)", "estoy", "I'm tired today &middot; estar for how you feel right now", "A1::verbs A1::estar"),
    verb("¿Dónde ___ el baño? (estar)", "está", "Where's the bathroom? &middot; estar for location", "A1::verbs A1::estar"),
    verb("Madrid ___ en España. (estar)", "está", "Madrid is in Spain &middot; even permanent locations take estar", "A1::verbs A1::estar"),
    verb("Nosotros ___ en casa. (estar)", "estamos", "We're at home &middot; en casa = at home, no article", "A1::verbs A1::estar"),
    verb("¿Cómo ___ tú? (estar)", "estás", "How are you? &middot; cómo + estar asks how you feel; cómo + ser asks what you're like", "A1::verbs A1::estar"),

    # ---- tener -----------------------------------------------------------
    verb("Yo ___ treinta y dos años. (tener)", "tengo", "I'm thirty-two &middot; age uses tener, not ser", "A1::verbs A1::tener"),
    verb("¿Cuántos años ___ tú? (tener)", "tienes", "How old are you? &middot; lit. how many years do you have", "A1::verbs A1::tener"),
    verb("Nosotros ___ dos hermanos. (tener)", "tenemos", "We have two brothers &middot; nosotros keeps the plain stem: tenemos", "A1::verbs A1::tener"),
    verb("Ella ___ un coche. (tener)", "tiene", "She has a car &middot; e &rarr; ie in all but nosotros / vosotros", "A1::verbs A1::tener"),
    verb("Ellos ___ mucho trabajo. (tener)", "tienen", "They have a lot of work &middot; mucho agrees with trabajo", "A1::verbs A1::tener"),

    # ---- haber (hay) -----------------------------------------------------
    verb("___ un supermercado cerca de aquí. (haber)", "Hay", "There's a supermarket near here &middot; hay never changes", "A1::verbs A1::haber"),
    verb("___ muchas personas en el restaurante. (haber)", "Hay", "There are a lot of people in the restaurant &middot; same hay for the plural", "A1::verbs A1::haber"),
    verb("¿___ un banco cerca? (haber)", "Hay", "Is there a bank nearby? &middot; hay + un/una to ask if something exists", "A1::verbs A1::haber"),
    verb("En mi ciudad ___ muchos parques. (haber)", "hay", "There are a lot of parks in my city &middot; hay introduces something new, está locates something known", "A1::verbs A1::haber"),
    verb("No ___ leche en la nevera. (haber)", "hay", "There's no milk in the fridge &middot; no hay + noun, with no article", "A1::verbs A1::haber"),

    # ---- hacer -----------------------------------------------------------
    verb("¿Qué ___ tú los fines de semana? (hacer)", "haces", "What do you do at weekends? &middot; los fines de semana = at weekends, as a habit", "A1::verbs A1::hacer"),
    verb("Yo ___ ejercicio todos los días. (hacer)", "hago", "I exercise every day &middot; hacer ejercicio &middot; irregular yo: hago", "A1::verbs A1::hacer"),
    verb("Ella ___ la comida. (hacer)", "hace", "She makes the food &middot; hacer la comida = to cook", "A1::verbs A1::hacer"),
    verb("Nosotros ___ muchas cosas hoy. (hacer)", "hacemos", "We're doing a lot of things today &middot; the present covers what's happening now", "A1::verbs A1::hacer"),
    verb("¿Qué ___ ahora? (hacer)", "haces", "What are you doing now? &middot; Spanish uses the plain present where English uses -ing", "A1::verbs A1::hacer"),

    # ---- ir / venir ------------------------------------------------------
    verb("Yo ___ al trabajo a las ocho. (ir)", "voy", "I go to work at eight &middot; a + el contracts to al", "A1::verbs A1::ir"),
    verb("¿Adónde ___ vosotros? (ir)", "vais", "Where are you all going? &middot; adónde with verbs of movement", "A1::verbs A1::ir"),
    verb("Mi amigo ___ mañana a Estocolmo. (venir)", "viene", "My friend is coming to Stockholm tomorrow &middot; e &rarr; ie: vengo, vienes, viene", "A1::verbs A1::venir"),
    verb("¿Quieres ___ conmigo? (venir)", "venir", "Do you want to come with me? &middot; after another verb the infinitive stays &middot; conmigo = with me", "A1::verbs A1::venir"),

    # ---- querer / poder / saber / conocer --------------------------------
    verb("Yo ___ aprender español. (querer)", "quiero", "I want to learn Spanish &middot; querer + infinitive", "A1::verbs A1::querer"),
    verb("¿___ un café, por favor? (querer)", "Quieres", "Would you like a coffee, please? &middot; querer + noun to offer something", "A1::verbs A1::querer"),
    verb("No ___ ir hoy. Estoy enfermo. (poder)", "puedo", "I can't go today. I'm ill. &middot; o &rarr; ue: puedo, puedes, puede", "A1::verbs A1::poder"),
    verb("¿___ hablar español? (poder)", "Puedes", "Can you speak Spanish? &middot; poder = be able to; saber = know how to", "A1::verbs A1::poder"),
    verb("Yo ___ nadar muy bien. (saber)", "sé", "I can swim very well &middot; saber + infinitive = know how to do something", "A1::verbs A1::saber"),
    verb("¿___ dónde está el restaurante? (saber)", "Sabes", "Do you know where the restaurant is? &middot; saber for facts", "A1::verbs A1::saber"),
    verb("Yo ___ a Ana. Es mi amiga. (conocer)", "conozco", "I know Ana. She's my friend. &middot; conocer for people, with the personal a", "A1::verbs A1::conocer"),
    verb("¿___ Madrid? (conocer)", "Conoces", "Do you know Madrid? &middot; conocer for places you're familiar with", "A1::verbs A1::conocer"),

    # ---- gustar ----------------------------------------------------------
    verb("Me ___ mucho el chocolate. (gustar)", "gusta", "I really like chocolate &middot; lit. chocolate pleases me, so the thing liked is the subject", "A1::verbs A1::gustar"),
    verb("Me ___ los perros. (gustar)", "gustan", "I like dogs &middot; a plural thing &rarr; gustan", "A1::verbs A1::gustar"),
    verb("¿Te ___ la música española? (gustar)", "gusta", "Do you like Spanish music? &middot; te = to you", "A1::verbs A1::gustar"),

    # ---- hablar / comer / vivir ------------------------------------------
    verb("Yo ___ español todos los días. (hablar)", "hablo", "I speak Spanish every day &middot; regular -ar: -o, -as, -a", "A1::verbs A1::hablar"),
    verb("¿___ inglés? (hablar — tú)", "hablas", "Do you speak English? &middot; the pronoun is usually left out", "A1::verbs A1::hablar"),
    verb("Mi madre ___ español y francés. (hablar)", "habla", "My mother speaks Spanish and French &middot; languages are lowercase", "A1::verbs A1::hablar"),
    verb("Nosotros ___ en un restaurante. (comer)", "comemos", "We're eating at a restaurant &middot; regular -er nosotros: -emos", "A1::verbs A1::comer"),
    verb("Yo ___ pizza los viernes. (comer)", "como", "I eat pizza on Fridays &middot; los viernes = on Fridays", "A1::verbs A1::comer"),
    verb("¿Qué ___ normalmente para desayunar? (comer — tú)", "comes", "What do you normally eat for breakfast? &middot; para + infinitive = for doing something", "A1::verbs A1::comer"),
    verb("Yo ___ en Estocolmo. (vivir)", "vivo", "I live in Stockholm &middot; -ir and -er share the yo / tú / él endings", "A1::verbs A1::vivir"),
    verb("¿Dónde ___ tú? (vivir)", "vives", "Where do you live? &middot; dónde takes an accent in a question", "A1::verbs A1::vivir"),
    verb("Mis padres ___ en Suecia. (vivir)", "viven", "My parents live in Sweden &middot; padres = parents as well as fathers", "A1::verbs A1::vivir"),

    # ---- trabajar / necesitar / llevar / poner / ver ---------------------
    verb("Yo ___ en una empresa tecnológica. (trabajar)", "trabajo", "I work at a tech company &middot; trabajar en for a workplace", "A1::verbs A1::trabajar"),
    verb("¿Dónde ___ tú? (trabajar)", "trabajas", "Where do you work? &middot; regular -ar tú ending: -as", "A1::verbs A1::trabajar"),
    verb("Mi hermana ___ en un hospital. (trabajar)", "trabaja", "My sister works at a hospital", "A1::verbs A1::trabajar"),
    verb("Yo ___ un nuevo ordenador. (necesitar)", "necesito", "I need a new computer &middot; ordenador in Spain, computadora in Latin America", "A1::verbs A1::necesitar"),
    verb("¿___ ayuda? (necesitar — tú)", "necesitas", "Do you need help? &middot; ayuda takes no article here", "A1::verbs A1::necesitar"),
    verb("Nosotros ___ más tiempo. (necesitar)", "necesitamos", "We need more time &middot; más + noun = more", "A1::verbs A1::necesitar"),
    verb("Yo ___ una camiseta azul. (llevar)", "llevo", "I'm wearing a blue T-shirt &middot; llevar = wear as well as carry", "A1::verbs A1::llevar"),
    verb("Ella ___ gafas. (llevar)", "lleva", "She wears glasses &middot; gafas is always plural", "A1::verbs A1::llevar"),
    verb("¿Qué ropa ___ hoy? (llevar — tú)", "llevas", "What are you wearing today? &middot; la ropa is singular in Spanish", "A1::verbs A1::llevar"),
    verb("Yo ___ las llaves sobre la mesa. (poner)", "pongo", "I put the keys on the table &middot; irregular yo: pongo", "A1::verbs A1::poner"),
    verb("¿Dónde ___ el teléfono? (poner — tú)", "pones", "Where do you put the phone?", "A1::verbs A1::poner"),
    verb("Ella ___ la comida en la mesa. (poner)", "pone", "She puts the food on the table", "A1::verbs A1::poner"),
    verb("Yo ___ la televisión por la noche. (ver)", "veo", "I watch TV in the evening &middot; ver = both see and watch", "A1::verbs A1::ver"),
    verb("¿Qué ___ tú en la televisión? (ver)", "ves", "What do you watch on TV? &middot; en la televisión = on TV", "A1::verbs A1::ver"),
    verb("Nosotros ___ una película. (ver)", "vemos", "We're watching a film &middot; ver is regular apart from veo", "A1::verbs A1::ver"),

    # ---- volver / empezar / jugar / salir / decir ------------------------
    verb("Yo ___ a casa a las seis. (volver)", "vuelvo", "I come home at six &middot; o &rarr; ue: vuelvo, but volvemos", "A1::verbs A1::volver"),
    verb("¿Cuándo ___ tú de Madrid? (volver)", "vuelves", "When do you come back from Madrid? &middot; volver de = come back from", "A1::verbs A1::volver"),
    verb("Nosotros ___ mañana. (volver)", "volvemos", "We come back tomorrow &middot; no stem change in nosotros", "A1::verbs A1::volver"),
    verb("La clase ___ a las nueve. (empezar)", "empieza", "The class starts at nine &middot; e &rarr; ie: empieza", "A1::verbs A1::empezar"),
    verb("Yo ___ a trabajar a las ocho. (empezar)", "empiezo", "I start work at eight &middot; empezar a + infinitive", "A1::verbs A1::empezar"),
    verb("Nosotros ___ hoy. (empezar)", "empezamos", "We start today &middot; z &rarr; c only in the yo preterite, not here", "A1::verbs A1::empezar"),
    verb("Yo ___ al fútbol los sábados. (jugar)", "juego", "I play football on Saturdays &middot; jugar a + sport: juego al fútbol", "A1::verbs A1::jugar"),
    verb("Los niños ___ en el parque. (jugar)", "juegan", "The children play in the park &middot; u &rarr; ue, unique to jugar", "A1::verbs A1::jugar"),
    verb("Nosotros ___ a las cartas. (jugar)", "jugamos", "We play cards &middot; jugar a las cartas", "A1::verbs A1::jugar"),
    verb("Yo ___ de casa a las ocho. (salir)", "salgo", "I leave home at eight &middot; irregular yo: salgo &middot; salir de = leave a place", "A1::verbs A1::salir"),
    verb("El tren ___ a las diez. (salir)", "sale", "The train leaves at ten &middot; salir for departures", "A1::verbs A1::salir"),
    verb("¿Vosotros ___ esta noche? (salir)", "salís", "Are you all going out tonight? &middot; salir = go out socially too", "A1::verbs A1::salir"),
    verb("Yo siempre ___ la verdad. (decir)", "digo", "I always tell the truth &middot; e &rarr; i, plus an irregular yo: digo", "A1::verbs A1::decir"),
    verb("¿Cómo se ___ \"apple\" en español? (decir)", "dice", "How do you say apple in Spanish? &middot; se dice = one says", "A1::verbs A1::decir"),
    verb("Ellos ___ que no. (decir)", "dicen", "They say no &middot; decir que = to say that", "A1::verbs A1::decir"),

    # ---- EN -> ES, one verb ---------------------------------------------
    verb("I am Swedish.", "Soy sueco/a.", "ser for a lasting trait &middot; sueca if you're female", "A1::translation A1::ser"),
    verb("I am tired.", "Estoy cansado/a.", "estar for a passing state", "A1::translation A1::estar"),
    verb("I have a car.", "Tengo un coche.", "coche in Spain, carro or auto in Latin America", "A1::translation A1::tener"),
    verb("There is a restaurant here.", "Hay un restaurante aquí.", "hay for existence, está for location", "A1::translation A1::haber"),
    verb("There are many people here.", "Hay muchas personas aquí.", "hay is the same in the plural", "A1::translation A1::haber"),
    verb("What are you doing?", "¿Qué haces?", "no -ing form and no helper verb", "A1::translation A1::hacer"),
    verb("I am going home.", "Voy a casa.", "a casa = home(wards), with no article", "A1::translation A1::ir"),
    verb("I want to learn Spanish.", "Quiero aprender español.", "querer + infinitive", "A1::translation A1::querer"),
    verb("I can speak Spanish.", "Puedo hablar español.", "poder = be able to (saber = know how to)", "A1::translation A1::poder"),
    verb("I don't know.", "No sé.", "sé takes an accent to keep it apart from se", "A1::translation A1::saber"),
    verb("I know Madrid.", "Conozco Madrid.", "conocer = be familiar with &middot; irregular yo: conozco", "A1::translation A1::conocer"),
    verb("I like coffee.", "Me gusta el café.", "the article stays: el café", "A1::translation A1::gustar"),
    verb("I like Spanish food.", "Me gusta la comida española.", "nationality adjectives follow the noun and stay lowercase", "A1::translation A1::gustar"),
    verb("I speak English.", "Hablo inglés.", "drop yo unless you're stressing it", "A1::translation A1::hablar"),
    verb("I eat breakfast at eight.", "Desayuno a las ocho.", "desayunar is a single verb for have breakfast", "A1::translation A1::comer"),
    verb("I live in Stockholm.", "Vivo en Estocolmo.", "cities have Spanish names: Estocolmo", "A1::translation A1::vivir"),
    verb("I work from home.", "Trabajo desde casa.", "desde casa = from home", "A1::translation A1::trabajar"),
    verb("I need some water.", "Necesito agua.", "no word for some &middot; agua is feminine but takes el", "A1::translation A1::necesitar"),
    verb("I have a blue shirt.", "Tengo una camisa azul.", "the colour follows the noun and agrees with it", "A1::translation A1::tener"),
    verb("I put my keys on the table.", "Pongo mis llaves en la mesa.", "en covers both on and in", "A1::translation A1::poner"),
    verb("I watch TV every evening.", "Veo la televisión todas las noches.", "todas las noches = every night", "A1::translation A1::ver"),

    # ---- EN -> ES, two verbs --------------------------------------------
    verb("I am at home because I am tired.", "Estoy en casa porque estoy cansado/a.", "porque = because &middot; ¿por qué? = why", "A1::mixed A1::estar"),
    verb("I am Swedish, but I live in Spain.", "Soy sueco/a, pero vivo en España.", "ser for who you are, a separate verb for where you live", "A1::mixed A1::ser A1::vivir"),
    verb("There is a restaurant near my house.", "Hay un restaurante cerca de mi casa.", "cerca de = near", "A1::mixed A1::haber"),
    verb("I have to work tomorrow.", "Tengo que trabajar mañana.", "tener que + infinitive = have to", "A1::mixed A1::tener A1::trabajar"),
    verb("I want to go to Spain.", "Quiero ir a España.", "two verbs: the second stays in the infinitive", "A1::mixed A1::querer A1::ir"),
    verb("I can't go today.", "No puedo ir hoy.", "no goes in front of the verb", "A1::mixed A1::poder A1::ir"),
    verb("Do you know where the bathroom is?", "¿Sabes dónde está el baño?", "saber for the fact, estar for the location &middot; dónde keeps its accent", "A1::mixed A1::saber A1::estar"),
    verb("Do you know Madrid?", "¿Conoces Madrid?", "conocer, not saber, for places", "A1::mixed A1::conocer"),
    verb("I like Spanish music.", "Me gusta la música española.", "a singular thing &rarr; gusta", "A1::mixed A1::gustar"),
    verb("I like Spanish movies.", "Me gustan las películas españolas.", "a plural thing &rarr; gustan", "A1::mixed A1::gustar"),
    verb("What do you want to eat?", "¿Qué quieres comer?", "querer + infinitive, with qué in front", "A1::mixed A1::querer A1::comer"),
    verb("What are you going to do tomorrow?", "¿Qué vas a hacer mañana?", "ir a + infinitive = going to", "A1::mixed A1::ir A1::hacer"),
    verb("I am going to work.", "Voy a trabajar.", "also I'm going to work (the place): context decides", "A1::mixed A1::ir A1::trabajar"),
    verb("My friend is coming tomorrow.", "Mi amigo/a viene mañana.", "the present covers a planned future", "A1::mixed A1::venir"),
    verb("I need to speak Spanish.", "Necesito hablar español.", "necesitar + infinitive", "A1::mixed A1::necesitar A1::hablar"),
    verb("I work in Stockholm but live outside Stockholm.", "Trabajo en Estocolmo pero vivo fuera de Estocolmo.", "fuera de = outside", "A1::mixed A1::trabajar A1::vivir"),
    verb("There are three people in my family.", "Hay tres personas en mi familia.", "persona is feminine, even for a man", "A1::mixed A1::haber"),
    verb("I have two brothers.", "Tengo dos hermanos.", "hermanos = brothers, or siblings of mixed gender", "A1::mixed A1::tener"),
    verb("I don't have a car.", "No tengo coche.", "no article after a negative tener", "A1::mixed A1::tener"),
    verb("I don't want to eat.", "No quiero comer.", "no + querer + infinitive", "A1::mixed A1::querer A1::comer"),
    verb("I can't speak Spanish very well.", "No puedo hablar español muy bien.", "muy bien goes at the end", "A1::mixed A1::poder A1::hablar"),
    verb("I see my friends every weekend.", "Veo a mis amigos todos los fines de semana.", "the personal a before people", "A1::mixed A1::ver"),
    verb("I put my phone on the table.", "Pongo mi teléfono en la mesa.", "no article with a possessive: mi teléfono", "A1::mixed A1::poner"),
    verb("I wear glasses.", "Llevo gafas.", "llevar for wearing &middot; gafas is plural", "A1::mixed A1::llevar"),
    verb("I come back home late.", "Vuelvo a casa tarde.", "volver a casa = go back home", "A1::translation A1::volver"),
    verb("When do you start work?", "¿Cuándo empiezas a trabajar?", "empezar a + infinitive", "A1::translation A1::empezar"),
    verb("We play football on Sundays.", "Jugamos al fútbol los domingos.", "jugar al + sport &middot; los domingos = on Sundays", "A1::translation A1::jugar"),
    verb("I go out with my friends on Fridays.", "Salgo con mis amigos los viernes.", "salir con = go out with", "A1::translation A1::salir"),
    verb("What are you saying?", "¿Qué dices?", "dices for tú &middot; decís is vosotros", "A1::translation A1::decir"),

    # ---- correr / nadar / llamar / llegar / mirar ------------------------
    verb("Yo ___ todos los días. (correr)", "corro", "I run every day &middot; regular -er, like comer", "A1::verbs A1::correr"),
    verb("Ella ___ muy rápido. (correr)", "corre", "She runs very fast &middot; rápido works as an adverb here", "A1::verbs A1::correr"),
    verb("Nosotros ___ en el parque. (correr)", "corremos", "We run in the park &middot; -er nosotros: -emos", "A1::verbs A1::correr"),
    verb("Yo ___ muy bien. (nadar)", "nado", "I swim very well &middot; regular -ar", "A1::verbs A1::nadar"),
    verb("¿___ tú en el mar? (nadar)", "Nadas", "Do you swim in the sea? &middot; el mar = the sea", "A1::verbs A1::nadar"),
    verb("Los niños ___ en la piscina. (nadar)", "nadan", "The children swim in the pool &middot; la piscina = swimming pool", "A1::verbs A1::nadar"),
    verb("Yo te ___ mañana. (llamar)", "llamo", "I'll call you tomorrow &middot; the plain present covers a near-future plan", "A1::verbs A1::llamar"),
    verb("Mi madre me ___ todos los domingos. (llamar)", "llama", "My mother calls me every Sunday &middot; todos los domingos = every Sunday", "A1::verbs A1::llamar"),
    verb("¿Cómo se ___ tu hermano? (llamar)", "llama", "What's your brother's name? &middot; llamarse = to be called, so the se stays", "A1::verbs A1::llamar"),
    verb("El tren ___ a las ocho. (llegar)", "llega", "The train arrives at eight &middot; llegar a + time or place", "A1::verbs A1::llegar"),
    verb("Yo siempre ___ tarde. (llegar)", "llego", "I always arrive late &middot; llegar tarde = to be late", "A1::verbs A1::llegar"),
    verb("Nosotros ___ mañana a Madrid. (llegar)", "llegamos", "We arrive in Madrid tomorrow &middot; llegar a, never llegar en", "A1::verbs A1::llegar"),
    verb("Yo ___ por la ventana. (mirar)", "miro", "I look out of the window &middot; mirar por la ventana", "A1::verbs A1::mirar"),
    verb("¿Qué ___ tú? (mirar)", "miras", "What are you looking at? &middot; mirar needs no preposition: miro la tele", "A1::verbs A1::mirar"),
    verb("Ellos ___ el menú. (mirar)", "miran", "They're looking at the menu &middot; mirar = look at, ver = see", "A1::verbs A1::mirar"),

    # ---- creer / aprender / oír / seguir / leer --------------------------
    verb("Yo ___ que sí. (creer)", "creo", "I think so &middot; creer que = to think / believe that", "A1::verbs A1::creer"),
    verb("¿___ tú en la suerte? (creer)", "Crees", "Do you believe in luck? &middot; creer en = to believe in", "A1::verbs A1::creer"),
    verb("Nosotros ___ que es verdad. (creer)", "creemos", "We think it's true &middot; regular -er: creemos", "A1::verbs A1::creer"),
    verb("Yo ___ español en una academia. (aprender)", "aprendo", "I learn Spanish at a language school &middot; regular -er", "A1::verbs A1::aprender"),
    verb("¿Dónde ___ tú español? (aprender)", "aprendes", "Where do you learn Spanish?", "A1::verbs A1::aprender"),
    verb("Los niños ___ muy rápido. (aprender)", "aprenden", "Children learn very fast", "A1::verbs A1::aprender"),
    verb("Yo no ___ nada. (oír)", "oigo", "I can't hear anything &middot; irregular yo: oigo &middot; Spanish needs no can here", "A1::verbs A1::oir"),
    verb("¿___ tú la música? (oír)", "Oyes", "Can you hear the music? &middot; i &rarr; y between vowels: oyes, oye, oyen", "A1::verbs A1::oir"),
    verb("Nosotros ___ un ruido. (oír)", "oímos", "We hear a noise &middot; the í keeps its accent: oímos, oís", "A1::verbs A1::oir"),
    verb("Yo ___ en Madrid. (seguir)", "sigo", "I'm still in Madrid &middot; seguir + place = to still be there &middot; e &rarr; i: sigo", "A1::verbs A1::seguir"),
    verb("¿___ tú trabajando aquí? (seguir)", "Sigues", "Are you still working here? &middot; seguir + -ando/-iendo = to keep on doing", "A1::verbs A1::seguir"),
    verb("Ellos ___ el mismo camino. (seguir)", "siguen", "They follow the same road &middot; siguen, but seguimos with no change", "A1::verbs A1::seguir"),
    verb("Yo ___ un libro cada mes. (leer)", "leo", "I read a book every month &middot; cada mes = every month", "A1::verbs A1::leer"),
    verb("¿Qué ___ tú ahora? (leer)", "lees", "What are you reading now?", "A1::verbs A1::leer"),
    verb("Nosotros ___ el periódico. (leer)", "leemos", "We read the newspaper &middot; el periódico", "A1::verbs A1::leer"),

    verb("I run in the mornings.", "Corro por las mañanas.", "por las mañanas = in the mornings, as a habit", "A1::translation A1::correr"),
    verb("We swim in the sea in summer.", "Nadamos en el mar en verano.", "en verano = in summer, with no article", "A1::translation A1::nadar"),
    verb("I'll call you later.", "Te llamo luego.", "the present does the job of will here &middot; te goes before the verb", "A1::translation A1::llamar"),
    verb("I always arrive on time.", "Siempre llego a tiempo.", "a tiempo = on time &middot; a la hora also works", "A1::translation A1::llegar"),
    verb("I'm looking at the photos.", "Miro las fotos.", "mirar takes the object directly, with no a", "A1::translation A1::mirar"),
    verb("I don't think so.", "Creo que no.", "lit. I believe that no &middot; the opposite is creo que sí", "A1::translation A1::creer"),
    verb("I'm learning to cook.", "Aprendo a cocinar.", "aprender a + infinitive", "A1::translation A1::aprender"),
    verb("I can't hear you.", "No te oigo.", "no can needed: no te oigo says it", "A1::translation A1::oir"),
    verb("I keep studying every day.", "Sigo estudiando todos los días.", "seguir + gerund = to keep on doing", "A1::translation A1::seguir"),
    verb("I read before going to sleep.", "Leo antes de dormir.", "antes de + infinitive", "A1::translation A1::leer"),

    # ---- pasar / dejar / quedar / parecer / deber ------------------------
    # the five highest-frequency verbs the collection was missing; each is
    # worth cards for its idioms rather than for its conjugation
    verb("¿Qué ___? (pasar)", "pasa", "What's going on? &middot; ¿qué pasa? is the everyday phrase, and ¿qué te pasa? asks what's wrong", "A1::verbs A1::pasar"),
    verb("El autobús ___ por aquí. (pasar)", "pasa", "The bus comes by here &middot; pasar por = to pass by a place", "A1::verbs A1::pasar"),
    verb("Yo ___ el fin de semana en Madrid. (pasar)", "paso", "I spend the weekend in Madrid &middot; pasar = to spend time, never gastar, which is money", "A1::verbs A1::pasar"),
    verb("___ las llaves en la mesa. (dejar — yo)", "Dejo", "I leave the keys on the table &middot; dejar = leave something behind; salir = leave a place", "A1::verbs A1::dejar"),
    verb("Mi hermano ___ de fumar. (dejar)", "deja", "My brother is giving up smoking &middot; dejar de + infinitive = to stop doing something", "A1::verbs A1::dejar"),
    verb("¿___ mañana a las ocho? (quedar — nosotros)", "Quedamos", "Shall we meet tomorrow at eight? &middot; quedar = to arrange to meet, the normal way to make a plan", "A1::verbs A1::quedar"),
    verb("___ dos semanas para las vacaciones. (quedar)", "Quedan", "There are two weeks left until the holidays &middot; quedar = to be left, agreeing with the thing remaining", "A1::verbs A1::quedar"),
    verb("Esta noche yo me ___ en casa. (quedarse)", "quedo", "Tonight I'm staying at home &middot; quedarse = to stay, and the pronoun changes the meaning", "A1::verbs A1::quedar"),
    verb("Me ___ bien. (parecer)", "parece", "It seems fine to me &middot; parecer works backwards like gustar", "A1::verbs A1::parecer"),
    verb("¿Qué te ___ la película? (parecer)", "parece", "What do you think of the film? &middot; lit. how does it seem to you - the standard way to ask an opinion", "A1::verbs A1::parecer"),
    verb("Estas casas ___ nuevas. (parecer)", "parecen", "These houses look new &middot; a plural subject &rarr; parecen", "A1::verbs A1::parecer"),
    verb("___ estudiar más. (deber — yo)", "Debo", "I should study more &middot; deber + infinitive = ought to", "A1::verbs A1::deber"),
    verb("Me ___ diez euros. (deber — tú)", "debes", "You owe me ten euros &middot; deber with money is the literal sense", "A1::verbs A1::deber"),
    verb("No ___ llegar tarde. (deber — nosotros)", "debemos", "We mustn't arrive late", "A1::verbs A1::deber"),

    verb("Nothing's wrong.", "No pasa nada.", "also it doesn't matter / never mind - one of the most useful phrases in Spain", "A1::translation A1::pasar"),
    verb("My parents let me go out on Fridays.", "Mis padres me dejan salir los viernes.", "dejar + infinitive = to let someone do something", "A1::translation A1::dejar"),
    verb("We're meeting my friends on Saturday.", "Quedamos con mis amigos el sábado.", "quedar con + person &middot; no reflexive here", "A1::translation A1::quedar"),
    verb("You look tired.", "Pareces cansado.", "parecer + adjective = to look or seem &middot; cansada if you're female", "A1::translation A1::parecer"),
    verb("You should speak with the teacher.", "Debes hablar con el profesor.", "deber = advice; tener que = obligation", "A1::translation A1::deber"),
]


# Pretérito indefinido - the finished past. Same two card shapes as VERBS,
# tagged A2 because the tense sits a level above the rest of the collection.
PAST = [
    # ---- regular -ar -----------------------------------------------------
    verb("Ayer ___ con María. (hablar — yo)", "hablé", "Yesterday I spoke with María &middot; -ar yo: -é, and the stress lands on it", "A2::verbs A2::pasado A2::hablar"),
    verb("La semana pasada ___ mucho. (trabajar — nosotros)", "trabajamos", "Last week we worked a lot &middot; -ar nosotros is identical to the present: only the time word tells you which", "A2::verbs A2::pasado A2::trabajar"),
    verb("¿A qué hora ___ la clase ayer? (empezar)", "empezó", "What time did the class start yesterday? &middot; él: -ó, with the accent", "A2::verbs A2::pasado A2::empezar"),
    verb("Anoche ___ al fútbol. (jugar — yo)", "jugué", "Last night I played football &middot; g &rarr; gu before é, to keep the hard sound", "A2::verbs A2::pasado A2::jugar"),
    verb("Ayer ___ las llaves media hora. (buscar — yo)", "busqué", "Yesterday I looked for the keys for half an hour &middot; c &rarr; qu before é", "A2::verbs A2::pasado A2::buscar"),
    verb("El lunes ___ el piano. (tocar — yo)", "toqué", "On Monday I played the piano &middot; c &rarr; qu before é, same as busqué", "A2::verbs A2::pasado A2::tocar"),
    verb("¿___ tú el libro? (encontrar)", "encontraste", "Did you find the book? &middot; no stem change in the past: encontraste, never encuentraste", "A2::verbs A2::pasado A2::encontrar"),
    verb("Ellos ___ más tiempo. (necesitar)", "necesitaron", "They needed more time &middot; -ar ellos: -aron", "A2::verbs A2::pasado A2::necesitar"),
    verb("Yo ___ una camiseta negra. (llevar)", "llevé", "I wore a black T-shirt &middot; regular -ar", "A2::verbs A2::pasado A2::llevar"),
    verb("¿En qué ___ tú? (pensar)", "pensaste", "What were you thinking about? &middot; pensar loses its ie in the past: pensaste", "A2::verbs A2::pasado A2::pensar"),

    # ---- regular -er / -ir -----------------------------------------------
    verb("Ayer ___ paella. (comer — yo)", "comí", "Yesterday I ate paella &middot; -er/-ir yo: -í", "A2::verbs A2::pasado A2::comer"),
    verb("¿Qué ___ anoche? (beber — tú)", "bebiste", "What did you drink last night? &middot; -iste for tú, with no accent", "A2::verbs A2::pasado A2::beber"),
    verb("Ella ___ dos años en Sevilla. (vivir)", "vivió", "She lived in Seville for two years &middot; él: -ió", "A2::verbs A2::pasado A2::vivir"),
    verb("Nosotros ___ a casa tarde. (volver)", "volvimos", "We came home late &middot; volver drops its ue here: volvimos", "A2::verbs A2::pasado A2::volver"),
    verb("Ellos ___ de casa a las ocho. (salir)", "salieron", "They left home at eight &middot; -ieron for ellos", "A2::verbs A2::pasado A2::salir"),
    verb("Yo ___ el tren. (perder)", "perdí", "I missed the train &middot; perder is regular in the past: perdí", "A2::verbs A2::pasado A2::perder"),
    verb("Él ___ ocho horas. (dormir)", "durmió", "He slept for eight hours &middot; o &rarr; u in él and ellos only: durmió, durmieron", "A2::verbs A2::pasado A2::dormir"),
    verb("Ellos ___ la cuenta. (pedir)", "pidieron", "They asked for the bill &middot; e &rarr; i in él and ellos only: pidió, pidieron", "A2::verbs A2::pasado A2::pedir"),
    verb("¿___ vosotros el partido? (ver)", "visteis", "Did you all see the match? &middot; ver takes the plain endings with no accents", "A2::verbs A2::pasado A2::ver"),
    verb("Yo ___ a Ana en 2020. (conocer)", "conocí", "I met Ana in 2020 &middot; conocer in the past means met for the first time", "A2::verbs A2::pasado A2::conocer"),

    # ---- strong stems, unstressed endings ---------------------------------
    verb("Ayer ___ un examen. (tener — yo)", "tuve", "Yesterday I had an exam &middot; tuv- + e &middot; no accent: tuve, never tuvé", "A2::verbs A2::pasado A2::tener"),
    verb("Ella ___ que trabajar el domingo. (tener)", "tuvo", "She had to work on Sunday &middot; tuvo que + infinitive", "A2::verbs A2::pasado A2::tener"),
    verb("¿Dónde ___ tú anoche? (estar)", "estuviste", "Where were you last night? &middot; estuv- + iste", "A2::verbs A2::pasado A2::estar"),
    verb("Nosotros ___ tres días en Madrid. (estar)", "estuvimos", "We were in Madrid for three days &middot; a finished stretch of time &rarr; estar in the preterite", "A2::verbs A2::pasado A2::estar"),
    verb("Nosotros no ___ ir. (poder)", "pudimos", "We couldn't go &middot; pud- + imos", "A2::verbs A2::pasado A2::poder"),
    verb("Ellos ___ la verdad. (decir)", "dijeron", "They told the truth &middot; a j stem takes -eron, not -ieron: dijeron", "A2::verbs A2::pasado A2::decir"),
    verb("¿Qué ___ el sábado? (hacer — tú)", "hiciste", "What did you do on Saturday? &middot; hic- + iste", "A2::verbs A2::pasado A2::hacer"),
    verb("Él ___ la cena anoche. (hacer)", "hizo", "He made dinner last night &middot; c &rarr; z in él only: hizo", "A2::verbs A2::pasado A2::hacer"),
    verb("Ella ___ la mesa. (poner)", "puso", "She set the table &middot; pus- + o, with no accent", "A2::verbs A2::pasado A2::poner"),
    verb("Mis amigos ___ a la fiesta. (venir)", "vinieron", "My friends came to the party &middot; vin- + ieron", "A2::verbs A2::pasado A2::venir"),
    verb("Yo no ___ nada de eso. (saber)", "supe", "I didn't know any of that &middot; sup- + e &middot; in the past supe often means I found out", "A2::verbs A2::pasado A2::saber"),
    verb("Él ___ el postre. (traer)", "trajo", "He brought the dessert &middot; traj- + o &middot; ellos: trajeron, not trajieron", "A2::verbs A2::pasado A2::traer"),
    verb("Yo ___ ir, pero no pude. (querer)", "quise", "I wanted to go, but I couldn't &middot; quis- + e", "A2::verbs A2::pasado A2::querer"),
    verb("___ mucha gente en la fiesta. (haber)", "Hubo", "There were a lot of people at the party &middot; hubo is the past of hay, and never goes plural", "A2::verbs A2::pasado A2::haber"),

    # ---- ser, ir, ver, dar, gustar ---------------------------------------
    verb("Ayer ___ un día perfecto. (ser)", "fue", "Yesterday was a perfect day &middot; ser: fui, fuiste, fue", "A2::verbs A2::pasado A2::ser"),
    verb("El año pasado ___ a México. (ir — nosotros)", "fuimos", "Last year we went to Mexico &middot; ser and ir share this form; only the sentence tells you which", "A2::verbs A2::pasado A2::ir"),
    verb("¿Cuándo ___ tú a España? (ir)", "fuiste", "When did you go to Spain? &middot; fuiste is both you went and you were", "A2::verbs A2::pasado A2::ir"),
    verb("Yo ___ la televisión anoche. (ver)", "vi", "I watched TV last night &middot; vi, with no accent - one syllable needs none", "A2::verbs A2::pasado A2::ver"),
    verb("Mi padre me ___ un libro. (dar)", "dio", "My father gave me a book &middot; dar borrows the -er endings: di, diste, dio", "A2::verbs A2::pasado A2::dar"),
    verb("Me ___ mucho la película. (gustar)", "gustó", "I really liked the film &middot; me gustó + one thing", "A2::verbs A2::pasado A2::gustar"),
    verb("Nos ___ mucho las tapas. (gustar)", "gustaron", "We really liked the tapas &middot; a plural thing &rarr; gustaron", "A2::verbs A2::pasado A2::gustar"),

    # ---- EN -> ES --------------------------------------------------------
    verb("Yesterday I worked from home.", "Ayer trabajé desde casa.", "ayer marks a finished moment &rarr; preterite", "A2::translation A2::pasado A2::trabajar"),
    verb("Last night we ate at a restaurant.", "Anoche comimos en un restaurante.", "anoche = last night", "A2::translation A2::pasado A2::comer"),
    verb("Last week I saw my friends.", "La semana pasada vi a mis amigos.", "la semana pasada &middot; the personal a before people", "A2::translation A2::pasado A2::ver"),
    verb("Last year they went to Spain.", "El año pasado fueron a España.", "fueron = they went, and also they were", "A2::translation A2::pasado A2::ir"),
    verb("What did you do yesterday?", "¿Qué hiciste ayer?", "no helper verb: the past is in hiciste alone", "A2::translation A2::pasado A2::hacer"),
    verb("I couldn't come.", "No pude venir.", "pude + infinitive &middot; no goes before the verb", "A2::translation A2::pasado A2::poder"),
    verb("She told me the truth.", "Me dijo la verdad.", "me dijo = she told me &middot; the pronoun still comes first", "A2::translation A2::pasado A2::decir"),
    verb("They had a problem.", "Tuvieron un problema.", "tuv- + ieron &middot; problema is masculine", "A2::translation A2::pasado A2::tener"),
    verb("It was a very good day.", "Fue un día muy bueno.", "fue for a finished whole: the day is over", "A2::translation A2::pasado A2::ser"),
    verb("I met my wife in 2015.", "Conocí a mi mujer en 2015.", "conocí = I met (for the first time)", "A2::translation A2::pasado A2::conocer"),
    verb("We got up early.", "Nos levantamos temprano.", "the reflexive pronoun stays in front: nos levantamos", "A2::translation A2::pasado A2::reflexivos"),
    verb("Did you like the food?", "¿Te gustó la comida?", "te gustó + one thing", "A2::translation A2::pasado A2::gustar"),
    verb("I gave him the keys.", "Le di las llaves.", "le = to him &middot; di, with no accent", "A2::translation A2::pasado A2::dar"),
    verb("Two years ago I lived in Barcelona.", "Hace dos años viví en Barcelona.", "hace + time = ago", "A2::translation A2::pasado A2::vivir"),
    verb("He came home late.", "Volvió a casa tarde.", "volvió, not vuelvió", "A2::translation A2::pasado A2::volver"),
    verb("I started work at eight.", "Empecé a trabajar a las ocho.", "z &rarr; c before é: empecé", "A2::translation A2::pasado A2::empezar"),
    verb("They asked for the bill.", "Pidieron la cuenta.", "pedir: pidió, pidieron in the third person", "A2::translation A2::pasado A2::pedir"),
    verb("I played tennis on Saturday.", "Jugué al tenis el sábado.", "jugué &middot; jugar a + sport", "A2::translation A2::pasado A2::jugar"),
    verb("We slept very well.", "Dormimos muy bien.", "dormimos is both we sleep and we slept", "A2::translation A2::pasado A2::dormir"),
    verb("I was at home all day.", "Estuve en casa todo el día.", "a finished stretch &rarr; estuve &middot; todo el día = all day", "A2::translation A2::pasado A2::estar"),

    # ---- the ten everyday verbs in the past -------------------------------
    verb("Ayer ___ diez kilómetros. (correr — yo)", "corrí", "Yesterday I ran ten kilometres &middot; regular -er: corrí", "A2::verbs A2::pasado A2::correr"),
    verb("El verano pasado ___ mucho. (nadar — yo)", "nadé", "Last summer I swam a lot &middot; regular -ar: nadé", "A2::verbs A2::pasado A2::nadar"),
    verb("Ayer te ___ tres veces. (llamar — yo)", "llamé", "I called you three times yesterday &middot; tres veces = three times", "A2::verbs A2::pasado A2::llamar"),
    verb("Yo ___ tarde a la reunión. (llegar)", "llegué", "I arrived late to the meeting &middot; g &rarr; gu before é: llegué", "A2::verbs A2::pasado A2::llegar"),
    verb("¿A qué hora ___ vosotros? (llegar)", "llegasteis", "What time did you all arrive? &middot; only the yo form changes its spelling", "A2::verbs A2::pasado A2::llegar"),
    verb("Ellos ___ las fotos toda la tarde. (mirar)", "miraron", "They looked at the photos all afternoon &middot; regular -ar: miraron", "A2::verbs A2::pasado A2::mirar"),
    verb("Nadie ___ mi historia. (creer)", "creyó", "Nobody believed my story &middot; i &rarr; y between vowels: creyó, creyeron", "A2::verbs A2::pasado A2::creer"),
    verb("Nosotros no ___ nada. (creer)", "creímos", "We didn't believe any of it &middot; the í keeps its accent: creí, creímos", "A2::verbs A2::pasado A2::creer"),
    verb("Yo ___ mucho en España. (aprender)", "aprendí", "I learnt a lot in Spain &middot; regular -er", "A2::verbs A2::pasado A2::aprender"),
    verb("¿___ tú el ruido anoche? (oír)", "Oíste", "Did you hear the noise last night? &middot; oíste, with the accent", "A2::verbs A2::pasado A2::oir"),
    verb("Ellos no ___ nada. (oír)", "oyeron", "They didn't hear anything &middot; i &rarr; y: oyó, oyeron", "A2::verbs A2::pasado A2::oir"),
    verb("Él ___ estudiando en Madrid. (seguir)", "siguió", "He kept studying in Madrid &middot; e &rarr; i in él and ellos: siguió, siguieron", "A2::verbs A2::pasado A2::seguir"),
    verb("Yo ___ dos libros el mes pasado. (leer)", "leí", "I read two books last month &middot; leí, with the accent", "A2::verbs A2::pasado A2::leer"),
    verb("Ella ___ la carta dos veces. (leer)", "leyó", "She read the letter twice &middot; leyó, leyeron with a y", "A2::verbs A2::pasado A2::leer"),

    verb("I ran five kilometres yesterday.", "Ayer corrí cinco kilómetros.", "ayer + preterite", "A2::translation A2::pasado A2::correr"),
    verb("She called me last night.", "Anoche me llamó.", "me llamó &middot; the pronoun stays before the verb", "A2::translation A2::pasado A2::llamar"),
    verb("They arrived late.", "Llegaron tarde.", "llegaron &middot; only llegué changes its spelling", "A2::translation A2::pasado A2::llegar"),
    verb("I read that book last year.", "Leí ese libro el año pasado.", "leí = I read (past) &middot; leo = I read (present)", "A2::translation A2::pasado A2::leer"),
]


# Vocabulary mined from a documentary, to drill the day before watching it.
# Comprehension direction on purpose: these words arrive through the ears.
# Counts are how often each word is spoken in the film.
VIDEO_LEONES = [
    sentence("la manada", "the pride (of lions)", "also a herd of buffalo or a pack of wolves &middot; the most repeated noun in the film, said about 23 times", "video::leones"),
    sentence("el macho / la hembra", "the male / the female", "el macho stays masculine even for a female animal's mate", "video::leones"),
    sentence("el cachorro", "the cub", "also a puppy &middot; los cachorros", "video::leones"),
    sentence("el león / la leona", "the lion / the lioness", "león drops its accent in the plural: los leones", "video::leones"),
    sentence("el búfalo", "the buffalo", "stressed on the first syllable, hence the accent", "video::leones"),
    sentence("la jirafa", "the giraffe", "the j sounds like the ch in Scottish loch", "video::leones"),
    sentence("el toro", "the bull", "la vaca = cow", "video::leones"),
    sentence("el bosque", "the woods, the forest", "la selva = jungle &middot; el bosque is temperate woodland", "video::leones"),
    sentence("el territorio", "the territory", "the film's theme: whose land this is", "video::leones"),
    sentence("la caza", "the hunt, hunting", "cazar = to hunt &middot; el cazador = hunter", "video::leones"),
    sentence("la sangre", "blood", "feminine despite the -e ending", "video::leones"),
    sentence("el peligro", "the danger", "peligroso = dangerous &middot; ¡peligro! on a sign", "video::leones"),
    sentence("la sombra", "the shade, the shadow", "one word for both &middot; a la sombra = in the shade", "video::leones"),
    sentence("la naturaleza", "nature", "la naturaleza, always with the article", "video::leones"),
    sentence("la supervivencia", "survival", "sobrevivir = to survive", "video::leones"),
    sentence("la generación", "the generation", "every -ción noun is feminine", "video::leones"),
    sentence("el líder", "the leader", "la líder for a woman &middot; liderar = to lead", "video::leones"),
    sentence("exiliado", "exiled, an exile", "el exiliado &middot; a lion driven out of its pride", "video::leones"),
    sentence("el adulto / el adolescente", "the adult / the adolescent", "both work as nouns and adjectives", "video::leones"),
    sentence("la oportunidad", "the opportunity, the chance", "every -dad noun is feminine", "video::leones"),
    sentence("fuerte", "strong", "one form for both genders &middot; fuertes in the plural", "video::leones"),
    sentence("mantenerse", "to keep, to stay (in a state)", "mantener = to maintain &middot; mantenerse fuerte = to keep strong", "video::leones"),
    sentence("la vida", "life", "also on the word bank: la vida, toda la vida = all your life", "video::leones"),
    sentence("la manera", "the way, the manner", "de esta manera = this way &middot; also on the word bank", "video::leones"),
    sentence("último", "last, final", "el último = the last one &middot; also on the word bank", "video::leones"),

    # second tier: everything else said more than once in the film
    sentence("el río", "the river", "also on the word bank &middot; los ríos", "video::leones"),
    sentence("los carroñeros", "the scavengers", "la carroña = carrion &middot; hyenas and vultures in this film", "video::leones"),
    sentence("los rivales", "the rivals", "la rivalidad = rivalry &middot; it is in the film's title", "video::leones"),
    sentence("la prueba", "the test, the proof", "poner a prueba = to put to the test", "video::leones"),
    sentence("la fuerza", "the strength, the force", "fuerte = strong &middot; a la fuerza = by force", "video::leones"),
    sentence("el miedo", "the fear", "tener miedo = to be afraid, with tener, never estar", "video::leones"),
    sentence("la muerte", "the death", "morir = to die &middot; muerto = dead", "video::leones"),
    sentence("las heridas", "the wounds, the injuries", "herido = wounded &middot; herir = to wound", "video::leones"),
    sentence("la seguridad", "the safety, the security", "seguro = safe, and also sure", "video::leones"),
    sentence("el rastro", "the trail, the track", "seguir el rastro = to follow the trail", "video::leones"),
    sentence("la señal", "the sign, the signal", "feminine despite the consonant ending &middot; las señales", "video::leones"),
    sentence("la compañía", "the company, the companionship", "el compañero = companion, the word for a colleague too", "video::leones"),
    sentence("la temporada", "the season, the period", "a stretch of time, not a season of the year, which is la estación", "video::leones"),
    sentence("la arena", "the sand", "also the sand of an arena - the English word comes from this", "video::leones"),
    sentence("la energía", "the energy", "the g sounds like the j of jirafa", "video::leones"),
    sentence("el resto", "the rest, the remainder", "el resto de la manada = the rest of the pride", "video::leones"),
    sentence("solitario", "solitary, lone", "el solitario = a loner &middot; solo = alone", "video::leones"),
    sentence("hambriento", "hungry, starving", "stronger than tener hambre &middot; el hambre = hunger", "video::leones"),
    sentence("prohibido", "forbidden", "prohibir = to forbid &middot; prohibido on a sign = no entry", "video::leones"),
    sentence("valiente", "brave", "one form for both genders, like fuerte", "video::leones"),
    sentence("unirse", "to join, to band together", "unir = to unite &middot; unirse a la manada", "video::leones"),
    sentence("gran", "great, big (before a noun)", "grande shortens to gran before any singular noun: un gran macho, una gran manada", "video::leones"),
]


VOCAB = [
    # ---- numbers ---------------------------------------------------------
    vocab("I have two brothers.", "Tengo dos hermanos.", "dos = two", "A1::vocab A1::numeros"),
    vocab("There are three rooms in the house.", "Hay tres habitaciones en la casa.", "hay = there is / there are (never changes)", "A1::vocab A1::numeros"),
    vocab("The coffee costs one euro.", "El café cuesta un euro.", "uno drops to un before a masculine noun", "A1::vocab A1::numeros"),
    vocab("I work eight hours a day.", "Trabajo ocho horas al día.", "al día = per day", "A1::vocab A1::numeros"),
    vocab("My sister is twenty years old.", "Mi hermana tiene veinte años.", "age uses tener, not ser", "A1::vocab A1::numeros"),
    vocab("I live on the fourth floor.", "Vivo en el cuarto piso.", "cuarto = fourth (ordinal)", "A1::vocab A1::numeros"),
    vocab("The book has one hundred pages.", "El libro tiene cien páginas.", "cien before a noun, ciento in 101-199", "A1::vocab A1::numeros"),
    vocab("I need five minutes.", "Necesito cinco minutos.", "cinco = five", "A1::vocab A1::numeros"),
    vocab("There are seven days in a week.", "Hay siete días en una semana.", "el día is masculine despite the -a", "A1::vocab A1::numeros"),
    vocab("It costs thirty-five euros.", "Cuesta treinta y cinco euros.", "31-99 are written as three words: treinta y cinco", "A1::vocab A1::numeros"),
    vocab("There are four of us at home.", "Somos cuatro en casa.", "somos cuatro = lit. we are four", "A1::vocab A1::numeros"),
    vocab("I buy a dozen eggs.", "Compro una docena de huevos.", "una docena de = a dozen", "A1::vocab A1::numeros"),
    vocab("I have ten fingers.", "Tengo diez dedos.", "diez = ten", "A1::vocab A1::numeros"),
    vocab("There are twelve months in a year.", "Hay doce meses en un año.", "doce = twelve", "A1::vocab A1::numeros"),
    vocab("The room number is two hundred.", "La habitación es la doscientos.", "numbering keeps the article: la doscientos", "A1::vocab A1::numeros"),

    # ---- days, months, time ---------------------------------------------
    vocab("Today is Monday.", "Hoy es lunes.", "weekdays are lowercase in Spanish", "A1::vocab A1::tiempo"),
    vocab("Tomorrow is Tuesday.", "Mañana es martes.", "mañana = tomorrow (and also 'morning')", "A1::vocab A1::tiempo"),
    vocab("I work from Monday to Friday.", "Trabajo de lunes a viernes.", "de ... a ... = from ... to ...", "A1::vocab A1::tiempo"),
    vocab("On Saturdays I don't work.", "Los sábados no trabajo.", "los + day = habitually, every ...", "A1::vocab A1::tiempo"),
    vocab("Sunday is my favorite day.", "El domingo es mi día favorito.", "el domingo = on Sunday / Sunday (specific)", "A1::vocab A1::tiempo"),
    vocab("My birthday is in January.", "Mi cumpleaños es en enero.", "months are lowercase too", "A1::vocab A1::tiempo"),
    vocab("In August we go on vacation.", "En agosto vamos de vacaciones.", "ir de vacaciones = to go on holiday", "A1::vocab A1::tiempo"),
    vocab("It's three o'clock.", "Son las tres.", "plural son for 2 o'clock onward", "A1::vocab A1::tiempo"),
    vocab("It's one o'clock.", "Es la una.", "only 1 o'clock takes singular es la", "A1::vocab A1::tiempo"),
    vocab("It's half past seven.", "Son las siete y media.", "y media = half past", "A1::vocab A1::tiempo"),
    vocab("It's a quarter to nine.", "Son las nueve menos cuarto.", "menos cuarto = quarter to", "A1::vocab A1::tiempo"),
    vocab("The train leaves at ten in the morning.", "El tren sale a las diez de la mañana.", "de la mañana with a stated hour; por la mañana on its own", "A1::vocab A1::tiempo"),
    vocab("I have lunch at two in the afternoon.", "Como a las dos de la tarde.", "comer = both 'to eat' and 'to have lunch' in Spain", "A1::vocab A1::tiempo"),
    vocab("I go to bed at eleven at night.", "Me acuesto a las once de la noche.", "acostarse is reflexive: me acuesto", "A1::vocab A1::tiempo"),
    vocab("What time is it?", "¿Qué hora es?", "always singular qué hora es", "A1::vocab A1::tiempo"),
    vocab("Today is the fifteenth of May.", "Hoy es quince de mayo.", "dates use plain numbers, not ordinals", "A1::vocab A1::tiempo"),
    vocab("Next week I travel to Madrid.", "La semana que viene viajo a Madrid.", "la semana que viene = next week", "A1::vocab A1::tiempo"),
    vocab("I always arrive early.", "Siempre llego temprano.", "siempre goes before the verb", "A1::vocab A1::tiempo"),
    vocab("Sometimes I arrive late.", "A veces llego tarde.", "a veces = sometimes", "A1::vocab A1::tiempo"),
    vocab("Right now I'm busy.", "Ahora mismo estoy ocupado.", "ahora mismo = right now", "A1::vocab A1::tiempo"),

    # ---- family ----------------------------------------------------------
    vocab("My mother is a teacher.", "Mi madre es profesora.", "no article before a profession after ser", "A1::vocab A1::familia"),
    vocab("My father works in an office.", "Mi padre trabaja en una oficina.", "trabajar en = to work at", "A1::vocab A1::familia"),
    vocab("I have an older sister.", "Tengo una hermana mayor.", "mayor = older (not 'más viejo' for people)", "A1::vocab A1::familia"),
    vocab("My younger brother is twelve.", "Mi hermano menor tiene doce años.", "menor = younger", "A1::vocab A1::familia"),
    vocab("My grandparents live in the countryside.", "Mis abuelos viven en el campo.", "abuelos = grandparents (mixed group takes masculine plural)", "A1::vocab A1::familia"),
    vocab("My grandmother cooks very well.", "Mi abuela cocina muy bien.", "muy bien = very well", "A1::vocab A1::familia"),
    vocab("My son goes to school.", "Mi hijo va al colegio.", "a + el = al", "A1::vocab A1::familia"),
    vocab("My daughter is three years old.", "Mi hija tiene tres años.", "tener ... años for age", "A1::vocab A1::familia"),
    vocab("My wife works at a hospital.", "Mi mujer trabaja en un hospital.", "mujer or esposa = wife", "A1::vocab A1::familia"),
    vocab("My husband speaks English.", "Mi marido habla inglés.", "marido or esposo = husband", "A1::vocab A1::familia"),
    vocab("I have two cousins in Mexico.", "Tengo dos primos en México.", "primos = cousins", "A1::vocab A1::familia"),
    vocab("My aunt and uncle live in Seville.", "Mis tíos viven en Sevilla.", "tíos covers 'aunt and uncle' together", "A1::vocab A1::familia"),
    vocab("My family is very big.", "Mi familia es muy grande.", "familia is singular in Spanish", "A1::vocab A1::familia"),
    vocab("I live with my parents.", "Vivo con mis padres.", "padres = parents; padre = father", "A1::vocab A1::familia"),
    vocab("My nephew is a baby.", "Mi sobrino es un bebé.", "sobrino = nephew, sobrina = niece", "A1::vocab A1::familia"),
    vocab("Do you have children?", "¿Tienes hijos?", "no article in this kind of yes/no question", "A1::vocab A1::familia"),
    vocab("My girlfriend is Spanish.", "Mi novia es española.", "nationalities are lowercase", "A1::vocab A1::familia"),
    vocab("I don't have any siblings.", "No tengo hermanos.", "plural hermanos with no article = any siblings", "A1::vocab A1::familia"),

    # ---- food and drink --------------------------------------------------
    vocab("I drink coffee every morning.", "Bebo café todas las mañanas.", "todas las mañanas = every morning", "A1::vocab A1::comida"),
    vocab("I want a glass of water.", "Quiero un vaso de agua.", "un vaso de = a glass of", "A1::vocab A1::comida"),
    vocab("I'm having breakfast now.", "Estoy desayunando ahora.", "estar + -ando = right now", "A1::vocab A1::comida"),
    vocab("We have lunch at two.", "Comemos a las dos.", "comer at midday = to have lunch", "A1::vocab A1::comida"),
    vocab("I have dinner with my family.", "Ceno con mi familia.", "cenar = to have dinner", "A1::vocab A1::comida"),
    vocab("The bread is fresh.", "El pan está fresco.", "estar for a current condition of food", "A1::vocab A1::comida"),
    vocab("I'd like a beer, please.", "Quiero una cerveza, por favor.", "quiero is the normal polite order in Spain", "A1::vocab A1::comida"),
    vocab("I don't eat meat.", "No como carne.", "la carne = meat", "A1::vocab A1::comida"),
    vocab("The fish is delicious.", "El pescado está delicioso.", "pescado = fish as food, pez = live fish", "A1::vocab A1::comida"),
    vocab("I like fruit a lot.", "Me gusta mucho la fruta.", "gustar takes the definite article: la fruta", "A1::vocab A1::comida"),
    vocab("I buy vegetables at the market.", "Compro verduras en el mercado.", "verduras = vegetables", "A1::vocab A1::comida"),
    vocab("Can you pass me the salt?", "¿Me pasas la sal?", "present tense as a polite request", "A1::vocab A1::comida"),
    vocab("The soup is very hot.", "La sopa está muy caliente.", "caliente = hot to the touch", "A1::vocab A1::comida"),
    vocab("I prefer tea.", "Prefiero el té.", "preferir: e -> ie in yo/tú/él", "A1::vocab A1::comida"),
    vocab("I need milk and eggs.", "Necesito leche y huevos.", "la leche, el huevo", "A1::vocab A1::comida"),
    vocab("The restaurant is closed.", "El restaurante está cerrado.", "estar for a temporary state", "A1::vocab A1::comida"),
    vocab("The chicken with rice is very good.", "El pollo con arroz está muy bueno.", "está bueno = tastes good; es bueno = is good quality", "A1::vocab A1::comida"),
    vocab("I eat a sandwich for lunch.", "Como un bocadillo al mediodía.", "bocadillo = baguette sandwich (Spain) &middot; al mediodía = at midday", "A1::vocab A1::comida"),
    vocab("Do you want dessert?", "¿Quieres postre?", "el postre = dessert", "A1::vocab A1::comida"),
    vocab("The cheese is from Spain.", "El queso es de España.", "ser de = origin", "A1::vocab A1::comida"),
    vocab("I don't drink alcohol.", "No bebo alcohol.", "beber or tomar = to drink", "A1::vocab A1::comida"),
    vocab("We cook at home every day.", "Cocinamos en casa todos los días.", "en casa without an article = at home", "A1::vocab A1::comida"),
    vocab("I'm hungry.", "Tengo hambre.", "hunger uses tener, not ser/estar", "A1::vocab A1::comida"),
    vocab("I'm thirsty.", "Tengo sed.", "tener sed = to be thirsty", "A1::vocab A1::comida"),
    vocab("The bill, please.", "La cuenta, por favor.", "la cuenta = the bill", "A1::vocab A1::comida"),

    # ---- home ------------------------------------------------------------
    vocab("I live in a small apartment.", "Vivo en un piso pequeño.", "piso = apartment in Spain", "A1::vocab A1::casa"),
    vocab("My house has three bedrooms.", "Mi casa tiene tres dormitorios.", "dormitorio or habitación = bedroom", "A1::vocab A1::casa"),
    vocab("The kitchen is very bright.", "La cocina es muy luminosa.", "ser for a permanent quality of a room", "A1::vocab A1::casa"),
    vocab("There's a table in the living room.", "Hay una mesa en el salón.", "hay + indefinite article", "A1::vocab A1::casa"),
    vocab("The bathroom is at the end of the hallway.", "El baño está al final del pasillo.", "de + el = del", "A1::vocab A1::casa"),
    vocab("I put the keys on the table.", "Pongo las llaves en la mesa.", "poner: yo pongo (irregular)", "A1::vocab A1::casa"),
    vocab("The window is open.", "La ventana está abierta.", "estar + participle for a resulting state", "A1::vocab A1::casa"),
    vocab("Please close the door.", "Cierra la puerta, por favor.", "cierra = informal command from cerrar", "A1::vocab A1::casa"),
    vocab("My bed is very comfortable.", "Mi cama es muy cómoda.", "cómodo/cómoda = comfortable", "A1::vocab A1::casa"),
    vocab("I clean the house on Saturdays.", "Limpio la casa los sábados.", "limpiar = to clean", "A1::vocab A1::casa"),
    vocab("The fridge is empty.", "La nevera está vacía.", "nevera (Spain) / refrigerador (Latin America)", "A1::vocab A1::casa"),
    vocab("I wash the dishes after dinner.", "Lavo los platos después de la cena.", "después de = after", "A1::vocab A1::casa"),
    vocab("There are two chairs in the kitchen.", "Hay dos sillas en la cocina.", "la silla = chair", "A1::vocab A1::casa"),
    vocab("I watch TV on the sofa.", "Veo la tele en el sofá.", "la tele = TV (short for televisión)", "A1::vocab A1::casa"),
    vocab("The light doesn't work.", "La luz no funciona.", "funcionar = to work (of machines)", "A1::vocab A1::casa"),
    vocab("My room is on the second floor.", "Mi habitación está en el segundo piso.", "estar for location", "A1::vocab A1::casa"),
    vocab("We have a small garden.", "Tenemos un jardín pequeño.", "adjectives normally follow the noun", "A1::vocab A1::casa"),
    vocab("I'm looking for my phone.", "Busco mi móvil.", "buscar already means 'look for' - no preposition", "A1::vocab A1::casa"),
    vocab("The rent is very expensive.", "El alquiler es muy caro.", "el alquiler = rent", "A1::vocab A1::casa"),
    vocab("I live near the center.", "Vivo cerca del centro.", "cerca de = near", "A1::vocab A1::casa"),
    vocab("The building has an elevator.", "El edificio tiene ascensor.", "no article after tener in this pattern", "A1::vocab A1::casa"),
    vocab("I put my clothes in the closet.", "Pongo la ropa en el armario.", "la ropa is singular and uncountable", "A1::vocab A1::casa"),

    # ---- work and studies ------------------------------------------------
    vocab("I work in an office.", "Trabajo en una oficina.", "trabajar en = to work in", "A1::vocab A1::trabajo"),
    vocab("I'm a programmer.", "Soy programador.", "no un/una before a profession", "A1::vocab A1::trabajo"),
    vocab("I study Spanish.", "Estudio español.", "languages are lowercase", "A1::vocab A1::trabajo"),
    vocab("I have a meeting at ten.", "Tengo una reunión a las diez.", "la reunión = meeting", "A1::vocab A1::trabajo"),
    vocab("My boss is very nice.", "Mi jefe es muy simpático.", "simpático = nice/friendly (not 'sympathetic')", "A1::vocab A1::trabajo"),
    vocab("I start work at nine.", "Empiezo a trabajar a las nueve.", "empezar a + infinitive", "A1::vocab A1::trabajo"),
    vocab("I work from home.", "Trabajo desde casa.", "desde = from", "A1::vocab A1::trabajo"),
    vocab("I need to finish this today.", "Necesito terminar esto hoy.", "necesitar + infinitive, no preposition", "A1::vocab A1::trabajo"),
    vocab("My colleagues speak English.", "Mis compañeros hablan inglés.", "compañero de trabajo = colleague", "A1::vocab A1::trabajo"),
    vocab("I go to class twice a week.", "Voy a clase dos veces por semana.", "dos veces por semana = twice a week", "A1::vocab A1::trabajo"),
    vocab("My teacher is from Argentina.", "Mi profesora es de Argentina.", "ser de for origin", "A1::vocab A1::trabajo"),
    vocab("I have a lot of work.", "Tengo mucho trabajo.", "mucho agrees with the noun it modifies", "A1::vocab A1::trabajo"),
    vocab("I don't work on weekends.", "No trabajo los fines de semana.", "fin de semana pluralises the first word", "A1::vocab A1::trabajo"),
    vocab("I'm learning Spanish.", "Estoy aprendiendo español.", "estar + gerund for in-progress action", "A1::vocab A1::trabajo"),
    vocab("I write emails every day.", "Escribo correos todos los días.", "correo = email (Spain)", "A1::vocab A1::trabajo"),
    vocab("The office is closed today.", "La oficina está cerrada hoy.", "cerrada agrees with oficina", "A1::vocab A1::trabajo"),
    vocab("I want to change jobs.", "Quiero cambiar de trabajo.", "cambiar de = to change (one's) ...", "A1::vocab A1::trabajo"),
    vocab("I take notes in class.", "Tomo apuntes en clase.", "apuntes = class notes", "A1::vocab A1::trabajo"),
    vocab("I have an exam on Friday.", "Tengo un examen el viernes.", "el viernes = on Friday", "A1::vocab A1::trabajo"),
    vocab("What do you do for a living?", "¿A qué te dedicas?", "dedicarse a = to do for a living", "A1::vocab A1::trabajo"),

    # ---- travel ----------------------------------------------------------
    vocab("I'm traveling to Spain in June.", "Viajo a España en junio.", "present tense covers near-future plans", "A1::vocab A1::viajes"),
    vocab("Where's the train station?", "¿Dónde está la estación de tren?", "estar for location", "A1::vocab A1::viajes"),
    vocab("I'd like a ticket to Barcelona.", "Quiero un billete para Barcelona.", "billete (Spain) / boleto (Latin America)", "A1::vocab A1::viajes"),
    vocab("The plane leaves at six.", "El avión sale a las seis.", "salir = to leave/depart", "A1::vocab A1::viajes"),
    vocab("I'm staying at a hotel.", "Me quedo en un hotel.", "quedarse = to stay", "A1::vocab A1::viajes"),
    vocab("How much does the room cost?", "¿Cuánto cuesta la habitación?", "costar: o -> ue", "A1::vocab A1::viajes"),
    vocab("I don't have a reservation.", "No tengo reserva.", "reserva = booking", "A1::vocab A1::viajes"),
    vocab("Is there a bus to the airport?", "¿Hay un autobús al aeropuerto?", "hay for existence", "A1::vocab A1::viajes"),
    vocab("I'm lost.", "Estoy perdido.", "estar perdida if you're female", "A1::vocab A1::viajes"),
    vocab("Can you help me?", "¿Me puedes ayudar?", "me goes before the conjugated verb", "A1::vocab A1::viajes"),
    vocab("The beach is far from here.", "La playa está lejos de aquí.", "lejos de = far from", "A1::vocab A1::viajes"),
    vocab("Turn right at the corner.", "Gira a la derecha en la esquina.", "a la derecha = to the right", "A1::vocab A1::viajes"),
    vocab("It's on the left.", "Está a la izquierda.", "a la izquierda = on the left", "A1::vocab A1::viajes"),
    vocab("Go straight ahead.", "Sigue todo recto.", "todo recto = straight on", "A1::vocab A1::viajes"),
    vocab("I go on foot.", "Voy a pie.", "a pie = on foot", "A1::vocab A1::viajes"),
    vocab("I take the metro every day.", "Cojo el metro todos los días.", "coger (Spain); use tomar in Latin America", "A1::vocab A1::viajes"),
    vocab("My suitcase is very heavy.", "Mi maleta es muy pesada.", "la maleta = suitcase", "A1::vocab A1::viajes"),
    vocab("I need a map.", "Necesito un mapa.", "el mapa is masculine despite the -a", "A1::vocab A1::viajes"),
    vocab("Do you speak English?", "¿Hablas inglés?", "informal tú form", "A1::vocab A1::viajes"),
    vocab("I don't understand.", "No entiendo.", "entender: e -> ie", "A1::vocab A1::viajes"),
    vocab("Can you repeat, please?", "¿Puedes repetir, por favor?", "poder + infinitive", "A1::vocab A1::viajes"),
    vocab("I'm on vacation.", "Estoy de vacaciones.", "estar de vacaciones = to be on holiday", "A1::vocab A1::viajes"),

    # ---- hobbies ---------------------------------------------------------
    vocab("I like to read.", "Me gusta leer.", "gustar + infinitive stays singular", "A1::vocab A1::ocio"),
    vocab("I play football on Sundays.", "Juego al fútbol los domingos.", "jugar a + sport", "A1::vocab A1::ocio"),
    vocab("I listen to music while I work.", "Escucho música mientras trabajo.", "escuchar needs no 'to'", "A1::vocab A1::ocio"),
    vocab("We watch a movie on Friday.", "Vemos una película el viernes.", "ver = to watch/see", "A1::vocab A1::ocio"),
    vocab("I run in the park.", "Corro en el parque.", "correr = to run", "A1::vocab A1::ocio"),
    vocab("I don't like dancing.", "No me gusta bailar.", "the infinitive translates the English -ing here", "A1::vocab A1::ocio"),
    vocab("My friends play guitar.", "Mis amigos tocan la guitarra.", "tocar for instruments, jugar for games", "A1::vocab A1::ocio"),
    vocab("I swim twice a week.", "Nado dos veces por semana.", "nadar = to swim", "A1::vocab A1::ocio"),
    vocab("I like traveling a lot.", "Me gusta mucho viajar.", "mucho goes after gusta", "A1::vocab A1::ocio"),
    vocab("We go to the movies on Saturday.", "Vamos al cine el sábado.", "el cine = the cinema", "A1::vocab A1::ocio"),
    vocab("I take photos with my phone.", "Hago fotos con el móvil.", "hacer fotos = to take photos", "A1::vocab A1::ocio"),
    vocab("I go for a walk in the evening.", "Doy un paseo por la tarde.", "dar un paseo = to take a walk", "A1::vocab A1::ocio"),
    vocab("I like cooking.", "Me gusta cocinar.", "cocinar = to cook", "A1::vocab A1::ocio"),
    vocab("I play video games.", "Juego a los videojuegos.", "jugar a + los videojuegos", "A1::vocab A1::ocio"),
    vocab("Do you want to go out tonight?", "¿Quieres salir esta noche?", "esta noche = tonight", "A1::vocab A1::ocio"),
    vocab("I go to the gym in the morning.", "Voy al gimnasio por la mañana.", "por la mañana with no stated hour", "A1::vocab A1::ocio"),
    vocab("We meet at the cafe.", "Nos vemos en la cafetería.", "nos vemos = we meet / see you", "A1::vocab A1::ocio"),
    vocab("I read the news every day.", "Leo las noticias todos los días.", "las noticias = the news (plural)", "A1::vocab A1::ocio"),

    # ---- common adjectives ----------------------------------------------
    vocab("The house is big.", "La casa es grande.", "grande keeps one form for both genders", "A1::vocab A1::adjetivos"),
    vocab("The car is small.", "El coche es pequeño.", "coche (Spain) / carro (Latin America)", "A1::vocab A1::adjetivos"),
    vocab("My coffee is cold.", "Mi café está frío.", "estar - it wasn't always cold", "A1::vocab A1::adjetivos"),
    vocab("The water is hot.", "El agua está caliente.", "el agua is feminine: agua fría, but el agua", "A1::vocab A1::adjetivos"),
    vocab("This book is interesting.", "Este libro es interesante.", "interesante has one form for both genders", "A1::vocab A1::adjetivos"),
    vocab("I'm tired.", "Estoy cansado.", "cansada if you're female", "A1::vocab A1::adjetivos"),
    vocab("She's happy.", "Ella está contenta.", "está contenta = mood right now", "A1::vocab A1::adjetivos"),
    vocab("The exercise is easy.", "El ejercicio es fácil.", "fácil = easy, difícil = hard", "A1::vocab A1::adjetivos"),
    vocab("Spanish is difficult sometimes.", "A veces el español es difícil.", "a veces goes at the front &middot; the language takes el", "A1::vocab A1::adjetivos"),
    vocab("The city is beautiful.", "La ciudad es bonita.", "bonito/bonita = pretty", "A1::vocab A1::adjetivos"),
    vocab("My neighbor is very nice.", "Mi vecino es muy simpático.", "el vecino = neighbour", "A1::vocab A1::adjetivos"),
    vocab("The movie is boring.", "La película es aburrida.", "ser aburrido = boring; estar aburrido = bored", "A1::vocab A1::adjetivos"),
    vocab("I'm sick today.", "Estoy enfermo hoy.", "estar enfermo = temporarily ill", "A1::vocab A1::adjetivos"),
    vocab("The store is open.", "La tienda está abierta.", "abierta agrees with tienda", "A1::vocab A1::adjetivos"),
    vocab("This shirt is too expensive.", "Esta camisa es demasiado cara.", "demasiado = too (much)", "A1::vocab A1::adjetivos"),
    vocab("The restaurant is cheap.", "El restaurante es barato.", "barato = cheap", "A1::vocab A1::adjetivos"),
    vocab("My brother is tall.", "Mi hermano es alto.", "ser for a lasting physical trait", "A1::vocab A1::adjetivos"),
    vocab("She has short hair.", "Ella tiene el pelo corto.", "Spanish uses el, not 'her', for body parts", "A1::vocab A1::adjetivos"),
    vocab("The exam is long.", "El examen es largo.", "largo = long (not 'large')", "A1::vocab A1::adjetivos"),
    vocab("I'm nervous.", "Estoy nervioso.", "estar for a passing feeling", "A1::vocab A1::adjetivos"),
    vocab("The weather is nice today.", "Hace buen tiempo hoy.", "weather uses hacer: hace frío, hace calor", "A1::vocab A1::adjetivos"),
    vocab("The room is dirty.", "La habitación está sucia.", "sucio = dirty, limpio = clean", "A1::vocab A1::adjetivos"),

    # ---- high-frequency verbs in context --------------------------------
    vocab("I have to work tomorrow.", "Tengo que trabajar mañana.", "tener que + infinitive = to have to", "A1::vocab A1::verbos"),
    vocab("I can't go today.", "No puedo ir hoy.", "poder: o -> ue", "A1::vocab A1::verbos"),
    vocab("I want to learn Spanish.", "Quiero aprender español.", "querer + infinitive", "A1::vocab A1::verbos"),
    vocab("I know her.", "La conozco.", "conocer for people; la = her", "A1::vocab A1::verbos"),
    vocab("I know the answer.", "Sé la respuesta.", "saber for facts; yo sé is irregular", "A1::vocab A1::verbos"),
    vocab("I'm going to the supermarket.", "Voy al supermercado.", "ir a + place", "A1::vocab A1::verbos"),
    vocab("She's coming tomorrow.", "Ella viene mañana.", "venir: yo vengo, tú vienes", "A1::vocab A1::verbos"),
    vocab("We're going to eat now.", "Vamos a comer ahora.", "ir a + infinitive = near future", "A1::vocab A1::verbos"),
    vocab("I need help.", "Necesito ayuda.", "la ayuda = help", "A1::vocab A1::verbos"),
    vocab("I'll bring the wine.", "Traigo el vino.", "traer: yo traigo", "A1::vocab A1::verbos"),
    vocab("I give a gift to my mother.", "Le doy un regalo a mi madre.", "dar: yo doy &middot; the le is not optional - Spanish doubles the indirect object", "A1::vocab A1::verbos"),
    vocab("I'm telling the truth.", "Digo la verdad.", "decir: yo digo, tú dices", "A1::vocab A1::verbos"),
    vocab("I leave the house at eight.", "Salgo de casa a las ocho.", "salir de = to leave (a place)", "A1::vocab A1::verbos"),
    vocab("I'm waiting for the bus.", "Espero el autobús.", "esperar already includes 'for'", "A1::vocab A1::verbos"),
    vocab("I understand a little Spanish.", "Entiendo un poco de español.", "un poco de = a little", "A1::vocab A1::verbos"),
    vocab("I think it's a good idea.", "Creo que es una buena idea.", "creer que = to think that", "A1::vocab A1::verbos"),
    vocab("I open the window.", "Abro la ventana.", "abrir = to open", "A1::vocab A1::verbos"),
    vocab("I'm wearing a black jacket.", "Llevo una chaqueta negra.", "llevar = to wear as well as to carry", "A1::vocab A1::verbos"),
    vocab("I take the kids to school.", "Llevo a los niños al colegio.", "personal a before a person object", "A1::vocab A1::verbos"),
    vocab("I put on my shoes.", "Me pongo los zapatos.", "ponerse = to put on (clothing)", "A1::vocab A1::verbos"),
    vocab("I see my friends on Saturday.", "Veo a mis amigos el sábado.", "personal a again", "A1::vocab A1::verbos"),
    vocab("I live in Stockholm.", "Vivo en Estocolmo.", "vivir en = to live in", "A1::vocab A1::verbos"),
    vocab("I speak a little Spanish.", "Hablo un poco de español.", "hablar = to speak", "A1::vocab A1::verbos"),
    vocab("He likes chocolate.", "Le gusta el chocolate.", "le = to him/her", "A1::vocab A1::verbos"),
    vocab("We like movies.", "Nos gustan las películas.", "plural thing liked -> gustan", "A1::vocab A1::verbos"),
]


GRAMMAR = [
    # ---- change the person ----------------------------------------------
    grammar("Yo vivo en Estocolmo. &rarr; <b>él</b>", "Él vive en Estocolmo.", "He lives in Stockholm &middot; -ir verbs: yo vivo, él vive", "A1::grammar A1::persona"),
    grammar("Yo hablo español. &rarr; <b>nosotros</b>", "Nosotros hablamos español.", "We speak Spanish &middot; -ar nosotros ending: -amos", "A1::grammar A1::persona"),
    grammar("Tú comes pan. &rarr; <b>ellos</b>", "Ellos comen pan.", "They eat bread &middot; -er ellos ending: -en", "A1::grammar A1::persona"),
    grammar("Yo tengo frío. &rarr; <b>ella</b>", "Ella tiene frío.", "She's cold &middot; tener: tengo but tiene", "A1::grammar A1::persona"),
    grammar("Nosotros trabajamos aquí. &rarr; <b>yo</b>", "Yo trabajo aquí.", "I work here &middot; -ar yo ending: -o", "A1::grammar A1::persona"),
    grammar("Yo soy sueco. &rarr; <b>ellos</b>", "Ellos son suecos.", "They're Swedish &middot; the adjective pluralises too", "A1::grammar A1::persona"),
    grammar("Él está cansado. &rarr; <b>nosotros</b>", "Nosotros estamos cansados.", "We're tired &middot; cansado &rarr; cansados", "A1::grammar A1::persona"),
    grammar("Yo voy al cine. &rarr; <b>tú</b>", "Tú vas al cine.", "You go to the cinema &middot; ir: voy, vas, va", "A1::grammar A1::persona"),
    grammar("Tú quieres café. &rarr; <b>yo</b>", "Yo quiero café.", "I want coffee &middot; querer: e &rarr; ie in yo/tú/él", "A1::grammar A1::persona"),
    grammar("Nosotros podemos ayudar. &rarr; <b>él</b>", "Él puede ayudar.", "He can help &middot; podemos has no stem change, puede does", "A1::grammar A1::persona"),
    grammar("Yo hago la cena. &rarr; <b>ella</b>", "Ella hace la cena.", "She makes dinner &middot; hacer: hago but hace", "A1::grammar A1::persona"),
    grammar("Ella sabe la respuesta. &rarr; <b>yo</b>", "Yo sé la respuesta.", "I know the answer &middot; saber: yo sé is irregular", "A1::grammar A1::persona"),
    grammar("Yo veo la tele. &rarr; <b>nosotros</b>", "Nosotros vemos la tele.", "We watch TV &middot; ver: veo, ves, ve, vemos", "A1::grammar A1::persona"),
    grammar("Tú vienes mañana. &rarr; <b>ellos</b>", "Ellos vienen mañana.", "They're coming tomorrow &middot; venir: vienes, vienen", "A1::grammar A1::persona"),
    grammar("Yo pongo la mesa. &rarr; <b>tú</b>", "Tú pones la mesa.", "You set the table &middot; poner: pongo but pones", "A1::grammar A1::persona"),
    grammar("Nosotros necesitamos dinero. &rarr; <b>yo</b>", "Yo necesito dinero.", "I need money &middot; regular -ar verb", "A1::grammar A1::persona"),
    grammar("Él conoce a María. &rarr; <b>yo</b>", "Yo conozco a María.", "I know María &middot; conocer: yo conozco (-zco)", "A1::grammar A1::persona"),
    grammar("Yo me levanto temprano. &rarr; <b>ella</b>", "Ella se levanta temprano.", "She gets up early &middot; the reflexive pronoun changes too: me &rarr; se", "A1::grammar A1::persona"),
    grammar("Yo llevo gafas. &rarr; <b>él</b>", "Él lleva gafas.", "He wears glasses &middot; regular -ar verb", "A1::grammar A1::persona"),
    grammar("Nosotros vivimos en Madrid. &rarr; <b>vosotros</b>", "Vosotros vivís en Madrid.", "You all live in Madrid &middot; -ir vosotros ending: -ís", "A1::grammar A1::persona"),

    # ---- make it negative ------------------------------------------------
    grammar("Tengo un hermano. &rarr; <b>negativo</b>", "No tengo un hermano.", "I don't have a brother &middot; no goes straight before the verb; 'No tengo hermanos' is more natural", "A1::grammar A1::negacion"),
    grammar("Hablo francés. &rarr; <b>negativo</b>", "No hablo francés.", "I don't speak French &middot; just add no", "A1::grammar A1::negacion"),
    grammar("Ella es española. &rarr; <b>negativo</b>", "Ella no es española.", "She isn't Spanish &middot; no sits between subject and verb", "A1::grammar A1::negacion"),
    grammar("Estamos en casa. &rarr; <b>negativo</b>", "No estamos en casa.", "We aren't at home &middot; no + estamos", "A1::grammar A1::negacion"),
    grammar("Me gusta el café. &rarr; <b>negativo</b>", "No me gusta el café.", "I don't like coffee &middot; no goes before the pronoun me", "A1::grammar A1::negacion"),
    grammar("Hay pan. &rarr; <b>negativo</b>", "No hay pan.", "There isn't any bread &middot; no hay = there isn't any", "A1::grammar A1::negacion"),
    grammar("Puedo ir. &rarr; <b>negativo</b>", "No puedo ir.", "I can't go &middot; no + conjugated verb only", "A1::grammar A1::negacion"),
    grammar("Siempre llego tarde. &rarr; <b>nunca</b>", "Nunca llego tarde.", "I'm never late &middot; nunca before the verb needs no 'no'", "A1::grammar A1::negacion"),
    grammar("Hay algo en la mesa. &rarr; <b>negativo</b>", "No hay nada en la mesa.", "There's nothing on the table &middot; algo &rarr; nada, and Spanish keeps the double negative", "A1::grammar A1::negacion"),
    grammar("Conozco a alguien aquí. &rarr; <b>negativo</b>", "No conozco a nadie aquí.", "I don't know anyone here &middot; alguien &rarr; nadie", "A1::grammar A1::negacion"),
    grammar("Quiero salir. &rarr; <b>negativo</b>", "No quiero salir.", "I don't want to go out &middot; no + querer", "A1::grammar A1::negacion"),
    grammar("Trabajo los sábados. &rarr; <b>negativo</b>", "No trabajo los sábados.", "I don't work on Saturdays &middot; no + trabajo", "A1::grammar A1::negacion"),
    grammar("Yo también voy. &rarr; <b>tampoco</b>", "Yo tampoco voy.", "I'm not going either &middot; también &rarr; tampoco = not ... either", "A1::grammar A1::negacion"),
    grammar("Sé cocinar. &rarr; <b>negativo</b>", "No sé cocinar.", "I can't cook &middot; no sé = I don't know how", "A1::grammar A1::negacion"),
    grammar("Tenemos tiempo. &rarr; <b>negativo</b>", "No tenemos tiempo.", "We don't have time &middot; no + tenemos", "A1::grammar A1::negacion"),

    # ---- make it a question ----------------------------------------------
    grammar("Tienes hermanos. &rarr; <b>pregunta</b>", "¿Tienes hermanos?", "Do you have any brothers or sisters? &middot; word order is unchanged - only the ¿ ? marks change", "A1::grammar A1::preguntas"),
    grammar("Ask <b>where she lives</b>.", "¿Dónde vive?", "dónde carries an accent in questions", "A1::grammar A1::preguntas"),
    grammar("Ask <b>what time the class starts</b>.", "¿A qué hora empieza la clase?", "a qué hora = at what time", "A1::grammar A1::preguntas"),
    grammar("Ask <b>how much it costs</b>.", "¿Cuánto cuesta?", "cuánto = how much", "A1::grammar A1::preguntas"),
    grammar("Ask <b>why he isn't coming</b>.", "¿Por qué no viene?", "por qué (two words) asks; porque (one) answers", "A1::grammar A1::preguntas"),
    grammar("Ask <b>what his name is</b>.", "¿Cómo se llama?", "lit. how does he call himself", "A1::grammar A1::preguntas"),
    grammar("Ask <b>where they are from</b>.", "¿De dónde son?", "de dónde = from where", "A1::grammar A1::preguntas"),
    grammar("Ask <b>when the train leaves</b>.", "¿Cuándo sale el tren?", "cuándo = when", "A1::grammar A1::preguntas"),
    grammar("Ask <b>which one she wants</b>.", "¿Cuál quiere?", "cuál = which one", "A1::grammar A1::preguntas"),
    grammar("Ask <b>who that is</b>.", "¿Quién es?", "quién = who (singular)", "A1::grammar A1::preguntas"),
    grammar("Ask <b>how you are</b> (informal).", "¿Cómo estás?", "estar, not ser, for how you feel", "A1::grammar A1::preguntas"),
    grammar("Ask <b>what he is doing</b>.", "¿Qué hace?", "qué = what", "A1::grammar A1::preguntas"),
    grammar("Ask <b>if there is a bathroom here</b>.", "¿Hay un baño aquí?", "hay for existence", "A1::grammar A1::preguntas"),
    grammar("Ask <b>how many people there are</b>.", "¿Cuántas personas hay?", "cuántas agrees with personas", "A1::grammar A1::preguntas"),
    grammar("Ask <b>what she does for work</b>.", "¿A qué se dedica?", "dedicarse a = to do for a living", "A1::grammar A1::preguntas"),

    # ---- gender and number -----------------------------------------------
    grammar("el libro rojo &rarr; <b>plural</b>", "los libros rojos", "the red books &middot; article, noun and adjective all pluralise", "A1::grammar A1::genero"),
    grammar("la casa blanca &rarr; <b>plural</b>", "las casas blancas", "the white houses &middot; feminine plural: las ... -as", "A1::grammar A1::genero"),
    grammar("un coche nuevo &rarr; <b>plural</b>", "unos coches nuevos", "some new cars &middot; un &rarr; unos = some", "A1::grammar A1::genero"),
    grammar("el profesor &rarr; <b>femenino</b>", "la profesora", "the teacher (female) &middot; -or &rarr; -ora", "A1::grammar A1::genero"),
    grammar("mi amigo español &rarr; <b>femenino</b>", "mi amiga española", "my Spanish friend (female) &middot; nationality adjectives on -ol add -a", "A1::grammar A1::genero"),
    grammar("la ciudad grande &rarr; <b>plural</b>", "las ciudades grandes", "the big cities &middot; consonant ending adds -es", "A1::grammar A1::genero"),
    grammar("el hombre joven &rarr; <b>plural</b>", "los hombres jóvenes", "the young men &middot; joven gains an accent as jóvenes", "A1::grammar A1::genero"),
    grammar("un problema difícil &rarr; <b>plural</b>", "unos problemas difíciles", "some difficult problems &middot; problema is masculine despite the -a", "A1::grammar A1::genero"),
    grammar("la mano &rarr; <b>plural</b>", "las manos", "the hands &middot; mano is feminine despite the -o", "A1::grammar A1::genero"),
    grammar("el día largo &rarr; <b>plural</b>", "los días largos", "the long days &middot; día is masculine", "A1::grammar A1::genero"),
    grammar("una chica alta &rarr; <b>plural</b>", "unas chicas altas", "some tall girls &middot; una &rarr; unas", "A1::grammar A1::genero"),
    grammar("el país pequeño &rarr; <b>plural</b>", "los países pequeños", "the small countries &middot; país loses its accent as países", "A1::grammar A1::genero"),

    # ---- ser vs estar ----------------------------------------------------
    grammar("Translate: <b>I am Swedish.</b>", "Soy sueco.", "ser for identity and origin", "A1::grammar A1::ser-estar"),
    grammar("Translate: <b>I am in Madrid.</b>", "Estoy en Madrid.", "estar for location", "A1::grammar A1::ser-estar"),
    grammar("Translate: <b>The soup is cold.</b>", "La sopa está fría.", "estar - it's a current condition", "A1::grammar A1::ser-estar"),
    grammar("Translate: <b>She is a doctor.</b>", "Ella es médica.", "ser for profession, no article", "A1::grammar A1::ser-estar"),
    grammar("___ las tres de la tarde. <b>(ser / estar)</b>", "Son", "It's three in the afternoon &middot; clock time always uses ser", "A1::grammar A1::ser-estar"),
    grammar("Mi hermana ___ enferma hoy. <b>(ser / estar)</b>", "está", "My sister is ill today &middot; illness is a passing state", "A1::grammar A1::ser-estar"),
    grammar("El libro ___ de mi padre. <b>(ser / estar)</b>", "es", "The book is my father's &middot; ser de = possession", "A1::grammar A1::ser-estar"),
    grammar("Nosotros ___ cansados. <b>(ser / estar)</b>", "estamos", "We're tired &middot; tiredness is temporary", "A1::grammar A1::ser-estar"),
    grammar("La fiesta ___ en mi casa. <b>(ser / estar)</b>", "es", "The party is at my house &middot; events take ser even though it looks like a location", "A1::grammar A1::ser-estar"),
    grammar("Translate: <b>I am tired but I am happy.</b>", "Estoy cansado pero estoy feliz.", "both are states &rarr; estar", "A1::grammar A1::ser-estar"),
    grammar("Madrid ___ en España. <b>(ser / estar)</b>", "está", "Madrid is in Spain &middot; physical location &rarr; estar", "A1::grammar A1::ser-estar"),
    grammar("Ellos ___ muy simpáticos. <b>(ser / estar)</b>", "son", "They're very nice &middot; personality &rarr; ser", "A1::grammar A1::ser-estar"),
    grammar("La puerta ___ abierta. <b>(ser / estar)</b>", "está", "The door is open &middot; estar + participle = resulting state", "A1::grammar A1::ser-estar"),
    grammar("Hoy ___ lunes. <b>(ser / estar)</b>", "es", "Today is Monday &middot; days of the week take ser", "A1::grammar A1::ser-estar"),
    grammar("Translate: <b>My brother is 20 years old.</b>", "Mi hermano tiene veinte años.", "age uses tener, not ser or estar", "A1::grammar A1::ser-estar"),

    # ---- hay vs está -----------------------------------------------------
    grammar("___ un banco en esta calle. <b>(hay / está)</b>", "Hay", "There's a bank on this street &middot; introducing something new &rarr; hay", "A1::grammar A1::hay-estar"),
    grammar("El banco ___ en esta calle. <b>(hay / está)</b>", "está", "The bank is on this street &middot; a specific known thing &rarr; estar", "A1::grammar A1::hay-estar"),
    grammar("¿___ un supermercado cerca? <b>(hay / está)</b>", "Hay", "Is there a supermarket nearby? &middot; hay + un/una", "A1::grammar A1::hay-estar"),
    grammar("¿Dónde ___ el supermercado? <b>(hay / está)</b>", "está", "Where's the supermarket? &middot; el + known thing &rarr; estar", "A1::grammar A1::hay-estar"),
    grammar("En mi clase ___ veinte estudiantes. <b>(hay / están)</b>", "hay", "There are twenty students in my class &middot; counting things &rarr; hay", "A1::grammar A1::hay-estar"),
    grammar("Los estudiantes ___ en clase. <b>(hay / están)</b>", "están", "The students are in class &middot; los + known group &rarr; estar", "A1::grammar A1::hay-estar"),
    grammar("Translate: <b>There are two bathrooms.</b>", "Hay dos baños.", "hay never changes for plural", "A1::grammar A1::hay-estar"),
    grammar("Translate: <b>The bathroom is upstairs.</b>", "El baño está arriba.", "arriba = upstairs", "A1::grammar A1::hay-estar"),

    # ---- gustar ----------------------------------------------------------
    grammar("Translate: <b>I like coffee.</b>", "Me gusta el café.", "lit. coffee pleases me; keep el", "A1::grammar A1::gustar"),
    grammar("Translate: <b>I like movies.</b>", "Me gustan las películas.", "plural thing liked &rarr; gustan", "A1::grammar A1::gustar"),
    grammar("Translate: <b>He likes to run.</b>", "Le gusta correr.", "infinitive counts as singular", "A1::grammar A1::gustar"),
    grammar("Translate: <b>We like this restaurant.</b>", "Nos gusta este restaurante.", "nos = to us", "A1::grammar A1::gustar"),
    grammar("Translate: <b>Do you like Spanish?</b>", "¿Te gusta el español?", "te = to you (informal)", "A1::grammar A1::gustar"),
    grammar("Me gusta el libro. &rarr; <b>los libros</b>", "Me gustan los libros.", "I like the books &middot; the verb agrees with the thing liked", "A1::grammar A1::gustar"),
    grammar("Translate: <b>They like to travel.</b>", "Les gusta viajar.", "les = to them", "A1::grammar A1::gustar"),
    grammar("Translate: <b>I don't like fish.</b>", "No me gusta el pescado.", "no comes before me", "A1::grammar A1::gustar"),
    grammar("Translate: <b>I like it a lot.</b>", "Me gusta mucho.", "mucho follows the verb", "A1::grammar A1::gustar"),
    grammar("Translate: <b>My friends like the music.</b>", "A mis amigos les gusta la música.", "a + person is doubled by les", "A1::grammar A1::gustar"),

    # ---- ir a / tener que / poder / querer -------------------------------
    grammar("Como en casa. &rarr; <b>ir a + infinitivo</b>", "Voy a comer en casa.", "I'm going to eat at home &middot; ir a + infinitive = going to", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>We're going to travel in July.</b>", "Vamos a viajar en julio.", "vamos a + infinitive", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>I have to study tonight.</b>", "Tengo que estudiar esta noche.", "tener que + infinitive = have to", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>You have to wait.</b>", "Tienes que esperar.", "the que is obligatory", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>Can I ask a question?</b>", "¿Puedo hacer una pregunta?", "hacer una pregunta = to ask a question", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>I want to go home.</b>", "Quiero ir a casa.", "querer + infinitive, no preposition", "A1::grammar A1::perifrasis"),
    grammar("Estudio español. &rarr; <b>ir a + infinitivo</b>", "Voy a estudiar español.", "I'm going to study Spanish &middot; voy a + infinitive", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>She's going to work tomorrow.</b>", "Ella va a trabajar mañana.", "va a + infinitive", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>We have to leave now.</b>", "Tenemos que salir ahora.", "tenemos que + infinitive", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>They can't come.</b>", "No pueden venir.", "poder + infinitive", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>I want to speak with Ana.</b>", "Quiero hablar con Ana.", "hablar con = to speak with", "A1::grammar A1::perifrasis"),
    grammar("Translate: <b>What are you going to do?</b>", "¿Qué vas a hacer?", "vas a + hacer", "A1::grammar A1::perifrasis"),

    # ---- articles, possessives, demonstratives ---------------------------
    grammar("Translate: <b>my parents</b>", "mis padres", "mi &rarr; mis before a plural noun", "A1::grammar A1::determinantes"),
    grammar("Translate: <b>our house</b>", "nuestra casa", "nuestro/nuestra agrees with the noun", "A1::grammar A1::determinantes"),
    grammar("Translate: <b>your books</b> (tú)", "tus libros", "tu &rarr; tus", "A1::grammar A1::determinantes"),
    grammar("Translate: <b>his car</b>", "su coche", "su covers his, her, your (usted) and their", "A1::grammar A1::determinantes"),
    grammar("Translate: <b>this table</b>", "esta mesa", "este/esta = this", "A1::grammar A1::determinantes"),
    grammar("Translate: <b>that man over there</b>", "aquel hombre", "aquel = that one further away", "A1::grammar A1::determinantes"),
    grammar("Translate: <b>these shoes</b>", "estos zapatos", "estos = these (masculine plural)", "A1::grammar A1::determinantes"),
    grammar("Voy ___ supermercado. <b>(a + el)</b>", "al", "I'm going to the supermarket &middot; a + el contracts to al", "A1::grammar A1::determinantes"),
    grammar("Vengo ___ oficina. <b>(de + la)</b>", "de la", "I'm coming from the office &middot; de + la does not contract", "A1::grammar A1::determinantes"),
    grammar("Es el coche ___ profesor. <b>(de + el)</b>", "del", "It's the teacher's car &middot; de + el contracts to del", "A1::grammar A1::determinantes"),

    # ---- reflexive verbs -------------------------------------------------
    grammar("Translate: <b>I get up at seven.</b>", "Me levanto a las siete.", "levantarse is reflexive", "A1::grammar A1::reflexivos"),
    grammar("Translate: <b>I shower in the morning.</b>", "Me ducho por la mañana.", "ducharse = to shower", "A1::grammar A1::reflexivos"),
    grammar("Me llamo Pierre. &rarr; <b>él</b>", "Se llama Pierre.", "His name is Pierre &middot; me &rarr; se", "A1::grammar A1::reflexivos"),
    grammar("Translate: <b>What's your name?</b> (informal)", "¿Cómo te llamas?", "te llamas = you call yourself", "A1::grammar A1::reflexivos"),
    grammar("Translate: <b>We go to bed late.</b>", "Nos acostamos tarde.", "acostarse: o &rarr; ue, but not in nosotros", "A1::grammar A1::reflexivos"),
    grammar("Nos levantamos temprano. &rarr; <b>yo</b>", "Me levanto temprano.", "I get up early &middot; nos &rarr; me", "A1::grammar A1::reflexivos"),
    grammar("Translate: <b>He shaves every day.</b>", "Se afeita todos los días.", "afeitarse = to shave", "A1::grammar A1::reflexivos"),
    grammar("Translate: <b>I put on my coat.</b>", "Me pongo el abrigo.", "ponerse; use el, not 'my'", "A1::grammar A1::reflexivos"),

    # ---- quantity and comparison ----------------------------------------
    grammar("Translate: <b>very tired</b>", "muy cansado", "muy modifies an adjective", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>I work a lot.</b>", "Trabajo mucho.", "mucho after a verb never changes", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>a lot of work</b>", "mucho trabajo", "mucho before a noun agrees with it", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>many friends</b>", "muchos amigos", "muchos agrees with amigos", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>My brother is taller than me.</b>", "Mi hermano es más alto que yo.", "más ... que = more ... than", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>This is less expensive.</b>", "Esto es menos caro.", "menos = less", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>I'm better now.</b>", "Estoy mejor ahora.", "mejor = better (no 'más bueno')", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>It's the best restaurant.</b>", "Es el mejor restaurante.", "el mejor = the best", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>too much coffee</b>", "demasiado café", "demasiado = too much", "A1::grammar A1::cantidad"),
    grammar("Translate: <b>a little bread</b>", "un poco de pan", "un poco de + noun", "A1::grammar A1::cantidad"),

    # ---- pretérito perfecto: he / has / ha + participle -------------------
    grammar("Hoy ___ comido en casa. <b>(haber — yo)</b>", "he", "Today I've eaten at home &middot; he + participle, and nothing may come between them", "A1::grammar A1::perfecto"),
    grammar("¿___ visto esta película? <b>(haber — tú)</b>", "Has", "Have you seen this film? &middot; has visto", "A1::grammar A1::perfecto"),
    grammar("Esta mañana ___ llegado tarde. <b>(haber — nosotros)</b>", "hemos", "This morning we arrived late &middot; esta mañana is still today, so the perfecto", "A1::grammar A1::perfecto"),
    grammar("Mis padres ___ llamado dos veces. <b>(haber)</b>", "han", "My parents have called twice", "A1::grammar A1::perfecto"),
    grammar("¿___ estado alguna vez en México? <b>(haber — vosotros)</b>", "Habéis", "Have you all ever been to Mexico? &middot; alguna vez = ever", "A1::grammar A1::perfecto"),

    grammar("hablar &rarr; <b>participio</b>", "hablado", "-ar verbs take -ado", "A1::grammar A1::perfecto"),
    grammar("comer &rarr; <b>participio</b>", "comido", "-er and -ir verbs take -ido", "A1::grammar A1::perfecto"),
    grammar("vivir &rarr; <b>participio</b>", "vivido", "-ir behaves like -er here: vivido", "A1::grammar A1::perfecto"),
    grammar("ver &rarr; <b>participio</b>", "visto", "irregular &middot; he visto", "A1::grammar A1::perfecto"),
    grammar("hacer &rarr; <b>participio</b>", "hecho", "irregular &middot; ¿qué has hecho?", "A1::grammar A1::perfecto"),
    grammar("decir &rarr; <b>participio</b>", "dicho", "irregular &middot; me ha dicho que sí", "A1::grammar A1::perfecto"),
    grammar("escribir &rarr; <b>participio</b>", "escrito", "irregular &middot; he escrito una carta", "A1::grammar A1::perfecto"),
    grammar("poner &rarr; <b>participio</b>", "puesto", "irregular &middot; he puesto la mesa", "A1::grammar A1::perfecto"),
    grammar("volver &rarr; <b>participio</b>", "vuelto", "irregular &middot; ha vuelto a casa", "A1::grammar A1::perfecto"),
    grammar("abrir &rarr; <b>participio</b>", "abierto", "irregular &middot; han abierto la tienda", "A1::grammar A1::perfecto"),

    grammar("Ella ha ___ la carta. <b>(escribir)</b>", "escrito", "She has written the letter &middot; the participle never agrees here: escrito, not escrita", "A1::grammar A1::perfecto"),
    grammar("Ayer comí paella. &rarr; <b>hoy</b>", "Hoy he comido paella.", "ayer takes the indefinido, hoy takes the perfecto - in Spain the day you're still in uses he comido", "A1::grammar A1::perfecto"),
    grammar("He comido. &rarr; <b>negativo</b>", "No he comido.", "no goes before haber, never between haber and the participle", "A1::grammar A1::perfecto"),
    grammar("Me levanto a las siete. &rarr; <b>pretérito perfecto</b>", "Me he levantado a las siete.", "the reflexive pronoun sits in front of haber", "A1::grammar A1::perfecto"),
    grammar("Lo veo. &rarr; <b>pretérito perfecto</b>", "Lo he visto.", "object pronouns also go in front of haber: lo he visto", "A1::grammar A1::perfecto"),

    grammar("Translate: <b>I've already finished.</b>", "Ya he terminado.", "ya = already, and it usually comes first", "A1::grammar A1::perfecto"),
    grammar("Translate: <b>I haven't eaten yet.</b>", "Todavía no he comido.", "todavía no = not yet &middot; aún no works the same", "A1::grammar A1::perfecto"),
    grammar("Translate: <b>Have you ever been to Spain?</b>", "¿Has estado alguna vez en España?", "alguna vez = ever &middot; estar, not ir, for having been somewhere", "A1::grammar A1::perfecto"),
    grammar("Translate: <b>This week we have worked a lot.</b>", "Esta semana hemos trabajado mucho.", "esta semana is unfinished time &rarr; perfecto", "A1::grammar A1::perfecto"),
    grammar("Translate: <b>What have you done today?</b>", "¿Qué has hecho hoy?", "the everyday question in Spain, and the reason hecho is worth knowing cold", "A1::grammar A1::perfecto"),
    grammar("Translate: <b>She has never been to Madrid.</b>", "Nunca ha estado en Madrid.", "nunca before the verb needs no second no", "A1::grammar A1::perfecto"),
    grammar("Translate: <b>Today I played padel at lunchtime.</b>", "Hoy he jugado al pádel a la hora de comer.", "hoy &rarr; perfecto, not jugué &middot; jugar al + sport &middot; in Spain lunch is la comida, so la hora de comer; el almuerzo is mostly Latin America", "A1::grammar A1::perfecto"),
]


SENTENCES = [
    # ---- greetings and introductions -------------------------------------
    sentence("¿Qué tal?", "How's it going?", "qué tal = how goes it &middot; the everyday informal greeting", "A1::sentences A1::saludos"),
    sentence("Mucho gusto.", "Nice to meet you.", "lit. much pleasure", "A1::sentences A1::saludos"),
    sentence("¿Cómo te llamas?", "What's your name?", "cómo = how &middot; te llamas = you call yourself", "A1::sentences A1::saludos"),
    sentence("Encantado de conocerte.", "Pleased to meet you.", "encantado = delighted (encantada if you're female) &middot; conocerte = to meet you", "A1::sentences A1::saludos"),
    sentence("Hasta luego.", "See you later.", "hasta = until &middot; luego = later", "A1::sentences A1::saludos"),
    sentence("Nos vemos mañana.", "See you tomorrow.", "nos vemos = we see each other", "A1::sentences A1::saludos"),
    sentence("¿De dónde eres?", "Where are you from?", "de dónde = from where &middot; eres = you are", "A1::sentences A1::saludos"),
    sentence("Soy de Suecia.", "I'm from Sweden.", "ser de = to be from", "A1::sentences A1::saludos"),
    sentence("Buenos días, ¿cómo está usted?", "Good morning, how are you?", "usted = formal you &middot; está, not estás", "A1::sentences A1::saludos"),
    sentence("Lo siento mucho.", "I'm very sorry.", "lo siento = lit. I feel it", "A1::sentences A1::saludos"),
    sentence("No pasa nada.", "It's no problem.", "lit. nothing happens", "A1::sentences A1::saludos"),
    sentence("Muchas gracias por todo.", "Thank you very much for everything.", "por todo = for everything", "A1::sentences A1::saludos"),
    sentence("De nada.", "You're welcome.", "lit. of nothing", "A1::sentences A1::saludos"),
    sentence("Perdona, ¿puedo pasar?", "Excuse me, can I get by?", "perdona = excuse me (informal) &middot; pasar = to pass", "A1::sentences A1::saludos"),
    sentence("¿Qué tal el fin de semana?", "How was your weekend?", "fin de semana = weekend", "A1::sentences A1::saludos"),
    sentence("Te presento a mi amigo Juan.", "Let me introduce you to my friend Juan.", "te presento a = I introduce to you", "A1::sentences A1::saludos"),
    sentence("¿Cuántos años tienes?", "How old are you?", "lit. how many years do you have", "A1::sentences A1::saludos"),
    sentence("Tengo treinta y dos años.", "I'm thirty-two.", "age with tener + años", "A1::sentences A1::saludos"),

    # ---- small talk and opinions -----------------------------------------
    sentence("¿Qué te parece?", "What do you think?", "te parece = it seems to you", "A1::sentences A1::opiniones"),
    sentence("Me parece bien.", "Sounds good to me.", "me parece = it seems to me", "A1::sentences A1::opiniones"),
    sentence("Creo que sí.", "I think so.", "creer que = to think that", "A1::sentences A1::opiniones"),
    sentence("No estoy seguro.", "I'm not sure.", "segura if you're female", "A1::sentences A1::opiniones"),
    sentence("Estoy de acuerdo contigo.", "I agree with you.", "estar de acuerdo = to agree &middot; contigo = with you", "A1::sentences A1::opiniones"),
    sentence("Depende del día.", "It depends on the day.", "depender de &middot; de + el = del", "A1::sentences A1::opiniones"),
    sentence("Más o menos.", "More or less.", "the standard lukewarm answer to ¿qué tal?", "A1::sentences A1::opiniones"),
    sentence("¡Qué bien!", "How great!", "qué + adjective = how ...!", "A1::sentences A1::opiniones"),
    sentence("¡Qué pena!", "What a shame!", "la pena = pity, shame", "A1::sentences A1::opiniones"),
    sentence("Tienes razón.", "You're right.", "lit. you have reason", "A1::sentences A1::opiniones"),
    sentence("No tengo ni idea.", "I have no idea.", "ni adds emphasis to the negative", "A1::sentences A1::opiniones"),
    sentence("Me da igual.", "I don't mind.", "lit. it gives me the same", "A1::sentences A1::opiniones"),
    sentence("Claro que sí.", "Of course.", "claro = clear, obviously", "A1::sentences A1::opiniones"),
    sentence("A mí también.", "Me too.", "agreeing with a positive statement", "A1::sentences A1::opiniones"),
    sentence("A mí tampoco.", "Me neither.", "agreeing with a negative statement", "A1::sentences A1::opiniones"),

    # ---- daily routine ----------------------------------------------------
    sentence("¿A qué hora te levantas normalmente?", "What time do you normally get up?", "a qué hora = at what time &middot; te levantas = you get up", "A1::sentences A1::rutina"),
    sentence("Me despierto a las siete.", "I wake up at seven.", "despertarse = to wake up (different from levantarse)", "A1::sentences A1::rutina"),
    sentence("Desayuno café con leche.", "I have coffee with milk for breakfast.", "desayunar = to have breakfast", "A1::sentences A1::rutina"),
    sentence("Salgo de casa a las ocho y media.", "I leave the house at half past eight.", "salir de = to leave &middot; y media = half past", "A1::sentences A1::rutina"),
    sentence("Voy al trabajo en metro.", "I go to work by metro.", "en + transport = by", "A1::sentences A1::rutina"),
    sentence("Como con mis compañeros.", "I have lunch with my colleagues.", "comer at midday = to have lunch", "A1::sentences A1::rutina"),
    sentence("Por la tarde hago deporte.", "In the afternoon I do sport.", "hacer deporte = to exercise", "A1::sentences A1::rutina"),
    sentence("Ceno sobre las nueve.", "I have dinner around nine.", "sobre + time = around", "A1::sentences A1::rutina"),
    sentence("Antes de dormir leo un poco.", "Before sleeping I read a bit.", "antes de + infinitive", "A1::sentences A1::rutina"),
    sentence("Los fines de semana duermo más.", "On weekends I sleep more.", "dormir: o &rarr; ue", "A1::sentences A1::rutina"),
    sentence("Siempre tengo prisa por la mañana.", "I'm always in a hurry in the morning.", "tener prisa = to be in a hurry", "A1::sentences A1::rutina"),
    sentence("Nunca desayuno en casa.", "I never have breakfast at home.", "nunca before the verb", "A1::sentences A1::rutina"),
    sentence("Hoy tengo mucho que hacer.", "Today I have a lot to do.", "mucho que hacer = a lot to do", "A1::sentences A1::rutina"),
    sentence("Estoy muy ocupado esta semana.", "I'm very busy this week.", "ocupada if you're female", "A1::sentences A1::rutina"),
    sentence("Normalmente llego a casa a las seis.", "I normally get home at six.", "llegar a casa = to get home", "A1::sentences A1::rutina"),

    # ---- shopping ---------------------------------------------------------
    sentence("¿Cuánto cuesta esto?", "How much does this cost?", "costar: o &rarr; ue", "A1::sentences A1::compras"),
    sentence("¿Me puede ayudar?", "Can you help me?", "formal usted form", "A1::sentences A1::compras"),
    sentence("Solo estoy mirando, gracias.", "I'm just looking, thanks.", "solo = only, just", "A1::sentences A1::compras"),
    sentence("¿Tiene esto en otra talla?", "Do you have this in another size?", "la talla = clothing size", "A1::sentences A1::compras"),
    sentence("Me lo llevo.", "I'll take it.", "lit. I carry it away - what you say at the till", "A1::sentences A1::compras"),
    sentence("¿Puedo pagar con tarjeta?", "Can I pay by card?", "con tarjeta = by card", "A1::sentences A1::compras"),
    sentence("Es demasiado caro para mí.", "It's too expensive for me.", "para mí = for me", "A1::sentences A1::compras"),
    sentence("¿Está en oferta?", "Is it on sale?", "la oferta = special offer", "A1::sentences A1::compras"),
    sentence("¿Dónde están los probadores?", "Where are the fitting rooms?", "el probador, from probar = to try on", "A1::sentences A1::compras"),
    sentence("Quiero devolver esto.", "I want to return this.", "devolver = to return an item", "A1::sentences A1::compras"),
    sentence("¿Tiene cambio de veinte euros?", "Do you have change for twenty euros?", "el cambio = change", "A1::sentences A1::compras"),
    sentence("¿A qué hora cierran?", "What time do you close?", "cierran = they close (cerrar: e &rarr; ie)", "A1::sentences A1::compras"),
    sentence("Necesito una bolsa, por favor.", "I need a bag, please.", "la bolsa = bag", "A1::sentences A1::compras"),
    sentence("¿Algo más?", "Anything else?", "what the cashier asks you", "A1::sentences A1::compras"),
    sentence("Nada más, gracias.", "That's all, thanks.", "nada más = nothing more", "A1::sentences A1::compras"),

    # ---- restaurant -------------------------------------------------------
    sentence("Una mesa para dos, por favor.", "A table for two, please.", "para dos = for two", "A1::sentences A1::restaurante"),
    sentence("¿Qué me recomienda?", "What do you recommend?", "formal &middot; recomendar: e &rarr; ie", "A1::sentences A1::restaurante"),
    sentence("Para mí, la sopa.", "For me, the soup.", "how you order at the table", "A1::sentences A1::restaurante"),
    sentence("¿Qué lleva este plato?", "What's in this dish?", "llevar here = to contain", "A1::sentences A1::restaurante"),
    sentence("Soy vegetariano.", "I'm vegetarian.", "vegetariana if you're female", "A1::sentences A1::restaurante"),
    sentence("No como carne ni pescado.", "I don't eat meat or fish.", "ni = nor, after a negative", "A1::sentences A1::restaurante"),
    sentence("¿Me trae la carta, por favor?", "Could you bring me the menu, please?", "la carta = menu &middot; traer = to bring", "A1::sentences A1::restaurante"),
    sentence("Está muy rico.", "It's delicious.", "rico with estar = tasty", "A1::sentences A1::restaurante"),
    sentence("La cuenta, por favor.", "The bill, please.", "la cuenta = the bill", "A1::sentences A1::restaurante"),
    sentence("¿Está incluida la propina?", "Is the tip included?", "la propina = tip", "A1::sentences A1::restaurante"),
    sentence("Otra cerveza, por favor.", "Another beer, please.", "otra = another (never 'una otra')", "A1::sentences A1::restaurante"),
    sentence("Sin hielo, por favor.", "Without ice, please.", "sin = without &middot; el hielo = ice", "A1::sentences A1::restaurante"),
    sentence("Tengo una reserva a nombre de Pierre.", "I have a reservation under the name Pierre.", "a nombre de = under the name of", "A1::sentences A1::restaurante"),
    sentence("¿Tienen wifi?", "Do you have wifi?", "tienen = you (plural/formal) have", "A1::sentences A1::restaurante"),
    sentence("Perdone, falta un plato.", "Excuse me, one dish is missing.", "faltar = to be missing", "A1::sentences A1::restaurante"),

    # ---- getting around ---------------------------------------------------
    sentence("¿Dónde está la estación, por favor?", "Where is the station, please?", "estar for location", "A1::sentences A1::viajes"),
    sentence("¿Está lejos de aquí?", "Is it far from here?", "lejos de = far from", "A1::sentences A1::viajes"),
    sentence("Está a diez minutos andando.", "It's ten minutes on foot.", "andando = walking", "A1::sentences A1::viajes"),
    sentence("Siga todo recto y gire a la izquierda.", "Go straight on and turn left.", "siga, gire = formal commands", "A1::sentences A1::viajes"),
    sentence("Está al lado del banco.", "It's next to the bank.", "al lado de = next to", "A1::sentences A1::viajes"),
    sentence("Está enfrente del parque.", "It's opposite the park.", "enfrente de = opposite", "A1::sentences A1::viajes"),
    sentence("¿Qué autobús va al centro?", "Which bus goes to the center?", "qué + noun = which", "A1::sentences A1::viajes"),
    sentence("¿Este tren para en Sevilla?", "Does this train stop in Sevilla?", "parar = to stop", "A1::sentences A1::viajes"),
    sentence("¿A qué hora sale el próximo tren?", "What time does the next train leave?", "próximo = next", "A1::sentences A1::viajes"),
    sentence("Un billete de ida y vuelta, por favor.", "A round-trip ticket, please.", "ida y vuelta = there and back", "A1::sentences A1::viajes"),
    sentence("¿Dónde puedo coger un taxi?", "Where can I get a taxi?", "coger (Spain) &middot; use tomar in Latin America", "A1::sentences A1::viajes"),
    sentence("Estoy buscando esta dirección.", "I'm looking for this address.", "la dirección = address", "A1::sentences A1::viajes"),
    sentence("Creo que estoy perdido.", "I think I'm lost.", "perdida if you're female", "A1::sentences A1::viajes"),
    sentence("¿Me puede llevar al aeropuerto?", "Can you take me to the airport?", "llevar a = to take someone to", "A1::sentences A1::viajes"),
    sentence("¿Cuánto se tarda en llegar?", "How long does it take to get there?", "tardar en = to take (time) to", "A1::sentences A1::viajes"),

    # ---- health and problems ----------------------------------------------
    sentence("No me encuentro bien.", "I don't feel well.", "encontrarse = to feel (health)", "A1::sentences A1::salud"),
    sentence("Me duele la cabeza.", "My head hurts.", "doler works like gustar &middot; la, not 'my'", "A1::sentences A1::salud"),
    sentence("Me duelen los pies.", "My feet hurt.", "plural subject &rarr; duelen", "A1::sentences A1::salud"),
    sentence("Necesito ir al médico.", "I need to go to the doctor.", "el médico = doctor", "A1::sentences A1::salud"),
    sentence("¿Hay una farmacia cerca?", "Is there a pharmacy nearby?", "cerca = nearby", "A1::sentences A1::salud"),
    sentence("Estoy resfriado.", "I have a cold.", "resfriada if you're female", "A1::sentences A1::salud"),
    sentence("Tengo fiebre.", "I have a fever.", "symptoms use tener", "A1::sentences A1::salud"),
    sentence("¿Está usted bien?", "Are you okay?", "formal usted", "A1::sentences A1::salud"),
    sentence("Soy alérgico a los frutos secos.", "I'm allergic to nuts.", "alérgico a &middot; frutos secos = nuts", "A1::sentences A1::salud"),
    sentence("Llame a una ambulancia.", "Call an ambulance.", "llame = formal command from llamar", "A1::sentences A1::salud"),

    # ---- learning Spanish -------------------------------------------------
    sentence("¿Cómo se dice 'table' en español?", "How do you say 'table' in Spanish?", "se dice = one says", "A1::sentences A1::clase"),
    sentence("¿Qué significa esta palabra?", "What does this word mean?", "significar = to mean", "A1::sentences A1::clase"),
    sentence("¿Puede hablar más despacio, por favor?", "Can you speak more slowly, please?", "despacio = slowly", "A1::sentences A1::clase"),
    sentence("No entiendo nada.", "I don't understand anything.", "double negative is correct here", "A1::sentences A1::clase"),
    sentence("¿Puede repetir, por favor?", "Can you repeat, please?", "formal puede + infinitive", "A1::sentences A1::clase"),
    sentence("Estoy aprendiendo español.", "I'm learning Spanish.", "estar + gerund", "A1::sentences A1::clase"),
    sentence("Hablo un poco de español.", "I speak a little Spanish.", "un poco de = a little", "A1::sentences A1::clase"),
    sentence("¿Cómo se escribe?", "How do you spell it?", "lit. how is it written", "A1::sentences A1::clase"),
    sentence("No sé cómo se dice.", "I don't know how to say it.", "no sé = I don't know", "A1::sentences A1::clase"),
    sentence("¿Está bien así?", "Is this right?", "así = like this", "A1::sentences A1::clase"),
    sentence("Tengo una pregunta.", "I have a question.", "la pregunta = question", "A1::sentences A1::clase"),
    sentence("Perdón por mi español.", "Sorry for my Spanish.", "perdón por = sorry for", "A1::sentences A1::clase"),

    # ---- plans and invitations --------------------------------------------
    sentence("¿Quieres tomar algo?", "Do you want to grab a drink?", "tomar algo = to have something to drink", "A1::sentences A1::planes"),
    sentence("¿Qué haces esta noche?", "What are you doing tonight?", "esta noche = tonight", "A1::sentences A1::planes"),
    sentence("¿Nos vemos el sábado?", "Shall we meet on Saturday?", "nos vemos = we see each other", "A1::sentences A1::planes"),
    sentence("Vale, perfecto.", "Okay, perfect.", "vale = okay (very common in Spain)", "A1::sentences A1::planes"),
    sentence("Lo siento, no puedo.", "Sorry, I can't.", "no puedo = I can't", "A1::sentences A1::planes"),
    sentence("Quizás otro día.", "Maybe another day.", "quizás = maybe", "A1::sentences A1::planes"),
    sentence("¿A qué hora quedamos?", "What time shall we meet?", "quedar = to arrange to meet", "A1::sentences A1::planes"),
    sentence("Quedamos a las ocho en la plaza.", "Let's meet at eight in the square.", "la plaza = square", "A1::sentences A1::planes"),
    sentence("Voy a llegar un poco tarde.", "I'm going to arrive a bit late.", "un poco tarde = a bit late", "A1::sentences A1::planes"),
    sentence("Estoy en camino.", "I'm on my way.", "el camino = the way", "A1::sentences A1::planes"),
    sentence("¿Vienes con nosotros?", "Are you coming with us?", "con nosotros = with us", "A1::sentences A1::planes"),
    sentence("Tengo otros planes.", "I have other plans.", "otros = other (no 'unos otros')", "A1::sentences A1::planes"),

    # ---- practical, at home -----------------------------------------------
    sentence("¿Puedo usar el baño?", "Can I use the bathroom?", "usar = to use", "A1::sentences A1::practico"),
    sentence("No funciona la ducha.", "The shower doesn't work.", "funcionar = to work (machines)", "A1::sentences A1::practico"),
    sentence("¿Dónde está la llave?", "Where's the key?", "la llave = key", "A1::sentences A1::practico"),
    sentence("Hace mucho calor aquí.", "It's very hot here.", "weather uses hacer + noun", "A1::sentences A1::practico"),
    sentence("Hace frío fuera.", "It's cold outside.", "fuera = outside", "A1::sentences A1::practico"),
    sentence("¿Puedes abrir la ventana?", "Can you open the window?", "abrir = to open", "A1::sentences A1::practico"),
    sentence("Voy a hacer la compra.", "I'm going to do the grocery shopping.", "hacer la compra = to do the food shop", "A1::sentences A1::practico"),
    sentence("La lavadora está rota.", "The washing machine is broken.", "roto/rota = broken", "A1::sentences A1::practico"),
    sentence("Vivo aquí desde hace dos años.", "I've lived here for two years.", "desde hace = for (a duration), with present tense", "A1::sentences A1::practico"),
    sentence("Comparto piso con dos amigos.", "I share a flat with two friends.", "compartir = to share", "A1::sentences A1::practico"),

    # ---- phone and messaging ----------------------------------------------
    sentence("¿Me das tu número?", "Can you give me your number?", "present tense as a request", "A1::sentences A1::movil"),
    sentence("Te escribo luego.", "I'll text you later.", "present tense covers the near future", "A1::sentences A1::movil"),
    sentence("No tengo cobertura.", "I have no signal.", "la cobertura = phone signal", "A1::sentences A1::movil"),
    sentence("¿Cuál es la contraseña del wifi?", "What's the wifi password?", "la contraseña = password", "A1::sentences A1::movil"),
    sentence("No tengo batería.", "My battery is dead.", "lit. I don't have battery", "A1::sentences A1::movil"),
    sentence("¿Puedes llamarme más tarde?", "Can you call me later?", "llamarme = to call me", "A1::sentences A1::movil"),
    sentence("¿Estás en WhatsApp?", "Are you on WhatsApp?", "estar en = to be on", "A1::sentences A1::movil"),
    sentence("Te mando la dirección.", "I'll send you the address.", "mandar = to send", "A1::sentences A1::movil"),

    # ---- everyday fillers -------------------------------------------------
    sentence("¿Puedo pedirte un favor?", "Can I ask you a favor?", "pedir = to ask for", "A1::sentences A1::expresiones"),
    sentence("Un momento, por favor.", "One moment, please.", "el momento = moment", "A1::sentences A1::expresiones"),
    sentence("Ya está.", "That's it / it's done.", "ya = already, now", "A1::sentences A1::expresiones"),
    sentence("Todavía no.", "Not yet.", "todavía = still, yet", "A1::sentences A1::expresiones"),
    sentence("Otra vez, por favor.", "Again, please.", "otra vez = another time", "A1::sentences A1::expresiones"),
    sentence("Poco a poco.", "Little by little.", "the language learner's motto", "A1::sentences A1::expresiones"),
    sentence("¡Buen provecho!", "Enjoy your meal!", "said before eating", "A1::sentences A1::expresiones"),
]


TOPICS = [
    # ---- talking about the weather --------------------------------------
    vocab("It's sunny and it's twenty-five degrees.", "Hace sol y estamos a veinticinco grados.", "both at once: impersonal hace + noun, and estar a + temperature (literally we are at)", "A1::topics A1::clima"),
    vocab("Today it's five degrees below zero.", "Hoy estamos a cinco grados bajo cero.", "bajo cero = below zero &middot; estar a puts us on the thermometer: Spanish says we where English says it", "A1::topics A1::clima"),
    vocab("In Stockholm it's ten degrees below zero.", "En Estocolmo hace diez grados bajo cero.", "hace + degrees is the fully impersonal alternative to estamos a - both are correct", "A1::topics A1::clima"),
    vocab("Today's high is twenty-eight degrees.", "La máxima de hoy es de veintiocho grados.", "la máxima / la mínima &middot; measurements take ser de", "A1::topics A1::clima"),
    vocab("What's the temperature?", "¿A cuántos grados estamos?", "lit. at how many degrees are we", "A1::topics A1::clima"),
    vocab("It's three degrees above zero.", "Estamos a tres grados sobre cero.", "sobre cero = above zero &middot; the same estamos a as with dates: estamos a 15 de mayo", "A1::topics A1::clima"),
    vocab("Today it's colder than yesterday.", "Hoy hace más frío que ayer.", "más frío que = colder than", "A1::topics A1::clima"),
    vocab("It's cloudy but it isn't cold.", "Está nublado pero no hace frío.", "estar + adjective vs hacer + noun, side by side", "A1::topics A1::clima"),
    vocab("It's foggy and very windy.", "Hay niebla y hace mucho viento.", "hay + noun vs hacer + noun &middot; mucho viento, not muy viento", "A1::topics A1::clima"),
    vocab("Tomorrow it's going to snow.", "Mañana va a nevar.", "nevar is impersonal - always third person singular", "A1::topics A1::clima"),

    # ---- numbers 0-100 ---------------------------------------------------
    vocab("The score is two to zero.", "El resultado es dos a cero.", "cero = zero", "A1::topics A1::numeros-100"),
    vocab("There are fifteen students in the class.", "Hay quince estudiantes en la clase.", "11-15 are one word: once, doce, trece, catorce, quince", "A1::topics A1::numeros-100"),
    vocab("My brother is sixteen years old.", "Mi hermano tiene dieciséis años.", "16-19 contract: dieciséis, diecisiete...", "A1::topics A1::numeros-100"),
    vocab("There are twenty-one days left.", "Quedan veintiún días.", "veintiuno drops to veintiún before a masculine noun", "A1::topics A1::numeros-100"),
    vocab("She has thirty-one books.", "Tiene treinta y un libros.", "from 31 up it's three words, and uno &rarr; un", "A1::topics A1::numeros-100"),
    vocab("There are thirty-one girls at the school.", "Hay treinta y una chicas en el colegio.", "feminine noun &rarr; treinta y una", "A1::topics A1::numeros-100"),
    vocab("I work forty hours a week.", "Trabajo cuarenta horas por semana.", "cuarenta = 40", "A1::topics A1::numeros-100"),
    vocab("There are fifty people at the party.", "Hay cincuenta personas en la fiesta.", "cincuenta = 50", "A1::topics A1::numeros-100"),
    vocab("I need seventy-five euros.", "Necesito setenta y cinco euros.", "setenta y cinco = 75", "A1::topics A1::numeros-100"),
    vocab("My grandfather is eighty-seven.", "Mi abuelo tiene ochenta y siete años.", "ochenta y siete = 87", "A1::topics A1::numeros-100"),

    # ---- numbers 100 to a million ----------------------------------------
    vocab("The flight costs one hundred euros.", "El vuelo cuesta cien euros.", "exactly 100 before a noun is cien, never ciento", "A1::topics A1::numeros-grandes"),
    vocab("There are one hundred and twenty people.", "Hay ciento veinte personas.", "101-199 use ciento, and there is no y after it", "A1::topics A1::numeros-grandes"),
    vocab("The hotel has two hundred rooms.", "El hotel tiene doscientas habitaciones.", "the hundreds agree in gender: doscientas habitaciones", "A1::topics A1::numeros-grandes"),
    vocab("This book has five hundred pages.", "Este libro tiene quinientas páginas.", "500 is quinientos, not 'cincocientos'", "A1::topics A1::numeros-grandes"),
    vocab("The car costs seven hundred euros.", "El coche cuesta setecientos euros.", "700 is setecientos, not 'sietecientos'", "A1::topics A1::numeros-grandes"),
    vocab("There are nine hundred students.", "Hay novecientos estudiantes.", "900 is novecientos, not 'nuevecientos'", "A1::topics A1::numeros-grandes"),
    vocab("I earn one thousand five hundred euros a month.", "Gano mil quinientos euros al mes.", "mil stands alone - never un mil", "A1::topics A1::numeros-grandes"),
    vocab("The town has two thousand inhabitants.", "El pueblo tiene dos mil habitantes.", "mil never pluralises as a number: dos mil", "A1::topics A1::numeros-grandes"),
    vocab("The house costs three hundred thousand euros.", "La casa cuesta trescientos mil euros.", "trescientos mil = 300,000", "A1::topics A1::numeros-grandes"),
    vocab("Madrid has more than three million inhabitants.", "Madrid tiene más de tres millones de habitantes.", "millón/millones always takes de before the noun", "A1::topics A1::numeros-grandes"),

    # ---- time of day -----------------------------------------------------
    vocab("It's a quarter past four.", "Son las cuatro y cuarto.", "y cuarto = quarter past", "A1::topics A1::hora"),
    vocab("It's ten to eight.", "Son las ocho menos diez.", "menos + minutes counts back from the next hour", "A1::topics A1::hora"),
    vocab("It's exactly six o'clock.", "Son las seis en punto.", "en punto = on the dot", "A1::topics A1::hora"),
    vocab("It's midday.", "Es mediodía.", "singular es, and no article", "A1::topics A1::hora"),
    vocab("It's midnight.", "Es medianoche.", "singular es, like es la una", "A1::topics A1::hora"),
    vocab("The shop opens at nine thirty.", "La tienda abre a las nueve y media.", "a las + hour for 'at'", "A1::topics A1::hora"),
    vocab("The film starts at eight in the evening.", "La película empieza a las ocho de la tarde.", "la tarde runs until about 9pm in Spain", "A1::topics A1::hora"),
    vocab("See you at half past one.", "Nos vemos a la una y media.", "a la una - singular, because it's one o'clock", "A1::topics A1::hora"),
    vocab("It's almost three o'clock.", "Son casi las tres.", "casi goes before las", "A1::topics A1::hora"),
    vocab("The bus arrives in twenty minutes.", "El autobús llega en veinte minutos.", "en + time = in (how long from now)", "A1::topics A1::hora"),

    # ---- at the cafe or restaurant ---------------------------------------
    vocab("A coffee with milk, please.", "Un café con leche, por favor.", "the default coffee order in Spain", "A1::topics A1::cafe"),
    vocab("Can we sit on the terrace?", "¿Podemos sentarnos en la terraza?", "sentarse = to sit down; la terraza = outdoor seating", "A1::topics A1::cafe"),
    vocab("Could we order, please?", "¿Podemos pedir, por favor?", "pedir = to order; e &rarr; i", "A1::topics A1::cafe"),
    vocab("What's the dish of the day?", "¿Cuál es el plato del día?", "el plato del día = daily special", "A1::topics A1::cafe"),
    vocab("I'll have the same.", "Para mí lo mismo.", "lo mismo = the same thing", "A1::topics A1::cafe"),
    vocab("Is there a set menu?", "¿Hay menú del día?", "menú del día = fixed-price lunch, usually three courses", "A1::topics A1::cafe"),
    vocab("Could you bring a little more water?", "¿Me pone un poco más de agua?", "me pone = the standard way to order in Spain", "A1::topics A1::cafe"),
    vocab("We're going to share a dessert.", "Vamos a compartir un postre.", "compartir = to share", "A1::topics A1::cafe"),
    vocab("Can we pay separately?", "¿Podemos pagar por separado?", "por separado = separately", "A1::topics A1::cafe"),
    vocab("Everything is delicious, thank you.", "Todo está buenísimo, gracias.", "-ísimo = really, extremely", "A1::topics A1::cafe"),

    # ---- time expressions ------------------------------------------------
    vocab("I'm coming right now!", "¡Voy ahora mismo!", "ahora = now &middot; mismo sharpens it to right now, this very moment", "A1::topics A1::expresiones-tiempo"),
    vocab("The waiter brings the bill straight away.", "El camarero trae la cuenta enseguida.", "enseguida = immediately, in a moment (also spelt en seguida)", "A1::topics A1::expresiones-tiempo"),
    vocab("Summer arrives soon.", "El verano llega pronto.", "pronto = soon &middot; it can also mean early: me levanto pronto", "A1::topics A1::expresiones-tiempo"),
    vocab("First I have breakfast and then I have a shower.", "Primero desayuno y después me ducho.", "primero... después = first... then, for putting a routine in order", "A1::topics A1::expresiones-tiempo"),
    vocab("I study in the morning.", "Estudio por la mañana.", "por la mañana with no clock time &middot; with a time it's de: a las ocho de la mañana", "A1::topics A1::expresiones-tiempo"),
    vocab("In the afternoon I work and at night I rest.", "Por la tarde trabajo y por la noche descanso.", "por la tarde / por la noche &middot; la tarde lasts until dinner, around 9pm in Spain", "A1::topics A1::expresiones-tiempo"),
    vocab("I always drink coffee with milk.", "Siempre bebo café con leche.", "siempre usually goes before the verb", "A1::topics A1::expresiones-tiempo"),
    vocab("I never eat meat.", "Nunca como carne.", "nunca before the verb needs no no &middot; after it, it does: no como carne nunca", "A1::topics A1::expresiones-tiempo"),
    vocab("Sometimes I walk to work.", "A veces voy al trabajo a pie.", "a veces = sometimes (vez &rarr; veces) &middot; a pie = on foot", "A1::topics A1::expresiones-tiempo"),
    vocab("I speak Spanish every day.", "Hablo español todos los días.", "todos los días = every day, plural with the article &middot; cada día also works", "A1::topics A1::expresiones-tiempo"),

    # ---- school subjects -------------------------------------------------
    vocab("What subjects do you have today?", "¿Qué asignaturas tienes hoy?", "la asignatura = school subject", "A1::topics A1::asignaturas"),
    vocab("On Mondays I have maths.", "Los lunes tengo matemáticas.", "las matemáticas is plural &middot; los lunes = on Mondays (every week)", "A1::topics A1::asignaturas"),
    vocab("History is very interesting.", "La historia es muy interesante.", "a subject as the subject of the sentence takes the article: la historia", "A1::topics A1::asignaturas"),
    vocab("Physical education is my favourite subject.", "La educación física es mi asignatura favorita.", "favorita agrees with asignatura, not with the sport", "A1::topics A1::asignaturas"),
    vocab("I study French at school.", "Estudio francés en el colegio.", "languages are lowercase and take no article after estudiar", "A1::topics A1::asignaturas"),
    vocab("My English teacher is from London.", "Mi profesor de inglés es de Londres.", "profesor de + subject = the teacher of that subject", "A1::topics A1::asignaturas"),
    vocab("The Spanish class starts at nine.", "La clase de español empieza a las nueve.", "la clase de español &middot; empezar e &rarr; ie", "A1::topics A1::asignaturas"),
    vocab("Philosophy is difficult, but I like it.", "La filosofía es difícil, pero me gusta.", "gusta singular because la filosofía is one thing", "A1::topics A1::asignaturas"),
    vocab("I like maths, but I don't like history.", "Me gustan las matemáticas, pero no me gusta la historia.", "gustan for the plural matemáticas, gusta for la historia", "A1::topics A1::asignaturas"),
    vocab("Break is at eleven.", "El recreo es a las once.", "el recreo = break / playtime &middot; events take ser + a las", "A1::topics A1::asignaturas"),

    # ---- gustar when you name the person ---------------------------------
    vocab("My friends like music.", "A mis amigos les gusta la música.", "naming the person takes both halves: a + person, and the pronoun stays &middot; les matches mis amigos, gusta matches la música", "A1::topics A1::gustar-personas"),
    vocab("Ana likes coffee.", "A Ana le gusta el café.", "one person &rarr; le &middot; a Ana, never just Ana", "A1::topics A1::gustar-personas"),
    vocab("My parents like to travel.", "A mis padres les gusta viajar.", "les for the people, gusta for the infinitive (an infinitive counts as singular)", "A1::topics A1::gustar-personas"),
    vocab("I like this restaurant.", "A mí me gusta este restaurante.", "a mí adds emphasis (I'm the one who likes it) &middot; me still can't be dropped", "A1::topics A1::gustar-personas"),
    vocab("Do you like Spanish films?", "¿A ti te gustan las películas españolas?", "a plural thing &rarr; gustan, whoever is doing the liking", "A1::topics A1::gustar-personas"),
    vocab("My brother doesn't like fish.", "A mi hermano no le gusta el pescado.", "no goes before the pronoun: no le gusta", "A1::topics A1::gustar-personas"),
    vocab("The children like animals.", "A los niños les gustan los animales.", "plural people &rarr; les, plural thing &rarr; gustan: both change here", "A1::topics A1::gustar-personas"),
    vocab("My sister likes dogs, but I don't.", "A mi hermana le gustan los perros, pero a mí no.", "a mí no is the whole answer - the verb isn't repeated", "A1::topics A1::gustar-personas"),
    vocab("Everyone likes the beach.", "A todos les gusta la playa.", "todos is plural &rarr; les", "A1::topics A1::gustar-personas"),
    vocab("Who likes chocolate?", "¿A quién le gusta el chocolate?", "even a question word takes a + le", "A1::topics A1::gustar-personas"),
    vocab("Do you all like the book?", "¿Os gusta el libro?", "os = to you all, the vosotros pronoun &middot; you'll hear it constantly in Spain and almost never in Latin America", "A1::topics A1::gustar-personas"),
    vocab("Do you all like Spanish films?", "¿Os gustan las películas españolas?", "os + gustan because películas is plural &middot; the pronoun never changes for the number of things", "A1::topics A1::gustar-personas"),
    vocab("We like playing the guitar.", "Nos gusta tocar la guitarra.", "an infinitive counts as one thing &rarr; gusta, even with two verbs after it", "A1::topics A1::gustar-personas"),
    vocab("We don't like getting up early.", "No nos gusta levantarnos temprano.", "the infinitive keeps its own reflexive pronoun: levantarnos, matching nos", "A1::topics A1::gustar-personas"),
    vocab("Do you like cats?", "¿Te gustan los gatos?", "te + gustan &middot; Spanish keeps the article: los gatos, not just gatos", "A1::topics A1::gustar-personas"),
    vocab("What do you like doing at weekends?", "¿Qué te gusta hacer los fines de semana?", "qué + te gusta + infinitive &middot; gusta stays singular whatever follows it", "A1::topics A1::gustar-personas"),
    vocab("You don't like fish, do you?", "No te gusta el pescado, ¿verdad?", "¿verdad? is the all-purpose tag question &middot; ¿no? works the same", "A1::topics A1::gustar-personas"),
    vocab("We really like this bar.", "Nos gusta mucho este bar.", "mucho follows the verb and never becomes muy here", "A1::topics A1::gustar-personas"),
    vocab("We don't like the cold.", "No nos gusta el frío.", "an abstract noun keeps its article: el frío, not just frío", "A1::topics A1::gustar-personas"),
    vocab("Do you all like paella?", "¿Os gusta la paella?", "os for a group you'd each call tú &middot; in Latin America this would be ¿les gusta?", "A1::topics A1::gustar-personas"),
    vocab("You all like travelling, don't you?", "Os gusta viajar, ¿verdad?", "os + infinitive &rarr; gusta, singular", "A1::topics A1::gustar-personas"),
    vocab("Did you all like the film?", "¿Os ha gustado la película?", "the perfecto of gustar: ha gustado agrees with la película, never with os", "A1::topics A1::gustar-personas"),
    vocab("What do you all like doing?", "¿Qué os gusta hacer?", "the same shape as ¿qué te gusta hacer?, one pronoun along", "A1::topics A1::gustar-personas"),
    vocab("He likes football, but she doesn't.", "A él le gusta el fútbol, pero a ella no.", "a él and a ella both take le - the a-phrase says who, the pronoun is still required", "A1::topics A1::gustar-personas"),
    vocab("We like the beach. How about you lot?", "A nosotros nos gusta la playa. ¿Y a vosotros?", "a nosotros / a vosotros &middot; a short question needs only the a-phrase: ¿y a vosotros?", "A1::topics A1::gustar-personas"),
    vocab("They like Spanish food.", "A ellos les gusta la comida española.", "a ellos + les &middot; drop the a-phrase and les gusta still works", "A1::topics A1::gustar-personas"),
    vocab("I do, you don't.", "A mí sí, a ti no.", "mí carries an accent to keep it apart from mi (my); ti never does, because there is no other ti", "A1::topics A1::gustar-personas"),
    vocab("Do you like wine, sir?", "¿A usted le gusta el vino?", "usted takes le, like él and ella - the verb is third person however polite you're being", "A1::topics A1::gustar-personas"),
    vocab("I like it, but my brother doesn't.", "A mí me gusta, pero a mi hermano no.", "both in one sentence: a mí with an accent (to me), a mi hermano without (my brother)", "A1::topics A1::gustar-personas"),

    # ---- years and dates -------------------------------------------------
    vocab("I was born in 1985.", "Nací en mil novecientos ochenta y cinco.", "a year is read as one whole number, never split in two like nineteen eighty-five &middot; nacer = to be born", "A1::topics A1::fechas"),
    vocab("She was born in 1995.", "Nació en mil novecientos noventa y cinco.", "mil stands alone: never un mil", "A1::topics A1::fechas"),
    vocab("What year were you born?", "¿En qué año naciste?", "en qué año &middot; naciste = you were born", "A1::topics A1::fechas"),
    vocab("In the year 2000 I lived in Madrid.", "En el año dos mil viví en Madrid.", "2000 = dos mil &middot; el año is usual before a round year", "A1::topics A1::fechas"),
    vocab("We're in 2025.", "Estamos en dos mil veinticinco.", "estamos en + year, the same estamos as with dates and temperatures", "A1::topics A1::fechas"),
    vocab("Columbus arrived in 1492.", "Colón llegó en mil cuatrocientos noventa y dos.", "the 1400s start with mil cuatrocientos &middot; en + year, with no article", "A1::topics A1::fechas"),
    vocab("I have lived here since 2019.", "Vivo aquí desde dos mil diecinueve.", "desde + year &middot; the plain present covers English's have lived", "A1::topics A1::fechas"),
    vocab("The course starts in 2026.", "El curso empieza en dos mil veintiséis.", "dos mil veintiséis &middot; veintiséis keeps its accent", "A1::topics A1::fechas"),
    vocab("My daughter was born on the 3rd of May 2010.", "Mi hija nació el tres de mayo de dos mil diez.", "a full date is el + number + de + month + de + year &middot; months are lowercase", "A1::topics A1::fechas"),
    vocab("In the nineties there was no internet.", "En los años noventa no había internet.", "los años noventa = the nineties &middot; había = there was / there were", "A1::topics A1::fechas"),

    # ---- object pronouns in use ------------------------------------------
    vocab("Do you see the book? - Yes, I see it.", "¿Ves el libro? - Sí, lo veo.", "lo stands in for el libro &middot; the pronoun goes before the verb", "A1::topics A1::pronombres-objeto"),
    vocab("Do you have the keys? - Yes, I have them.", "¿Tienes las llaves? - Sí, las tengo.", "las llaves is feminine plural &rarr; las", "A1::topics A1::pronombres-objeto"),
    vocab("Do you buy the newspaper? - Yes, I buy it every day.", "¿Compras el periódico? - Sí, lo compro todos los días.", "lo = el periódico &middot; it never disappears the way English drops it", "A1::topics A1::pronombres-objeto"),
    vocab("I don't know her.", "No la conozco.", "no goes first, then the pronoun, then the verb", "A1::topics A1::pronombres-objeto"),
    vocab("She calls me every Sunday.", "Me llama todos los domingos.", "me = me &middot; still in front of the verb", "A1::topics A1::pronombres-objeto"),
    vocab("Do you eat meat? - No, I don't eat it.", "¿Comes carne? - No, no la como.", "la = la carne &middot; the gender comes from the noun, not from the thing", "A1::topics A1::pronombres-objeto"),
    vocab("Do you know my sister? - Yes, I know her.", "¿Conoces a mi hermana? - Sí, la conozco.", "the personal a in the question, la for her in the answer", "A1::topics A1::pronombres-objeto"),
    vocab("I'm going to do it tomorrow.", "Voy a hacerlo mañana.", "with an infinitive you may also say lo voy a hacer - both are correct", "A1::topics A1::pronombres-objeto"),
    vocab("Can you call me tomorrow?", "¿Puedes llamarme mañana?", "attached to the infinitive: llamarme &middot; ¿me puedes llamar? works just as well", "A1::topics A1::pronombres-objeto"),
    vocab("I don't want to see it.", "No quiero verlo.", "no + conjugated verb, and the pronoun rides on the infinitive", "A1::topics A1::pronombres-objeto"),
    vocab("Where are the tickets? I don't have them.", "¿Dónde están las entradas? No las tengo.", "la entrada = ticket &middot; las tengo, never tengo las", "A1::topics A1::pronombres-objeto"),
    vocab("I give him the book.", "Le doy el libro.", "le is for the person receiving it", "A1::topics A1::pronombres-objeto"),
    vocab("I give it to him.", "Se lo doy.", "le + lo is impossible, so le becomes se: se lo doy", "A1::topics A1::pronombres-objeto"),
    vocab("They invite us to the party.", "Nos invitan a la fiesta.", "nos = us", "A1::topics A1::pronombres-objeto"),
    vocab("I'm listening to you.", "Te escucho.", "escuchar takes the object directly: no a, no to", "A1::topics A1::pronombres-objeto"),
    vocab("I always tell her the truth.", "Siempre le digo la verdad.", "le = to her &middot; decir takes the person as le, the thing as the object", "A1::topics A1::pronombres-objeto"),
    vocab("The teacher explains the lesson to us.", "El profesor nos explica la lección.", "nos = to us &middot; explicar works like decir", "A1::topics A1::pronombres-objeto"),
    vocab("I'm buying you a present.", "Te compro un regalo.", "te = for you &middot; Spanish needs no word for for here", "A1::topics A1::pronombres-objeto"),
    vocab("She writes to them every week.", "Les escribe todas las semanas.", "les = to them, even though the people aren't named", "A1::topics A1::pronombres-objeto"),
    vocab("Can you lend me ten euros?", "¿Me prestas diez euros?", "prestar = to lend &middot; me = to me", "A1::topics A1::pronombres-objeto"),
    vocab("My parents send us money.", "Mis padres nos mandan dinero.", "mandar / enviar = to send", "A1::topics A1::pronombres-objeto"),

    # ---- where things are -------------------------------------------------
    vocab("The book is on the table.", "El libro está encima de la mesa.", "encima de = on top of &middot; sobre la mesa works too", "A1::topics A1::lugar"),
    vocab("The cat is under the chair.", "El gato está debajo de la silla.", "debajo de = under", "A1::topics A1::lugar"),
    vocab("The pharmacy is next to the bank.", "La farmacia está al lado del banco.", "al lado de + el &rarr; del", "A1::topics A1::lugar"),
    vocab("The supermarket is opposite the school.", "El supermercado está enfrente del colegio.", "enfrente de = opposite, facing", "A1::topics A1::lugar"),
    vocab("My house is between the park and the church.", "Mi casa está entre el parque y la iglesia.", "entre takes no de", "A1::topics A1::lugar"),
    vocab("The car is in front of the house.", "El coche está delante de la casa.", "delante de = in front of", "A1::topics A1::lugar"),
    vocab("The garden is behind the house.", "El jardín está detrás de la casa.", "detrás de = behind", "A1::topics A1::lugar"),
    vocab("The bathroom is at the end of the corridor.", "El baño está al final del pasillo.", "al final de = at the end of &middot; el pasillo = corridor", "A1::topics A1::lugar"),
    vocab("The station is far from the centre.", "La estación está lejos del centro.", "lejos de &harr; cerca de", "A1::topics A1::lugar"),
    vocab("The keys are inside the bag.", "Las llaves están dentro del bolso.", "dentro de = inside &middot; el bolso = bag", "A1::topics A1::lugar"),
    vocab("The children are outside.", "Los niños están fuera.", "fuera on its own needs no de", "A1::topics A1::lugar"),
    vocab("Is there a pharmacy near here?", "¿Hay una farmacia por aquí cerca?", "hay to ask whether something exists &middot; por aquí cerca = round here", "A1::topics A1::lugar"),

    # ---- health ------------------------------------------------------------
    vocab("My head hurts.", "Me duele la cabeza.", "doler works backwards like gustar &middot; la cabeza, not mi cabeza", "A1::topics A1::salud"),
    vocab("My feet hurt.", "Me duelen los pies.", "a plural body part &rarr; duelen", "A1::topics A1::salud"),
    vocab("I have a sore throat.", "Me duele la garganta.", "Spanish says the throat hurts me", "A1::topics A1::salud"),
    vocab("My stomach hurts.", "Me duele el estómago.", "el estómago keeps its accent", "A1::topics A1::salud"),
    vocab("I have a temperature.", "Tengo fiebre.", "tener + fiebre, with no article", "A1::topics A1::salud"),
    vocab("I have a cold.", "Estoy resfriado/a.", "estar for a passing state &middot; resfriada if you're female", "A1::topics A1::salud"),
    vocab("I don't feel well.", "No me encuentro bien.", "encontrarse = to feel &middot; no me siento bien also works", "A1::topics A1::salud"),
    vocab("How are you feeling?", "¿Cómo te encuentras?", "the everyday question when someone is ill", "A1::topics A1::salud"),
    vocab("What's wrong?", "¿Qué te pasa?", "lit. what happens to you", "A1::topics A1::salud"),
    vocab("I need to go to the doctor.", "Necesito ir al médico.", "ir al médico = to go to the doctor's", "A1::topics A1::salud"),

    # ---- colours -----------------------------------------------------------
    vocab("I have a red car.", "Tengo un coche rojo.", "the colour follows the noun and agrees with it", "A1::topics A1::colores"),
    vocab("She's wearing a white shirt.", "Lleva una camisa blanca.", "blanco &rarr; blanca for a feminine noun", "A1::topics A1::colores"),
    vocab("I have two white cats.", "Tengo dos gatos blancos.", "masculine plural: blancos", "A1::topics A1::colores"),
    vocab("The walls are green.", "Las paredes son verdes.", "verde has no separate feminine: just add -s", "A1::topics A1::colores"),
    vocab("I like blue shoes.", "Me gustan los zapatos azules.", "azul &rarr; azules &middot; gustan for a plural thing", "A1::topics A1::colores"),
    vocab("The house is grey.", "La casa es gris.", "gris is the same for both genders", "A1::topics A1::colores"),
    vocab("I want a brown coat.", "Quiero un abrigo marrón.", "marrón &rarr; marrones in the plural", "A1::topics A1::colores"),
    vocab("The black trousers are on the bed.", "Los pantalones negros están encima de la cama.", "pantalones is plural in Spanish &rarr; negros", "A1::topics A1::colores"),
    vocab("My favourite colour is yellow.", "Mi color favorito es el amarillo.", "a colour on its own takes el: el amarillo", "A1::topics A1::colores"),
    vocab("What colour is your car?", "¿De qué color es tu coche?", "de qué color, with de", "A1::topics A1::colores"),
    vocab("What's your favourite colour?", "¿Cuál es tu color favorito?", "cuál + ser to pick one out of a set", "A1::topics A1::colores"),
    vocab("I want an orange T-shirt.", "Quiero una camiseta naranja.", "colours borrowed from fruit don't agree: naranja, rosa and violeta stay as they are", "A1::topics A1::colores"),
    vocab("She has pink shoes.", "Tiene unos zapatos rosa.", "rosa doesn't change for number either &middot; zapatos rosas is heard, but rosa is the careful form", "A1::topics A1::colores"),
    vocab("The purple flowers are beautiful.", "Las flores moradas son bonitas.", "morado agrees like any other adjective &middot; violeta, the other word for purple, does not", "A1::topics A1::colores"),
    vocab("The red door is open.", "La puerta roja está abierta.", "rojo &rarr; roja for a feminine noun &middot; estar for the state of being open", "A1::topics A1::colores"),
    vocab("The yellow houses are old.", "Las casas amarillas son viejas.", "amarillo has all four forms: amarillo, amarilla, amarillos, amarillas", "A1::topics A1::colores"),
    vocab("I like light blue.", "Me gusta el azul claro.", "claro = light, oscuro = dark &middot; el azul claro as a noun takes el", "A1::topics A1::colores"),
    vocab("He has dark green eyes.", "Tiene los ojos verde oscuro.", "claro and oscuro freeze the colour: verde oscuro, never verdes oscuros &middot; Spanish says los ojos, not sus ojos", "A1::topics A1::colores"),

    # ---- colloquial Spain ------------------------------------------------

    # ---- describing people -----------------------------------------------
    vocab("My brother is married.", "Mi hermano está casado.", "estar for marital status &middot; ser casado is also heard, estar is safer", "A1::topics A1::personas"),
    vocab("My sister is single.", "Mi hermana es soltera.", "soltero / soltera agrees &middot; both ser and estar are used here", "A1::topics A1::personas"),
    vocab("He's dark-haired and tall.", "Es moreno y alto.", "moreno covers dark hair and dark skin &middot; ser for what someone is like", "A1::topics A1::personas"),
    vocab("My mother is fair-haired.", "Mi madre es rubia.", "rubio &rarr; rubia &middot; never una rubia unless you mean a blonde woman", "A1::topics A1::personas"),
    vocab("Our neighbour is very kind.", "Nuestro vecino es muy amable.", "amable has one form for both genders", "A1::topics A1::personas"),
    vocab("His girlfriend is really intelligent.", "Su novia es muy inteligente.", "inteligente, also one form for both &middot; su = his, her or their", "A1::topics A1::personas"),
    vocab("Your sister is very pretty.", "Tu hermana es muy guapa.", "guapo / guapa works for men and women alike in Spain", "A1::topics A1::personas"),
    vocab("What's he like?", "¿Cómo es?", "ser asks about character; ¿cómo está? asks how he's feeling", "A1::topics A1::personas"),
    vocab("He has a beard.", "Tiene barba.", "tener for features, with no article: tiene barba, tiene bigote", "A1::topics A1::personas"),
    vocab("He has long dark hair.", "Tiene el pelo largo y moreno.", "el pelo, not su pelo &middot; moreno describes hair as well as a person", "A1::topics A1::personas"),

    # ---- feelings ----------------------------------------------------------
    vocab("I'm sad today.", "Hoy estoy triste.", "estar for how you feel &middot; triste has one form for both genders", "A1::topics A1::sentimientos"),
    vocab("My boss is angry.", "Mi jefe está enfadado.", "enfadado in Spain, enojado in Latin America &middot; el jefe = boss", "A1::topics A1::sentimientos"),
    vocab("I'm worried about the exam.", "Estoy preocupado por el examen.", "preocupado por + what worries you", "A1::topics A1::sentimientos"),
    vocab("We're surprised.", "Estamos sorprendidos.", "the adjective agrees with us: sorprendidos", "A1::topics A1::sentimientos"),
    vocab("I fancy a coffee.", "Me apetece un café.", "apetecer works backwards like gustar &middot; the single most Spanish way to say you want something", "A1::topics A1::sentimientos"),
    vocab("Do you fancy going out tonight?", "¿Te apetece salir esta noche?", "te apetece + infinitive &middot; the standard way to invite someone", "A1::topics A1::sentimientos"),
    vocab("I feel like travelling.", "Tengo ganas de viajar.", "tener ganas de + infinitive = to feel like &middot; stronger than me apetece", "A1::topics A1::sentimientos"),
    vocab("The film is boring. I'm bored.", "La película es aburrida. Estoy aburrido.", "the ser/estar pair that changes the meaning: es aburrido = boring, está aburrido = bored", "A1::topics A1::sentimientos"),
    vocab("I'm scared of dogs.", "Tengo miedo a los perros.", "tener miedo a (or de) &middot; fear is something you have, not something you are", "A1::topics A1::sentimientos"),
    vocab("Are you all right? You look worried.", "¿Estás bien? Pareces preocupado.", "parecer + adjective to say how someone looks", "A1::topics A1::sentimientos"),

    # ---- the body ----------------------------------------------------------
    vocab("My arm hurts.", "Me duele el brazo.", "one arm &rarr; duele &middot; el brazo, never mi brazo", "A1::topics A1::cuerpo"),
    vocab("My legs hurt after running.", "Me duelen las piernas después de correr.", "two legs &rarr; duelen &middot; después de + infinitive", "A1::topics A1::cuerpo"),
    vocab("My back hurts from the computer.", "Me duele la espalda del ordenador.", "la espalda = back &middot; de + el contracts to del", "A1::topics A1::cuerpo"),
    vocab("My eyes hurt from the screen.", "Me duelen los ojos de la pantalla.", "la pantalla = screen", "A1::topics A1::cuerpo"),
    vocab("The human body.", "El cuerpo humano.", "el cuerpo &middot; the adjective follows the noun", "A1::topics A1::cuerpo"),
    vocab("I need medicine for my throat.", "Necesito medicina para la garganta.", "medicina with no article after necesito", "A1::topics A1::cuerpo"),
    vocab("The doctor has given me a prescription.", "El médico me ha dado una receta.", "la receta is both a prescription and a recipe &middot; ha dado, the perfecto", "A1::topics A1::cuerpo"),
    vocab("I wash my hands before eating.", "Me lavo las manos antes de comer.", "the reflexive carries the my: me lavo las manos, not mis manos", "A1::topics A1::cuerpo"),

    # ---- shopping and paying ----------------------------------------------
    vocab("How much is it altogether?", "¿Cuánto es todo?", "¿cuánto es? at the till; ¿cuánto cuesta? about one item", "A1::topics A1::compras-dinero"),
    vocab("The price is too high.", "El precio es demasiado alto.", "el precio &middot; demasiado = too much", "A1::topics A1::compras-dinero"),
    vocab("I'd like a white coffee, please.", "Quisiera un café con leche, por favor.", "quisiera is the polite I would like &middot; softer than quiero", "A1::topics A1::compras-dinero"),
    vocab("Can I pay by card?", "¿Puedo pagar con tarjeta?", "con tarjeta, with no article", "A1::topics A1::compras-dinero"),
    vocab("I'll pay cash.", "Pago en efectivo.", "en efectivo = in cash &middot; the present tense does the job of I'll", "A1::topics A1::compras-dinero"),
    vocab("There's a twenty percent discount.", "Hay un descuento del veinte por ciento.", "un descuento del + number &middot; por ciento = percent", "A1::topics A1::compras-dinero"),
    vocab("The sales start in January.", "Las rebajas empiezan en enero.", "las rebajas, always plural &middot; months are lowercase", "A1::topics A1::compras-dinero"),
    vocab("Can I try it on?", "¿Puedo probármelo?", "probarse + lo, both stuck on the infinitive &middot; ¿me lo puedo probar? works too", "A1::topics A1::compras-dinero"),

    # ---- quantities --------------------------------------------------------
    vocab("A litre of milk, please.", "Un litro de leche, por favor.", "quantity + de + the thing, with no article", "A1::topics A1::cantidades"),
    vocab("A bottle of water.", "Una botella de agua.", "agua is feminine but takes el: el agua, una botella de agua", "A1::topics A1::cantidades"),
    vocab("A packet of biscuits.", "Un paquete de galletas.", "las galletas = biscuits", "A1::topics A1::cantidades"),
    vocab("A tin of tomatoes.", "Una lata de tomates.", "la lata = tin &middot; also what you call something annoying: ¡qué lata!", "A1::topics A1::cantidades"),
    vocab("Half a kilo of cheese.", "Medio kilo de queso.", "medio, with no un in front", "A1::topics A1::cantidades"),
    vocab("Two beers, please.", "Dos cañas, por favor.", "una caña is a small draught beer, the default order in a Spanish bar", "A1::topics A1::cantidades"),
    vocab("I'm going to the bakery.", "Voy a la panadería.", "the -ería ending names the shop: panadería, frutería, librería", "A1::topics A1::cantidades"),

    # ---- nature ------------------------------------------------------------
    vocab("There are birds in the tree.", "Hay pájaros en el árbol.", "el árbol &rarr; los árboles &middot; hay for existence", "A1::topics A1::naturaleza"),
    vocab("We're going to the mountains this weekend.", "Vamos a la montaña este fin de semana.", "la montaña, singular, where English uses the plural", "A1::topics A1::naturaleza"),
    vocab("The sky is very blue today.", "Hoy el cielo está muy azul.", "estar because it's how the sky looks today", "A1::topics A1::naturaleza"),
    vocab("Mallorca is an island.", "Mallorca es una isla.", "la isla &middot; ser for what something permanently is", "A1::topics A1::naturaleza"),
    vocab("I like walking in the countryside.", "Me gusta pasear por el campo.", "pasear = to stroll &middot; por = around, through", "A1::topics A1::naturaleza"),
    vocab("The flowers in the garden are beautiful.", "Las flores del jardín son preciosas.", "de + el = del &middot; precioso is stronger than bonito", "A1::topics A1::naturaleza"),

    # ---- phone and computer ------------------------------------------------
    vocab("I'll send you a message.", "Te mando un mensaje.", "mandar or enviar &middot; the present covers I'll", "A1::topics A1::tecnologia"),
    vocab("The screen is broken.", "La pantalla está rota.", "estar for the state &middot; roto / rota from romper", "A1::topics A1::tecnologia"),
    vocab("I'm going to download the app.", "Voy a descargar la aplicación.", "descargar = to download &middot; la app is said too", "A1::topics A1::tecnologia"),
    vocab("Can you send me the link?", "¿Me mandas el enlace?", "el enlace = link &middot; el link is also heard", "A1::topics A1::tecnologia"),
    vocab("I turn the computer off at seven.", "Apago el ordenador a las siete.", "apagar &harr; encender &middot; el ordenador in Spain", "A1::topics A1::tecnologia"),
    vocab("My phone won't turn on.", "Mi móvil no se enciende.", "se enciende: the phone turns itself on, so Spanish makes it reflexive", "A1::topics A1::tecnologia"),
    vocab("What's the wifi password?", "¿Cuál es la contraseña del wifi?", "la contraseña &middot; cuál, not qué, to pick out the one you mean", "A1::topics A1::tecnologia"),
    vocab("I've got no battery left.", "No me queda batería.", "quedar again: no me queda = I have none left", "A1::topics A1::tecnologia"),

    # ---- odds and ends the audit turned up ---------------------------------
    vocab("Where's the bus stop?", "¿Dónde está la parada del autobús?", "la parada &middot; de + el = del", "A1::topics A1::varios"),
    vocab("You have to cross the street.", "Tienes que cruzar la calle.", "cruzar &middot; c &rarr; c, but crucé in the past", "A1::topics A1::varios"),
    vocab("What's the train timetable?", "¿Cuál es el horario del tren?", "el horario = timetable, and also working hours", "A1::topics A1::varios"),
    vocab("The salary is good.", "El sueldo es bueno.", "el sueldo = salary &middot; el salario is the formal word", "A1::topics A1::varios"),
    vocab("I get dressed quickly in the morning.", "Me visto rápido por la mañana.", "vestirse: e &rarr; i, me visto, te vistes, se viste", "A1::topics A1::varios"),
    vocab("I need my passport to travel.", "Necesito el pasaporte para viajar.", "el pasaporte, with the article where English says my", "A1::topics A1::varios"),
    vocab("Of course!", "¡Por supuesto!", "also claro and desde luego &middot; all three mean of course", "A1::topics A1::varios"),
    vocab("In my opinion, it's important.", "En mi opinión, es importante.", "en mi opinión &middot; creo que is the everyday alternative", "A1::topics A1::varios"),
    vocab("This app is very useful.", "Esta aplicación es muy útil.", "útil keeps one form for both genders &middot; inútil = useless", "A1::topics A1::varios"),
    vocab("I have a missed call.", "Tengo una llamada perdida.", "la llamada from llamar &middot; perdida = missed, literally lost", "A1::topics A1::varios"),
    vocab("Are you free on Friday?", "¿Estás libre el viernes?", "estar libre = to be free &middot; ser libre is about liberty", "A1::topics A1::varios"),
    vocab("That coat is very fashionable.", "Ese abrigo está muy de moda.", "estar de moda = to be in fashion &middot; la moda = fashion", "A1::topics A1::varios"),
    vocab("That bag is ugly.", "Ese bolso es feo.", "feo &rarr; fea &middot; ese for something near the person you're talking to", "A1::topics A1::varios"),

    vocab("He drives like a maniac.", "Va hecho un fitipaldi.", "from Emerson Fittipaldi, F1 champion in 1972 and 1974, spelt the Spanish way with one t &middot; someone who goes fast, happily and a bit madly - it's affectionate, not a warning", "A1::topics A1::coloquial"),
    vocab("Slow down, you're not a racing driver!", "¡Más despacio, que no eres fitipaldi!", "que opens a friendly reproach and barely translates &middot; más despacio = slower", "A1::topics A1::coloquial"),

    # ---- the school timetable: asking and answering ----------------------
    vocab("What time do you start your first class on Monday?", "¿A qué hora empiezas la primera clase el lunes?", "a qué hora = at what time &middot; el lunes = this coming Monday; los lunes = every Monday", "A1::topics A1::horario"),
    vocab("My first class starts at a quarter past eight.", "Mi primera clase empieza a las ocho y cuarto.", "empezar: e &rarr; ie &middot; y cuarto = quarter past", "A1::topics A1::horario"),
    vocab("How many minutes is one lesson?", "¿Cuántos minutos dura una clase?", "durar = to last, the natural verb here - Spanish asks how long a class lasts, not how many minutes it is", "A1::topics A1::horario"),
    vocab("Each class lasts fifty minutes.", "Cada clase dura cincuenta minutos.", "cada + singular noun, never cada clases", "A1::topics A1::horario"),
    vocab("Which subjects do you have this year?", "¿Qué asignaturas tienes este año?", "qué + noun for which &middot; este año = this year", "A1::topics A1::horario"),
    vocab("How many Spanish classes do you have a week?", "¿Cuántas clases de español tienes a la semana?", "cuántas agrees with clases &middot; a la semana = per week (por semana works too)", "A1::topics A1::horario"),
    vocab("I have three Spanish classes a week.", "Tengo tres clases de español a la semana.", "clase de + subject, and the subject stays lowercase", "A1::topics A1::horario"),
    vocab("Which subject is your favourite?", "¿Cuál es tu asignatura favorita?", "cuál + ser to pick one out of a set &middot; ¿qué asignatura...? also works", "A1::topics A1::horario"),
    vocab("My favourite subject is history.", "Mi asignatura favorita es la historia.", "the subject keeps its article after es: la historia", "A1::topics A1::horario"),
    vocab("What time do you usually finish?", "¿A qué hora terminas normalmente?", "terminar = to finish (acabar works the same) &middot; normalmente sits after the verb", "A1::topics A1::horario"),
    vocab("I usually finish at half past two.", "Normalmente termino a las dos y media.", "normalmente can also open the sentence &middot; y media = half past", "A1::topics A1::horario"),
    vocab("Classes finish at three in the afternoon.", "Las clases terminan a las tres de la tarde.", "de la tarde with a clock time; por la tarde without one", "A1::topics A1::horario"),
]


if __name__ == "__main__":
    total = 0
    total += write("spanish_A1_verbs_anki.tsv", VERBS, PRODUCTION, guard=False)
    EXISTING.update(row[0] for row in VERBS)
    total += write("spanish_A1_vocab_anki.tsv", VOCAB, PRODUCTION)
    total += write("spanish_A1_grammar_anki.tsv", GRAMMAR, PRODUCTION)
    total += write("spanish_A1_sentences_anki.tsv", SENTENCES, COMPREHENSION)
    total += write("spanish_A1_topics_anki.tsv", TOPICS, PRODUCTION)
    total += write("spanish_A2_pasado_anki.tsv", PAST, PRODUCTION)
    total += write("video_leones_anki.tsv", VIDEO_LEONES, COMPREHENSION)
    print(f"total: {total} cards")
