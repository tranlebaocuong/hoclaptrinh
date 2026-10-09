// ========================================================
// ĐỀ TÀI: NHẬN DIỆN CÁC LOẠI RỄ CÂY (PLANT ROOT CLASSIFIER)
// Thư viện: ml5.js & p5.js (Teachable Machine Model)
// Tông màu chủ đề: Thực vật & Đất cát (Forest Green & Earth Tone)
// ========================================================

// Biến phân loại (Classifier)
let classifier;

// Đường dẫn Model Teachable Machine của bạn
let imageModelURL = 'https://teachablemachine.withgoogle.com/models/VIjgspcLq/';

// Biến Video
let video;
let flippedVideo;

// Lưu trữ nhãn kết quả và độ tin cậy (Confidence)
let label = "Đang quét rễ cây...";
let confidence = 0;

// Nạp model AI trước khi khởi chạy chương trình
function preload() {
  classifier = ml5.imageClassifier(imageModelURL + 'model.json');
}

function setup() {
  // Mở rộng canvas 320x300 để có không gian hiển thị thông tin rễ cây đẹp mắt
  createCanvas(320, 305);
  
  // Khởi tạo camera
  video = createCapture(VIDEO);
  video.size(320, 240);
  video.hide();

  flippedVideo = ml5.flipImage(video);
  
  // Bắt đầu nhận diện
  classifyVideo();
}

function draw() {
  // 1. Nền canvas tông màu đất mùn hữu cơ (Deep Soil Brown / Botanical Dark)
  background(27, 38, 30); // Xanh rừng rậm pha đất tối (#1b261e)

  // 2. Vẽ hình ảnh từ webcam
  image(flippedVideo, 0, 0, 320, 240);

  // 3. Khung viền kính ngắm quan sát mẫu thực vật (Botanical Viewfinder Border)
  noFill();
  stroke(82, 183, 136, 120); // Màu xanh lá mầm dịu (#52b788)
  strokeWeight(2);
  rect(8, 8, 304, 224, 6);

  // Điểm đánh dấu 4 góc kính ngắm lấy nét mẫu rễ
  stroke(116, 198, 157); // Xanh ngọc lục bảo nhạt (#74c69d)
  strokeWeight(3);
  let cLen = 14;
  // Góc trên-trái
  line(8, 8, 8 + cLen, 8); line(8, 8, 8, 8 + cLen);
  // Góc trên-phải
  line(312, 8, 312 - cLen, 8); line(312, 8, 312, 8 + cLen);
  // Góc dưới-trái
  line(8, 232, 8 + cLen, 232); line(8, 232, 8, 232 - cLen);
  // Góc dưới-phải
  line(312, 232, 312 - cLen, 232); line(312, 232, 312, 232 - cLen);

  // 4. Bảng hiển thị kết quả (Bottom Dashboard) mang tông màu thiên nhiên
  noStroke();
  fill(19, 42, 31); // Xanh rêu đậm thực vật (#132a1f)
  rect(0, 240, 320, 65);

  // Đường viền ngăn cách màu nâu đất phù sa (#8c6239)
  stroke(140, 98, 57);
  strokeWeight(2);
  line(0, 240, 320, 240);

  // 5. Hiển thị nhãn loại rễ cây
  noStroke();
  fill(216, 243, 220); // Màu lá non sáng (#d8f3dc)
  textSize(14);
  textFont('sans-serif');
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  
  // Icon mầm cây và tên loại rễ (Ví dụ: Rễ cọc, Rễ chùm, Rễ củ,...)
  text("🌱 " + label, width / 2, 260);

  // 6. Hiển thị % Độ chính xác (Confidence) và Thanh đo sinh học (Progress Bar)
  fill(149, 213, 178); // Xanh lục nhạt (#95d5b2)
  textSize(11);
  textStyle(NORMAL);
  text("Độ tin cậy: " + confidence + "%", width / 2, 278);

  // Vẽ thanh đo phần trăm độ tin cậy bên dưới
  let barWidth = 180;
  let barHeight = 5;
  let barX = (width - barWidth) / 2;
  let barY = 289;

  // Khung nền thanh đo (Màu đất tối)
  fill(45, 60, 50);
  rect(barX, barY, barWidth, barHeight, 3);

  // Mức độ tin cậy thực tế (Màu mầm cây phát triển xanh tươi)
  let fillWidth = map(confidence, 0, 100, 0, barWidth, true);
  fill(82, 183, 136); // #52b788
  rect(barX, barY, fillWidth, barHeight, 3);
}

// Lấy dự đoán cho khung hình video hiện tại
function classifyVideo() {
  flippedVideo = ml5.flipImage(video);
  classifier.classify(flippedVideo, gotResult);
}

// Xử lý khi nhận được kết quả từ Model
function gotResult(error, results) {
  if (error) {
    console.error(error);
    return;
  }
  // Lấy nhãn có độ tin cậy cao nhất
  label = results[0].label;
  // Tính phần trăm độ tin cậy (0 - 100%)
  confidence = floor(results[0].confidence * 100);

  // Tiếp tục nhận diện khung hình tiếp theo
  classifyVideo();
}
