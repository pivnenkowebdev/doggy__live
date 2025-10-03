import pygame as p
import time as t
from random import randint, choice

p.init()

scr_width = 1280
scr_height = 1000
icon_size = 80
padding = 5
dog_width = 310
dog_height = 500
dog_y = 100
font = p.font.Font(None, 40)
font_jr = p.font.Font(None, 15)
but_width = 200
but_height = 60
menuX = 90
menuY = 130
sz = (dog_width//1.7, dog_height//1.7)

def load_img(file, width, height):
    image = p.image.load(file).convert_alpha()
    image = p.transform.scale(image, (width, height))
    return image

def text_render(text, text_font=font):
    return text_font.render(str(text), True, "black")

class Button:
    def __init__(self, text, x, y, width=but_width, height=but_height, text_font=font, func=None):
        self.func = func
        self.idle_image = load_img("images/button.png", width, height)
        self.pressed_image = load_img("images/button_clicked.png", width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_pressed = False
        self.text = text_render(text, text_font)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = p.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else:
                self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()
        elif event.type == p.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False



class ITEM:
    def __init__(self, name, price, item_icon, satiety=0, med_pow=0):
        self.name = name
        self.price = price
        self.sat_pow = satiety
        self.med_pow = med_pow

        self.item_img = load_img(item_icon, dog_width, dog_height)
        self.item_img_rect = self.item_img.get_rect()
        self.item_img_rect.center = (scr_width//2, scr_height//2)

        self.item_img_jr = load_img(item_icon, sz[0], sz[1])
        self.item_img_jr_rect = self.item_img_jr.get_rect()
        self.item_img_jr_rect.center = (scr_width//2, scr_height//2)

        self.is_bought = False
        self.is_using = False

class JRDOG(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = load_img("images/dog.png", menuX*1.7, menuY*1.7)
        self.start_pos = (scr_width//2 - 50, scr_height - menuY - 170)
        self.ground = True
        self.rect = self.image.get_rect()
        self.rect.center = self.start_pos


    def moves(self):
        keys = p.key.get_pressed()
        if keys[p.K_a]:
            self.dog_rect.x -= 5
        if keys[p.K_d]:
            self.dog_rect.x -= 5
        if keys[p.K_space] and self.ground:
            self.dog_rect.y += 10
            p.timer(self.dog_rect, 1000)

class TOY(p.sprite.Sprite):
    def __init__(self, toy_rect):
        p.sprite.Sprite.__init__(self)
        self.image = load_img(f"images/toys/{choice(["ball", "blue bone", "red bone"])}.png", 80, 80)
        self.rect = toy_rect


    def update(self):
        self.rect[1] -= 1

class MINI_GAME:
    def __init__(self, happiness):
        self.happiness = happiness
        self.bckgrnd = load_img("images/game_background.png", scr_width, scr_height)
        self.game_menu = False
        self.dog = JRDOG()
        self.toys_group = p.sprite.Group()
        self.score = 0
        self.interval = 1000 * 30
        self.start_time = 0

    def new_game(self):
        self.dog = JRDOG()

        self.score = 0

        self.start_time = p.time.get_ticks()
        self.interval = 1000 * 30
        return None

    def update(self):
        self.dog.update()
        self.toys_group.update()

        # hits = p.sprite.spritecollide(self.dog, self.toys_group, True, p.sprite.collide_rect_ratio(0.6))
        # self.score += hits

        if p.time.get_ticks() - self.start_time >= self.interval:
            self.happiness += self.score
            self.game_menu = False

    def is_clicked(self, event):
        pass

    def draw(self, screen):
        screen.blit(self.bckgrnd, (0, 0))
        screen.blit(self.dog.image, self.dog.rect.center)
        screen.blit(text_render(self.score), (menuX + 70, menuY + 20))




class MENU:
    def __init__(self, games_link):
        self.mode = games_link.mode
        #мне нужно здесь обрабатывать моды из games_link (turn on/off)
        self.menu_page = load_img("images/menu/menu_page.png", scr_width, scr_height)
        self.bottom_label_off = load_img("images/menu/bottom_label_off.png", scr_width, scr_height)
        self.bottom_label_on = load_img("images/menu/bottom_label_on.png", scr_width, scr_height)
        self.top_label_off = load_img("images/menu/top_label_off.png", scr_width, scr_height)
        self.top_label_on = load_img("images/menu/top_label_on.png", scr_width, scr_height)

        self.buy_text = text_render("Куплено")
        self.b_t_rect = self.buy_text.get_rect()
        self.b_t_rect.center = (scr_width // 1.28, scr_height // 2.8)

        self.use_text = text_render("Надето")
        self.u_t_rect = self.use_text.get_rect()
        self.u_t_rect.center = (scr_width // 1.29, scr_height // 4)

        self.current_item = 0

        self.items = {
              "food": [
                       ITEM("Apple", 5, "images/food/apple.png", 2, 0),
                       ITEM("Bone", 10, "images/food/bone.png", 5, 0),
                       ITEM("DogFood", 9, "images/food/dog_food.png", 4, 0),
                       ITEM("Elite DogFood", 45, "images/food/dog_food_elite.png", 35, 15),
                       ITEM("Meat", 60, "images/food/meat.png", 50, 25),
                       ITEM("Medicine", 120, "images/food/medicine.png", 100, 50)
                       ]

                       ,

            "clothes": [
                       ITEM("Blue T-Shirt", 50, "images/items/blue t-shirt.png"),
                       ITEM("Green Boots", 150, "images/items/boots.png"),
                       ITEM("Pink Butterfly (Bow)", 15, "images/items/bow.png"),
                       ITEM("Orange Cap", 20, "images/items/cap.png"),
                       ITEM("Gold Chain", 100, "images/items/gold chain.png"),
                       ITEM("Yellow Hat", 40, "images/items/hat.png"),
                       ITEM("Red T-Shirt", 50, "images/items/red t-shirt.png"),
                       ITEM("Silver Chain", 60, "images/items/silver chain.png"),
                       ITEM("Blue Sunglasses", 50, "images/items/sunglasses.png"),
                       ITEM("Yellow T-Shirt", 50, "images/items/yellow t-shirt.png")
                       ]
        }

        self.use_items = []
        self.buy_items = []

        self.next_but = Button("Вперёд", scr_width - menuX - but_width - 25, scr_height - menuY - but_height,
                               width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.next)

        self.back_but = Button("Назад", but_width - but_height + 10, scr_height - menuY - but_height,
                               width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.back)

        self.use_but = Button("Надеть", but_width - but_height + 10, scr_height - menuY - 2 * but_height,
                               width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.use)

        self.unuse_but = Button("Снять", but_width - but_height + 10, scr_height - menuY - 3 * but_height,
                               width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.unuse)

        self.buy_but = Button("Купить", scr_width // 2 - 80, scr_height - menuY - 3 * but_height,
                               width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.buy)

        self.price = self.items[self.mode][self.current_item].price

    def next(self):
        if self.current_item < len(self.items[self.mode]) - 1:
            self.current_item += 1
            self.price = self.items[self.mode][self.current_item].price

    def back(self):
        if self.current_item > 0:
            self.current_item -= 1
            self.price = self.items[self.mode][self.current_item].price

    def use(self):
        if self.items[self.mode][self.current_item].is_bought:
            self.use_items.append(self.items[self.mode][self.current_item])
            self.items[self.mode][self.current_item].is_using = True

    def unuse(self):
        self.use_items.remove(self.items[self.mode][self.current_item])
        self.items[self.mode][self.current_item].is_using = False

    def buy(self):
        if self.games_link.money >= self.items[self.mode][self.current_item].price:
            self.buy_items.append(self.items[self.mode][self.current_item])
            print(self.items[self.mode][self.current_item])
            self.items[self.mode][self.current_item].is_bought = True
            #проверить что куплено
            self.games_link.money -= self.items[self.mode][self.current_item].price
            print(self.use_items)

    def update(self):
        self.next_but.update()
        self.back_but.update()
        self.use_but.update()
        self.unuse_but.update()
        self.buy_but.update()

    def is_clicked(self, event):
        self.next_but.is_clicked(event)
        self.back_but.is_clicked(event)
        self.use_but.is_clicked(event)
        self.unuse_but.is_clicked(event)
        self.buy_but.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.mode][self.current_item].item_img, self.items[self.mode][self.current_item].item_img_rect)

        self.next_but.draw(screen)
        self.back_but.draw(screen)
        screen.blit(text_render(self.price), (scr_width // 2 - 10, scr_height // 3.2))



        if self.mode == "clothes":
            if not self.items[self.mode][self.current_item].is_bought:
                self.buy_but.draw(screen)

            if not self.items[self.mode][self.current_item].is_using:
                self.use_but.draw(screen)
            else:
                self.unuse_but.draw(screen)

            if self.items[self.mode][self.current_item].is_bought:
                screen.blit(self.bottom_label_on, (0, 0))
            else:
                screen.blit(self.bottom_label_off, (0, 0))

            if self.items[self.mode][self.current_item].is_using:
                screen.blit(self.bottom_label_on, (0, -112))
            else:
                screen.blit(self.bottom_label_off, (0, -112))

            screen.blit(self.buy_text, self.b_t_rect)
            screen.blit(self.use_text, self.u_t_rect)
        elif self.mode == "food":
            self.buy_but.draw(screen)



class Game:
    def __init__(self):
        self.mode = "main"
        self.screen = p.display.set_mode((scr_width, scr_height))
        p.display.set_caption("Виртуальный питомец")
        pet_icon = p.Surface.convert(p.image.load("images/dog.png"))
        p.display.set_icon(pet_icon)
        self.menu = None
        self.mini_game = None

        self.items_price = 0
        self.coins_per_second = 1000
        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}
        self.start_time = t.time()

        self.satiety = 100
        self.money = 100
        self.health = 100
        self.happiness = 100

        self.background = load_img("images/background.png", scr_width, scr_height)
        self.happin_img = load_img("images/happiness.png", icon_size, icon_size)
        self.money_img = load_img("images/money.png", icon_size, icon_size)
        self.satiety_img = load_img("images/satiety.png", icon_size, icon_size)
        self.health_img = load_img("images/health.png", icon_size, icon_size)
        self.dog_img = load_img("images/dog.png", dog_width, dog_height)

        button_x = scr_width - but_width

        # кнопки создавались сразу с вызванными колбеками - нужны лямбды
        self.buttons = [
            Button("Еда", button_x, padding * 2 + icon_size, func=lambda: self.HANDLE_MODE("food")),
            Button("Одежда", button_x, (padding * 2 + icon_size) * 1.7, func=lambda: self.HANDLE_MODE("clothes")),
            Button("Игры", button_x, (padding * 2 + icon_size) * 2.4, func=lambda: self.HANDLE_MODE("mini_game")),
            Button("Улучшить", scr_width - but_width // 2, scr_height - but_height // 2,
                   but_width // 2, but_height // 2, font_jr, func=self.increase_money)
        ]

        self.FARM_MONEY = p.USEREVENT + 1
        p.time.set_timer(self.FARM_MONEY, 1000)

        self.DECREASE_PROPERTY = p.USEREVENT + 2
        p.time.set_timer(self.DECREASE_PROPERTY, 1000)

        self.run()

    def HANDLE_MODE(self, mode="main"):
        self.mode = mode
        if self.mode == "food":
            self.menu = MENU(self)
        elif self.mode == "clothes":
            self.menu = MENU(self)
        elif self.mode == "mini_game":
            self.mini_game = MINI_GAME(self)


    def increase_money(self):
        for cost, check in self.costs_of_upgrade.items():
            if not check and self.money >= cost:
                self.coins_per_second += 1
                self.money -= cost
                self.costs_of_upgrade[cost] = True
                break

    def DECREASE(self):
        chance = randint(1, 10)
        if chance <= 5:
            self.satiety -= 1
        elif 5 >= chance <= 9:
            self.happiness -= 1
        else:
            self.health -= 1

    def click(self, event):
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            self.money += 1

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def event(self):
        for event in p.event.get():

            self.click(event)
            # по хорошему тогда нужно убрать ниже все проверки и вынести в отдельные методы как и click (писать обработку условия внутри)

            if event.type == p.QUIT:
                p.quit()
                exit()
                # если есть возможность избежать вложенных условий - круто
            if event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                self.menu.current_menu = -1

            elif event.type == self.FARM_MONEY:
                self.money += 1

            elif event.type == self.DECREASE_PROPERTY:
                self.DECREASE()

            for btn in self.buttons:
                btn.is_clicked(event)

                if self.mode == "food":
                    self.menu.is_clicked(event)
                if self.mode == "clothes":
                    self.menu.is_clicked(event)

            if self.mode == "mini_game":
                self.mini_game.is_clicked(event)

    def update(self):
        for btn in self.buttons:
            btn.update()

        if self.mode == "food":
            self.menu.update()

        if self.mode == "clothes":
            self.menu.update()

        if self.mode == "mini_game":
            self.mini_game.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.happin_img, (padding * 2, padding * 2))
        self.screen.blit(self.satiety_img, (padding * 2, padding * 2 + icon_size))
        self.screen.blit(self.health_img, (padding * 2, padding * 2 + icon_size * 2))
        self.screen.blit(self.money_img, (scr_width - icon_size, padding * 2))

        self.screen.blit(text_render(self.happiness), (padding + icon_size, (icon_size - padding * 2) // 2))
        self.screen.blit(text_render(self.satiety), (padding + icon_size, (icon_size - padding * 2) * 1.7))
        self.screen.blit(text_render(self.health), (padding + icon_size, (icon_size - padding * 2) * 2.8))
        self.screen.blit(text_render(self.money), (scr_width - icon_size * 1.5, (icon_size - padding * 2) // 2))

        for btn in self.buttons:
            btn.draw(self.screen)

        self.screen.blit(self.dog_img, (scr_width // 2 - dog_width // 2, dog_y))

        # вот тут добавил проверку на то, что меню инициализиировано
        if self.menu:
            for item in self.menu.use_items:
                self.screen.blit(item.item_img, (scr_width // 2 - dog_width // 2, dog_y))

        if self.mode == "food":
            self.menu.draw(self.screen)
        if self.mode == "clothes":
            self.menu.draw(self.screen)

        if self.mini_game and self.mini_game.game_menu:
            self.mini_game.draw(self.screen)

        p.display.flip()


if __name__ == "__main__":
    Game()

#1 refactor услвие для смены режимов в игре(меню одежды и еды, мини игра, мейн)
#1.1 рефактор MENU.draw()

    #1. Отрисовать окно мини-игры при нажатии на кнопку "Игры" в меню +
    #1.1 Отрисовать собаку +
    #1.2 Отрисовка игрушек
    #2. разработать контакт собаки и игрушек
    #3. закрытие игры по времени