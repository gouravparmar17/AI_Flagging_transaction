document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Canvas Neural Network Background Effect ---
    const canvas = document.getElementById('neural-canvas');
    const ctx = canvas.getContext('2d');

    let particles = [];
    const particleCount = 60; // Adjust for density
    const connectionDistance = 150;

    // Resize canvas
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * 1.5; // Speed X
            this.vy = (Math.random() - 0.5) * 1.5; // Speed Y
            this.size = Math.random() * 2 + 1;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // Bounce off edges
            if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
        }

        draw() {
            ctx.fillStyle = 'rgba(0, 242, 255, 0.5)'; // Primary color
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    // Init Particles
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();

            // Draw Connections
            for (let j = i; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < connectionDistance) {
                    ctx.beginPath();
                    // Opacity based on distance
                    ctx.strokeStyle = `rgba(188, 19, 254, ${1 - distance / connectionDistance})`;
                    ctx.lineWidth = 1;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animateParticles);
    }
    animateParticles();


    // --- 2. Scroll Reveal Animation ---
    const observerOptions = { threshold: 0.1 };
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show-scroll');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.hidden-scroll').forEach((el) => {
        scrollObserver.observe(el);
    });


    // --- 3. Number Counter Animation ---
    const counters = document.querySelectorAll('.counter');
    const statsSection = document.getElementById('stats-section');
    let counted = false;

    const startCounting = () => {
        if(counted) return;
        counted = true;
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const increment = target / 100;
            const update = () => {
                const c = +counter.innerText;
                if(c < target) {
                    counter.innerText = Math.ceil(c + increment);
                    setTimeout(update, 20);
                } else {
                    counter.innerText = target.toLocaleString() + "+";
                }
            };
            update();
        });
    };

    const statsObserver = new IntersectionObserver((entries) => {
        if(entries[0].isIntersecting) startCounting();
    }, { threshold: 0.5 });

    if(statsSection) statsObserver.observe(statsSection);


    // --- 4. Logic: Drag & Drop + Simulation ---
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const fileInfo = document.getElementById('file-info');
    const uploadBtn = document.getElementById('upload-analyze-btn');
    const loader = document.getElementById('loader-overlay');
    const loadingText = document.getElementById('loading-text');

    browseBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });

    function handleFile(file) {
        if (file.name.endsWith('.csv')) {
            fileInfo.innerHTML = `<i class="fa-solid fa-file-csv"></i> ${file.name}`;
            fileInfo.classList.remove('hidden');
            uploadBtn.disabled = false;
        } else {
            alert('Only CSV files are allowed for the batch processor.');
        }
    }

    function runSimulation() {
        loader.classList.remove('hidden');
        const phrases = ["Connecting to Neural Network...", "Sanitizing Data...", "Running Inference Models...", "Calculating Risk Score..."];

        let i = 0;
        const interval = setInterval(() => {
            if(i < phrases.length) {
                loadingText.innerText = phrases[i];
                i++;
            }
        }, 600);

        setTimeout(() => {
            clearInterval(interval);
            loader.classList.add('hidden');
            const isFraud = Math.random() > 0.5;

            if(isFraud) {
                alert("⚠️ ALERT: High Risk Transaction Detected!\nRisk Score: 92/100\nAction: Flagged for Review");
            } else {
                alert("✅ Success: Transaction is Safe.\nRisk Score: 05/100\nAction: Approved");
            }

            // Reset
            document.getElementById('transaction-form').reset();
            fileInfo.classList.add('hidden');
            uploadBtn.disabled = true;
        }, 3000);
    }

    document.getElementById('transaction-form').addEventListener('submit', (e) => {
        e.preventDefault();
        runSimulation();
    });

    uploadBtn.addEventListener('click', runSimulation);
});