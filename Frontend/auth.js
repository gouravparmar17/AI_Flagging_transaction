document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Background Animation (Reused for consistency) ---
    const canvas = document.getElementById('neural-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        let particles = [];
        for (let i = 0; i < 50; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 1,
                vy: (Math.random() - 0.5) * 1,
                size: Math.random() * 2 + 1
            });
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach((p, index) => {
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

                ctx.fillStyle = 'rgba(0, 242, 255, 0.3)';
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();

                // Simple connections
                particles.forEach((p2, i2) => {
                    if (index !== i2) {
                        const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                        if (dist < 100) {
                            ctx.strokeStyle = `rgba(188, 19, 254, ${1 - dist/100})`;
                            ctx.beginPath();
                            ctx.moveTo(p.x, p.y);
                            ctx.lineTo(p2.x, p2.y);
                            ctx.stroke();
                        }
                    }
                });
            });
            requestAnimationFrame(animate);
        }
        animate();
    }

    // --- 2. Login Logic ---
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = loginForm.querySelector('button');
            const originalText = btn.innerText;

            // Simulate processing
            btn.innerText = "Authenticating...";
            btn.style.opacity = "0.7";

            setTimeout(() => {
                alert("Login Successful! \nRedirecting to Dashboard...");
                window.location.href = "webpage.html"; // Redirect back to home
            }, 1500);
        });
    }

    // --- 3. Sign Up Logic ---
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = signupForm.querySelector('button');

            // Simulate processing
            btn.innerText = "Creating Profile...";
            btn.style.opacity = "0.7";

            setTimeout(() => {
                alert("Account Created Successfully! \nPlease Login.");
                window.location.href = "login.html"; // Redirect to login
            }, 1500);
        });
    }
});