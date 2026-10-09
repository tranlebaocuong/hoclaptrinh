/**
 * =========================================================
 * PLAYLIST MANAGER & MUSIC PLAYER - JAVASCRIPT
 * Tích hợp Trình phát nhạc thực tế (HTML5 Audio + Web Audio Synth)
 * - Nghe nhạc trực tiếp trên trình duyệt
 * - Chọn file MP3/WAV từ máy tính để nghe
 * - Tua nhạc (Seek bar), chỉnh âm lượng, lặp lại, xáo trộn
 * - Tương thích 1:1 với logic Python (Thêm, Đổi STT, Kéo thả, Xóa)
 * =========================================================
 */

// Danh sách nhạc mẫu mặc định với link MP3 thực tế chất lượng cao
const DEFAULT_PLAYLIST = [
  {
    title: "Shape of You",
    audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    sourceDesc: "Bản nhạc demo Pop Beat",
    isLocal: false
  },
  {
    title: "Blinding Lights",
    audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    sourceDesc: "Bản nhạc demo Synthwave Retro",
    isLocal: false
  },
  {
    title: "Dynamite",
    audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    sourceDesc: "Bản nhạc demo Upbeat Funk",
    isLocal: false
  }
];

const FALLBACK_DEMO_URLS = [
  "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
  "https://raw.githubusercontent.com/rafaelreis-hotmart/Audio-Sample-files/master/sample.mp3"
];

// Khởi tạo trạng thái ứng dụng
let playlist = loadPlaylist();
let currentTrackIndex = 0;
let isPlaying = false;
let isMuted = false;
let isShuffle = false;
let isRepeat = false; // true: lặp lại bài hiện tại
let deleteCandidateIndex = null;
let searchQuery = "";
let isBackendConnected = false;

// DOM Elements
const realAudio = document.getElementById("realAudio");
const playlistUl = document.getElementById("playlistUl");
const emptyState = document.getElementById("emptyState");
const songCountBadge = document.getElementById("songCountBadge");
const songInput = document.getElementById("songInput");
const addSongBtn = document.getElementById("addSongBtn");
const audioFileInput = document.getElementById("audioFileInput");
const searchInput = document.getElementById("searchInput");
const resetDefaultBtn = document.getElementById("resetDefaultBtn");

// Player Controls & Progress
const nowPlayingCard = document.getElementById("nowPlayingCard");
const trackThumb = document.getElementById("trackThumb");
const headerVinyl = document.getElementById("headerVinyl");
const trackStatus = document.getElementById("trackStatus");
const currentTrackTitle = document.getElementById("currentTrackTitle");
const currentTrackSource = document.getElementById("currentTrackSource");
const equalizer = document.getElementById("equalizer");
const playPauseBtn = document.getElementById("playPauseBtn");
const prevTrackBtn = document.getElementById("prevTrackBtn");
const nextTrackBtn = document.getElementById("nextTrackBtn");
const progressBar = document.getElementById("progressBar");
const progressFill = document.getElementById("progressFill");
const currentTimeLabel = document.getElementById("currentTimeLabel");
const durationLabel = document.getElementById("durationLabel");
const volumeSlider = document.getElementById("volumeSlider");
const muteBtn = document.getElementById("muteBtn");
const shuffleBtn = document.getElementById("shuffleBtn");
const repeatBtn = document.getElementById("repeatBtn");

// Modal Reorder
const openReorderModalBtn = document.getElementById("openReorderModalBtn");
const reorderModal = document.getElementById("reorderModal");
const closeReorderModal = document.getElementById("closeReorderModal");
const cancelReorderBtn = document.getElementById("cancelReorderBtn");
const confirmReorderBtn = document.getElementById("confirmReorderBtn");
const fromIndexInput = document.getElementById("fromIndexInput");
const toIndexInput = document.getElementById("toIndexInput");

// Modal Delete
const deleteModal = document.getElementById("deleteModal");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
const deleteSongName = document.getElementById("deleteSongName");

// Theme & Toast
const themeToggleBtn = document.getElementById("themeToggleBtn");
const toastContainer = document.getElementById("toastContainer");

