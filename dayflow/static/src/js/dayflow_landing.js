/** Landing page interactions — scoped to .o_dayflow_landing only. */

document.addEventListener('DOMContentLoaded', function () {
    var root = document.querySelector('.o_dayflow_landing');
    if (!root) {
        return;
    }

    var nav = root.querySelector('.df-nav');
    var menuBtn = root.querySelector('.df-menu');
    var links = root.querySelector('.df-links');
    var menuOpenIcon = root.querySelector('.df-menu-icon-open');
    var menuCloseIcon = root.querySelector('.df-menu-icon-close');

    function setMenuOpen(open) {
        if (!links || !menuBtn) {
            return;
        }
        links.classList.toggle('open', open);
        menuBtn.setAttribute('aria-expanded', String(open));
        if (menuOpenIcon) {
            menuOpenIcon.hidden = open;
        }
        if (menuCloseIcon) {
            menuCloseIcon.hidden = !open;
        }
    }

    if (menuBtn && links) {
        menuBtn.addEventListener('click', function () {
            setMenuOpen(!links.classList.contains('open'));
        });

        links.querySelectorAll('a[href^="#"]').forEach(function (link) {
            link.addEventListener('click', function () {
                setMenuOpen(false);
            });
        });
    }

    window.addEventListener('scroll', function () {
        if (nav) {
            nav.classList.toggle('is-scrolled', window.scrollY > 20);
        }
    });
});
