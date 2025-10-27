// DevPal - Tinder-like Swipe Functionality
class SwipeCardManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.cards = [];
        this.currentCardIndex = 0;
        this.isAnimating = false;
        this.startX = 0;
        this.startY = 0;
        this.currentX = 0;
        this.currentY = 0;
        this.threshold = 100;
        
        this.init();
    }

    init() {
        if (!this.container) return;
        
        this.loadCards();
        this.setupEventListeners();
        this.showCurrentCard();
    }

    async loadCards() {
        try {
            // Check if user is authenticated
            const token = localStorage.getItem('access_token');
            if (!token) {
                this.showError('Please log in to view projects');
                return;
            }
            
            const response = await fetch('/api/projects/api/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });
            
            if (response.status === 401) {
                this.showError('Please log in to view projects');
                return;
            }
            
            const projects = await response.json();
            
            this.cards = projects.map(project => ({
                id: project.id,
                title: project.title,
                description: project.description,
                techStack: project.tech_stack || [],
                neededRoles: project.needed_roles || [],
                createdBy: project.created_by,
                members: project.members || [],
                createdAt: project.created_at
            }));
            
            this.renderCards();
        } catch (error) {
            console.error('Error loading projects:', error);
            this.showError('Failed to load projects');
        }
    }

    renderCards() {
        this.container.innerHTML = '';
        
        if (this.cards.length === 0) {
            this.showEmptyState();
            return;
        }

        this.cards.forEach((card, index) => {
            const cardElement = this.createCardElement(card, index);
            this.container.appendChild(cardElement);
        });

        this.showCurrentCard();
    }

    createCardElement(card, index) {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'swipe-card';
        cardDiv.style.zIndex = this.cards.length - index;
        cardDiv.dataset.cardId = card.id;
        
        const techTags = card.techStack.map(tech => 
            `<span class="tag tech">${tech}</span>`
        ).join('');
        
        const roleTags = card.neededRoles.map(role => 
            `<span class="tag role">${role}</span>`
        ).join('');

        cardDiv.innerHTML = `
            <div class="card-header">
                <h3 class="card-title">${card.title}</h3>
                <p class="card-subtitle">Created by User #${card.createdBy}</p>
            </div>
            <div class="card-body">
                <p class="card-description">${card.description}</p>
                <div class="card-tags">
                    ${techTags}
                    ${roleTags}
                </div>
            </div>
            <div class="card-footer">
                <div class="card-meta">
                    <i class="fas fa-users"></i>
                    ${card.members.length} members
                </div>
                <div class="card-meta">
                    <i class="fas fa-calendar"></i>
                    ${new Date(card.createdAt).toLocaleDateString()}
                </div>
            </div>
            <div class="swipe-indicator left">NOPE</div>
            <div class="swipe-indicator right">LIKE</div>
        `;

        return cardDiv;
    }

    showCurrentCard() {
        const cards = this.container.querySelectorAll('.swipe-card');
        cards.forEach((card, index) => {
            if (index === this.currentCardIndex) {
                card.style.display = 'block';
                card.classList.add('fade-in');
            } else {
                card.style.display = 'none';
            }
        });
    }

    showEmptyState() {
        this.container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-project-diagram"></i>
                <h3>No more projects!</h3>
                <p>You've seen all available projects. Check back later for new ones!</p>
                <button class="btn btn-primary" onclick="location.reload()">
                    <i class="fas fa-refresh"></i> Refresh
                </button>
            </div>
        `;
    }

    showError(message) {
        this.container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Error</h3>
                <p>${message}</p>
                <button class="btn btn-primary" onclick="location.reload()">
                    <i class="fas fa-refresh"></i> Try Again
                </button>
            </div>
        `;
    }

    setupEventListeners() {
        const currentCard = this.getCurrentCard();
        if (!currentCard) return;

        // Touch events
        currentCard.addEventListener('touchstart', this.handleStart.bind(this), { passive: false });
        currentCard.addEventListener('touchmove', this.handleMove.bind(this), { passive: false });
        currentCard.addEventListener('touchend', this.handleEnd.bind(this), { passive: false });

        // Mouse events
        currentCard.addEventListener('mousedown', this.handleStart.bind(this));
        currentCard.addEventListener('mousemove', this.handleMove.bind(this));
        currentCard.addEventListener('mouseup', this.handleEnd.bind(this));
        currentCard.addEventListener('mouseleave', this.handleEnd.bind(this));

        // Action buttons
        this.setupActionButtons();
    }

    setupActionButtons() {
        const actionButtons = document.querySelector('.action-buttons');
        if (!actionButtons) return;

        actionButtons.innerHTML = `
            <button class="action-btn pass" onclick="swipeManager.swipeLeft()">
                <i class="fas fa-times"></i>
            </button>
            <button class="action-btn info" onclick="swipeManager.showDetails()">
                <i class="fas fa-info"></i>
            </button>
            <button class="action-btn like" onclick="swipeManager.swipeRight()">
                <i class="fas fa-heart"></i>
            </button>
        `;
    }

    handleStart(e) {
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        
        this.startX = clientX;
        this.startY = clientY;
        
        const currentCard = this.getCurrentCard();
        if (currentCard) {
            currentCard.classList.add('swiping');
        }
        
        e.preventDefault();
    }

    handleMove(e) {
        if (!this.isAnimating) return;
        
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        
        this.currentX = clientX - this.startX;
        this.currentY = clientY - this.startY;
        
        const currentCard = this.getCurrentCard();
        if (currentCard) {
            const rotation = this.currentX / 10;
            currentCard.style.transform = `translateX(${this.currentX}px) translateY(${this.currentY}px) rotate(${rotation}deg)`;
            
            // Show swipe indicators
            const leftIndicator = currentCard.querySelector('.swipe-indicator.left');
            const rightIndicator = currentCard.querySelector('.swipe-indicator.right');
            
            if (this.currentX < -50) {
                leftIndicator.classList.add('show');
                rightIndicator.classList.remove('show');
            } else if (this.currentX > 50) {
                rightIndicator.classList.add('show');
                leftIndicator.classList.remove('show');
            } else {
                leftIndicator.classList.remove('show');
                rightIndicator.classList.remove('show');
            }
        }
        
        e.preventDefault();
    }

    handleEnd(e) {
        if (!this.isAnimating) return;
        
        const currentCard = this.getCurrentCard();
        if (!currentCard) return;
        
        currentCard.classList.remove('swiping');
        
        // Reset indicators
        const leftIndicator = currentCard.querySelector('.swipe-indicator.left');
        const rightIndicator = currentCard.querySelector('.swipe-indicator.right');
        leftIndicator.classList.remove('show');
        rightIndicator.classList.remove('show');
        
        if (Math.abs(this.currentX) > this.threshold) {
            if (this.currentX < 0) {
                this.swipeLeft();
            } else {
                this.swipeRight();
            }
        } else {
            // Snap back
            currentCard.style.transform = '';
        }
        
        this.isAnimating = false;
        e.preventDefault();
    }

    swipeLeft() {
        const currentCard = this.getCurrentCard();
        if (!currentCard || this.currentCardIndex >= this.cards.length) return;
        
        currentCard.classList.add('swipe-left');
        
        setTimeout(() => {
            this.nextCard();
        }, 300);
    }

    swipeRight() {
        const currentCard = this.getCurrentCard();
        if (!currentCard || this.currentCardIndex >= this.cards.length) return;
        
        currentCard.classList.add('swipe-right');
        
        // Join the project
        this.joinProject(this.cards[this.currentCardIndex].id);
        
        setTimeout(() => {
            this.nextCard();
        }, 300);
    }

    async joinProject(projectId) {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`/api/projects/api/${projectId}/join/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message, 'success');
            } else {
                this.showNotification('Failed to join project', 'error');
            }
        } catch (error) {
            console.error('Error joining project:', error);
            this.showNotification('Failed to join project', 'error');
        }
    }

    showDetails() {
        const currentCard = this.cards[this.currentCardIndex];
        if (!currentCard) return;
        
        window.location.href = `/api/projects/${currentCard.id}/`;
    }

    nextCard() {
        this.currentCardIndex++;
        this.showCurrentCard();
        this.setupEventListeners();
    }

    getCurrentCard() {
        const cards = this.container.querySelectorAll('.swipe-card');
        return cards[this.currentCardIndex] || null;
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#00ff88' : type === 'error' ? '#ff4757' : '#007bff'};
            color: ${type === 'success' ? '#000' : '#fff'};
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('swipe-container')) {
        window.swipeManager = new SwipeCardManager('swipe-container');
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
