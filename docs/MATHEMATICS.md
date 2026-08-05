# NeuroLearn Research Suite - Mathematical Equations & Derivations

This document presents the complete mathematical formulations employed across signal processing, spectral estimation, feature extraction, attention indices, and statistical evaluation in the **NeuroLearn Research Suite**.

---

## 1. Biomedical Signal Preprocessing

### 1.1 Zero-Phase Butterworth Bandpass Filter
A 4th-order Butterworth bandpass filter is defined by the magnitude response:
$$|H(j\omega)|^2 = \frac{1}{1 + \left(\frac{\omega^2 - \omega_0^2}{\omega \cdot B}\right)^{2N}}$$
where $N=4$, $B = \omega_H - \omega_L$ is the passband width (1–40 Hz), and $\omega_0 = \sqrt{\omega_L \omega_H}$ is the center frequency. Zero-phase filtering is achieved via forward-backward filtering ($y(t) = f(f(x(t)))$).

### 1.2 IIR Powerline Notch Filter (50 Hz / 60 Hz)
$$H(z) = b_0 \frac{1 - 2\cos(\omega_0)z^{-1} + z^{-2}}{1 - 2r\cos(\omega_0)z^{-1} + r^2 z^{-2}}$$
where $\omega_0 = \frac{2\pi f_{\text{notch}}}{f_s}$ and $r = 1 - \frac{\pi B}{f_s}$ with quality factor $Q = \frac{f_{\text{notch}}}{B} = 30$.

---

## 2. Time Domain & Hjorth Parameters

### 2.1 Hjorth Activity
$$A = \text{var}(x(t)) = \sigma_x^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2$$

### 2.2 Hjorth Mobility
$$M = \sqrt{\frac{\text{var}\left(\frac{dx(t)}{dt}\right)}{\text{var}(x(t))}} = \frac{\sigma_{x'}}{\sigma_x}$$

### 2.3 Hjorth Complexity
$$C = \frac{\text{Mobility}\left(\frac{dx(t)}{dt}\right)}{\text{Mobility}(x(t))} = \frac{\sigma_{x''}/\sigma_{x'}}{\sigma_{x'}/\sigma_x}$$

---

## 3. Frequency Domain & Spectral Analysis

### 3.1 Welch Power Spectral Density (PSD)
Signal $x(t)$ is partitioned into $K$ overlapping segments $x_k(m)$ of length $L$ with Hanning window $w(m)$:
$$P_{x,k}(f) = \frac{1}{L U} \left| \sum_{m=0}^{L-1} x_k(m) w(m) e^{-j 2\pi f m / f_s} \right|^2$$
$$\text{PSD}(f) = \frac{1}{K} \sum_{k=1}^K P_{x,k}(f)$$
where $U = \frac{1}{L} \sum_{m=0}^{L-1} w^2(m)$ is the window normalization factor.

### 3.2 Spectral Edge Frequency (SEF95)
The frequency $f_{95}$ below which 95% of total spectral power resides:
$$\int_{0}^{f_{95}} \text{PSD}(f) \, df = 0.95 \times \int_{0}^{f_s/2} \text{PSD}(f) \, df$$

### 3.3 Spectral Entropy
$$H_s = -\frac{1}{\log_2(M)} \sum_{i=1}^M p(f_i) \log_2 p(f_i), \quad p(f_i) = \frac{\text{PSD}(f_i)}{\sum_{j=1}^M \text{PSD}(f_j)}$$

---

## 4. Time-Frequency & Wavelet Metrics

### 4.1 Wavelet Entropy
Using Discrete Wavelet Transform (DWT) coefficients $C_j(k)$ at decomposition level $j$:
$$E_j = \sum_k |C_j(k)|^2, \quad E_{\text{total}} = \sum_j E_j, \quad p_j = \frac{E_j}{E_{\text{total}}}$$
$$H_{\text{wavelet}} = -\sum_{j} p_j \log_2(p_j)$$

---

## 5. Mathematical Attention Indices

### 5.1 Classic Engagement Ratio
$$\text{Attention}_{\text{raw}, 1} = \frac{P_{\beta}}{P_{\theta}} = \frac{\int_{13}^{30} \text{PSD}(f) df}{\int_{4}^{8} \text{PSD}(f) df}$$

### 5.2 Extended Cognitive Index
$$\text{Attention}_{\text{raw}, 2} = \frac{P_{\beta} + P_{\gamma}}{P_{\theta} + P_{\alpha}} = \frac{\int_{13}^{30} \text{PSD}(f) df + \int_{30}^{40} \text{PSD}(f) df}{\int_{4}^{8} \text{PSD}(f) df + \int_{8}^{13} \text{PSD}(f) df}$$

### 5.3 Sigmoidal 0–100 Normalization
$$\text{Score}_{\text{attention}} = \frac{100}{1 + \exp\left(-\frac{I - \text{median}(I)}{\text{std}(I) + \epsilon}\right)}$$

---

## 6. Statistical Analysis & Bland-Altman Agreement

### 6.1 Cohen's $d$ Effect Size
$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}}, \quad s_{\text{pooled}} = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}$$

### 6.2 Bland-Altman Limits of Agreement
$$\bar{d} = \frac{1}{n} \sum_{i=1}^n (x_{1,i} - x_{2,i}), \quad s_d = \sqrt{\frac{1}{n-1} \sum_{i=1}^n (d_i - \bar{d})^2}$$
$$\text{Limits of Agreement (95\%)} = \bar{d} \pm 1.96 \, s_d$$
