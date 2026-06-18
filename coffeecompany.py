import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json
import os

# ------------------------------------------------------------
# ЦВЕТОВАЯ СХЕМА (гармоничная, тёмная, с терракотовыми акцентами)
# ------------------------------------------------------------
COLORS = {
    "bg_main": "#1a2f1a",
    "bg_tab": "#2b4a2b",
    "card_bg": "#2d2b1f",
    "card_border": "#6b4c3b",
    "btn_plus": "#8b5a2b",
    "btn_plus_hover": "#a06e3e",
    "btn_danger": "#9b2c2c",
    "btn_success": "#2c6e2c",
    "btn_warning": "#b87c2e",
    "cat_active": "#b85c1a",
    "cat_inactive": "#4a3525",
    "text_light": "#f0f0e0",
    "text_dark": "#d0d0c0",
    "price_color": "#d4a017",
    "scrollbar_bg": "#3a2a1a",
    "scrollbar_thumb": "#8b5a2b",
}

# ------------------------------------------------------------
# УПРАВЛЕНИЕ ДАННЫМИ (заказы)
# ------------------------------------------------------------
class DataManager:
    def __init__(self):
        self.orders_file = "orders.json"
        self._load_orders()

    def _load_orders(self):
        if os.path.exists(self.orders_file):
            with open(self.orders_file, "r", encoding="utf-8") as f:
                self.orders = json.load(f)
        else:
            self.orders = []

    def save_orders(self):
        with open(self.orders_file, "w", encoding="utf-8") as f:
            json.dump(self.orders, f, ensure_ascii=False, indent=2)

    def add_order(self, order):
        self.orders.append(order)
        self.save_orders()

    def get_orders(self):
        return self.orders

