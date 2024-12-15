import tkinter as tk
from tkinter import messagebox
import random
import time

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("贪吃蛇游戏")
        
        # 游戏常量
        self.GRID_SIZE = 20
        self.GRID_COUNT = 30
        self.GAME_SIZE = self.GRID_SIZE * self.GRID_COUNT
        
        # 颜色定义
        self.COLORS = {
            'background': '#F0F0F0',
            'snake_head': '#006400',  # 深绿色蛇头
            'snake_body': '#32CD32',  # 浅绿色蛇身
            'food': '#FF0000',        # 红色食物
            'grid': '#E0E0E0'         # 网格线颜色
        }
        
        # 游戏状态
        self.snake = [(self.GRID_COUNT//2, self.GRID_COUNT//2)]
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.food = self.generate_food()
        self.score = 0
        self.speed = 200
        self.game_running = False
        
        # 创建UI元素
        self.setup_ui()
        
        # 绑定按键
        self.root.bind('<Key>', self.handle_keypress)
        
    def setup_ui(self):
        # 分数显示
        self.score_label = tk.Label(
            self.root,
            text=f"分数: {self.score}",
            font=('Arial', 16)
        )
        self.score_label.pack(pady=10)
        
        # 游戏画布
        self.canvas = tk.Canvas(
            self.root,
            width=self.GAME_SIZE,
            height=self.GAME_SIZE,
            bg=self.COLORS['background']
        )
        self.canvas.pack(padx=10, pady=10)
        
        # 开始按钮
        self.start_button = tk.Button(
            self.root,
            text="开始游戏",
            command=self.start_game,
            font=('Arial', 12)
        )
        self.start_button.pack(pady=10)
        
        # 绘制网格
        self.draw_grid()
        
    def draw_grid(self):
        # 绘制垂直线
        for i in range(self.GRID_COUNT + 1):
            x = i * self.GRID_SIZE
            self.canvas.create_line(
                x, 0, x, self.GAME_SIZE,
                fill=self.COLORS['grid']
            )
        
        # 绘制水平线
        for i in range(self.GRID_COUNT + 1):
            y = i * self.GRID_SIZE
            self.canvas.create_line(
                0, y, self.GAME_SIZE, y,
                fill=self.COLORS['grid']
            )
            
    def generate_food(self):
        while True:
            x = random.randint(0, self.GRID_COUNT-1)
            y = random.randint(0, self.GRID_COUNT-1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def draw_game(self):
        self.canvas.delete('snake', 'food')
        
        # 绘制食物
        food_x = self.food[0] * self.GRID_SIZE
        food_y = self.food[1] * self.GRID_SIZE
        self.canvas.create_oval(
            food_x + 2, food_y + 2,
            food_x + self.GRID_SIZE - 2,
            food_y + self.GRID_SIZE - 2,
            fill=self.COLORS['food'],
            tags='food'
        )
        
        # 绘制蛇
        for i, (x, y) in enumerate(self.snake):
            color = self.COLORS['snake_head'] if i == 0 else self.COLORS['snake_body']
            self.canvas.create_rectangle(
                x * self.GRID_SIZE + 1,
                y * self.GRID_SIZE + 1,
                (x + 1) * self.GRID_SIZE - 1,
                (y + 1) * self.GRID_SIZE - 1,
                fill=color,
                tags='snake'
            )
    
    def move_snake(self):
        if not self.game_running:
            return
            
        # 更新方向
        self.direction = self.next_direction
        
        # 获取蛇头位置
        head = self.snake[0]
        
        # 根据方向移动蛇头
        if self.direction == 'Up':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'Down':
            new_head = (head[0], head[1] + 1)
        elif self.direction == 'Left':
            new_head = (head[0] - 1, head[1])
        else:  # Right
            new_head = (head[0] + 1, head[1])
            
        # 检查碰撞
        if (new_head[0] < 0 or new_head[0] >= self.GRID_COUNT or
            new_head[1] < 0 or new_head[1] >= self.GRID_COUNT or
            new_head in self.snake):
            self.game_over()
            return
            
        # 移动蛇
        self.snake.insert(0, new_head)
        
        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"分数: {self.score}")
            self.food = self.generate_food()
            self.increase_speed()
        else:
            self.snake.pop()
            
        self.draw_game()
        self.root.after(self.speed, self.move_snake)
        
    def increase_speed(self):
        if self.speed > 50:
            self.speed = max(50, self.speed - 10)
            
    def handle_keypress(self, event):
        key = event.keysym
        
        # 防止蛇反向移动
        if (key == 'Up' and self.direction != 'Down' or
            key == 'Down' and self.direction != 'Up' or
            key == 'Left' and self.direction != 'Right' or
            key == 'Right' and self.direction != 'Left'):
            self.next_direction = key
            
    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.start_button.config(state='disabled')
            self.move_snake()
            
    def game_over(self):
        self.game_running = False
        messagebox.showinfo("游戏结束", f"游戏结束！\n最终得分: {self.score}")
        self.reset_game()
        
    def reset_game(self):
        self.snake = [(self.GRID_COUNT//2, self.GRID_COUNT//2)]
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.food = self.generate_food()
        self.score = 0
        self.speed = 200
        self.score_label.config(text=f"分数: {self.score}")
        self.start_button.config(state='normal')
        self.draw_game()

if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop() 