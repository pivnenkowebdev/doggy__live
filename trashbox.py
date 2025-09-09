#dry
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
                      Food("Корм", 24, "images/food/dog_food.png", 15),
                      Food("Элитный корм", 60, "images/food/dog_food_elite.png",30, 5),
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
        if self.current_item < len(self.items) - 1:
            self.current_item += 1
            self.price = self.items[self.current_item].price
            self.item_rect = self.items[self.current_item].food_img.get_rect()
            self.item_rect.center = scr_width // 2, scr_height // 2

    def back(self):
        if self.current_item > 0:
            self.current_item -= 1
            self.price = self.items[self.current_item].price
            self.item_rect = self.items[self.current_item].food_img.get_rect()
            self.item_rect.center = scr_width // 2, scr_height // 2

    def update(self):
        self.next_but.update()
        self.back_but.update()

    def is_clicked(self, event):
        self.next_but.is_clicked(event)
        self.back_but.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.current_item].food_img, self.item_rect)

        self.next_but.draw(screen)
        self.back_but.draw(screen)
        screen.blit(text_render(self.price), (scr_width//2, scr_height//3))

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))

        if self.items[self.current_item].is_using:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))

# DRY
class ClothesMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_img("images/menu/menu_page.png", scr_width, scr_height)


        self.bottom_label_off = load_img("images/menu/bottom_label_off.png", scr_width, scr_height)
        self.bottom_label_on = load_img("images/menu/bottom_label_on.png", scr_width, scr_height)

        self.buy_text = text_render("Куплено")
        self.b_t_rect = self.buy_text.get_rect()
        self.b_t_rect.center = (scr_width//1.28, scr_height//2.8)

        self.top_label_off = load_img("images/menu/top_label_off.png", scr_width, scr_height)
        self.top_label_on = load_img("images/menu/top_label_on.png", scr_width, scr_height)

        self.use_text = text_render("Надето")
        self.u_t_rect = self.use_text.get_rect()
        self.u_t_rect.center = (scr_width//1.29, scr_height//4)



        self.items = [Item("Синяя футболка", 10, "images/items/blue t-shirt.png"),
                      Item("Ботинки", 50, "images/items/boots.png"),
                      Item("Шляпа", 50, "images/items/hat.png")]

        self.current_item = 0



        self.item_rect = self.items[0].item_icon.get_rect()
        self.item_rect.center = scr_width // 2, scr_height // 2



        self.price = self.items[self.current_item].price

    def next(self):
        if self.current_item < len(self.items) - 1:
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
        screen.blit(text_render(self.price), (scr_width//2, scr_height//3))

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))



        if self.items[self.current_item].is_using:
            screen.blit(self.top_label_on, (0, 15))
        else:
            screen.blit(self.top_label_off, (0, 15))
        screen.blit(self.buy_text, self.b_t_rect)
        screen.blit(self.use_text, self.u_t_rect)