# ------------------------------------------------------------
# КЛАСС ДЛЯ ЗАКРУГЛЁННОГО ФРЕЙМА (карточка блюда)
# ------------------------------------------------------------
class RoundedFrame(tk.Canvas):
    def __init__(self, parent, radius=15, bg=COLORS["card_bg"], border_color=COLORS["card_border"], **kwargs):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, **kwargs)
        self.radius = radius
        self.bg_color = bg
        self.border_color = border_color
        self.configure(bg=parent["bg"])
        self.bind("<Configure>", self._draw)
        self._draw()

    def _draw(self, event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w <= 1 or h <= 1:
            return
        self.create_rounded_rect(0, 0, w, h, self.radius, fill=self.bg_color, outline=self.border_color, width=2)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = (x1+r, y1,
                  x2-r, y1,
                  x2, y1,
                  x2, y1+r,
                  x2, y2-r,
                  x2, y2,
                  x2-r, y2,
                  x1+r, y2,
                  x1, y2,
                  x1, y2-r,
                  x1, y1+r,
                  x1, y1)
        return self.create_polygon(points, smooth=True, **kwargs)

# ------------------------------------------------------------
# ДАННЫЕ МЕНЮ (все позиции) – без изменений
# ------------------------------------------------------------
MENU_DATA = {
    "Салаты": [
        ("Салат Цезарь с курицей", 520, "курица, салат Айсберг, черри, пармезан, сухарики, соус Цезарь"),
        ("Салат из рукколы, креветок и помидоров черри", 870, "руккола, креветки, черри, пармезан, кедровые орехи, бальзамик"),
        ("Теплый салат из киноа с баклажанами", 510, "киноа, черри, баклажаны фри, азиатская заправка"),
        ("Теплый салат из куриной печени с апельсинами", 570, "печень в панировке, апельсин, шпинат, черри, кунжут, медовая заправка"),
        ("Гриль салат с индейкой", 600, "индейка, кабачок, перец, баклажан, картофель, салатный микс, терияки"),
        ("Салат из нежной утки и овощей", 690, "утка, салатный микс, черри, огурец, вяленые томаты, апельсин, заправка"),
        ("Теплый салат из пасты с курицей, вялеными томатами и соусом песто", 520, "паста фузилли, томаты вяленые, черри, курица, пармезан, соус песто"),
        ("Салат с рваной уткой Конфи", 620, "утка конфи, айсберг, шпинат, морковь, перец, черри, яйцо перепелиное, орехи"),
        ("Теплый салат с треской", 620, "треска, кальмары, картофель, шпинат, айсберг, яйцо, лук красный, горошек"),
        ("Салат с куриными стрипсами и соусом Цезарь", 270, "куриное филе в панировке, микс капусты, айсберг, черри, пармезан, крутоны, соус Цезарь"),
        ("Салат Нисуаз", 270, "тунец, фасоль стручковая, картофель, лук красный, микс салата, заправка горчичная"),
        ("Салат с грушей и копченой курицей", 670, "копченая курица, айсберг, шпинат, груша, моцарелла, черри, грецкий орех, заправка"),
    ],
    "Супы": [
        ("Крем-суп тыквенный", 350, "тыква, картофель, лук, морковь, сливки, мускатный орех, семечки, сухарики"),
        ("Крем-суп грибной", 270, "шампиньоны, лук, картофель, сливки, сухарики"),
    ],
    "Горячее (мясо)": [
        ("Свинина на гриле", 690, "стейк из свиной шеи, перец, кабачок, томаты гриль"),
        ("Курица гриль", 690, "куриная грудка, рататуй, соус Пилати, зелень"),
        ("Венский шницель", 1030, "говядина в панировке из сухарей, салат, лимон"),
        ("Шницель по-венски из курицы", 620, "куриная грудка в панировке, салат, лимон"),
        ("Жаркое со свининой", 670, "свиная шея, картофель, перец, зелень, специи"),
        ("Жаркое с белыми грибами", 810, "свиная шея, картофель, белые грибы, лук порей, зелень"),
        ("Индейка в апельсиновом соусе", 660, "филе индейки, апельсиновый соус, рис, зелень"),
        ("Говяжьи щечки с булгуром", 610, "булгур, щечки томленые, черри, перец, кабачок, соус Демиглас"),
        ("Утка в медово-цитрусовом соусе", 870, "утка, шпинат, руккола, гранат, апельсин, медово-цитрусовый соус"),
        ("Бифштекс рубленый из свинины", 610, "бифштекс из свинины, яйцо, пюре, руккола, черри, перец"),
        ("Утка Конфи", 910, "утка, вишневый соус, яблоки в глазури, вишня, грецкий орех"),
    ],
    "Рыба/морепродукты": [
        ("Плато из королевских креветок", 950, "креветки, руккола, грейпфрут, соус терияки, кунжут, лимон"),
        ("Рыба в облаке", 730, "треска, лосось, белковое облако, капуста, черри, заправка"),
        ("Треска с креветками и грибами", 780, "треска отварная, фасоль стручковая, сливки, креветки, шампиньоны"),
        ("Стейк из палтуса", 910, "палтус, пюре, сырно-сливочный соус, шпинат, кедровые орехи, лимон"),
        ("Запеченный палтус на сковороде", 750, "палтус, пюре, сливки, моцарелла, черри, лимон (сковорода горячая)"),
        ("Стейк из лосося со сливочно-икорным соусом", 1250, "лосось, спаржа, сливки, икра, лимон, зелень"),
        ("Лосось в кленовом сиропе с пюре из цветной капусты", 1030, "лосось, кленовый сироп, терияки, пюре из цветной капусты, черри, лимон"),
    ],
    "Паста и лазанья": [
        ("Лазанья", 730, "листы лазаньи, соус болоньезе, бешамель, моцарелла, черри, зелень"),
        ("Паста Карбонара", 580, "спагетти, бекон, черри, пармезан, сливки, чеснок, желток"),
        ("Паста Болоньезе", 720, "феттучини, говяжий фарш, перец, томаты, пармезан"),
        ("Паста с курицей и грибами", 590, "феттучини, курица, шампиньоны, пармезан, сливки"),
        ("Феттучини с говядиной", 830, "феттучини, говядина, лук, пармезан, сливки, соус Пилати"),
        ("Фузилли с брокколи и лососем", 760, "фузилли, лосось, брокколи, лук порей, пармезан, сливки"),
        ("Паста с морепродуктами и соусом Том ям", 880, "спагетти с чернилами каракатицы, креветки, шампиньоны, черри, шпинат, чили, лайм"),
    ],
    "Пицца": [
        ("Цезарь", 620, "курица, айсберг, черри, моцарелла, пармезан, соус Цезарь"),
        ("Неаполитано", 680, "окорок, бекон, колбаса, томаты, огурцы маринованные, моцарелла, чипсы"),
        ("Болоньезе", 870, "говяжий фарш, перец, томаты, моцарелла"),
        ("Пепперони", 590, "колбаса пепперони, моцарелла, томатный соус"),
        ("Маргарита", 410, "томаты, моцарелла, томатный соус"),
        ("Беллини", 750, "копченая курица, бекон, грибы, маслины, моцарелла, сливочный соус"),
        ("Веджетариана", 570, "перец, кабачок, томаты, лук порей, шампиньоны, моцарелла"),
        ("Венеция", 1250, "треска, креветки, лук порей, яйцо, моцарелла, сливочный соус"),
        ("Карбонара", 620, "окорок, бекон, лук порей, моцарелла, сливочный соус, желток"),
        ("Барбекю", 660, "свинина копченая, курица, огурцы маринованные, томаты, лук красный, соус барбекю, моцарелла"),
    ],
    "Бургеры/роллы": [
        ("Венский классический бургер", 520, "котлета из говядины, салат, лук, огурец маринованный, горчичный соус, булочка Бриошь, фри/коул-слоу"),
        ("Чизбургер BBQ с беконом", 580, "говядина, салат, помидоры, сыр чеддер, бекон, соус барбекю, булочка Бриошь, фри/коул-слоу"),
        ("Чикенбургер", 510, "куриная котлета, томаты, огурцы, салат, сыр чеддер, сырно-горчичный соус, фри/коул-слоу"),
        ("Ролл с курицей", 335, "тортилья, курица, помидор, капуста, огурец, сливочный соус"),
        ("Ролл с лососем", 470, "тортилья, лосось, капуста, огурец, сливочный соус, соус хрен"),
        ("Ролл с креветками", 390, "тортилья, креветки, капуста, огурец, томаты, сливочный соус, соус хрен"),
        ("Бейгл с лососем", 470, "булочка бейгл, лосось, айсберг, огурец, сливочный соус, медово-горчичный"),
        ("Круассан с красной рыбой", 450, "круассан, лосось, айсберг, огурец, сливочный соус"),
        ("Круассан с ветчиной и сыром", 310, "круассан, ветчина, сыр чеддер, айсберг, сливочный соус"),
        ("Круассан с томатами и моцареллой", 380, "круассан, томаты, моцарелла, айсберг, соус песто, сливочный соус"),
    ],
    "Летнее меню 2026": [
        ("Тёплый салат с курицей и овощами", 600, "курица, кабачок, черри, морковь, айсберг, руккола, кунжут, азиатская заправка"),
        ("Салат с гребешком и цитрусами", 1100, "гребешок, айсберг, шпинат, черри, апельсин, грейпфрут, кунжут"),
        ("Запеченный палтус на сковородочке", 750, "филе палтуса, пюре, сливки, моцарелла, черри, лимон (сковорода горячая)"),
        ("Запеченная треска на сковородочке", 690, "филе трески, пюре, сливки, моцарелла, черри, лимон (сковорода горячая)"),
        ("Пикката из говядины", 1400, "говяжья вырезка, панировка, спаржа, каперсы, черри, лимон"),
        ("Пикката из индейки", 950, "филе индейки, панировка, спаржа, каперсы, черри, лимон"),
        ("Свиной рябчик", 950, "свиной рябчик, соус Свит Чили, картофельные дольки, квашеная капуста, тушеная капуста, черри"),
        ("Говяжьи рёбра", 1100, "говяжьи рёбра кальби, соус Демиглас, пюре, зелень; + овощи гриль (доп.)"),
    ],
    "Гарниры и соусы": [
        ("Картофель фри", 200, ""),
        ("Картофельное пюре", 200, ""),
        ("Запеченный картофель", 200, ""),
        ("Овощи гриль", 200, "кабачок, томат, болгарский перец, шампиньон"),
        ("Паровые овощи", 200, "цветная капуста, брокколи"),
        ("Фасоль стручковая жареная", 200, ""),
        ("Спаржа зеленая жареная", 200, ""),
        ("Соус Пилати (томатный)", 100, ""),
        ("Соус Барбекю", 100, ""),
        ("Соус Песто", 100, ""),
        ("Соус Тар-тар", 100, ""),
        ("Соус Сырный", 100, ""),
    ],
    "Выпечка": [
        ("Круассан классический", 170, "вес 60 г"),
        ("Круассан с шоколадом и фундуком", 190, "вес 95 г"),
        ("Улитка с корицей", 210, "вес 85 г"),
    ],
    "Блины": [
        ("Блины с ягодным соусом и взбитыми сливками", 200, "блины 2 шт, ягодный соус, взбитые сливки"),
        ("Блины со свежим бананом и шоколадом", 200, "банан, топпинг Шоколад"),
        ("Блины со слабосоленым лососем", 410, "слабосоленый лосось, зелень"),
        ("Блины, запеченные с курицей и грибами", 320, "куриное филе, шампиньоны, сметана, сыр Пармезан, черри, зелень"),
        ("Блины классические", 150, "блины классические 2 шт."),
        ("Блины со сметаной", 170, "блины классические 2 шт., сметана"),
        ("Блины со сгущеным молоком", 170, "блины классические 2 шт., сгущеное молоко"),
        ("Блины с сыром и ветчиной", 200, "блины классические 2 шт., ветчина, сыр, зелень"),
    ],
    "Сладости": [
        ("Макарони", 120, "1 шт, 18 г"),
        ("Мороженое в ассортименте", 90, "50 г"),
        ("Вафля венская с корицей и какао", 200, "90 г"),
        ("Вафля венская сливки, орео, шоколад", 305, "190 г"),
        ("Вафля венская с мороженым и ягодным соусом", 290, "190 г"),
        ("Штрудель с мороженым вишневый / с яблоком и корицей", 310, "120/50 г"),
    ],
    "Кофе": [
        ("Эспрессо 40 мл", 140, ""),
        ("Эспрессо 80 мл", 210, ""),
        ("Эспрессо 120 мл", 220, ""),
        ("Эспрессо Кон Панна / Маккиато 40 мл", 170, ""),
        ("Эспрессо Кон Панна / Маккиато 80 мл", 210, ""),
        ("Эспрессо Кон Панна / Маккиато 120 мл", 230, ""),
        ("Американо 200 мл", 220, ""),
        ("Американо 300 мл", 270, ""),
        ("Американо 400 мл", 290, ""),
        ("Капучино 200 мл", 270, ""),
        ("Капучино 300 мл", 315, ""),
        ("Капучино 400 мл", 340, ""),
        ("Латте 200 мл", 270, ""),
        ("Латте 300 мл", 315, ""),
        ("Латте 400 мл", 340, ""),
        ("Флэт уайт", 320, "200 мл"),
        ("Мокачино белый/чёрный 200 мл", 285, ""),
        ("Мокачино белый/чёрный 300 мл", 340, ""),
        ("Мокачино белый/чёрный 400 мл", 360, ""),
        ("Раф кофе", 350, "300 мл"),
        ("Венский кофе белый/чёрный", 350, "300 мл"),
        ("Сливочный латте с кокосом", 370, "400 мл"),
        ("Карамельно-ореховый латте", 360, "300 мл"),
        ("Эспрессо фредо", 250, "200 мл"),
        ("Кофе санрайз", 420, "400 мл"),
        ("Эспрессо тоник", 390, "400 мл"),
        ("Айс матча (зелёная/синяя)", 450, "400 мл. готовится на альтернативном молоке (кокосовое, миндальное, банановое)"),
        ("Айс латте арахисовое печенье", 360, "400 мл"),
        ("Карамельный айс латте с тапиокой", 480, "400 мл"),
        ("Вишневый бамбл кофе", 360, "400 мл"),
    ],
    "Чай": [
        ("Классический черный чай", 320, "чайник 650 мл"),
        ("Королевский эрл грей", 320, "чайник 650 мл"),
        ("Классический зеленый чай", 320, "чайник 650 мл"),
        ("Зеленый чай с жасмином", 320, "чайник 650 мл"),
        ("Молочный улун", 320, "чайник 650 мл"),
        ("Горные травы", 320, "чайник 650 мл"),
        ("Ягодный фреш", 320, "чайник 650 мл"),
        ("Матча латте", 330, "400 мл"),
        ("Чай облепиховый", 390, "чайник 650 мл"),
        ("Чай имбирно-цитрусовый", 390, "чайник 650 мл"),
        ("Глогги чай", 390, "чайник 650 мл"),
    ],
    "Холодные напитки": [
        ("Молочный коктейль в ассортименте", 320, "400 мл"),
        ("Кофе глясе", 320, "300 мл"),
        ("Сок свежевыжатый в ассортименте", 450, "300 мл"),
        ("Лимонад в ассортименте 400 мл", 290, ""),
        ("Лимонад в ассортименте 1000 мл", 720, ""),
        ("Сникерс шейк", 370, "400 мл"),
        ("Орео шейк", 370, "400 мл"),
        ("Смеш манго", 440, "400 мл"),
        ("Смеш клубника", 440, "400 мл"),
        ("Фраппе айс шоколадный/карамельный", 390, "400 мл"),
        ("Капучино айс", 340, "400 мл"),
    ],
    "Лимонады": [
        ("Апероль б/а", 320, "400 мл"),
        ("Гранат-чёрная смородина", 350, "с черничным баббл джусом, 400 мл"),
        ("Клубника-кокос", 350, "с кокосовым желе, 400 мл"),
        ("Клюквенный лимонад", 320, "400 мл"),
        ("Лимонад вишня-виноград", 350, "с виноградным желе, 400 мл"),
        ("Лимонад груша-банан", 320, "400 мл"),
        ("Лимонад в ассортименте (мохито, ежевика-фиалка, киви-фейхоа, базилик-лимон)", 290, "400 мл / 1000 мл 720 руб."),
    ],
    "Какао и шоколад": [
        ("Какао классическое/сливочное 200 мл", 260, ""),
        ("Какао классическое/сливочное 300 мл", 290, ""),
        ("Какао классическое/сливочное 400 мл", 315, ""),
        ("Чоколате кокос", 350, "400 мл"),
        ("Чоколате классик", 350, "400 мл"),
        ("Чоколате ваниль", 350, "400 мл"),
        ("Чоколате орех", 350, "400 мл"),
    ],
    "Топпинги": [
        ("мёд", 50, ""),
        ("молоко", 50, ""),
        ("взбитые сливки", 30, ""),
        ("мята/розмарин/чабрец", 30, ""),
        ("крошка печенья Орео", 80, ""),
        ("альтернативное молоко", 100, ""),
        ("маршмеллоу", 50, ""),
        ("орешки", 30, ""),
        ("эспрессо", 60, ""),
        ("мороженое", 90, ""),
    ],
}

# ------------------------------------------------------------
# ГЛАВНОЕ ПРИЛОЖЕНИЕ
# ------------------------------------------------------------
class CoffeeKioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Company – КИОСК")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg=COLORS["bg_main"])

        # Иконка (если файл есть)
        try:
            self.icon_img = tk.PhotoImage(file="coffee_icon.png")
            self.root.iconphoto(True, self.icon_img)
        except Exception:
            pass

        self.data_manager = DataManager()
        self.setup_scrollbar_style()
        self.cart = []  # корзина
        self.admin_window = None  # ссылка на окно админа

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=COLORS["bg_main"], borderwidth=0)
        style.configure("TNotebook.Tab", background=COLORS["bg_tab"], foreground=COLORS["text_light"], padding=[15, 5], font=("Arial", 12, "bold"))
        style.map("TNotebook.Tab", background=[("selected", COLORS["cat_active"])])

        # Верхняя панель с кнопкой входа
        top_frame = tk.Frame(root, bg=COLORS["bg_main"])
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10,0))

        self.admin_btn = tk.Button(top_frame, text="Вход (админ)", command=self.login_admin,
                                   bg=COLORS["btn_warning"], fg=COLORS["text_light"],
                                   font=("Arial", 10, "bold"), padx=10)
        self.admin_btn.pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.menu_tab = tk.Frame(self.notebook, bg=COLORS["bg_main"])
        self.cart_tab = tk.Frame(self.notebook, bg=COLORS["bg_main"])
        self.notebook.add(self.menu_tab, text="Меню")
        self.notebook.add(self.cart_tab, text="Корзина")

        self.build_menu_tab()
        self.build_cart_tab()

        self.status_var = tk.StringVar()
        self.status_var.set("Добро пожаловать! Выбирайте блюда и добавляйте в корзину +")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                              bg=COLORS["bg_main"], fg=COLORS["text_light"], font=("Arial", 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_cart_display()
        self.bind_mousewheel()

    def setup_scrollbar_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Vertical.TScrollbar",
                        background=COLORS["scrollbar_bg"],
                        troughcolor=COLORS["bg_main"],
                        bordercolor=COLORS["scrollbar_bg"],
                        arrowcolor=COLORS["scrollbar_thumb"])
        style.map("Vertical.TScrollbar",
                  background=[("active", COLORS["scrollbar_thumb"]), ("pressed", COLORS["cat_active"])])
        style.configure("Horizontal.TScrollbar",
                        background=COLORS["scrollbar_bg"],
                        troughcolor=COLORS["bg_main"],
                        bordercolor=COLORS["scrollbar_bg"],
                        arrowcolor=COLORS["scrollbar_thumb"])
        style.map("Horizontal.TScrollbar",
                  background=[("active", COLORS["scrollbar_thumb"]), ("pressed", COLORS["cat_active"])])

    def bind_mousewheel(self):
        def _on_mousewheel(event):
            if self.notebook.index(self.notebook.select()) != 0:
                return
            if event.delta:
                self.menu_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif event.num == 4:
                self.menu_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.menu_canvas.yview_scroll(1, "units")
            self.update_active_category()

        self.root.bind_all("<MouseWheel>", _on_mousewheel)
        self.root.bind_all("<Button-4>", _on_mousewheel)
        self.root.bind_all("<Button-5>", _on_mousewheel)
        self.menu_canvas.bind("<MouseWheel>", _on_mousewheel)
        self.menu_canvas.bind("<Button-4>", _on_mousewheel)
        self.menu_canvas.bind("<Button-5>", _on_mousewheel)

    # ------------------- ВХОД В АДМИНКУ -------------------
    def login_admin(self):
        # Простая аутентификация
        login = simpledialog.askstring("Вход", "Логин:", parent=self.root)
        if login != "admin":
            messagebox.showerror("Ошибка", "Неверный логин")
            return
        password = simpledialog.askstring("Вход", "Пароль:", parent=self.root, show="*")
        if password != "admin123":
            messagebox.showerror("Ошибка", "Неверный пароль")
            return
        # Успешный вход
        self.status_var.set("Администратор вошёл в систему. Открыта админ-панель.")
        self.open_admin_panel()

    def open_admin_panel(self):
        if self.admin_window is not None and self.admin_window.winfo_exists():
            self.admin_window.lift()
            return

        self.admin_window = tk.Toplevel(self.root)
        self.admin_window.title("Панель администратора")
        self.admin_window.geometry("800x500")
        self.admin_window.configure(bg=COLORS["bg_main"])

        tk.Label(self.admin_window, text="Управление заказами", font=("Arial", 18, "bold"),
                 bg=COLORS["bg_main"], fg=COLORS["text_light"]).pack(pady=10)

        # Таблица заказов
        tree_frame = tk.Frame(self.admin_window, bg=COLORS["bg_main"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.admin_tree = ttk.Treeview(tree_frame, columns=("id", "date", "phone", "total", "items"), show="headings",
                                       yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.admin_tree.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.admin_tree.pack(fill=tk.BOTH, expand=True)

        self.admin_tree.heading("id", text="№")
        self.admin_tree.heading("date", text="Дата")
        self.admin_tree.heading("phone", text="Телефон")
        self.admin_tree.heading("total", text="Сумма (₽)")
        self.admin_tree.heading("items", text="Позиции")
        self.admin_tree.column("id", width=50, anchor="center")
        self.admin_tree.column("date", width=150)
        self.admin_tree.column("phone", width=120)
        self.admin_tree.column("total", width=100, anchor="center")
        self.admin_tree.column("items", width=300)

        self.refresh_admin_table()

        btn_frame = tk.Frame(self.admin_window, bg=COLORS["bg_main"])
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Обновить", command=self.refresh_admin_table,
                  bg=COLORS["btn_success"], fg=COLORS["text_light"], padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Экспорт в CSV", command=self.export_orders_csv,
                  bg=COLORS["btn_warning"], fg=COLORS["text_light"], padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Закрыть", command=self.admin_window.destroy,
                  bg=COLORS["btn_danger"], fg=COLORS["text_light"], padx=10).pack(side=tk.LEFT, padx=5)

        self.admin_window.protocol("WM_DELETE_WINDOW", self.on_admin_close)

    def refresh_admin_table(self):
        for row in self.admin_tree.get_children():
            self.admin_tree.delete(row)
        orders = self.data_manager.get_orders()
        for order in orders:
            items_str = ", ".join([f"{i['name']} x{i['quantity']}" for i in order.get("items", [])])
            self.admin_tree.insert("", tk.END, values=(
                order.get("id", ""),
                order.get("date", ""),
                order.get("phone", ""),
                order.get("total", 0),
                items_str
            ))

    def export_orders_csv(self):
        orders = self.data_manager.get_orders()
        if not orders:
            messagebox.showinfo("Экспорт", "Нет заказов для экспорта")
            return
        import csv
        filename = f"orders_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Дата", "Телефон", "Сумма", "Позиции"])
            for order in orders:
                items_str = "; ".join([f"{i['name']} x{i['quantity']}" for i in order.get("items", [])])
                writer.writerow([order.get("id", ""), order.get("date", ""),
                                 order.get("phone", ""), order.get("total", 0), items_str])
        messagebox.showinfo("Экспорт", f"Данные экспортированы в {filename}")

    def on_admin_close(self):
        self.admin_window.destroy()
        self.admin_window = None
        self.status_var.set("Админ-панель закрыта.")

    # ------------------- ВКЛАДКА МЕНЮ -------------------
    def build_menu_tab(self):
        search_frame = tk.Frame(self.menu_tab, bg=COLORS["bg_main"])
        search_frame.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(search_frame, text="Найти блюдо:", font=("Arial", 12, "bold"), bg=COLORS["bg_main"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_menu())
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=35, bg=COLORS["card_bg"], fg=COLORS["text_light"], insertbackground=COLORS["text_light"])
        self.search_entry.pack(side=tk.LEFT, padx=5)
        clear_btn = tk.Button(search_frame, text="Сбросить", command=self.clear_search, bg=COLORS["btn_warning"], fg=COLORS["text_light"], font=("Arial", 10, "bold"), padx=10)
        clear_btn.pack(side=tk.LEFT, padx=10)

        cat_container = tk.Frame(self.menu_tab, bg=COLORS["bg_main"])
        cat_container.pack(fill=tk.X, padx=10, pady=(0,5))
        cat_canvas = tk.Canvas(cat_container, bg=COLORS["bg_main"], highlightthickness=0, height=40)
        cat_scrollbar = ttk.Scrollbar(cat_container, orient=tk.HORIZONTAL, command=cat_canvas.xview, style="Horizontal.TScrollbar")
        cat_canvas.configure(xscrollcommand=cat_scrollbar.set)
        cat_canvas.pack(side=tk.TOP, fill=tk.X, expand=True)
        cat_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        cat_inner = tk.Frame(cat_canvas, bg=COLORS["bg_main"])
        cat_canvas.create_window((0,0), window=cat_inner, anchor="nw")
        cat_inner.bind("<Configure>", lambda e: cat_canvas.configure(scrollregion=cat_canvas.bbox("all")))

        self.category_buttons = {}
        for cat in MENU_DATA.keys():
            btn = tk.Button(cat_inner, text=cat, font=("Arial", 10, "bold"), bg=COLORS["cat_inactive"], fg=COLORS["text_light"],
                           activebackground=COLORS["cat_active"], padx=10, pady=4, bd=0,
                           command=lambda c=cat: self.scroll_to_category(c))
            btn.pack(side=tk.LEFT, padx=3, pady=2)
            self.category_buttons[cat] = btn

        canvas_container = tk.Frame(self.menu_tab, bg=COLORS["bg_main"])
        canvas_container.pack(fill=tk.BOTH, expand=True)
        self.menu_canvas = tk.Canvas(canvas_container, bg=COLORS["bg_main"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.menu_canvas.yview, style="Vertical.TScrollbar")
        self.menu_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.menu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.menu_inner = tk.Frame(self.menu_canvas, bg=COLORS["bg_main"])
        self.menu_canvas.create_window((0,0), window=self.menu_inner, anchor="nw")
        self.menu_inner.bind("<Configure>", self._on_menu_configure)
        self.menu_canvas.bind("<Configure>", self._on_menu_canvas_configure)

        self.category_frames = {}
        self.load_menu()

    def load_menu(self):
        for cat, dishes in MENU_DATA.items():
            cat_frame = tk.Frame(self.menu_inner, bg=COLORS["bg_main"])
            cat_frame.pack(fill=tk.X, pady=(10,0))
            header = tk.Label(cat_frame, text=f"● {cat}", font=("Arial", 18, "bold"), bg=COLORS["bg_main"], fg=COLORS["text_light"], anchor="w")
            header.pack(fill=tk.X, padx=20, pady=(10,5))
            dishes_container = tk.Frame(cat_frame, bg=COLORS["bg_main"])
            dishes_container.pack(fill=tk.X, padx=30, pady=5)
            cat_frame.dishes_container = dishes_container
            cat_frame.dishes = []

            for dish_name, price, ingredients in dishes:
                card = RoundedFrame(dishes_container, radius=20)
                card.pack(fill=tk.X, pady=6, padx=5)
                content = tk.Frame(card, bg=COLORS["card_bg"])
                content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                tk.Label(content, text=dish_name, font=("Arial", 13, "bold"), bg=COLORS["card_bg"], fg=COLORS["text_light"], anchor="w").pack(anchor="w")
                if ingredients:
                    tk.Label(content, text=ingredients, font=("Arial", 9), bg=COLORS["card_bg"], fg=COLORS["text_dark"], anchor="w").pack(anchor="w", pady=(2,0))
                bottom = tk.Frame(content, bg=COLORS["card_bg"])
                bottom.pack(fill=tk.X, pady=(5,0))
                tk.Label(bottom, text=f"{price} ₽", font=("Arial", 14, "bold"), bg=COLORS["card_bg"], fg=COLORS["price_color"]).pack(side=tk.LEFT)
                btn = tk.Button(bottom, text="+", font=("Arial", 14, "bold"), bg=COLORS["btn_plus"], fg=COLORS["text_light"], bd=0,
                                padx=10, pady=2, command=lambda d=dish_name, p=price: self.add_to_cart(d, p))
                btn.pack(side=tk.RIGHT)
                cat_frame.dishes.append((dish_name, card, btn, price))
            self.category_frames[cat] = cat_frame

    def filter_menu(self):
        search_text = self.search_var.get().strip().lower()
        for cat, frame in self.category_frames.items():
            any_visible = False
            for dish_name, card, _, _ in frame.dishes:
                if search_text == "" or search_text in dish_name.lower():
                    card.pack(fill=tk.X, pady=6, padx=5)
                    any_visible = True
                else:
                    card.pack_forget()
            if not any_visible and search_text != "":
                frame.pack_forget()
            else:
                frame.pack(fill=tk.X, pady=(10,0))
        self._on_menu_configure(None)

    def clear_search(self):
        self.search_var.set("")
        self.filter_menu()

    def scroll_to_category(self, category):
        if category in self.category_frames:
            frame = self.category_frames[category]
            if not frame.winfo_ismapped():
                self.clear_search()
                frame = self.category_frames[category]
            y = frame.winfo_y()
            total = self.menu_inner.winfo_height()
            if total > 0:
                self.menu_canvas.yview_moveto(y / total)
            self.root.after(100, self.update_active_category)

    def update_active_category(self):
        view_top = self.menu_canvas.canvasy(0)
        view_bottom = view_top + self.menu_canvas.winfo_height()
        view_center = (view_top + view_bottom) / 2
        best_cat = None
        best_dist = float('inf')
        for cat, frame in self.category_frames.items():
            if not frame.winfo_ismapped():
                continue
            y = frame.winfo_y()
            dist = abs(y - view_center)
            if dist < best_dist:
                best_dist = dist
                best_cat = cat
        for cat, btn in self.category_buttons.items():
            if cat == best_cat:
                btn.config(bg=COLORS["cat_active"], fg=COLORS["text_light"])
            else:
                btn.config(bg=COLORS["cat_inactive"], fg=COLORS["text_light"])

    # ------------------- ВКЛАДКА КОРЗИНА -------------------
    def build_cart_tab(self):
        main_frame = tk.Frame(self.cart_tab, bg=COLORS["bg_main"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(main_frame, text="ВАШ ЗАКАЗ", font=("Arial", 22, "bold"), bg=COLORS["bg_main"], fg=COLORS["text_light"]).pack(pady=(0,15))

        tree_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        self.cart_tree = ttk.Treeview(tree_frame, columns=("name", "qty", "sum"), show="headings", yscrollcommand=tree_scroll.set, height=15)
        tree_scroll.config(command=self.cart_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview", background=COLORS["card_bg"], foreground=COLORS["text_light"], fieldbackground=COLORS["card_bg"], font=("Arial", 11))
        style.configure("Treeview.Heading", background=COLORS["bg_tab"], foreground=COLORS["text_light"], font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", COLORS["cat_active"])])

        self.cart_tree.heading("name", text="Блюдо")
        self.cart_tree.heading("qty", text="Кол-во")
        self.cart_tree.heading("sum", text="Сумма (₽)")
        self.cart_tree.column("name", width=400, anchor="w")
        self.cart_tree.column("qty", width=100, anchor="center")
        self.cart_tree.column("sum", width=120, anchor="center")

        total_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        total_frame.pack(fill=tk.X, pady=15)
        self.total_label = tk.Label(total_frame, text="Итого: 0 ₽", font=("Arial", 20, "bold"), bg=COLORS["bg_main"], fg=COLORS["price_color"])
        self.total_label.pack(side=tk.RIGHT, padx=20)

        btn_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Удалить выбранное", command=self.remove_from_cart, bg=COLORS["btn_danger"], fg=COLORS["text_light"], font=("Arial", 12, "bold"), padx=15, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Очистить корзину", command=self.clear_cart, bg=COLORS["btn_warning"], fg=COLORS["text_light"], font=("Arial", 12, "bold"), padx=15, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Оформить заказ", command=self.checkout, bg=COLORS["btn_success"], fg=COLORS["text_light"], font=("Arial", 12, "bold"), padx=20, pady=5).pack(side=tk.LEFT, padx=20)

    # ------------------- ОБЩАЯ ЛОГИКА -------------------
    def add_to_cart(self, dish_name, price, quantity=1):
        for item in self.cart:
            if item["name"] == dish_name:
                item["quantity"] += quantity
                break
        else:
            self.cart.append({"name": dish_name, "price": price, "quantity": quantity})
        self.update_cart_display()
        self.status_var.set(f"Добавлено: {dish_name}")

    def update_cart_display(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        total = 0
        for item in self.cart:
            summ = item["price"] * item["quantity"]
            total += summ
            self.cart_tree.insert("", tk.END, values=(item["name"], item["quantity"], summ))
        self.total_label.config(text=f"Итого: {total} ₽")
        return total

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            self.status_var.set("Выберите позицию для удаления")
            return
        values = self.cart_tree.item(selected[0], "values")
        if not values:
            return
        dish_name = values[0]
        for i, item in enumerate(self.cart):
            if item["name"] == dish_name:
                del self.cart[i]
                break
        self.update_cart_display()
        self.status_var.set("Позиция удалена")

    def clear_cart(self):
        if messagebox.askyesno("Очистка", "Удалить всё из корзины?"):
            self.cart.clear()
            self.update_cart_display()
            self.status_var.set("Корзина очищена")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Корзина пуста", "Добавьте блюда для оформления заказа")
            return
        phone = simpledialog.askstring("Контактные данные", "Введите номер телефона:", parent=self.root)
        if not phone:
            return
        delivery = messagebox.askyesno("Доставка", "Вы хотите заказать доставку? (Да – доставка, Нет – самовывоз)")
        delivery_str = "Доставка" if delivery else "Самовывоз"

        order_id = len(self.data_manager.get_orders()) + 1
        total = sum(item["price"] * item["quantity"] for item in self.cart)
        order = {
            "id": order_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "phone": phone,
            "delivery": delivery,
            "total": total,
            "status": "Новый",
            "items": self.cart.copy()
        }
        self.data_manager.add_order(order)

        self.show_receipt(order)

        self.cart.clear()
        self.update_cart_display()
        self.status_var.set(f"Заказ №{order_id} оформлен. Спасибо!")

    def show_receipt(self, order):
        win = tk.Toplevel(self.root)
        win.title("ЧЕК")
        win.geometry("450x450")
        win.configure(bg=COLORS["bg_main"])
        text = tk.Text(win, wrap=tk.WORD, font=("Courier", 10), bg=COLORS["card_bg"], fg=COLORS["text_light"])
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        receipt = f"Кофейня 'Coffee Company'\nЗаказ №{order['id']}\nДата: {order['date']}\n"
        receipt += f"Телефон: {order['phone']}\nСпособ: {'Доставка' if order['delivery'] else 'Самовывоз'}\n"
        receipt += "-"*40 + "\n"
        for item in order["items"]:
            receipt += f"{item['name']} x{item['quantity']} = {item['price']*item['quantity']} ₽\n"
        receipt += "-"*40 + f"\nИТОГО: {order['total']} ₽\nСпасибо за заказ!"
        text.insert(tk.END, receipt)
        text.config(state=tk.DISABLED)
        tk.Button(win, text="Закрыть", command=win.destroy, bg=COLORS["btn_success"], fg=COLORS["text_light"]).pack(pady=10)

    # ------------------- ОБРАБОТЧИКИ ПРОКРУТКИ -------------------
    def _on_menu_configure(self, event):
        self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all"))
        self.update_active_category()

    def _on_menu_canvas_configure(self, event):
        self.menu_canvas.itemconfig(1, width=event.width)

# ------------------------------------------------------------
# ЗАПУСК
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeKioskApp(root)
    root.mainloop()