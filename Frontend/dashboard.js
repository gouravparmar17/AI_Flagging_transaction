document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Tab Switching Logic ---
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    const pageTitle = document.getElementById('page-title');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remove active class from all nav items
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active to clicked
            item.classList.add('active');

            // Hide all sections
            sections.forEach(section => section.classList.remove('active'));

            // Show target section
            const tabName = item.getAttribute('data-tab');
            document.getElementById(tabName).classList.add('active');

            // Update Title
            const titleMap = {
                'overview': 'Security Overview',
                'transactions': 'Live Transaction Feed',
                'behavior': 'User Behavior Analytics',
                'alerts': 'Critical Alerts Management',
                'settings': 'System Settings'
            };
            pageTitle.innerText = titleMap[tabName];
        });
    });

    // --- 2. Notification & Message Dropdowns ---
    const setupDropdown = (btnId, menuId) => {
        const btn = document.getElementById(btnId);
        const menu = document.getElementById(menuId);

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('hidden');
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!btn.contains(e.target) && !menu.contains(e.target)) {
                menu.classList.add('hidden');
            }
        });
    };

    setupDropdown('notif-btn', 'notif-dropdown');
    setupDropdown('msg-btn', 'msg-dropdown');


    // --- 3. Search Functionality (Live Filter) ---
    const searchInput = document.getElementById('global-search');
    searchInput.addEventListener('keyup', (e) => {
        const term = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('#txn-table-body tr');

        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(term) ? '' : 'none';
        });
    });


    // --- 4. Chart 1: Overview Line Chart ---
    const ctxMain = document.getElementById('mainChart').getContext('2d');
    const gradient1 = ctxMain.createLinearGradient(0, 0, 0, 400);
    gradient1.addColorStop(0, 'rgba(0, 242, 255, 0.5)');
    gradient1.addColorStop(1, 'rgba(0, 242, 255, 0.0)');

    new Chart(ctxMain, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Transactions',
                data: [1200, 1900, 1500, 2200, 2800, 2400, 3100],
                borderColor: '#00f2ff',
                backgroundColor: gradient1,
                fill: true,
                tension: 0.4
            }]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false }, ticks: { color: '#8b9bb4' } }, y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8b9bb4' } } } }
    });

    // --- 5. Chart 2: Doughnut Chart ---
    new Chart(document.getElementById('doughnutChart').getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Safe', 'Review', 'Critical'],
            datasets: [{
                data: [85, 10, 5],
                backgroundColor: ['#00f2ff', '#bc13fe', '#ff2a6d'],
                borderWidth: 0
            }]
        },
        options: { responsive: true, cutout: '75%', plugins: { legend: { position: 'bottom', labels: { color: '#8b9bb4' } } } }
    });

    // --- 6. Chart 3: Behavior Bar Chart (New) ---
    new Chart(document.getElementById('behaviorChart').getContext('2d'), {
        type: 'bar',
        data: {
            labels: ['Login: NY', 'Login: London', 'Login: Tokyo', 'High Value Txn', 'Pass Change'],
            datasets: [{
                label: 'User Actions Count',
                data: [45, 30, 15, 60, 10],
                backgroundColor: ['#00f2ff', '#00f2ff', '#00f2ff', '#bc13fe', '#ff2a6d'],
                borderRadius: 5
            }]
        },
        options: { responsive: true, scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } }, plugins: { legend: { display: false } } }
    });


    // --- 7. Populate Transaction Table ---
    const tableBody = document.getElementById('txn-table-body');
    const transactions = [
        { id: 'TXN-8841', loc: 'New York, USA', amt: '$5,200', score: 92, status: 'critical', verdict: 'Block', time: '10:42 AM' },
        { id: 'TXN-8842', loc: 'London, UK', amt: '$120', score: 12, status: 'safe', verdict: 'Pass', time: '10:40 AM' },
        { id: 'TXN-8843', loc: 'Lagos, NG', amt: '$950', score: 45, status: 'moderate', verdict: 'Review', time: '10:38 AM' },
        { id: 'TXN-8844', loc: 'Tokyo, JP', amt: '$12,000', score: 88, status: 'critical', verdict: 'Block', time: '10:35 AM' },
        { id: 'TXN-8845', loc: 'Paris, FR', amt: '$45', score: 5, status: 'safe', verdict: 'Pass', time: '10:30 AM' },
        { id: 'TXN-8846', loc: 'Berlin, DE', amt: '$2,300', score: 70, status: 'moderate', verdict: 'Review', time: '10:28 AM' },
        { id: 'TXN-8847', loc: 'Toronto, CA', amt: '$15.50', score: 2, status: 'safe', verdict: 'Pass', time: '10:25 AM' },
    ];

    transactions.forEach(txn => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td style="color:#fff; font-weight:bold;">${txn.id}</td>
            <td>${txn.loc}</td>
            <td>${txn.amt}</td>
            <td><span class="score">${txn.score}/100</span></td>
            <td><span class="status-badge ${txn.status}">${txn.verdict}</span></td>
            <td style="color:var(--text-muted); font-size:0.8rem;">${txn.time}</td>
            <td><button class="action-btn">Details</button></td>
        `;
        tableBody.appendChild(row);
    });
});