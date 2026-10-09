// Copyright (c) 2019 ml5
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

/* ===
ml5 Example
Sound Classification using a pre-trained customized model and p5.js
Chủ đề: Phân biệt tiếng hót các loài chim (Bài tập thầy Dũng)
Màu sắc: Bầu trời rừng sâu, Xanh ngọc bích & Sóng âm thanh
=== */

// Biến phân loại âm thanh toàn cục
let classifier;

// Nhãn ban đầu
let label = "Đang lắng nghe tiếng chim...";
let confidence = 0;

// URL Model Teachable Machine của bạn:
let soundModelURL = 'https://teachablemachine.withgoogle.com/models/R7Skz_Jk8/model.json';

// Bảng cấu hình 6 loài chim của thầy Dũng
const BIRD_MAP = {
  'chim vành khuyên': { name: "Chim Vành Khuyên", icon: "🟡", color: "#ffd166" },
  'chim chào mào':    { name: "Chim Chào Mào",    icon: "🔴", color: "#f77f00" },
  'chim chích chòe':  { name: "Chim Chích Chòe",  icon: "⚪", color: "#e2e8f0" },
  'chim họa mi':      { name: "Chim Họa Mi",      icon: "🟤", color: "#e9c46a" },
  'chim thanh tước':  { name: "Chim Thanh Tước",  icon: "🟢", color: "#74c69d" },
  'chim se sẻ':       { name: "Chim Se Sẻ",       icon: "🟠", color: "#ddb892" },
  'background noise': { name: "Tiếng ồn môi trường", icon: "🎧", color: "#90e0ef" }
};

// Biến điều khiển sóng âm thanh
let wavePhase = 0;
let numBars = 26;
let isSimulating = false;

function preload() {
  classifier = ml5.soundClassifier(soundModelURL);
}

function setup() {
  // Lọc cảnh báo sampling rate để màn hình Console sạch tinh tươm
  let originalWarn = console.warn;
  console.warn = function(...args) {
    if (args[0] && typeof args[0] === 'string' && args[0].includes('sampling rate')) return;
    originalWarn.apply(console, args);
  };

  // Tạo canvas kích thước 320x240 chuẩn xác
  let canvas = createCanvas(320, 240);

  // Gắn canvas gọn gàng vào khung #canvas-holder trong index.html
  let container = document.getElementById('canvas-holder');
  if (container) {
    container.appendChild(canvas.elt);
  }

  // Bắt đầu lắng nghe qua microphone liên tục
  if (classifier) {
    classifier.classify(gotResult);
  }
}

function draw() {
  // 1. Nền canvas tông màu đêm rừng thẳm (#06141b)
  background(6, 20, 27);

  // 2. Vẽ vòng tròn sóng âm lan tỏa
  drawSoundRipples();

  // 3. Vẽ 26 cột sóng âm thanh Equalizer dao động theo tiếng hót
  drawAudioSpectrum();

  // 4. Biểu tượng chim hót trung tâm
  drawBirdCenterpiece();

  // 5. Bảng hiển thị kết quả loài chim nhận diện được
  drawResultDashboard();

  wavePhase += 0.06;
}

// 1. Sóng âm thanh lan tỏa tròn đều
function drawSoundRipples() {
  noFill();
  let centerX = width / 2;
  let centerY = 82;

  let isNoise = label.toLowerCase().includes("noise") || label.toLowerCase().includes("lắng nghe");
  let rippleColor = isNoise ? color(72, 202, 228) : getBirdInfo().color;

  for (let r = 0; r < 3; r++) {
    let currentRadius = (60 + r * 35 + sin(wavePhase + r) * 10);
    let alpha = map(r, 0, 2, 70, 15);
    stroke(red(rippleColor), green(rippleColor), blue(rippleColor), alpha);
    strokeWeight(1.5);
    ellipse(centerX, centerY, currentRadius, currentRadius);
  }
}