/* =========================================================
   1. QUẢN LÝ DỮ LIỆU & CHUẨN HÓA BÀI HÁT
   ========================================================= */
function normalizeSong(item, index = 0) {
  if (typeof item === "string") {
    const demoUrl = (index < DEFAULT_PLAYLIST.length) 
      ? DEFAULT_PLAYLIST[index].audioUrl 
      : FALLBACK_DEMO_URLS[index % FALLBACK_DEMO_URLS.length];
    return {
      title: item,
      audioUrl: demoUrl,
      sourceDesc: "Bản nhạc demo chất lượng cao",
      isLocal: false
    };
  }
  return {
    title: item.title || "Bài hát không tên",
    audioUrl: item.audioUrl || FALLBACK_DEMO_URLS[0],
    sourceDesc: item.sourceDesc || (item.isLocal ? "File từ máy tính" : "Bản nhạc demo"),
    isLocal: !!item.isLocal
  };
}

function loadPlaylist() {
  const saved = localStorage.getItem("my_music_playlist_v2");
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed) && parsed.length > 0) {
        return parsed.map((item, idx) => normalizeSong(item, idx));
      }
    } catch (e) {
      console.error("Lỗi đọc localStorage:", e);
    }
  }
  return DEFAULT_PLAYLIST.map((item, idx) => normalizeSong(item, idx));
}

function savePlaylist() {
  localStorage.setItem("my_music_playlist_v2", JSON.stringify(playlist));
}

// Kiểm tra và đồng bộ với API Python nếu chạy qua http://
async function checkAndSyncBackend() {
  if (window.location.protocol.startsWith("http")) {
    try {
      const res = await fetch("/api/playlist");
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data.playlist)) {
          playlist = data.playlist.map((item, idx) => normalizeSong(item, idx));
          isBackendConnected = true;
          savePlaylist();
          renderPlaylist();
          showToast("⚡ Đã kết nối đồng bộ với Backend Python FastAPI!", "success");
        }
      }
    } catch (e) {
      // Chế độ Offline LocalStorage
    }
  }
}

/* =========================================================
   2. HÀM HIỂN THỊ PLAYLIST
   ========================================================= */
function renderPlaylist() {
  playlistUl.innerHTML = "";
  songCountBadge.innerHTML = `<i class="fa-solid fa-music"></i> ${playlist.length} bài hát`;

  if (playlist.length === 0) {
    emptyState.style.display = "block";
    updatePlayerUI();
    return;
  }

  emptyState.style.display = "none";

  const filtered = playlist.map((song, index) => ({ song, index }))
    .filter(item => item.song.title.toLowerCase().includes(searchQuery.toLowerCase()));

  if (filtered.length === 0) {
    playlistUl.innerHTML = `<li style="text-align: center; padding: 30px; color: var(--text-muted);">
      Không tìm thấy bài hát nào khớp với "${escapeHtml(searchQuery)}"
    </li>`;
    return;
  }

  filtered.forEach(item => {
    const { song, index } = item;
    const stt = index + 1;
    const isCurrent = index === currentTrackIndex;
    const isCurrentPlaying = isCurrent && isPlaying;

    const li = document.createElement("li");
    li.className = `playlist-item ${isCurrent ? 'active' : ''}`;
    li.setAttribute("draggable", "true");
    li.dataset.index = index;

    const sourceTag = song.isLocal 
      ? '<span class="audio-tag tag-local"><i class="fa-solid fa-file-audio"></i> Máy tính</span>'
      : '<span class="audio-tag tag-demo"><i class="fa-solid fa-cloud"></i> Online</span>';

    li.innerHTML = `
      <span class="col-stt">${stt}</span>
      <div class="col-title" title="${escapeHtml(song.title)}">
        <i class="fa-solid fa-grip-vertical item-icon" title="Kéo thả để đổi thứ tự"></i>
        <span>${escapeHtml(song.title)}</span>
        ${sourceTag}
      </div>
      <div class="col-status">
        <span class="status-pill ${isCurrentPlaying ? 'status-playing' : 'status-idle'}">
          <i class="fa-solid ${isCurrentPlaying ? 'fa-volume-high' : 'fa-circle-stop'}"></i>
          ${isCurrentPlaying ? 'Đang phát' : (isCurrent ? 'Tạm dừng' : 'Chờ')}
        </span>
      </div>
      <div class="col-actions" onclick="event.stopPropagation()">
        <button class="item-btn btn-play-song" title="Phát bài này" onclick="playSongAt(${index})">
          <i class="fa-solid ${isCurrentPlaying ? 'fa-pause' : 'fa-play'}"></i>
        </button>
        <button class="item-btn" title="Di chuyển lên" onclick="moveUp(${index})" ${index === 0 ? 'disabled style="opacity:0.3; cursor:not-allowed"' : ''}>
          <i class="fa-solid fa-arrow-up"></i>
        </button>
        <button class="item-btn" title="Di chuyển xuống" onclick="moveDown(${index})" ${index === playlist.length - 1 ? 'disabled style="opacity:0.3; cursor:not-allowed"' : ''}>
          <i class="fa-solid fa-arrow-down"></i>
        </button>
        <button class="item-btn btn-delete" title="Xóa bài này" onclick="openDeleteModal(${index})">
          <i class="fa-solid fa-trash-can"></i>
        </button>
      </div>
    `;

    // Click vào cả dòng để phát nhạc
    li.addEventListener("click", () => {
      playSongAt(index);
    });

    // Thiết lập kéo thả
    setupDragAndDrop(li);

    playlistUl.appendChild(li);
  });

  updatePlayerUI();
}

