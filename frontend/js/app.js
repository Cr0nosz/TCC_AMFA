// Main Application
class App {
    constructor() {
        this.app = document.getElementById('app');
        this.currentRoute = window.location.pathname;
        this.init();
    }
    
    init() {
        // Initialize binary rain
        initBinaryRain();
        
        // Setup routing
        window.addEventListener('popstate', () => this.router());
        
        // Initial route
        this.router();
    }
    
    navigate(path) {
        window.history.pushState({}, '', path);
        this.router();
    }
    
    router() {
        const path = window.location.pathname;
        const urlParams = new URLSearchParams(window.location.search);
        
        if (path === '/' || path === '/login') {
            this.renderLogin();
        } else if (path === '/register') {
            this.renderRegister();
        } else if (path === '/verify-email') {
            const email = urlParams.get('email');
            this.renderEmailVerification(email);
        } else if (path === '/verify-security') {
            this.renderSecurityVerification();
        } else if (path === '/dashboard') {
            this.renderDashboard();
        } else {
            this.render404();
        }
    }
    
    renderLogin() {
        this.app.innerHTML = `
            <div class="min-h-screen relative flex items-center justify-center p-4">
                <div class="bg-gradient-overlay"></div>
                
                <div class="relative z-10 container">
                    <!-- Header -->
                    <div class="text-center mb-8">
                        <div class="flex justify-center mb-4">
                            <div class="shield-container">
                                <svg class="shield-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </div>
                        </div>
                        <h1 class="text-3xl font-bold mb-2" style="color: var(--primary)">AMFA</h1>
                        <p class="text-sm" style="color: var(--muted-foreground)">
                            <span id="hacker-text"></span><span class="typing-cursor">|</span>
                        </p>
                    </div>
                    
                    <!-- Login Card -->
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title">
                                <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                ACESSO RESTRITO
                            </h2>
                            <div class="flex gap-2 mt-2">
                                <span class="badge badge-outline" style="color: var(--primary); border-color: rgba(23, 184, 144, 0.3)">
                                    <svg class="icon-sm" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                    </svg>
                                    ONLINE
                                </span>
                                <span class="badge badge-outline" style="color: var(--chart-2); border-color: rgba(92, 173, 219, 0.3)">
                                    <svg class="icon-sm" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                                    </svg>
                                    ENCRYPTED
                                </span>
                            </div>
                        </div>
                        
                        <div class="card-content">
                            <form id="login-form" class="flex flex-col gap-4">
                                <!-- Email -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                        </svg>
                                        EMAIL
                                    </label>
                                    <input type="email" id="email" class="input" placeholder="user@domain.com" required data-testid="input-email">
                                    <div id="email-error"></div>
                                </div>
                                
                                <!-- Password -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                        </svg>
                                        SENHA
                                    </label>
                                    <div class="password-wrapper">
                                        <input type="password" id="password" class="input" placeholder="••••••••" required data-testid="input-password">
                                        <button type="button" class="password-toggle" onclick="togglePassword('password')">
                                            <svg id="eye-icon" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                            </svg>
                                        </button>
                                    </div>
                                    <div id="password-error"></div>
                                </div>
                                
                                <!-- Captcha -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                                        </svg>
                                        VERIFICAÇÃO ANTI-BOT
                                    </label>
                                    <div class="captcha-container">
                                        <div class="captcha-display" id="captcha-question"></div>
                                        <button type="button" class="button button-outline button-icon" onclick="refreshCaptcha()" data-testid="button-refresh-captcha">↻</button>
                                    </div>
                                    <input type="number" id="captcha" class="input mt-2" placeholder="Digite o resultado" required data-testid="input-captcha">
                                    <div id="captcha-error"></div>
                                </div>
                                
                                <!-- Remember me -->
                                <div class="checkbox-wrapper">
                                    <input type="checkbox" id="rememberMe" class="checkbox" data-testid="checkbox-remember-me">
                                    <label for="rememberMe" class="text-sm" style="color: var(--muted-foreground)">Manter-me conectado</label>
                                </div>
                                
                                <!-- Submit -->
                                <button type="submit" class="button button-primary w-full" id="login-button" data-testid="button-login">
                                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                    </svg>
                                    ACESSAR SISTEMA
                                </button>
                            </form>
                            
                            <!-- Register Link -->
                            <div class="text-center mt-4">
                                <p class="text-sm" style="color: var(--muted-foreground)">
                                    Novo usuário?
                                    <a href="/register" onclick="app.navigate('/register'); return false;" style="color: var(--primary); cursor: pointer" data-testid="link-register">Cadastrar novo usuário</a>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.initLoginForm();
        this.startHackerText();
        this.generateCaptcha();
    }
    
    initLoginForm() {
        const form = document.getElementById('login-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const captcha = document.getElementById('captcha').value;
            
            // Validate captcha
            if (parseInt(captcha) !== window.captchaAnswer) {
                Toast.show('Erro', 'Captcha incorreto', 'destructive');
                this.generateCaptcha();
                return;
            }
            
            const button = document.getElementById('login-button');
            button.disabled = true;
            button.innerHTML = `
                <span class="spinner"></span>
                AUTENTICANDO...
            `;
            
            try {
                const result = await api.login(email, password);
                
                if (result.requiresSecurity) {
                    // Store for security verification
                    localStorage.setItem('securitySessionId', result.sessionId);
                    localStorage.setItem('userEmail', result.userEmail);
                    Toast.show('Verificação de Segurança Necessária', result.message);
                    setTimeout(() => this.navigate('/verify-security'), 2000);
                } else {
                    Toast.show('Acesso Autorizado', 'Login realizado com sucesso!');
                    setTimeout(() => this.navigate('/dashboard'), 2000);
                }
            } catch (error) {
                Toast.show('Acesso Negado', error.message, 'destructive');
                this.generateCaptcha();
            } finally {
                button.disabled = false;
                button.innerHTML = `
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                    ACESSAR SISTEMA
                `;
            }
        });
    }
    
    generateCaptcha() {
        const num1 = Math.floor(Math.random() * 10) + 1;
        const num2 = Math.floor(Math.random() * 10) + 1;
        window.captchaAnswer = num1 + num2;
        const questionEl = document.getElementById('captcha-question');
        if (questionEl) {
            questionEl.textContent = `${num1} + ${num2} = ?`;
        }
        const captchaInput = document.getElementById('captcha');
        if (captchaInput) {
            captchaInput.value = '';
        }
    }
    
    startHackerText() {
        const messages = [
            'CONEXÃO SEGURA ESTABELECIDA...',
            'STATUS DO FIREWALL: ATIVO',
            'PROTOCOLO DE CRIPTOGRAFIA: AES-256',
            'CONTROLE DE ACESSO: HABILITADO',
            'DETECÇÃO DE AMEAÇAS: ONLINE'
        ];
        
        let messageIndex = 0;
        let charIndex = 0;
        let currentMessage = '';
        
        const typeWriter = () => {
            const textEl = document.getElementById('hacker-text');
            if (!textEl) return;
            
            if (messageIndex < messages.length) {
                if (charIndex < messages[messageIndex].length) {
                    currentMessage += messages[messageIndex].charAt(charIndex);
                    textEl.textContent = currentMessage;
                    charIndex++;
                    setTimeout(typeWriter, 50);
                } else {
                    setTimeout(() => {
                        messageIndex++;
                        charIndex = 0;
                        currentMessage = '';
                        if (messageIndex >= messages.length) {
                            messageIndex = 0;
                        }
                        typeWriter();
                    }, 2000);
                }
            }
        };
        
        typeWriter();
    }
    
    renderRegister() {
        this.app.innerHTML = `
            <div class="min-h-screen relative flex items-center justify-center p-4">
                <div class="bg-gradient-overlay"></div>
                
                <div class="relative z-10 container">
                    <!-- Header -->
                    <div class="text-center mb-8">
                        <div class="flex justify-center mb-4">
                            <div class="shield-container">
                                <svg class="shield-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                                </svg>
                            </div>
                        </div>
                        <h1 class="text-3xl font-bold mb-2" style="color: var(--primary)">AMFA</h1>
                        <p class="text-sm" style="color: var(--muted-foreground)">
                            NOVO REGISTRO DE USUÁRIO
                        </p>
                    </div>
                    
                    <!-- Register Card -->
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title">
                                <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                                </svg>
                                CRIAR CONTA
                            </h2>
                        </div>
                        
                        <div class="card-content">
                            <form id="register-form" class="flex flex-col gap-4">
                                <!-- Name -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                        </svg>
                                        NOME COMPLETO
                                    </label>
                                    <input type="text" id="name" class="input" placeholder="Digite seu nome completo" required data-testid="input-name">
                                </div>
                                
                                <!-- Email -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                        </svg>
                                        EMAIL
                                    </label>
                                    <input type="email" id="reg-email" class="input" placeholder="user@domain.com" required data-testid="input-email">
                                </div>
                                
                                <!-- Password -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                        </svg>
                                        SENHA
                                    </label>
                                    <div class="password-wrapper">
                                        <input type="password" id="reg-password" class="input" placeholder="••••••••" required data-testid="input-password">
                                        <button type="button" class="password-toggle" onclick="togglePassword('reg-password')">
                                            <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                                
                                <!-- Confirm Password -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                        </svg>
                                        CONFIRMAR SENHA
                                    </label>
                                    <div class="password-wrapper">
                                        <input type="password" id="reg-confirm-password" class="input" placeholder="••••••••" required data-testid="input-confirm-password">
                                        <button type="button" class="password-toggle" onclick="togglePassword('reg-confirm-password')">
                                            <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                                
                                <!-- Submit -->
                                <button type="submit" class="button button-primary w-full" id="register-button" data-testid="button-register">
                                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                                    </svg>
                                    CRIAR CONTA
                                </button>
                            </form>
                            
                            <!-- Login Link -->
                            <div class="text-center mt-4">
                                <p class="text-sm" style="color: var(--muted-foreground)">
                                    Já tem uma conta?
                                    <a href="/login" onclick="app.navigate('/login'); return false;" style="color: var(--primary); cursor: pointer" data-testid="link-login">Fazer login</a>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.initRegisterForm();
    }
    
