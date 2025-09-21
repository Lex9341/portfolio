/* static/js/main.js
   Терминал + фильтр проектов + модалки
   Работает с Alpine.js, но имеет fallback на чистый JS
*/

/* безопасное экранирование для вывода в терминал */
function _escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (s) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    })[s]);
}

/* --- Терминал --- */
function terminal() {
    return {
        cmd: '',
        output: '<div>Добро пожаловать! Попробуй команды: <strong>about</strong>, <strong>skills</strong>, <strong>projects</strong>, <strong>help</strong></div>',
        history: [],
        runCmd() {
            const c = (this.cmd || '').trim().toLowerCase();
            if (!c) return;

            this.history.push(c);

            if (c === 'about') {
                this.output += '<div>Я — Python/Django разработчик. Введи <strong>projects</strong> чтобы посмотреть проекты.</div>';
            } else if (c === 'skills') {
                this.output += '<div>Навыки: Python, Django, JS, SQL, Git.</div>';
                setTimeout(() => document.querySelector('#skills')?.scrollIntoView({ behavior: 'smooth' }), 80);
            } else if (c === 'projects') {
                this.output += '<div>Открываю раздел Projects...</div>';
                setTimeout(() => document.querySelector('#projects')?.scrollIntoView({ behavior: 'smooth' }), 80);
            } else if (c === 'help') {
                this.output += '<div>Команды: <strong>about</strong>, <strong>skills</strong>, <strong>projects</strong>, <strong>help</strong></div>';
            } else {
                this.output += `<div>Неизвестная команда: ${_escapeHtml(c)}</div>`;
            }

            this.cmd = '';
            setTimeout(() => {
                const out = document.querySelector('.terminal-output');
                if (out) out.scrollTop = out.scrollHeight;
            }, 0);
        }
    };
}

/* --- Фильтр проектов --- */
function projectsFilter() {
    return {
        active: 'all',
        filter(tag) {
            this.active = tag || 'all';
            const activeLower = this.active.toLowerCase();
            const cards = document.querySelectorAll('.project-card');

            cards.forEach(c => {
                const tags = (c.dataset.tags || '')
                    .toLowerCase()
                    .split(/[\s,]+/)
                    .filter(Boolean);

                const visible = (activeLower === 'all') || tags.includes(activeLower);

                c.style.display = visible ? '' : 'none';
            });

            // обновляем кнопки
            document.querySelectorAll('.tags-bar button').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.tag?.toLowerCase() === activeLower);
            });
        }
    };
}

document.addEventListener('DOMContentLoaded', () => {
    // fallback фильтр без Alpine
    if (!window.Alpine) {
        document.querySelectorAll('.tags-bar button').forEach(btn => {
            btn.addEventListener('click', () => {
                projectsFilter().filter(btn.dataset.tag);
            });
        });
        projectsFilter().filter('all');
    }

    /* --- Модалка проектов --- */
    const projectModal = document.getElementById("projectModal");
    const closeProjectModal = document.getElementById("closeProjectModal");

    document.querySelectorAll(".btn-details").forEach(btn => {
        btn.addEventListener("click", () => {
            projectModal.querySelector("#modalTitle").textContent = btn.dataset.title;
            projectModal.querySelector("#modalDescription").textContent = btn.dataset.description;
            projectModal.querySelector("#modalImage").src = btn.dataset.image;
            projectModal.style.display = "flex";
        });
    });

    if (closeProjectModal) {
        closeProjectModal.addEventListener("click", () => {
            projectModal.style.display = "none";
        });
    }
    window.addEventListener("click", e => {
        if (e.target === projectModal) projectModal.style.display = "none";
    });

    /* --- Модалка Спасибо (после формы) --- */
    const thankModal = document.getElementById("thankYouModal");
    const closeModalBtn = document.getElementById("closeModal");

    if (thankModal) {
        thankModal.style.display = "flex";
        function closeWithAnimation() {
            thankModal.classList.add("closing");
            setTimeout(() => {
                thankModal.style.display = "none";
                thankModal.classList.remove("closing");
            }, 400);
        }
        if (closeModalBtn) closeModalBtn.addEventListener("click", closeWithAnimation);
        window.addEventListener("click", (e) => {
            if (e.target === thankModal) closeWithAnimation();
        });
    }
});
