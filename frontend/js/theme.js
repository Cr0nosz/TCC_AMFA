// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        this.applyTheme();
    }
    
    applyTheme() {
        document.body.classList.remove('light', 'dark');
        document.body.classList.add(this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
    }
    
    toggle() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme();
        return this.currentTheme;
    }
    
    getTheme() {
        return this.currentTheme;
    }
}

const themeManager = new ThemeManager();
