document.addEventListener('DOMContentLoaded', () => {
  // 1. Chức năng Chuyển đổi Giao diện Sáng / Tối (Dark / Light Mode)
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const root = document.documentElement;

  const getInitialTheme = () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };

  const applyTheme = (theme) => {
    if (theme === 'dark') {
      root.setAttribute('data-theme', 'dark');
      if (themeIcon) themeIcon.textContent = '☀️';
    } else {
      root.removeAttribute('data-theme');
      if (themeIcon) themeIcon.textContent = '🌙';
    }
    localStorage.setItem('theme', theme);
  };

  applyTheme(getInitialTheme());

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
    });
  }

  // 2. Chức năng Hiệu ứng Chuyển đổi Lời chào (Greeting cycle)
  const greetingPrefix = document.querySelector('.greeting-prefix');
  const greetings = ['Xin chào,', 'Chào bạn,', 'Hi there,', 'Hello World,'];
  let greetingIndex = 0;

  if (greetingPrefix) {
    setInterval(() => {
      greetingPrefix.style.opacity = '0';
      greetingPrefix.style.transform = 'translateY(-4px)';

      setTimeout(() => {
        greetingIndex = (greetingIndex + 1) % greetings.length;
        greetingPrefix.textContent = greetings[greetingIndex];
        greetingPrefix.style.opacity = '1';
        greetingPrefix.style.transform = 'translateY(0)';
      }, 300);
    }, 4000);
  }

  // 3. Nút Toggle mở rộng thông tin "Mục tiêu & Định hướng"
  const toggleBtn = document.getElementById('toggleInfoBtn');
  const infoBox = document.getElementById('extraInfo');

  if (toggleBtn && infoBox) {
    const setInfoState = (isOpen) => {
      infoBox.classList.toggle('is-open', isOpen);
      infoBox.setAttribute('aria-hidden', String(!isOpen));
      toggleBtn.setAttribute('aria-expanded', String(isOpen));
      
      const btnSpan = toggleBtn.querySelector('span');
      if (btnSpan) {
        btnSpan.textContent = isOpen ? 'Thu gọn thông tin' : 'Mục tiêu & Định hướng tiếp theo';
      }
    };

    toggleBtn.addEventListener('click', () => {
      const shouldOpen = !infoBox.classList.contains('is-open');
      setInfoState(shouldOpen);
    });

    setInfoState(false);
  }

  // 4. Chức năng Sao chép Email nhanh kèm Toast thông báo
  const copyBtn = document.getElementById('copyEmailBtn');
  const emailText = document.getElementById('emailText');
  const toast = document.getElementById('toast');
  let toastTimer = null;

  const showToast = (message) => {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2500);
  };

  if (copyBtn && emailText) {
    copyBtn.addEventListener('click', async () => {
      const email = emailText.textContent.trim();
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(email);
        } else {
          // Fallback cho trình duyệt cũ
          const textArea = document.createElement('textarea');
          textArea.value = email;
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand('copy');
          document.body.removeChild(textArea);
        }
        showToast('✓ Đã sao chép email: ' + email);
      } catch (err) {
        showToast('Không thể sao chép, vui lòng copy thủ công!');
      }
    });
  }
});
