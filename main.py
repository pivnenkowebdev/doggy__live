import pygame as p

# Инициализация pg
p.init()

# Размеры окна
scr_width = 1000
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
food_sz = 200

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

class Item:
    def __init__(self, name, price, file):
        self.name = name
        self.price = price
        self.is_bought = False
        self.is_using = False

        self.item_icon = load_img(file, dog_width//1.7, dog_height//1.7)
        self.item = load_img(file, dog_width, dog_height)

class Food:
    def __init__(self, name, price, item_icon, satiety, med_pow = 0):
        self.name = name
        self.price = price
        self.food_img = load_img(item_icon, food_sz, food_sz)
        self.sat_pow = satiety
        self.med_pow = med_pow

class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_img("images/menu/menu_page.png", scr_width, scr_height)

        self.bottom_label_off = load_img("images/menu/bottom_label_off.png", scr_width, scr_height)
        self.bottom_label_on = load_img("images/menu/bottom_label_on.png", scr_width, scr_height)
        self.top_label_off = load_img("images/menu/top_label_off.png", scr_width, scr_height)
        self.top_label_on = load_img("images/menu/top_label_on.png", scr_width, scr_height)

        self.items = [Food("Яблоко", 5, "images/food/apple.png", 3),
                      Food("Кость", 8, "images/food/bone.png", 5),
                      Food("Корм", 24, "images/food/dog food.png", 15),
                      Food("Элитный корм", 60, "images/food/dog food elite.png",30, 5),
                      Food("Мясо", 75, "images/food/meat.png", 45, 5),
                      Food("Лекарство", 100, "images/food/medicine.png", 0, 15),]

        self.current_item = 0

        self.item_rect = self.items[0].food_img.get_rect()
        self.item_rect.center = scr_width // 2, scr_height // 2

        self.next_but = Button("Вперёд", scr_width - menuX - but_width, scr_height - menuY - but_height, width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.next)
        self.back_but = Button("Назад", but_width - but_height - 15, scr_height - menuY - but_height, width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.back)
        self.price = self.items[self.current_item].price

    def next(self):
        if self.current_item != len(self.items):
            self.current_item += 1

    def back(self):
        if self.current_item != 0:
            self.current_item -= 1

    def update(self):
        self.next_but.update()
        self.back_but.update()

    def is_clicked(self, event):
        self.next_but.is_clicked(event)
        self.back_but.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].item_icon, self.item_rect)

        self.next_but.draw(screen)
        self.back_but.draw(screen)
        screen.blit(self.price, scr_width//2, scr_height//3)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))


        if self.items[self.current_item].is_using:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))

class ClothesMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_img("images/menu/menu_page.png", scr_width, scr_height)

        self.bottom_label_off = load_img("images/menu/bottom_label_off.png", scr_width, scr_height)
        self.bottom_label_on = load_img("images/menu/bottom_label_on.png", scr_width, scr_height)
        self.top_label_off = load_img("images/menu/top_label_off.png", scr_width, scr_height)
        self.top_label_on = load_img("images/menu/top_label_on.png", scr_width, scr_height)

        self.items = [Item("Синяя футболка", 10, "images/items/blue t-shirt.png"),
                      Item("Ботинки", 50, "images/items/boots.png"),
                      Item("Шляпа", 50, "images/items/hat.png")]

        self.current_item = 0

        self.item_rect = self.items[0].item_icon.get_rect()
        self.item_rect.center = scr_width // 2, scr_height // 2

        self.next_but = Button("Вперёд", scr_width - menuX - but_width, scr_height - menuY - but_height, width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.next)
        self.back_but = Button("Назад", but_width - but_height - 15, scr_height - menuY - but_height, width=int(but_width // 1.2),
                               height=int(but_height // 1.2), func=self.back)
        self.price = self.items[self.current_item].price
    def next(self):
        if self.current_item != len(self.items):
            self.current_item += 1

    def back(self):
        if self.current_item != 0:
            self.current_item -= 1

    def update(self):
        self.next_but.update()
        self.back_but.update()

    def is_clicked(self, event):
        self.next_but.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].item_icon, self.item_rect)

        self.next_but.draw(screen)
        self.back_but.draw(screen)
        screen.blit(self.price, scr_width//2, scr_height//3)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))


        if self.items[self.current_item].is_using:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))


class Game:
    def __init__(self):
        self.screen = p.display.set_mode((scr_width, scr_height))
        p.display.set_caption("Виртуальный питомец")
        i_c_o_n = p.Surface.convert(p.image.load("images/dog.png"))
        p.display.set_icon(i_c_o_n)

        self.mode = "Food menu"

        self.money = 10
        self.coins_per_second = 1000
        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}

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

        self.Cmenu = ClothesMenu(self.money)
        self.Fmenu = FoodMenu(self.money)

        button_x = scr_width - but_width

        self.buttons = [Button("Еда", button_x, padding * 2 + icon_size), Button("Одежда", button_x, (padding * 2 + icon_size)*1.7, func=self.clothes_menu_on), Button("Игры", button_x, (padding * 2 + icon_size)*2.4), Button("Улучшить", scr_width-but_width//2, scr_height-but_height//2, but_width//2, but_height//2, font_jr, func=self.increase_money)]

        self.FARM_MONEY = p.USEREVENT + 1

        p.time.set_timer(self.FARM_MONEY, 1000)
        self.run()

    def clothes_menu_on(self):
        self.mode = "Clothes menu"
    def food_menu_on(self):
        self.mode = "Food menu"



    def increase_money(self):
        for cost, check in self.costs_of_upgrade.items():
            if not check and self.money >= cost:
                self.coins_per_second += 1
                self.money -= cost
                self.costs_of_upgrade[cost] = True
                break

    def click(self, event):
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            self.money += 1
            self.screen.blit("images/money.png")

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def event(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    self.mode = "Main"
            elif event.type == self.FARM_MONEY:
                self.money += 1

            self.buttons[0].is_clicked(event)
            self.buttons[1].is_clicked(event)
            self.buttons[2].is_clicked(event)
            self.buttons[3].is_clicked(event)

    def update(self):
        self.buttons[0].update()
        self.buttons[1].update()
        self.buttons[2].update()
        self.buttons[3].update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.happin_img, (padding * 2, padding * 2))
        self.screen.blit(self.satiety_img, (padding * 2, padding  * 2 + icon_size))
        self.screen.blit(self.health_img, (padding * 2, padding * 2 + icon_size * 2))
        self.screen.blit(self.money_img, (scr_width - icon_size, padding * 2))


        self.screen.blit(text_render(self.happiness), (padding + icon_size, (icon_size - padding * 2)//2))
        self.screen.blit(text_render(self.satiety), (padding + icon_size, (icon_size - padding * 2) * 1.7))
        self.screen.blit(text_render(self.health), (padding + icon_size, (icon_size - padding * 2) * 2.8))
        self.screen.blit(text_render(self.money), (scr_width - icon_size * 1.5, (icon_size - padding * 2)//2))

        self.buttons[0].draw(self.screen)
        self.buttons[1].draw(self.screen)
        self.buttons[2].draw(self.screen)
        self.buttons[3].draw(self.screen)

        self.screen.blit(self.dog_img, (scr_width//2 - dog_width//2, dog_y))

        if self.mode == "Clothes menu":
            self.Cmenu.draw(self.screen)
        if self.mode == "Food menu":
            self.Fmenu.draw(self.screen)
        p.display.flip()


if __name__ == "__main__":
    Game()