const canvas = document.getElementById('whiteboard');
const ctx = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');
let currentColor = 'black';

let draw = false;

canvas.addEventListener('mousedown', (e) => {
  draw = true;
  drawLine(e);
});

canvas.addEventListener('mouseup', () => {
  draw = false;
  ctx.beginPath();
});

canvas.addEventListener('mousemove', drawLine);

colorPicker.addEventListener('change', (e) => {
  currentColor = e.target.value;
});

document.getElementById('clear').addEventListener('click', () => {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
});

document.getElementById('back').addEventListener('click', () => {
  window.location.href = '/';  // Assuming 'index.html' is the main page
});

function drawLine(e) {
    if (!draw) return;
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = currentColor;
  
    // Add window scroll positions to ensure proper coordinates
    let x = e.clientX - canvas.offsetLeft + window.scrollX;
    let y = e.clientY - canvas.offsetTop + window.scrollY;
  
    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
  }