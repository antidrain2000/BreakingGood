import arcade
import random

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
SCREEN_TITLE = "BreakingGood"

TRUCK_SCALE = 0.8
CAR_SCALE = 0.5
COIN_SCALE = 0.3

TRUCK_SPEED = 1
CAR_SPEED = 4
CAR_COUNT = 3
COIN_COUNT = 2
WINNING_COINS = 30

LANE_COUNT = 3
LANE_WIDTH = SCREEN_WIDTH // LANE_COUNT


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Заставки
        self.start_screen_index = 0
        self.start_screens = [
            arcade.load_texture("start_screen1.png"),
            arcade.load_texture("start_screen2.png")
        ]
        self.game_over_screen = arcade.load_texture("game_over.png")
        self.win_screen = arcade.load_texture("win.png")

        # Фон
        self.background = arcade.load_texture("background.png")

        # Фура
        self.truck = arcade.Sprite("truck.png", TRUCK_SCALE)
        self.truck.center_x = LANE_WIDTH // 2
        self.truck.center_y = 50
        self.current_lane = 1

        self.car_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        self.score = 0
        self.game_over = False
        self.win = False

        self.setup()

    def setup(self):
        self.truck.center_x = LANE_WIDTH // 2
        self.truck.center_y = 50
        self.current_lane = 1
        self.car_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.score = 0
        self.game_over = False
        self.win = False

        # Встречные машины
        for _ in range(CAR_COUNT):
            car = arcade.Sprite("car.png", CAR_SCALE)
            car.center_x = random.choice(
                [300, 550, 800])
            car.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
            self.car_list.append(car)

        # Бочки
        for _ in range(COIN_COUNT):
            coin = arcade.Sprite("coin.png", COIN_SCALE)
            coin.center_x = random.choice(
                [300, 550, 800])
            coin.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
            self.coin_list.append(coin)

    def on_draw(self):
        arcade.start_render()

        if self.start_screen_index < len(self.start_screens):
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.start_screens[self.start_screen_index])

        elif self.game_over:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_over_screen)
            arcade.draw_text(f"You collected {self.score} coins", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                             arcade.color.WHITE, 24, anchor_x="center")
        elif self.win:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.win_screen)
            arcade.draw_text(f"You collected {self.score} coins", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                             arcade.color.WHITE, 24, anchor_x="center")
        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
            self.truck.draw()
            self.car_list.draw()
            self.coin_list.draw()
            arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 16)

    def on_update(self, delta_time):
        if not self.start_screen_index < len(self.start_screens) and not self.game_over and not self.win:
            self.truck.update()
            self.car_list.update()
            self.coin_list.update()

            for car in self.car_list:
                car.center_y -= CAR_SPEED
                if car.center_y < 0:
                    car.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
                    car.center_x = random.choice(
                        [300, 550 , 800])

            for coin in self.coin_list:
                coin.center_y -= CAR_SPEED
                if coin.center_y < 0:
                    coin.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
                    coin.center_x = random.choice(
                        [LANE_WIDTH // 2, LANE_WIDTH // 2 + LANE_WIDTH, LANE_WIDTH // 2 + 2 * LANE_WIDTH])

            if arcade.check_for_collision_with_list(self.truck, self.car_list):
                self.game_over = True

            coins_hit = arcade.check_for_collision_with_list(self.truck, self.coin_list)
            for coin in coins_hit:
                coin.remove_from_sprite_lists()
                self.score += 1

            if self.score >= WINNING_COINS:
                self.win = True

    def on_key_press(self, key, modifiers):
        if self.start_screen_index < len(self.start_screens):
            if key == arcade.key.SPACE:
                self.start_screen_index += 1
        elif self.game_over or self.win:
            if key == arcade.key.SPACE:
                self.setup()
        else:
            if key == arcade.key.LEFT and self.current_lane > 0:
                self.current_lane -= 1
                self.truck.center_x = LANE_WIDTH // 2 + self.current_lane * LANE_WIDTH
            elif key == arcade.key.RIGHT and self.current_lane < LANE_COUNT - 1:
                self.current_lane += 1
                self.truck.center_x = LANE_WIDTH // 2 + self.current_lane * LANE_WIDTH


def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
