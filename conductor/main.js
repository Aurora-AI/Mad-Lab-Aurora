/* AURORA CONDUCTOR - INTERACTIVE ENGINE */

document.addEventListener('DOMContentLoaded', () => {
    // GSAP initialization
    gsap.registerPlugin(ScrollTrigger);

    // Hero Animations
    gsap.from(".hero h1", {
        y: 50,
        opacity: 0,
        duration: 1,
        ease: "power4.out"
    });

    gsap.from(".hero p", {
        y: 30,
        opacity: 0,
        duration: 1,
        delay: 0.3,
        ease: "power4.out"
    });

    gsap.from(".hero-actions", {
        y: 20,
        opacity: 0,
        duration: 1,
        delay: 0.5,
        ease: "power4.out"
    });

    // Reveal animations on scroll
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        gsap.from(section, {
            scrollTrigger: {
                trigger: section,
                start: "top 80%",
                toggleActions: "play none none none"
            },
            opacity: 0,
            y: 50,
            duration: 1,
            ease: "power3.out"
        });
    });

    // Grid Card stagger
    gsap.from(".grid-card", {
        scrollTrigger: {
            trigger: ".diag-grid",
            start: "top 80%"
        },
        y: 100,
        opacity: 0,
        stagger: 0.2,
        duration: 1,
        ease: "power2.out"
    });

    // Matrix background simulation (optional but cool)
    console.log("Aurora Conductor Engine Initialized. Logic Extraction Active.");
});