/* =========================================================
   3. TRÌNH PHÁT NHẠC AUDIO THỰC TẾ (AUDIO ENGINE)
   ========================================================= */
function loadTrack(index, autoPlay = true) {
  if (playlist.length === 0) {
    realAudio.src = "";
    isPlaying = false;
    updatePlayerUI();
    return;
  }

  currentTrackIndex = Math.max(0, Math.min(index, playlist.length - 1));
  const currentSong = playlist[currentTrackIndex];

  realAudio.src = currentSong.audioUrl;
  realAudio.load();

  if (autoPlay) {
    const playPromise = realAudio.play();
    if (playPromise !== undefined) {
      playPromise
        .then(() => {
          isPlaying = true;
          updatePlayerUI();
        })
        .catch((err) => {
          console.warn("Trình duyệt chặn autoplay hoặc link cần tương tác:", err);
          isPlaying = false;
          updatePlayerUI();
        });
    }
  } else {
    isPlaying = false;
    updatePlayerUI();
  }
}

async function togglePlay() {
  if (playlist.length === 0) return;

  if (!realAudio.src || realAudio.src === "" || realAudio.src === window.location.href) {
    loadTrack(currentTrackIndex, true);
    return;
  }

  if (realAudio.paused) {
    try {
      await realAudio.play();
      isPlaying = true;
    } catch (err) {
      console.warn("Lỗi phát audio:", err);
      // Fallback: Web Audio Melody Synthesizer nếu URL bị lỗi mạng
      playSynthMelody();
      isPlaying = true;
    }
  } else {
    realAudio.pause();
    isPlaying = false;
  }
  updatePlayerUI();
}

window.playSongAt = function(index) {
  if (currentTrackIndex === index && realAudio.src) {
    togglePlay();
  } else {
    loadTrack(index, true);
  }
};

function playNextTrack() {
  if (playlist.length === 0) return;
  if (isRepeat) {
    realAudio.currentTime = 0;
    realAudio.play();
    return;
  }

  if (isShuffle && playlist.length > 1) {
    let nextIdx = currentTrackIndex;
    while (nextIdx === currentTrackIndex) {
      nextIdx = Math.floor(Math.random() * playlist.length);
    }
    loadTrack(nextIdx, true);
  } else {
    const nextIdx = (currentTrackIndex + 1) % playlist.length;
    loadTrack(nextIdx, true);
  }
}

function playPrevTrack() {
  if (playlist.length === 0) return;
  if (realAudio.currentTime > 3) {
    realAudio.currentTime = 0;
    return;
  }
  const prevIdx = (currentTrackIndex - 1 + playlist.length) % playlist.length;
  loadTrack(prevIdx, true);
}

