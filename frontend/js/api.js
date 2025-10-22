// API Client
const API_BASE = '/api/auth';

class APIClient {
    async request(method, endpoint, data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include' // Important for session cookies
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, options);
            const responseData = await response.json();
            
            if (!response.ok) {
                throw new Error(responseData.message || 'Request failed');
            }
            
            return responseData;
        } catch (error) {
            throw error;
        }
    }
    
    // Auth endpoints
    async register(name, email, password, confirmPassword) {
        return this.request('POST', '/register', {
            name,
            email,
            password,
            confirmPassword
        });
    }
    
    async login(email, password) {
        return this.request('POST', '/login', {
            email,
            password
        });
    }
    
    async verifyEmail(email, code) {
        return this.request('POST', '/verify-code', {
            email,
            code
        });
    }
    
    async resendVerificationCode(email) {
        return this.request('POST', '/resend-verification-code', {
            email
        });
    }
    
    async verifySecurity(sessionId, code) {
        return this.request('POST', '/verify-security', {
            sessionId,
            code
        });
    }
    
    async resendSecurityCode(sessionId) {
        return this.request('POST', '/resend-security-code', {
            sessionId
        });
    }
    
    async getCurrentUser() {
        return this.request('GET', '/me');
    }
    
    async getAccessLogs() {
        return this.request('GET', '/access-logs');
    }
    
    async logout() {
        return this.request('POST', '/logout');
    }
}

const api = new APIClient();

// Toast notification system
class Toast {
    static show(title, description, variant = 'default') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${variant === 'destructive' ? 'toast-destructive' : ''}`;
        
        toast.innerHTML = `
            <div class="toast-title">${title}</div>
            ${description ? `<div class="toast-description">${description}</div>` : ''}
        `;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }
}
