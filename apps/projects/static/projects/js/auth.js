// DevPal - Authentication Helper
class AuthManager {
    constructor() {
        this.tokenKey = 'access_token';
        this.refreshKey = 'refresh_token';
        this.init();
    }

    init() {
        this.checkAuthStatus();
        this.setupAuthButtons();
    }

    checkAuthStatus() {
        const token = localStorage.getItem(this.tokenKey);
        const isAuthenticated = !!token;
        
        // Update UI based on auth status
        this.updateAuthUI(isAuthenticated);
        
        return isAuthenticated;
    }

    updateAuthUI(isAuthenticated) {
        const authElements = document.querySelectorAll('[data-auth="required"]');
        const guestElements = document.querySelectorAll('[data-auth="guest"]');
        
        authElements.forEach(element => {
            element.style.display = isAuthenticated ? 'block' : 'none';
        });
        
        guestElements.forEach(element => {
            element.style.display = isAuthenticated ? 'none' : 'block';
        });
    }

    setupAuthButtons() {
        // Login button
        const loginBtn = document.querySelector('[data-action="login"]');
        if (loginBtn) {
            loginBtn.addEventListener('click', () => this.showLoginModal());
        }

        // Logout button
        const logoutBtn = document.querySelector('[data-action="logout"]');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }
    }

    async login(username, password) {
        try {
            const response = await fetch('/api/users/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem(this.tokenKey, data.access);
                localStorage.setItem(this.refreshKey, data.refresh);
                
                this.updateAuthUI(true);
                this.showNotification('Login successful!', 'success');
                return true;
            } else {
                const error = await response.json();
                this.showNotification(error.detail || 'Login failed', 'error');
                return false;
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showNotification('Login failed', 'error');
            return false;
        }
    }

    async logout() {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.refreshKey);
        this.updateAuthUI(false);
        this.showNotification('Logged out successfully', 'info');
        
        // Redirect to home page
        window.location.href = '/';
    }

    async refreshToken() {
        const refreshToken = localStorage.getItem(this.refreshKey);
        if (!refreshToken) return false;

        try {
            const response = await fetch('/api/users/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem(this.tokenKey, data.access);
                return true;
            } else {
                this.logout();
                return false;
            }
        } catch (error) {
            console.error('Token refresh error:', error);
            this.logout();
            return false;
        }
    }

    getAuthHeaders() {
        const token = localStorage.getItem(this.tokenKey);
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }

    showLoginModal() {
        const modal = document.createElement('div');
        modal.className = 'auth-modal';
        modal.innerHTML = `
            <div class="modal-overlay">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>Login to DevPal</h3>
                        <button class="modal-close" onclick="this.closest('.auth-modal').remove()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <form class="auth-form" onsubmit="handleLogin(event)">
                        <div class="form-group">
                            <label>Username</label>
                            <input type="text" name="username" required>
                        </div>
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" name="password" required>
                        </div>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-sign-in-alt"></i> Login
                        </button>
                    </form>
                    <div class="modal-footer">
                        <p>Don't have an account? <a href="/api/users/register/" onclick="window.location.href='/api/users/register/'; return false;">Register here</a></p>
                    </div>
                </div>
            </div>
        `;

        // Add modal styles
        const style = document.createElement('style');
        style.textContent = `
            .auth-modal {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 10000;
            }
            
            .modal-overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 2rem;
            }
            
            .modal-content {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 2rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
                max-width: 400px;
                width: 100%;
            }
            
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
            }
            
            .modal-header h3 {
                color: #ffffff;
                font-size: 1.5rem;
                font-weight: 600;
            }
            
            .modal-close {
                background: none;
                border: none;
                color: rgba(255, 255, 255, 0.7);
                cursor: pointer;
                font-size: 1.2rem;
                padding: 0.5rem;
                border-radius: 50%;
                transition: all 0.3s ease;
            }
            
            .modal-close:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #ffffff;
            }
            
            .auth-form {
                margin-bottom: 1.5rem;
            }
            
            .modal-footer {
                text-align: center;
                color: rgba(255, 255, 255, 0.7);
            }
            
            .modal-footer a {
                color: #00ff88;
                text-decoration: none;
            }
            
            .modal-footer a:hover {
                text-decoration: underline;
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(modal);
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
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Global functions for form handling
async function handleLogin(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const username = formData.get('username');
    const password = formData.get('password');
    
    const success = await window.authManager.login(username, password);
    if (success) {
        event.target.closest('.auth-modal').remove();
        // Reload the page to update the UI
        window.location.reload();
    }
}

// Initialize auth manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.authManager = new AuthManager();
});
