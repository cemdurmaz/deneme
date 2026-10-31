/**
 * 4 İşlem Hesap Makinesi Mantığı
 * Desteklenen işlemler: Toplama (+), Çıkarma (-), Çarpma (×), Bölme (÷)
 */

class FourOperationCalculator {
  constructor() {
    this.currentInput = "0";
    this.previousInput = null;
    this.operator = null;
    this.resetInputOnNextDigit = false;
    this.history = [];

    // DOM Elemanları
    this.resultDisplay = document.getElementById("result-display");
    this.expressionDisplay = document.getElementById("expression-display");
    this.opIndicator = document.getElementById("current-op-indicator");
    this.historyDrawer = document.getElementById("history-drawer");
    this.historyList = document.getElementById("history-list");
    this.historyToggleBtn = document.getElementById("history-toggle-btn");
    this.clearHistoryBtn = document.getElementById("clear-history-btn");

    this.initAudio();
    this.bindEvents();
    this.updateDisplay();
  }

  // Web Audio API ile zarif tıklama sesi sentezleyici
  initAudio() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
    } catch (e) {
      this.audioCtx = null;
    }
  }

  playClickSound(freq = 600, duration = 0.04) {
    if (!this.audioCtx) return;
    if (this.audioCtx.state === "suspended") {
      this.audioCtx.resume();
    }
    try {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
      gain.gain.setValueAtTime(0.04, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start();
      osc.stop(this.audioCtx.currentTime + duration);
    } catch (e) {
      // Ses engellense dahi arayüz kesintisiz çalışmaya devam eder
    }
  }

  bindEvents() {
    // Tuş Takımı Tıklamaları
    const keypad = document.getElementById("keypad");
    keypad.addEventListener("click", (e) => {
      const btn = e.target.closest("button");
      if (!btn) return;

      this.triggerButtonVisual(btn);

      if (btn.dataset.num !== undefined) {
        this.appendDigit(btn.dataset.num);
        this.playClickSound(520, 0.03);
      } else if (btn.dataset.op !== undefined) {
        this.setOperator(btn.dataset.op);
        this.playClickSound(750, 0.05);
      } else if (btn.dataset.action) {
        this.handleAction(btn.dataset.action);
        this.playClickSound(420, 0.06);
      }
    });

    // Klavye Dinleyicisi
    window.addEventListener("keydown", (e) => {
      const key = e.key;

      if (!isNaN(key) && key !== " ") {
        this.appendDigit(key);
        this.highlightButton(`[data-num="${key}"]`);
        this.playClickSound(520, 0.03);
      } else if (key === "+" || key === "-" || key === "*" || key === "/") {
        e.preventDefault();
        this.setOperator(key);
        this.highlightButton(`[data-op="${key}"]`);
        this.playClickSound(750, 0.05);
      } else if (key === "Enter" || key === "=") {
        e.preventDefault();
        this.calculate();
        this.highlightButton('[data-action="calculate"]');
        this.playClickSound(900, 0.07);
      } else if (key === "Backspace") {
        this.handleBackspace();
        this.highlightButton('[data-action="backspace"]');
        this.playClickSound(400, 0.03);
      } else if (key === "Escape" || key.toLowerCase() === "c") {
        this.clearAll();
        this.highlightButton('[data-action="clear"]');
        this.playClickSound(300, 0.05);
      } else if (key === "." || key === ",") {
        this.appendDecimal();
        this.highlightButton('[data-action="decimal"]');
        this.playClickSound(520, 0.03);
      }
    });

    // Geçmiş Çekmecesi Aç/Kapat
    this.historyToggleBtn.addEventListener("click", () => {
      this.historyDrawer.classList.toggle("open");
    });

    // Geçmişi Temizle
    this.clearHistoryBtn.addEventListener("click", () => {
      this.history = [];
      this.renderHistory();
    });
  }

  triggerButtonVisual(button) {
    button.classList.add("active-key");
    setTimeout(() => button.classList.remove("active-key"), 120);
  }

  highlightButton(selector) {
    const btn = document.querySelector(selector);
    if (btn) this.triggerButtonVisual(btn);
  }

  appendDigit(digit) {
    if (this.currentInput === "0" || this.resetInputOnNextDigit) {
      this.currentInput = digit;
      this.resetInputOnNextDigit = false;
    } else {
      if (this.currentInput.length >= 14) return; // Sayı taşmasını önle
      this.currentInput += digit;
    }
    this.updateDisplay();
  }

  appendDecimal() {
    if (this.resetInputOnNextDigit) {
      this.currentInput = "0.";
      this.resetInputOnNextDigit = false;
      this.updateDisplay();
      return;
    }
    if (!this.currentInput.includes(".")) {
      this.currentInput += ".";
      this.updateDisplay();
    }
  }

  handleBackspace() {
    if (this.resetInputOnNextDigit) {
      return;
    }
    if (this.currentInput.length > 1) {
      this.currentInput = this.currentInput.slice(0, -1);
    } else {
      this.currentInput = "0";
    }
    this.updateDisplay();
  }

  handleAction(action) {
    switch (action) {
      case "clear":
        this.clearAll();
        break;
      case "backspace":
        this.handleBackspace();
        break;
      case "decimal":
        this.appendDecimal();
        break;
      case "toggle-sign":
        if (this.currentInput !== "0") {
          this.currentInput = this.currentInput.startsWith("-")
            ? this.currentInput.slice(1)
            : "-" + this.currentInput;
          this.updateDisplay();
        }
        break;
      case "calculate":
        this.calculate();
        break;
    }
  }

  setOperator(op) {
    if (this.operator && !this.resetInputOnNextDigit) {
      this.calculate(false);
    }
    this.previousInput = this.currentInput;
    this.operator = op;
    this.resetInputOnNextDigit = true;
    this.updateDisplay();
  }

  // 4 Temel İşlem Mantığı
  calculate(isFinal = true) {
    if (this.operator === null || this.previousInput === null) return;

    const prev = parseFloat(this.previousInput);
    const curr = parseFloat(this.currentInput);
    let result = 0;

    switch (this.operator) {
      case "+":
        result = prev + curr;
        break;
      case "-":
        result = prev - curr;
        break;
      case "*":
        result = prev * curr;
        break;
      case "/":
        if (curr === 0) {
          this.currentInput = "0'a bölünemez";
          this.expressionDisplay.textContent = `${this.formatNumber(prev)} ÷ 0 =`;
          this.operator = null;
          this.previousInput = null;
          this.resetInputOnNextDigit = true;
          this.updateDisplay(true);
          return;
        }
        result = prev / curr;
        break;
    }

    const opSymbol = this.getOperatorSymbol(this.operator);
    const exprText = `${this.formatNumber(prev)} ${opSymbol} ${this.formatNumber(curr)} =`;

    // Geçmişe ekle
    if (isFinal) {
      this.addHistory(exprText, this.formatNumber(result));
    }

    this.expressionDisplay.textContent = exprText;
    this.currentInput = String(this.roundAccurately(result));
    this.operator = null;
    this.previousInput = null;
    this.resetInputOnNextDigit = true;
    this.updateDisplay();
  }

  // Sayısal yuvarlama ve IEEE 754 float hassasiyet düzeltmesi (örn. 0.1 + 0.2 = 0.3)
  roundAccurately(num) {
    return Math.round((num + Number.EPSILON) * 1e10) / 1e10;
  }

  formatNumber(num) {
    if (isNaN(num)) return num;
    if (Number.isInteger(num)) return num.toString();
    return num.toString();
  }

  getOperatorSymbol(op) {
    switch (op) {
      case "+": return "+";
      case "-": return "−";
      case "*": return "×";
      case "/": return "÷";
      default: return "";
    }
  }

  clearAll() {
    this.currentInput = "0";
    this.previousInput = null;
    this.operator = null;
    this.resetInputOnNextDigit = false;
    this.expressionDisplay.innerHTML = "&nbsp;";
    this.updateDisplay();
  }

  updateDisplay(isError = false) {
    this.resultDisplay.textContent = this.currentInput;
    if (isError) {
      this.resultDisplay.style.fontSize = "1.8rem";
      this.resultDisplay.style.color = "#f87171";
    } else {
      this.resultDisplay.style.fontSize = "";
      this.resultDisplay.style.color = "";
    }

    if (this.operator && this.previousInput !== null) {
      const opSym = this.getOperatorSymbol(this.operator);
      this.expressionDisplay.textContent = `${this.formatNumber(parseFloat(this.previousInput))} ${opSym}`;
      this.opIndicator.textContent = opSym;
    } else {
      this.opIndicator.textContent = "";
    }

    // Aktif operatör butonunu vurgula
    document.querySelectorAll(".key-operator").forEach(btn => {
      btn.classList.toggle("active-op", btn.dataset.op === this.operator && this.resetInputOnNextDigit);
    });
  }

  addHistory(expression, result) {
    this.history.unshift({ expression, result });
    if (this.history.length > 20) this.history.pop();
    this.renderHistory();
  }

  renderHistory() {
    if (this.history.length === 0) {
      this.historyList.innerHTML = '<p class="history-empty">Henüz kaydedilmiş işlem yok.</p>';
      return;
    }

    this.historyList.innerHTML = this.history
      .map(item => `
        <div class="history-item" onclick="calc.loadHistory('${item.result}')">
          <span class="history-item-expr">${item.expression}</span>
          <span class="history-item-res">${item.result}</span>
        </div>
      `)
      .join("");
  }

  loadHistory(val) {
    this.currentInput = val;
    this.resetInputOnNextDigit = true;
    this.updateDisplay();
  }
}

// Uygulamayı Başlat
const calc = new FourOperationCalculator();
