let canvas = document.getElementById('gameCanvas');
let context = canvas.getContext('2d');
let box = 20;
let snake;
let food;
let direction;
let score;
let game;

document.getElementById('startGame').addEventListener('click', startGame);
document.getElementById('tryAgain').addEventListener('click', startGame);

function startGame() {
    document.getElementById('startGame').style.display = 'none';
    document.getElementById('tryAgain').style.display = 'none';
    snake = [
        { x: 9 * box, y: 10 * box },
        { x: 8 * box, y: 10 * box },
        { x: 7 * box, y: 10 * box }
    ];
    direction = null;
    score = 0;
    document.getElementById('score').textContent = 'Score: ' + score;

    food = {
        x: Math.floor(Math.random() * 19 + 1) * box,
        y: Math.floor(Math.random() * 19 + 1) * box
    };

    document.addEventListener('keydown', setDirection);
    game = setInterval(draw, 100);
}

function setDirection(event) {
    if (event.keyCode === 37 && direction !== 'RIGHT') direction = 'LEFT';
    if (event.keyCode === 38 && direction !== 'DOWN') direction = 'UP';
    if (event.keyCode === 39 && direction !== 'LEFT') direction = 'RIGHT';
    if (event.keyCode === 40 && direction !== 'UP') direction = 'DOWN';
}

function draw() {
    context.fillStyle = '#343434';
    context.fillRect(0, 0, 400, 400);

    for (let i = 0; i < snake.length; i++) {
        context.fillStyle = i === 0 ? '#00FF00' : 'lightgreen';
        context.fillRect(snake[i].x, snake[i].y, box, box);
        context.strokeStyle = '#343434';
        context.strokeRect(snake[i].x, snake[i].y, box, box);
    }

    context.fillStyle = '#FFA836';
    context.beginPath();
    context.arc(food.x + box / 2, food.y + box / 2, box / 2, 0, Math.PI * 2);
    context.fill();

    if (direction) {
        let snakeX = snake[0].x;
        let snakeY = snake[0].y;

        if (direction === 'LEFT') snakeX -= box;
        if (direction === 'UP') snakeY -= box;
        if (direction === 'RIGHT') snakeX += box;
        if (direction === 'DOWN') snakeY += box;

        if (snakeX === food.x && snakeY === food.y) {
            score++;
            document.getElementById('score').textContent = 'Score: ' + score;
            food = {
                x: Math.floor(Math.random() * 19 + 1) * box,
                y: Math.floor(Math.random() * 19 + 1) * box
            };
        } else {
            snake.pop();
        }

        let newHead = { x: snakeX, y: snakeY };

        if (snakeX < 0 || snakeY < 0 || snakeX >= 400 || snakeY >= 400 || collision(newHead, snake)) {
            clearInterval(game);
            document.getElementById('tryAgain').style.display = 'block';
            saveGameResult(score);
        }

        snake.unshift(newHead);
    }
}

function collision(head, array) {
    for (let i = 0; i < array.length; i++) {
        if (head.x === array[i].x && head.y === array[i].y) {
            return true;
        }
    }
    return false;
}

function saveGameResult(score) {
    fetch("{% url 'save_game_result' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: `score=${score}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Game result saved!');
        } else {
            alert('Failed to save game result.');
        }
    });
}
