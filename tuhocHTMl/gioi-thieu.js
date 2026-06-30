const infoBox = document.getElementById('extraInfo');
const toggleBtn = document.getElementById('toggleInfoBtn');

if (toggleBtn && infoBox) {
  toggleBtn.addEventListener('click', () => {
    const isHidden = infoBox.style.display === 'none' || infoBox.style.display === '';
    infoBox.style.display = isHidden ? 'block' : 'none';
    toggleBtn.textContent = isHidden ? 'Ẩn thông tin thêm' : 'Xem thêm thông tin';
  });
}

const greeting = document.querySelector('header h1');
const greetings = ['Xin chào', 'Chào bạn', 'Hi there', 'Hello'];
let index = 0;

if (greeting) {
  setInterval(() => {
    index = (index + 1) % greetings.length;
    greeting.textContent = `${greetings[index]}, mình là: TRẦN LÊ BẢO CƯỜNG`;
  }, 5000);
}
