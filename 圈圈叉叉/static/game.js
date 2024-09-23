const boardElement = document.getElementById('board');
const resultElement = document.getElementById('result');
let gameActive = true;

// 當點擊一個格子時，發送API請求
boardElement.addEventListener('click', async (event) => {
    if (!gameActive) return;
    
    const index = event.target.getAttribute('data-index');
    
    if (index !== null) {
        const response = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ index: parseInt(index) })
        });
        
        const gameState = await response.json();
        updateBoard(gameState.board);
        checkResult(gameState);
    }
});

function updateBoard(board) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        cell.textContent = board[index];
    });
}

function checkResult(gameState) {
    if (!gameState.game_active) {
        if (gameState.winner) {
            resultElement.textContent = `${gameState.winner} wins!`;
        } else {
            resultElement.textContent = 'It\'s a tie!';
        }
        gameActive = false;
    }
}

async function resetGame() {
    const response = await fetch('/reset', { method: 'POST' });
    const gameState = await response.json();
    updateBoard(gameState.board);
    resultElement.textContent = '';
    gameActive = true;
}
