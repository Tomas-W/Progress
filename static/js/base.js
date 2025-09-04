// Nav hover effects
const navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach(link => {
    link.addEventListener("mouseenter", () => {
        navLinks.forEach(otherLink => {
            const animation = otherLink.animate(
                [
                    { color: getComputedStyle(otherLink).color },
                    { color: otherLink === link ? "var(--text-hovered)" : "var(--text-unhovered)" }
                ],
                {
                    duration: 400,
                    easing: "ease",
                    fill: "forwards"
                }
            );
        });
    });

    link.addEventListener("mouseleave", () => {
        navLinks.forEach(otherLink => {
            const animation = otherLink.animate(
                [
                    { color: getComputedStyle(otherLink).color },
                    { color: "var(--text-white)" }
                ],
                {
                    duration: 1500,
                    easing: "ease",
                    fill: "forwards"
                }
            );
        });
    });
}); 