// Cập nhật giao diện Trình phát nhạc
function updatePlayerUI() {
  if (playlist.length === 0) {
    currentTrackTitle.textContent = "Chưa có bài hát nào";
    currentTrackSource.textContent = "Hãy thêm bài hát để bắt đầu nghe";
    trackStatus.textContent = "Chờ bài hát";
    equalizer.classList.remove("playing");
    trackThumb.classList.remove("playing");
    headerVinyl.classList.remove("playing");
    playPauseBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
    currentTimeLabel.textContent = "0:00";
    durationLabel.textContent = "0:00";
    progressBar.value = 0;
    progressFill.style.width = "0%";
    return;
  }

  const currentSong = playlist[currentTrackIndex];
  currentTrackTitle.textContent = currentSong.title;
  currentTrackSource.innerHTML = currentSong.isLocal
    ? `<i class="fa-solid fa-file-audio"></i> ${escapeHtml(currentSong.sourceDesc)}`
    : `<i class="fa-solid fa-cloud"></i> ${escapeHtml(currentSong.sourceDesc)}`;

  if (isPlaying) {
    trackStatus.textContent = "Đang phát";
    equalizer.classList.add("playing");
    trackThumb.classList.add("playing");
    headerVinyl.classList.add("playing");
    playPauseBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
  } else {
    trackStatus.textContent = "Tạm dừng";
    equalizer.classList.remove("playing");
    trackThumb.classList.remove("playing");
    headerVinyl.classList.remove("playing");
    playPauseBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
  }

  // Cập nhật active class cho danh sách
  document.querySelectorAll(".playlist-item").forEach((el) => {
    const idx = parseInt(el.dataset.index, 10);
    if (idx === currentTrackIndex) {
      el.classList.add("active");
      const pill = el.querySelector(".status-pill");
      const playIcon = el.querySelector(".btn-play-song i");
      if (pill) {
        pill.className = `status-pill ${isPlaying ? 'status-playing' : 'status-idle'}`;
        pill.innerHTML = `<i class="fa-solid ${isPlaying ? 'fa-volume-high' : 'fa-circle-stop'}"></i> ${isPlaying ? 'Đang phát' : 'Tạm dừng'}`;
      }
      if (playIcon) {
        playIcon.className = `fa-solid ${isPlaying ? 'fa-pause' : 'fa-play'}`;
      }
    } else {
      el.classList.remove("active");
      const pill = el.querySelector(".status-pill");
      const playIcon = el.querySelector(".btn-play-song i");
      if (pill) {
        pill.className = "status-pill status-idle";
        pill.innerHTML = '<i class="fa-solid fa-circle-stop"></i> Chờ';
      }
      if (playIcon) {
        playIcon.className = "fa-solid fa-play";
      }
    }
  });
}

// Cập nhật thanh tiến trình phát nhạc
realAudio.addEventListener("timeupdate", () => {
  if (!realAudio.duration) return;
  const current = realAudio.currentTime;
  const duration = realAudio.duration;
  const percent = (current / duration) * 100;

  progressBar.value = percent;
  progressFill.style.width = `${percent}%`;
  currentTimeLabel.textContent = formatTime(current);
  durationLabel.textContent = formatTime(duration);
});

realAudio.addEventListener("loadedmetadata", () => {
  durationLabel.textContent = formatTime(realAudio.duration);
});

realAudio.addEventListener("ended", () => {
  playNextTrack();
});

realAudio.addEventListener("error", (e) => {
  console.warn("Lỗi tải nguồn âm thanh, kích hoạt bộ tổng hợp:", e);
});

// Tua bài hát (Seek)
progressBar.addEventListener("input", (e) => {
  if (!realAudio.duration) return;
  const percent = parseFloat(e.target.value);
  realAudio.currentTime = (percent / 100) * realAudio.duration;
  progressFill.style.width = `${percent}%`;
});

// Điều chỉnh âm lượng
volumeSlider.addEventListener("input", (e) => {
  const vol = parseFloat(e.target.value);
  realAudio.volume = vol;
  if (vol === 0) {
    muteBtn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
    isMuted = true;
  } else {
    muteBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
    isMuted = false;
  }
});

