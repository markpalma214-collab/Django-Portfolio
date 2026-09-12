document.addEventListener("DOMContentLoaded", () => {
    /* ---------------- Mobile navigation toggle ---------------- */
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });

        navLinks.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => navLinks.classList.remove("open"));
        });
    }

    /* ---------------- CSRF helper (Django convention) ---------------- */
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(";").shift();
        return null;
    }
    const csrftoken = getCookie("csrftoken");

    /* ---------------- Review like / unlike ---------------- */
    document.querySelectorAll(".like-btn").forEach((button) => {
        button.addEventListener("click", async () => {
            if (button.disabled) return;

            const reviewId = button.dataset.reviewId;
            button.disabled = true;

            try {
                const response = await fetch(`/reviews/${reviewId}/like/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                });

                if (!response.ok) {
                    throw new Error("Request failed");
                }

                const data = await response.json();
                const countEl = button.querySelector(".like-count");
                countEl.textContent = data.like_count;
                button.classList.toggle("liked", data.liked);
            } catch (err) {
                console.error("Could not toggle like:", err);
            } finally {
                button.disabled = false;
            }
        });
    });

    /* ---------------- Highlight active nav link on scroll ---------------- */
    const sections = document.querySelectorAll(".section[id]");
    const navAnchors = document.querySelectorAll(".nav-link[href^='#']");

    if (sections.length && navAnchors.length && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        navAnchors.forEach((a) => a.classList.remove("active"));
                        const match = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
                        if (match) match.classList.add("active");
                    }
                });
            },
            { threshold: 0.5 }
        );

        sections.forEach((section) => observer.observe(section));
    }
});