    initRegisterForm() {
        const form = document.getElementById('register-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const email = document.getElementById('reg-email').value;
            const password = document.getElementById('reg-password').value;
            const confirmPassword = document.getElementById('reg-confirm-password').value;
            
            // Validate passwords match
            if (password !== confirmPassword) {
                Toast.show('Erro', 'As senhas não coincidem', 'destructive');
                return;
            }
            
            const button = document.getElementById('register-button');
            button.disabled = true;
            button.innerHTML = `
                <span class="spinner"></span>
                CRIANDO CONTA...
            `;
            
            try {
                await api.register(name, email, password, confirmPassword);
                Toast.show('Sucesso', 'Conta criada! Verifique seu email.');
                setTimeout(() => this.navigate(`/verify-email?email=${encodeURIComponent(email)}`), 2000);
            } catch (error) {
                Toast.show('Erro', error.message, 'destructive');
            } finally {
                button.disabled = false;
                button.innerHTML = `
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    CRIAR CONTA
                `;
            }
        });
    }
    
    renderEmailVerification(email) {
        if (!email) {
            Toast.show('Erro', 'Email não fornecido', 'destructive');
            this.navigate('/');
            return;
        }
        
        this.app.innerHTML = `
            <div class="min-h-screen relative flex items-center justify-center p-4">
                <div class="bg-gradient-overlay"></div>
                
                <div class="relative z-10 container">
                    <!-- Header -->
                    <div class="text-center mb-8">
                        <div class="flex justify-center mb-4">
                            <div class="shield-container">
                                <svg class="shield-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                            </div>
                        </div>
                        <h1 class="text-3xl font-bold mb-2" style="color: var(--primary)">VERIFICAÇÃO DE EMAIL</h1>
                        <p class="text-sm" style="color: var(--muted-foreground)">
                            Código enviado para: ${email}
                        </p>
                    </div>
                    
                    <!-- Verification Card -->
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title">
                                <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                </svg>
                                VERIFICAR EMAIL
                            </h2>
                        </div>
                        
                        <div class="card-content">
                            <form id="email-verify-form" class="flex flex-col gap-4">
                                <!-- Code -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                                        </svg>
                                        CÓDIGO DE VERIFICAÇÃO
                                    </label>
                                    <input type="text" id="verification-code" class="input" placeholder="Digite o código de 6 dígitos" required maxlength="6" data-testid="input-verification-code">
                                </div>
                                
                                <!-- Submit -->
                                <button type="submit" class="button button-primary w-full" id="verify-button" data-testid="button-verify">
                                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    VERIFICAR CÓDIGO
                                </button>
                                
                                <!-- Resend -->
                                <button type="button" class="button button-outline w-full" id="resend-button" data-testid="button-resend">
                                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                    </svg>
                                    REENVIAR CÓDIGO
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.initEmailVerifyForm(email);
    }
    
    initEmailVerifyForm(email) {
        const form = document.getElementById('email-verify-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const code = document.getElementById('verification-code').value;
            const button = document.getElementById('verify-button');
            
            button.disabled = true;
            button.innerHTML = `
                <span class="spinner"></span>
                VERIFICANDO...
            `;
            
            try {
                await api.verifyEmail(email, code);
                Toast.show('Sucesso', 'Email verificado! Redirecionando...');
                setTimeout(() => this.navigate('/login'), 2000);
            } catch (error) {
                Toast.show('Erro', error.message, 'destructive');
            } finally {
                button.disabled = false;
                button.innerHTML = `
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    VERIFICAR CÓDIGO
                `;
            }
        });
        
        // Resend button
        document.getElementById('resend-button').addEventListener('click', async () => {
            const button = document.getElementById('resend-button');
            button.disabled = true;
            button.innerHTML = `
                <span class="spinner"></span>
                REENVIANDO...
            `;
            
            try {
                await api.resendVerificationCode(email);
                Toast.show('Sucesso', 'Código reenviado para seu email');
            } catch (error) {
                Toast.show('Erro', error.message, 'destructive');
            } finally {
                button.disabled = false;
                button.innerHTML = `
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    REENVIAR CÓDIGO
                `;
            }
        });
    }
    
    renderSecurityVerification() {
        const sessionId = localStorage.getItem('securitySessionId');
        const userEmail = localStorage.getItem('userEmail');
        
        if (!sessionId || !userEmail) {
            Toast.show('Erro', 'Sessão de segurança não encontrada', 'destructive');
            this.navigate('/');
            return;
        }
        
        this.app.innerHTML = `
            <div class="min-h-screen relative flex items-center justify-center p-4">
                <div class="bg-gradient-overlay"></div>
                
                <div class="relative z-10 container">
                    <!-- Header -->
                    <div class="text-center mb-8">
                        <div class="flex justify-center mb-4">
                            <div class="shield-container">
                                <svg class="shield-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </div>
                        </div>
                        <h1 class="text-3xl font-bold mb-2" style="color: var(--primary)">VERIFICAÇÃO DE SEGURANÇA</h1>
                        <p class="text-sm" style="color: var(--muted-foreground)">
                            Atividade suspeita detectada - Verificação adicional necessária
                        </p>
                    </div>
                    
                    <!-- Security Verification Card -->
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title">
                                <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                </svg>
                                AUTENTICAÇÃO DE 2 FATORES
                            </h2>
                            <p class="text-sm mt-2" style="color: var(--muted-foreground)">
                                Um código de segurança foi enviado para: ${userEmail}
                            </p>
                        </div>
                        
                        <div class="card-content">
                            <form id="security-verify-form" class="flex flex-col gap-4">
                                <!-- Code -->
                                <div>
                                    <label class="label">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                                        </svg>
                                        CÓDIGO DE SEGURANÇA
                                    </label>
                                    <input type="text" id="security-code" class="input" placeholder="Digite o código de 6 dígitos" required maxlength="6" data-testid="input-security-code">
                                </div>
                                
                                <!-- Submit -->
                                <button type="submit" class="button button-primary w-full" id="security-verify-button" data-testid="button-security-verify">
                                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    VERIFICAR CÓDIGO
                                </button>
                                
                                <!-- Resend -->
                                <button type="button" class="button button-outline w-full" id="security-resend-button" data-testid="button-security-resend">
                                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                    </svg>
                                    REENVIAR CÓDIGO
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.initSecurityVerifyForm(sessionId);
    }
    
    initSecurityVerifyForm(sessionId) {
        const form = document.getElementById('security-verify-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const code = document.getElementById('security-code').value;
            const button = document.getElementById('security-verify-button');
            
            button.disabled = true;
            button.innerHTML = `
                <span class="spinner"></span>
                VERIFICANDO...
            `;
            
            try {
                await api.verifySecurity(sessionId, code);
                Toast.show('Sucesso', 'Verificação concluída! Bem-vindo.');
                localStorage.removeItem('securitySessionId');
                localStorage.removeItem('userEmail');
                setTimeout(() => this.navigate('/dashboard'), 2000);
            } catch (error) {
                Toast.show('Erro', error.message, 'destructive');
            } finally {
                button.disabled = false;
                button.innerHTML = `
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    VERIFICAR CÓDIGO
                `;
            }
        });
        
        // Resend button
        document.getElementById('security-resend-button').addEventListener('click', async () => {
            const button = document.getElementById('security-resend-button');
            button.disabled = true;
            button.innerHTML = `
                <span class="spinner"></span>
                REENVIANDO...
            `;
            
            try {
                await api.resendSecurityCode(sessionId);
                Toast.show('Sucesso', 'Código de segurança reenviado');
            } catch (error) {
                Toast.show('Erro', error.message, 'destructive');
            } finally {
                button.disabled = false;
                button.innerHTML = `
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    REENVIAR CÓDIGO
                `;
            }
        });
    }
    
    async renderDashboard() {
        this.app.innerHTML = `
            <div class="min-h-screen relative">
                <div class="bg-gradient-overlay"></div>
                
                <div class="relative z-10">
                    <!-- Header -->
                    <header class="border-b" style="border-color: var(--border); background-color: var(--card)">
                        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
                            <h1 class="text-2xl font-bold" style="color: var(--primary)">AMFA Dashboard</h1>
                            <div class="flex gap-2">
                                <button id="theme-toggle" class="button button-outline button-icon" data-testid="button-theme-toggle">
                                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                                    </svg>
                                </button>
                                <button id="logout-button" class="button button-destructive" data-testid="button-logout">
                                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                    </svg>
                                    Sair
                                </button>
                            </div>
                        </div>
                    </header>
                    
                    <!-- Content -->
                    <div class="container mx-auto px-4 py-8">
                        <!-- Loading state -->
                        <div id="dashboard-loading" class="text-center py-8">
                            <span class="spinner inline-block"></span>
                            <p class="mt-4" style="color: var(--muted-foreground)">Carregando dados...</p>
                        </div>
                        
                        <!-- Dashboard content (hidden initially) -->
                        <div id="dashboard-content" style="display: none;">
                            <!-- User Info -->
                            <div class="card mb-6">
                                <div class="card-header">
                                    <h2 class="card-title">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                        </svg>
                                        Informações do Usuário
                                    </h2>
                                </div>
                                <div class="card-content">
                                    <div class="flex flex-col gap-2">
                                        <p><strong>Nome:</strong> <span id="user-name" data-testid="text-user-name">-</span></p>
                                        <p><strong>Email:</strong> <span id="user-email" data-testid="text-user-email">-</span></p>
                                        <p><strong>Email Verificado:</strong> <span id="user-verified" data-testid="text-user-verified">-</span></p>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Access Logs -->
                            <div class="card">
                                <div class="card-header">
                                    <h2 class="card-title">
                                        <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        Histórico de Acessos
                                    </h2>
                                </div>
                                <div class="card-content">
                                    <div id="access-logs-list" class="flex flex-col gap-3">
                                        <!-- Logs will be populated here -->
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.initDashboard();
    }
    
    async initDashboard() {
        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => {
            themeManager.toggle();
        });
        
        // Logout button
        document.getElementById('logout-button').addEventListener('click', async () => {
            try {
                await api.logout();
                Toast.show('Sucesso', 'Logout realizado com sucesso');
                this.navigate('/');
            } catch (error) {
                Toast.show('Erro', error.message, 'destructive');
            }
        });
        
        // Load user data and access logs
        try {
            const [userData, logsData] = await Promise.all([
                api.getCurrentUser(),
                api.getAccessLogs()
            ]);
            
            // Populate user info
            document.getElementById('user-name').textContent = userData.name;
            document.getElementById('user-email').textContent = userData.email;
            document.getElementById('user-verified').textContent = userData.emailVerified ? 'Sim' : 'Não';
            
            // Populate access logs
            const logsList = document.getElementById('access-logs-list');
            if (logsData.logs && logsData.logs.length > 0) {
                logsList.innerHTML = logsData.logs.map((log, index) => `
                    <div class="border-l-4 pl-4" style="border-color: ${log.success ? 'var(--primary)' : 'var(--destructive)'}" data-testid="log-entry-${index}">
                        <div class="flex justify-between items-start">
                            <div>
                                <p class="font-semibold">${log.action.toUpperCase()}</p>
                                <p class="text-sm" style="color: var(--muted-foreground)">
                                    ${log.ipAddress} • ${log.location || 'Localização desconhecida'}
                                </p>
                                <p class="text-sm" style="color: var(--muted-foreground)">
                                    ${log.deviceInfo || 'Dispositivo desconhecido'}
                                </p>
                            </div>
                            <span class="badge ${log.success ? 'badge-outline' : 'badge-destructive'}" style="${log.success ? 'color: var(--primary); border-color: rgba(23, 184, 144, 0.3)' : ''}">
                                ${log.success ? 'SUCESSO' : 'FALHA'}
                            </span>
                        </div>
                        <p class="text-xs mt-1" style="color: var(--muted-foreground)">
                            ${new Date(log.timestamp).toLocaleString('pt-BR')}
                        </p>
                    </div>
                `).join('');
            } else {
                logsList.innerHTML = '<p style="color: var(--muted-foreground)">Nenhum acesso registrado</p>';
            }
            
            // Show content, hide loading
            document.getElementById('dashboard-loading').style.display = 'none';
            document.getElementById('dashboard-content').style.display = 'block';
            
        } catch (error) {
            Toast.show('Erro', 'Falha ao carregar dados do dashboard', 'destructive');
            document.getElementById('dashboard-loading').innerHTML = `
                <p style="color: var(--destructive)">Erro ao carregar dados</p>
                <button class="button button-primary mt-4" onclick="app.navigate('/login')">Voltar ao Login</button>
            `;
        }
    }
    
    render404() {
        this.app.innerHTML = `
            <div class="min-h-screen flex items-center justify-center p-4">
                <div class="text-center">
                    <h1 class="text-4xl font-bold mb-4" style="color: var(--primary)">404</h1>
                    <p class="text-lg mb-4">Página não encontrada</p>
                    <button class="button button-primary" onclick="app.navigate('/')">Voltar ao Login</button>
                </div>
            </div>
        `;
    }
}

// Helper functions
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    input.type = input.type === 'password' ? 'text' : 'password';
}

function refreshCaptcha() {
    app.generateCaptcha();
}

// Initialize app
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new App();
});