muteBtn.addEventListener("click", () => {
  if (isMuted) {
    realAudio.volume = volumeSlider.value || 0.8;
    muteBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
    isMuted = false;
  } else {
    realAudio.volume = 0;
    muteBtn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
    isMuted = true;
  }
});

// Shuffle & Repeat
shuffleBtn.addEventListener("click", () => {
  isShuffle = !isShuffle;
  shuffleBtn.classList.toggle("active", isShuffle);
  showToast(isShuffle ? "🔀 Đã bật chế độ phát ngẫu nhiên!" : "➡️ Đã tắt chế độ phát ngẫu nhiên", "success");
});

repeatBtn.addEventListener("click", () => {
  isRepeat = !isRepeat;
  repeatBtn.classList.toggle("active", isRepeat);
  showToast(isRepeat ? "🔂 Đã bật lặp lại bài hát hiện tại!" : "➡️ Đã tắt lặp lại bài hát", "success");
});

playPauseBtn.addEventListener("click", togglePlay);
nextTrackBtn.addEventListener("click", playNextTrack);
prevTrackBtn.addEventListener("click", playPrevTrack);

function formatTime(seconds) {
  if (isNaN(seconds) || seconds < 0) return "0:00";
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

/* =========================================================
   4. CHỌN FILE NHẠC TỪ MÁY TÍNH (UPLOAD LOCAL AUDIO)
   ========================================================= */
audioFileInput.addEventListener("change", (e) => {
  const files = e.target.files;
  if (!files || files.length === 0) return;

  let addedCount = 0;
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    // Lấy tên file bỏ phần mở rộng .mp3/.wav
    const songName = file.name.replace(/\.[^/.]+$/, "");
    const blobUrl = URL.createObjectURL(file);

    playlist.push({
      title: songName,
      audioUrl: blobUrl,
      sourceDesc: `File máy tính (${(file.size / (1024 * 1024)).toFixed(1)} MB)`,
      isLocal: true
    });
    addedCount++;
  }

  savePlaylist();
  renderPlaylist();
  showToast(`🎉 Đã thêm thành công ${addedCount} bài hát từ máy tính của bạn!`, "success");

  // Tự động phát bài vừa thêm
  loadTrack(playlist.length - addedCount, true);
  audioFileInput.value = "";
});

/* =========================================================
   5. CHỨC NĂNG 1: THÊM BÀI HÁT QUA Ô NHẬP
   ========================================================= */
async function handleAddSong() {
  const songName = songInput.value.trim();
  if (!songName) {
    showToast("⚠️ Tên bài hát không được để trống!", "warning");
    songInput.focus();
    return;
  }

  // Kiểm tra trùng lặp
  const exists = playlist.some(s => s.title.toLowerCase() === songName.toLowerCase());
  if (exists) {
    const confirmAdd = confirm(`⚠️ Bài hát "${songName}" đã có trong danh sách. Bạn vẫn muốn thêm?`);
    if (!confirmAdd) {
      showToast("↩️ Đã hủy thêm bài hát trùng.", "warning");
      return;
    }
  }

  // Nếu kết nối backend, gọi API
  if (isBackendConnected) {
    try {
      await fetch("/api/playlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: songName })
      });
    } catch (e) {
      console.warn("Lỗi đồng bộ API, lưu cục bộ.");
    }
  }

  const demoUrl = FALLBACK_DEMO_URLS[playlist.length % FALLBACK_DEMO_URLS.length];
  playlist.push({
    title: songName,
    audioUrl: demoUrl,
    sourceDesc: "Bản nhạc demo chất lượng cao",
    isLocal: false
  });

  savePlaylist();
  songInput.value = "";
  renderPlaylist();
  showToast(`✅ Đã thêm: "${songName}" (Vị trí ${playlist.length})`, "success");

  // Tự động phát bài mới thêm
  loadTrack(playlist.length - 1, true);
}

/* =========================================================
   6. CHỨC NĂNG 2: ĐỔI THỨ TỰ BÀI HÁT
   ========================================================= */
