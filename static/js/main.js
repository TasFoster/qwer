// Счётчик количества на карточке товара
document.querySelectorAll('.qty button[data-step]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const input = btn.parentElement.querySelector('input[type=number]');
    const step = Number(btn.dataset.step);
    const next = Math.min(50, Math.max(1, Number(input.value) + step));
    input.value = next;
  });
});

// Автоскрытие сообщений
setTimeout(() => {
  document.querySelectorAll('.messages li').forEach((li) => {
    li.style.transition = 'opacity .4s, transform .4s';
    li.style.opacity = '0';
    li.style.transform = 'translateY(-8px)';
    setTimeout(() => li.remove(), 400);
  });
}, 3500);
