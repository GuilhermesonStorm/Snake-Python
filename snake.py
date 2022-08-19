from random import randint
from tkinter import *
from PIL import Image, ImageTk

#Constante de movimento
MOVE_INCREMENT = 20
moves_per_second = 15
GAME_SPEED = 1000 // moves_per_second

class Snake(Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, 
        background='black', highlightthickness=0)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_food_position()
        self.score = 0
        self.direction = "Right"

        self.load_assets()
        self.create_objects()
        self.bind_all('<Key>', self.on_key_press)

        self.after(GAME_SPEED, self.perform_actions)
    
    #Carregando as imagens
    def load_assets(self):
        #Try - except no caso de não haver imagens
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.snake_food_image = Image.open("./assets/food.png")
            self.snake_food = ImageTk.PhotoImage(self.snake_food_image)
        except IOError as error:
            print(error)
            root.destroy()
    
    #criando os objetos Snake e Food e a interface
    def create_objects(self):
        #Criando o texto da pontuação
        self.create_text(
            300, 
            12, 
            text=f"Pontos: {self.score} (Velocidade: {moves_per_second})", 
            tag="score", 
            fill="#fff", 
            font=("TkDefaultFont", 14)
        )

        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")
        
        #asterisco faz a desestruturação da tupla
        self.create_image(*self.food_position, image=self.snake_food, tag="food")

        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    #Criando o movimento do objeto Snake
    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]
        new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction =="Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction =="Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction =="Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)



        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    #movendo o objeto Snake
    def perform_actions(self):
        if self.check_collisions():
            self.game_over()
            return
        
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    #Criando as colisões
    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return(
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]
        )
    
    def on_key_press(self, event):
        new_direction = event.keysym
        all_directions = ("Up", "Down", "Right", "Left")
        opposites = ({"Up", "Down"}, {"Right", "Left"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction
    
    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global moves_per_second
                moves_per_second += 1

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            self.food_position = self.set_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(
                score, 
                text=f"Pontos: {self.score} (Velocidade: {moves_per_second})", 
                tag="score"
            )

    def set_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

    def game_over(self):
        self.delete(ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"FIM DE JOGO! Sua pontuação foi: {self.score}",
            fill="#fff",
            font=("TkDefaultFont", 24)
        )

root = Tk()
root.title('Snake')
root.resizable(False, False)

board = Snake()
board.pack()

root.mainloop()