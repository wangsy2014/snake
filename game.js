const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const gridSize = 20;
const tileCount = canvas.width / gridSize;

let snake = [
    { x: 10, y: 10 },
];
let food = { x: 15, y: 15 };
let dx = 0;
let dy = 0;
let score = 0;
let gameSpeed = 200;
let gameLoop;

// 游戏主循环
function game() {
    moveSnake();
    if (checkCollision()) {
        gameOver();
        return;
    }
    
    checkFood();
    drawGame();
}

// 移动蛇
function moveSnake() {
    const head = { x: snake[0].x + dx, y: snake[0].y + dy };
    snake.unshift(head);
    if (!checkFood()) {
        snake.pop();
    }
}

// 检查碰撞
function checkCollision() {
    const head = snake[0];
    
    // 检查墙壁碰撞
    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
        return true;
    }
    
    // 检查自身碰撞
    for (let i = 1; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            return true;
        }
    }
    return false;
}

// 检查是否吃到食物
function checkFood() {
    const head = snake[0];
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        document.getElementById('score').textContent = score;
        generateFood();
        increaseSpeed();
        return true;
    }
    return false;
}

// 生成食物
function generateFood() {
    food.x = Math.floor(Math.random() * tileCount);
    food.y = Math.floor(Math.random() * tileCount);
    
    // 确保食物不会生成在蛇身上
    for (let part of snake) {
        if (food.x === part.x && food.y === part.y) {
            generateFood();
            break;
        }
    }
}

// 绘制游戏
function drawGame() {
    // 清空画布
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 绘制蛇
    ctx.fillStyle = 'green';
    for (let part of snake) {
        ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
    }
    
    // 绘制蛇头
    ctx.fillStyle = 'darkgreen';
    ctx.fillRect(snake[0].x * gridSize, snake[0].y * gridSize, gridSize - 2, gridSize - 2);
    
    // 绘制食物
    ctx.fillStyle = 'red';
    ctx.beginPath();
    ctx.arc(
        food.x * gridSize + gridSize/2,
        food.y * gridSize + gridSize/2,
        gridSize/2 - 2,
        0,
        Math.PI * 2
    );
    ctx.fill();
}

// 增加游戏速度
function increaseSpeed() {
    if (gameSpeed > 100) {
        gameSpeed -= 1;
        clearInterval(gameLoop);
        gameLoop = setInterval(game, gameSpeed);
    }
}

// 游戏结束
function gameOver() {
    clearInterval(gameLoop);
    document.getElementById('gameOver').style.display = 'block';
    document.getElementById('finalScore').textContent = score;
}

// 重新开始游戏
function restartGame() {
    snake = [{ x: 10, y: 10 }];
    dx = 0;
    dy = 0;
    score = 0;
    gameSpeed = 200;
    document.getElementById('score').textContent = '0';
    document.getElementById('gameOver').style.display = 'none';
    generateFood();
    gameLoop = setInterval(game, gameSpeed);
}

// 键盘控制
document.addEventListener('keydown', (event) => {
    switch(event.key) {
        case 'ArrowUp':
            if (dy === 0) { dx = 0; dy = -1; }
            break;
        case 'ArrowDown':
            if (dy === 0) { dx = 0; dy = 1; }
            break;
        case 'ArrowLeft':
            if (dx === 0) { dx = -1; dy = 0; }
            break;
        case 'ArrowRight':
            if (dx === 0) { dx = 1; dy = 0; }
            break;
    }
});

// 开始游戏
generateFood();
gameLoop = setInterval(game, gameSpeed); 