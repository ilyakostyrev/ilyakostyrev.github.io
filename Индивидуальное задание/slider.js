(function() {
    const track = document.getElementById('reviewsTrack');
    const cards = document.querySelectorAll('.review-card');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (!track || cards.length === 0) return;

    let currentIndex = 0;
    let visibleCards = getVisibleCardsCount();
    let maxIndex = cards.length - visibleCards;

    // Определяем количество видимых карточек
    function getVisibleCardsCount() {
        if (window.innerWidth <= 576) return 1;
        if (window.innerWidth <= 768) return 2;
        if (window.innerWidth <= 992) return 3;
        return 4;
    }

    // Обновляем maxIndex и видимость
    function updateBreakpoint() {
        visibleCards = getVisibleCardsCount();
        maxIndex = cards.length - visibleCards;
        if (currentIndex > maxIndex) {
            currentIndex = Math.max(0, maxIndex);
        }
        updateDots();
        moveTrack();
    }

    // Двигаем трек
    function moveTrack() {
        const cardWidth = cards[0]?.offsetWidth || 0;
        const gap = 24; // margin 12px с двух сторон = 24
        const shift = currentIndex * (cardWidth + gap);
        track.style.transform = `translateX(-${shift}px)`;
    }

    // Обновляем точки
    function updateDots() {
        dots.forEach((dot, idx) => {
            if (idx === currentIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    // Нажатие на точки
    dots.forEach((dot, idx) => {
        dot.addEventListener('click', () => {
            if (idx <= maxIndex) {
                currentIndex = idx;
                updateDots();
                moveTrack();
            }
        });
    });

    // Стрелки
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                updateDots();
                moveTrack();
            }
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            if (currentIndex < maxIndex) {
                currentIndex++;
                updateDots();
                moveTrack();
            }
        });
    }

    // При изменении размера окна
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            updateBreakpoint();
        }, 150);
    });

    // При загрузке
    window.addEventListener('load', () => {
        updateBreakpoint();
    });
})();