async function moveSong(fromIdx, toIdx) {
  if (fromIdx < 0 || fromIdx >= playlist.length || toIdx < 0 || toIdx >= playlist.length) {
    showToast("❌ STT không hợp lệ!", "error");
    return false;
  }

  if (fromIdx === toIdx) {
    showToast(`ℹ️ Bài hát đã ở vị trí ${toIdx + 1} rồi, không thay đổi.`, "warning");
    return false;
  }

  const [movedSong] = playlist.splice(fromIdx, 1);
  playlist.splice(toIdx, 0, movedSong);

  // Cập nhật vị trí bài đang phát nếu bị ảnh hưởng
  if (currentTrackIndex === fromIdx) {
    currentTrackIndex = toIdx;
  } else if (fromIdx < currentTrackIndex && toIdx >= currentTrackIndex) {
    currentTrackIndex--;
  } else if (fromIdx > currentTrackIndex && toIdx <= currentTrackIndex) {
    currentTrackIndex++;
  }

  // Đồng bộ PUT với backend nếu có
  if (isBackendConnected) {
    try {
      await fetch("/api/playlist/reorder", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stt_cu: fromIdx + 1, stt_moi: toIdx + 1 })
      });
    } catch (e) {
      console.warn("Lỗi đồng bộ API reorder.");
    }
  }

  savePlaylist();
  renderPlaylist();
  showToast(`✅ Đã chuyển "${movedSong.title}" từ vị trí ${fromIdx + 1} sang vị trí ${toIdx + 1}!`, "success");
  return true;
}

window.moveUp = function(index) {
  if (index > 0) moveSong(index, index - 1);
};
window.moveDown = function(index) {
  if (index < playlist.length - 1) moveSong(index, index + 1);
};

// Modal Đổi thứ tự
openReorderModalBtn.addEventListener("click", () => {
  if (playlist.length < 2) {
    showToast("⚠️ Cần ít nhất 2 bài hát để đổi vị trí!", "warning");
    return;
  }
  fromIndexInput.value = "";
  toIndexInput.value = "";
  fromIndexInput.max = playlist.length;
  toIndexInput.max = playlist.length;
  reorderModal.classList.add("active");
  fromIndexInput.focus();
});

function closeReorder() {
  reorderModal.classList.remove("active");
}
closeReorderModal.addEventListener("click", closeReorder);
cancelReorderBtn.addEventListener("click", closeReorder);

confirmReorderBtn.addEventListener("click", () => {
  const fromVal = parseInt(fromIndexInput.value, 10);
  const toVal = parseInt(toIndexInput.value, 10);

  if (isNaN(fromVal) || fromVal < 1 || fromVal > playlist.length) {
    showToast(`❌ STT bài muốn chuyển phải từ 1 đến ${playlist.length}!`, "error");
    fromIndexInput.focus();
    return;
  }
  if (isNaN(toVal) || toVal < 1 || toVal > playlist.length) {
    showToast(`❌ Vị trí chuyển đến phải từ 1 đến ${playlist.length}!`, "error");
    toIndexInput.focus();
    return;
  }

  const success = moveSong(fromVal - 1, toVal - 1);
  if (success) {
    closeReorder();
  }
});

/* =========================================================
   7. CHỨC NĂNG 3: XÓA BÀI HÁT
   ========================================================= */
window.openDeleteModal = function(index) {
  deleteCandidateIndex = index;
  deleteSongName.textContent = `"${playlist[index].title}" (Vị trí ${index + 1})`;
  deleteModal.classList.add("active");
};

function closeDelete() {
  deleteCandidateIndex = null;
  deleteModal.classList.remove("active");
}
closeDeleteModal.addEventListener("click", closeDelete);
cancelDeleteBtn.addEventListener("click", closeDelete);

confirmDeleteBtn.addEventListener("click", async () => {
  if (deleteCandidateIndex === null || deleteCandidateIndex < 0 || deleteCandidateIndex >= playlist.length) {
    closeDelete();
    return;
  }

  const stt = deleteCandidateIndex + 1;
  const deletedSong = playlist.splice(deleteCandidateIndex, 1)[0];

  const wasPlaying = (currentTrackIndex === deleteCandidateIndex);

  if (currentTrackIndex >= playlist.length) {
    currentTrackIndex = Math.max(0, playlist.length - 1);
  } else if (deleteCandidateIndex < currentTrackIndex) {
    currentTrackIndex--;
  }

  // Đồng bộ DELETE với backend nếu có
  if (isBackendConnected) {
    try {
      await fetch(`/api/playlist/${stt}`, { method: "DELETE" });
    } catch (e) {
      console.warn("Lỗi đồng bộ DELETE.");
    }
  }

  savePlaylist();
  renderPlaylist();
  closeDelete();
  showToast(`🗑️ Đã xóa thành công: "${deletedSong.title}"`, "success");

  if (wasPlaying && playlist.length > 0) {
    loadTrack(currentTrackIndex, isPlaying);
  }
});

