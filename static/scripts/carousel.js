const blocks = document.querySelectorAll('.celeb');
let currentIndex = 0;

function showNextBlock() {
  const currentBlock = blocks[currentIndex];
  const nextIndex = (currentIndex + 1) % blocks.length;
  const nextBlock = blocks[nextIndex];

  currentBlock.classList.remove('active', 'fade-in');
  currentBlock.classList.add('fade-out');

  nextBlock.classList.add('active', 'fade-in');
  nextBlock.classList.remove('fade-out');

  currentIndex = nextIndex;
}

setInterval(showNextBlock, 4000);