// 2. Cột sóng phổ âm thanh Equalizer
function drawAudioSpectrum() {
  let barWidth = 7;
  let gap = 4;
  let totalW = numBars * (barWidth + gap);
  let startX = (width - totalW) / 2;
  let baseY = 165;

  let isNoise = label.toLowerCase().includes("noise") || label.toLowerCase().includes("lắng nghe");

  for (let i = 0; i < numBars; i++) {
    let intensity = isNoise ? 12 : 28;
    let barH = 8 + sin(wavePhase * 2.5 + i * 0.4) * intensity + noise(i, wavePhase) * 10;
    barH = max(5, barH);

    let inter = map(i, 0, numBars, 0, 1);
    let c1 = color(0, 180, 216);
    let c2 = color(getBirdInfo().color);
    let barColor = lerpColor(c1, c2, inter);

    fill(barColor);
    noStroke();
    rect(startX + i * (barWidth + gap), baseY - barH, barWidth, barH, 3);
  }
}

// 3. Biểu tượng chim hót trung tâm
function drawBirdCenterpiece() {
  let centerX = width / 2;
  let centerY = 82;
  let info = getBirdInfo();

  noStroke();
  fill(0, 180, 216, 25);
  ellipse(centerX, centerY, 70, 70);

  fill(14, 40, 52);
  stroke(info.color);
  strokeWeight(2);
  ellipse(centerX, centerY, 52, 52);

  noStroke();
  textSize(24);
  textAlign(CENTER, CENTER);
  text(info.icon, centerX, centerY);
}

// 4. Bảng hiển thị kết quả (Bottom Dashboard)
function drawResultDashboard() {
  let bannerY = 175;
  let bannerH = 65;
  let info = getBirdInfo();

  noStroke();
  fill(10, 30, 39);
  rect(0, bannerY, width, bannerH);

  stroke(info.color);
  strokeWeight(1.5);
  line(0, bannerY, width, bannerY);

  noStroke();
  fill(info.color);
  textSize(15);
  textFont('sans-serif');
  textStyle(BOLD);
  textAlign(CENTER, CENTER);

  let isNoise = label.toLowerCase().includes("noise");
  let displayTitle = isNoise ? "🎧 Đang lắng nghe tiếng chim..." : "🎵 " + info.name;
  text(displayTitle, width / 2, bannerY + 20);

  fill(144, 224, 239);
  textSize(11);
  textStyle(NORMAL);
  let subText = isNoise ? "Môi trường yên tĩnh" : "Độ chính xác: " + confidence + "%";
  text(subText, width / 2, bannerY + 38);

  let barWidth = 180;
  let barHeight = 4;
  let barX = (width - barWidth) / 2;
  let barY = bannerY + 50;

  fill(20, 48, 60);
  rect(barX, barY, barWidth, barHeight, 2);

  let fillWidth = isNoise ? 30 : map(confidence, 0, 100, 0, barWidth, true);
  fill(info.color);
  rect(barX, barY, fillWidth, barHeight, 2);
}

function getBirdInfo() {
  let lower = label.toLowerCase().trim();
  for (let key in BIRD_MAP) {
    if (lower.includes(key)) {
      return BIRD_MAP[key];
    }
  }
  return { name: label, icon: "🦜", color: "#48cae4" };
}

// Khi model nhận diện được âm thanh
function gotResult(error, results) {
  if (error) {
    console.error(error);
    return;
  }

  if (!isSimulating && results && results.length > 0) {
    label = results[0].label;
    confidence = floor(results[0].confidence * 100);
  }
}

// Hàm hỗ trợ nút bấm trong index.html
function toggleListening() {
  let micBtnText = document.getElementById('micBtnText');
  let micBtn = document.getElementById('micBtn');

  if (isSimulating) {
    isSimulating = false;
    if (micBtn) micBtn.classList.add('listening');
    if (micBtnText) micBtnText.innerText = "Micro: Đang Lắng Nghe...";
  } else {
    simulateBirdSound();
  }
}

// Nút bấm thử giả lập ngẫu nhiên 6 loài chim của Thầy Dũng
function simulateBirdSound() {
  isSimulating = true;
  let birdKeys = Object.keys(BIRD_MAP).filter(k => k !== 'background noise');
  let randKey = random(birdKeys);
  label = BIRD_MAP[randKey].name;
  confidence = floor(random(88, 99));

  let micBtnText = document.getElementById('micBtnText');
  let micBtn = document.getElementById('micBtn');
  if (micBtnText) micBtnText.innerText = "Chế Độ Thử: " + BIRD_MAP[randKey].name;
  if (micBtn) micBtn.classList.remove('listening');
}

// Đăng ký toàn cục lên window để HTML luôn gọi được
window.toggleListening = toggleListening;
window.simulateBirdSound = simulateBirdSound;