/* =========================================================
   8. KÉO THẢ SẮP XẾP BÀI HÁT (DRAG AND DROP)
   ========================================================= */
let dragStartIndex = null;

function setupDragAndDrop(itemElement) {
  itemElement.addEventListener("dragstart", (e) => {
    dragStartIndex = parseInt(itemElement.dataset.index, 10);
    itemElement.classList.add("dragging");
    e.dataTransfer.effectAllowed = "move";
  });

  itemElement.addEventListener("dragend", () => {
    itemElement.classList.remove("dragging");
  });

  itemElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  });

  itemElement.addEventListener("drop", (e) => {
    e.preventDefault();
    const dragEndIndex = parseInt(itemElement.dataset.index, 10);
    if (dragStartIndex !== null && dragStartIndex !== dragEndIndex) {
      moveSong(dragStartIndex, dragEndIndex);
    }
    dragStartIndex = null;
  });
}

/* =========================================================
   9. WEB AUDIO MELODY SYNTHESIZER (FALLBACK KHI OFFLINE)
   ========================================================= */
function playSynthMelody() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const notes = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25]; // C D E G A C
    let time = ctx.currentTime + 0.1;

    for (let i = 0; i < 8; i++) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const noteFreq = notes[i % notes.length];

      osc.type = "sine";
      osc.frequency.setValueAtTime(noteFreq, time);

      gain.gain.setValueAtTime(0.2, time);
      gain.gain.exponentialRampToValueAtTime(0.001, time + 0.35);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(time);
      osc.stop(time + 0.4);

      time += 0.3;
    }
  } catch (e) {
    console.error("Web Audio Synthesizer error:", e);
  }
}

/* =========================================================
   10. CÁC TÍNH NĂNG PHỤ TRỢ (TÌM KIẾM, RESET, TOAST, THEME)
   ========================================================= */
songInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") handleAddSong();
});
addSongBtn.addEventListener("click", handleAddSong);

searchInput.addEventListener("input", (e) => {
  searchQuery = e.target.value.trim();
  renderPlaylist();
});

resetDefaultBtn.addEventListener("click", () => {
  if (confirm("Khôi phục playlist về 3 bài hát mặc định ban đầu?")) {
    playlist = DEFAULT_PLAYLIST.map((item, idx) => normalizeSong(item, idx));
    currentTrackIndex = 0;
    savePlaylist();
    renderPlaylist();
    loadTrack(0, false);
    showToast("🔄 Đã khôi phục playlist mặc định!", "success");
  }
});

function initTheme() {
  const savedTheme = localStorage.getItem("playlist_theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);
}

function updateThemeIcon(theme) {
  themeToggleBtn.innerHTML = theme === "dark" 
    ? '<i class="fa-solid fa-sun"></i>' 
    : '<i class="fa-solid fa-moon"></i>';
}

themeToggleBtn.addEventListener("click", () => {
  const current = document.documentElement.getAttribute("data-theme") || "dark";
  const newTheme = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("playlist_theme", newTheme);
  updateThemeIcon(newTheme);
});

function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  
  let iconClass = "fa-circle-check";
  if (type === "error") iconClass = "fa-circle-xmark";
  if (type === "warning") iconClass = "fa-triangle-exclamation";

  toast.innerHTML = `<i class="fa-solid ${iconClass}"></i><span>${escapeHtml(message)}</span>`;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(50px)";
    setTimeout(() => toast.remove(), 300);
  }, 2800);
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Khởi chạy ứng dụng
initTheme();
renderPlaylist();
loadTrack(0, false); // Nạp bài đầu tiên sẵn sàng phát
checkAndSyncBackend();
